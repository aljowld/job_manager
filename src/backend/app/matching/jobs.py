"""Deterministic, explainable matching engine between a user profile and a job offer.

This module is intentionally independent of FastAPI and SQLAlchemy: it takes plain
in-memory data (``MatchProfile`` / ``MatchJob``) and returns a plain result
(``JobMatchResult``). No database session, no SQL query and no HTTP concern is
involved, so the engine can be unit tested without PostgreSQL/Docker.

Criteria deferred for V1 (documented, not implemented):

* ``PreferredJobRole`` — no sufficiently reliable ``JobOffer`` field currently
  allows comparing a free-form desired job role to an offer title.
* salary — ``UserProfile`` only exposes ``desired_salary_min``/``desired_salary_max``
  as raw integers with no currency/period, while ``JobOffer`` carries
  ``salary_currency``/``salary_period``. Comparing the two would assume matching
  units, which is not safe.
* technologies / skills — ``JobOffer`` does not persist a structured technology
  list (only free-text description), so no reliable comparison is possible.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.schemas.profile import PreferenceLevelEnum

MATCHING_VERSION = "v1"

# Deterministic weight mapping for positive preference levels, used both for
# scoring. REQUIRED and EXCLUDED intentionally have no score weight: they act
# purely on eligibility (see `match_job`) and must not inflate the score after
# already having served as a hard constraint.
_POSITIVE_WEIGHTS: dict[PreferenceLevelEnum, int] = {
    PreferenceLevelEnum.BONUS: 1,
    PreferenceLevelEnum.IMPORTANT: 2,
    PreferenceLevelEnum.VERY_IMPORTANT: 3,
}
# AVOID is a soft negative preference: it carries a significant, non-blocking
# weight (equivalent to IMPORTANT) so that a matched "avoided" value visibly
# penalizes the score without affecting eligibility.
_AVOID_WEIGHT = 2

# Fixed weights for criteria that are not driven by a preference_level, because
# the current profile model exposes them as plain fields (no per-criterion
# level). Chosen as the equivalent of IMPORTANT for the same reason as AVOID.
_LOCATION_WEIGHT = 2
_REMOTE_WEIGHT = 2


class MatchState(StrEnum):
    """Tri-state outcome of a single matching criterion."""

    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    UNKNOWN = "UNKNOWN"


class _RawComparison(StrEnum):
    """Internal result of a plain normalized-string comparison."""

    EQUAL = "EQUAL"
    DIFFERENT = "DIFFERENT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class PreferenceItem:
    """A single user preference value with its expressed level."""

    value: str
    level: PreferenceLevelEnum


@dataclass(frozen=True, slots=True)
class MatchProfile:
    """Minimal, matching-only view of a user profile, decoupled from persistence."""

    location: str | None = None
    remote_preference: str | None = None
    contract_types: list[PreferenceItem] = field(default_factory=list)
    job_types: list[PreferenceItem] = field(default_factory=list)
    industries: list[PreferenceItem] = field(default_factory=list)
    preferred_companies: list[PreferenceItem] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class MatchJob:
    """Minimal, matching-only view of a job offer, decoupled from persistence."""

    company_name: str | None = None
    contract_type: str | None = None
    job_type: str | None = None
    industry: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    location_text: str | None = None
    remote_type: str | None = None


@dataclass(frozen=True, slots=True)
class CriterionMatchResult:
    """Explainable outcome for a single matching criterion."""

    criterion: str
    state: MatchState
    user_value: str | None
    job_value: str | None
    weight: int
    reason: str


@dataclass(frozen=True, slots=True)
class JobMatchResult:
    """Overall matching outcome for a (profile, job) pair."""

    matching_version: str
    eligible: bool
    score: float | None
    criteria: list[CriterionMatchResult]


def _normalize_text(value: str | None) -> str | None:
    """Trim, casefold and collapse internal whitespace; empty becomes None."""
    if value is None:
        return None
    normalized = " ".join(value.strip().split()).casefold()
    return normalized or None


def _raw_equality(user_value: str | None, job_value: str | None) -> _RawComparison:
    normalized_user = _normalize_text(user_value)
    normalized_job = _normalize_text(job_value)
    if normalized_user is None or normalized_job is None:
        return _RawComparison.UNKNOWN
    return _RawComparison.EQUAL if normalized_user == normalized_job else _RawComparison.DIFFERENT


def _weight_for_level(level: PreferenceLevelEnum) -> int:
    if level in (PreferenceLevelEnum.REQUIRED, PreferenceLevelEnum.EXCLUDED):
        return 0
    if level is PreferenceLevelEnum.AVOID:
        return _AVOID_WEIGHT
    return _POSITIVE_WEIGHTS[level]


def _state_for_level(level: PreferenceLevelEnum, raw: _RawComparison) -> MatchState:
    if raw is _RawComparison.UNKNOWN:
        return MatchState.UNKNOWN
    is_equal = raw is _RawComparison.EQUAL
    if level in (PreferenceLevelEnum.EXCLUDED, PreferenceLevelEnum.AVOID):
        return MatchState.MISMATCH if is_equal else MatchState.MATCH
    # REQUIRED, VERY_IMPORTANT, IMPORTANT, BONUS all express a positive preference.
    return MatchState.MATCH if is_equal else MatchState.MISMATCH


def _build_reason(
    criterion: str,
    level: PreferenceLevelEnum,
    state: MatchState,
    user_value: str,
    job_value: str | None,
) -> str:
    if state is MatchState.UNKNOWN:
        return f"{criterion} preference '{user_value}' ({level.value}): job {criterion} is unknown"
    if level is PreferenceLevelEnum.EXCLUDED:
        if state is MatchState.MISMATCH:
            return (
                f"{criterion} '{job_value}' matches excluded value '{user_value}'"
                " (offer ineligible)"
            )
        return f"{criterion} '{job_value}' differs from excluded value '{user_value}'"
    if level is PreferenceLevelEnum.AVOID:
        if state is MatchState.MISMATCH:
            return (
                f"{criterion} '{job_value}' matches avoided value '{user_value}' (score penalized)"
            )
        return f"{criterion} '{job_value}' differs from avoided value '{user_value}'"
    if state is MatchState.MATCH:
        return (
            f"{criterion} preference '{user_value}' ({level.value}) matches job value '{job_value}'"
        )
    if level is PreferenceLevelEnum.REQUIRED:
        return (
            f"{criterion} preference '{user_value}' (REQUIRED) does not match"
            f" job value '{job_value}' (offer ineligible)"
        )
    return (
        f"{criterion} preference '{user_value}' ({level.value}) does not match"
        f" job value '{job_value}'"
    )


def _evaluate_string_preferences(
    criterion: str,
    preferences: list[PreferenceItem],
    job_value: str | None,
) -> list[CriterionMatchResult]:
    """Evaluate every expressed preference of one criterion against the job value."""
    results: list[CriterionMatchResult] = []
    for preference in preferences:
        raw = _raw_equality(preference.value, job_value)
        state = _state_for_level(preference.level, raw)
        results.append(
            CriterionMatchResult(
                criterion=criterion,
                state=state,
                user_value=preference.value,
                job_value=job_value,
                weight=_weight_for_level(preference.level),
                reason=_build_reason(
                    criterion, preference.level, state, preference.value, job_value
                ),
            )
        )
    return results


def _evaluate_location(location: str | None, job: MatchJob) -> CriterionMatchResult | None:
    """Deterministic, conservative location comparison.

    Priority: exact normalized match on city, then region, then country. If none
    of the structured fields is available, fall back to a token-exact comparison
    on `location_text` (split on commas) — never a naive substring match. If
    structured fields are known but none matches, the location is a genuine
    mismatch. If only free text is available and no token matches, the outcome
    is UNKNOWN rather than a guessed mismatch.
    """
    if location is None or not location.strip():
        return None  # no preference expressed: not applicable, excluded from score

    normalized_user = _normalize_text(location)

    structured_fields = [("city", job.city), ("region", job.region), ("country", job.country)]
    known_structured = [(name, value) for name, value in structured_fields if value is not None]

    for name, value in known_structured:
        if _normalize_text(value) == normalized_user:
            return CriterionMatchResult(
                criterion="location",
                state=MatchState.MATCH,
                user_value=location,
                job_value=value,
                weight=_LOCATION_WEIGHT,
                reason=f"profile location '{location}' matches job {name} '{value}'",
            )

    if known_structured:
        job_value = known_structured[0][1]
        return CriterionMatchResult(
            criterion="location",
            state=MatchState.MISMATCH,
            user_value=location,
            job_value=job_value,
            weight=_LOCATION_WEIGHT,
            reason=f"profile location '{location}' does not match any known job location field",
        )

    if job.location_text:
        tokens = {t for t in (_normalize_text(part) for part in job.location_text.split(",")) if t}
        if normalized_user in tokens:
            return CriterionMatchResult(
                criterion="location",
                state=MatchState.MATCH,
                user_value=location,
                job_value=job.location_text,
                weight=_LOCATION_WEIGHT,
                reason=(
                    f"profile location '{location}' matches a token of"
                    f" location_text '{job.location_text}'"
                ),
            )
        return CriterionMatchResult(
            criterion="location",
            state=MatchState.UNKNOWN,
            user_value=location,
            job_value=job.location_text,
            weight=_LOCATION_WEIGHT,
            reason=(
                f"profile location '{location}' cannot be reliably compared"
                " to free-text location_text"
            ),
        )

    return CriterionMatchResult(
        criterion="location",
        state=MatchState.UNKNOWN,
        user_value=location,
        job_value=None,
        weight=_LOCATION_WEIGHT,
        reason="job location is unknown",
    )


def _evaluate_remote(
    remote_preference: str | None, remote_type: str | None
) -> CriterionMatchResult | None:
    if remote_preference is None or not remote_preference.strip():
        return None  # no preference expressed: not applicable, excluded from score

    raw = _raw_equality(remote_preference, remote_type)
    if raw is _RawComparison.UNKNOWN:
        return CriterionMatchResult(
            criterion="remote",
            state=MatchState.UNKNOWN,
            user_value=remote_preference,
            job_value=remote_type,
            weight=_REMOTE_WEIGHT,
            reason="job remote_type is unknown",
        )
    state = MatchState.MATCH if raw is _RawComparison.EQUAL else MatchState.MISMATCH
    reason = (
        f"remote preference '{remote_preference}' matches job remote_type '{remote_type}'"
        if state is MatchState.MATCH
        else (
            f"remote preference '{remote_preference}' does not match"
            f" job remote_type '{remote_type}'"
        )
    )
    return CriterionMatchResult(
        criterion="remote",
        state=state,
        user_value=remote_preference,
        job_value=remote_type,
        weight=_REMOTE_WEIGHT,
        reason=reason,
    )


def _compute_score(criteria: list[CriterionMatchResult]) -> float | None:
    """score = matched_weight / known_weight, expressed as a 0-100 percentage.

    UNKNOWN criteria are excluded from both the numerator and the denominator.
    Hard-constraint criteria (REQUIRED/EXCLUDED) always carry weight 0 and thus
    never affect the score. Returns None when no criterion is known, since a
    score of 0 would wrongly imply a bad match.
    """
    known = [c for c in criteria if c.state is not MatchState.UNKNOWN]
    known_weight = sum(c.weight for c in known)
    if known_weight == 0:
        return None
    matched_weight = sum(c.weight for c in known if c.state is MatchState.MATCH)
    return round(100 * matched_weight / known_weight, 2)


def match_job(profile: MatchProfile, job: MatchJob) -> JobMatchResult:
    """Compute a deterministic, explainable matching result for one job offer."""
    criteria: list[CriterionMatchResult] = []
    criteria.extend(
        _evaluate_string_preferences("contract_type", profile.contract_types, job.contract_type)
    )
    criteria.extend(_evaluate_string_preferences("job_type", profile.job_types, job.job_type))
    criteria.extend(_evaluate_string_preferences("industry", profile.industries, job.industry))
    criteria.extend(
        _evaluate_string_preferences("company", profile.preferred_companies, job.company_name)
    )

    location_result = _evaluate_location(profile.location, job)
    if location_result is not None:
        criteria.append(location_result)

    remote_result = _evaluate_remote(profile.remote_preference, job.remote_type)
    if remote_result is not None:
        criteria.append(remote_result)

    # Invariant: weight == 0 only ever occurs for REQUIRED/EXCLUDED criteria
    # (see `_weight_for_level`), so this is exactly the hard-constraint check.
    eligible = not any(
        criterion.weight == 0 and criterion.state is MatchState.MISMATCH for criterion in criteria
    )

    return JobMatchResult(
        matching_version=MATCHING_VERSION,
        eligible=eligible,
        score=_compute_score(criteria),
        criteria=criteria,
    )
