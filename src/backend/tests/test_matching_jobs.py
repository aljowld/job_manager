"""Unit tests for the deterministic job-matching engine (v1)."""

from __future__ import annotations

from app.matching import (
    MATCHING_VERSION,
    MatchJob,
    MatchProfile,
    MatchState,
    PreferenceItem,
    match_job,
)
from app.schemas.profile import PreferenceLevelEnum


def _pref(value: str, level: PreferenceLevelEnum) -> PreferenceItem:
    return PreferenceItem(value=value, level=level)


def _criterion(result, criterion: str):
    matches = [c for c in result.criteria if c.criterion == criterion]
    assert len(matches) == 1, f"expected exactly one '{criterion}' criterion, got {len(matches)}"
    return matches[0]


# --- Tri-state basics -------------------------------------------------------


def test_tri_state_match_mismatch_unknown_on_contract_type() -> None:
    profile = MatchProfile(
        contract_types=[_pref("internship", PreferenceLevelEnum.IMPORTANT)]
    )

    matched = match_job(profile, MatchJob(contract_type="internship"))
    mismatched = match_job(profile, MatchJob(contract_type="cdi"))
    unknown = match_job(profile, MatchJob(contract_type=None))

    assert _criterion(matched, "contract_type").state is MatchState.MATCH
    assert _criterion(mismatched, "contract_type").state is MatchState.MISMATCH
    assert _criterion(unknown, "contract_type").state is MatchState.UNKNOWN


# --- REQUIRED ----------------------------------------------------------------


def test_required_present_and_compatible_is_match_and_eligible() -> None:
    profile = MatchProfile(contract_types=[_pref("internship", PreferenceLevelEnum.REQUIRED)])
    result = match_job(profile, MatchJob(contract_type="internship"))

    criterion = _criterion(result, "contract_type")
    assert criterion.state is MatchState.MATCH
    assert criterion.weight == 0
    assert result.eligible is True


def test_required_present_and_incompatible_is_ineligible() -> None:
    profile = MatchProfile(contract_types=[_pref("internship", PreferenceLevelEnum.REQUIRED)])
    result = match_job(profile, MatchJob(contract_type="cdi"))

    assert _criterion(result, "contract_type").state is MatchState.MISMATCH
    assert result.eligible is False


def test_required_unknown_job_value_is_unknown_and_still_eligible() -> None:
    profile = MatchProfile(contract_types=[_pref("internship", PreferenceLevelEnum.REQUIRED)])
    result = match_job(profile, MatchJob(contract_type=None))

    assert _criterion(result, "contract_type").state is MatchState.UNKNOWN
    assert result.eligible is True


# --- EXCLUDED ----------------------------------------------------------------


def test_excluded_value_present_makes_offer_ineligible() -> None:
    profile = MatchProfile(preferred_companies=[_pref("BadCorp", PreferenceLevelEnum.EXCLUDED)])
    result = match_job(profile, MatchJob(company_name="BadCorp"))

    criterion = _criterion(result, "company")
    assert criterion.state is MatchState.MISMATCH
    assert criterion.weight == 0
    assert result.eligible is False


def test_excluded_value_different_is_match() -> None:
    profile = MatchProfile(preferred_companies=[_pref("BadCorp", PreferenceLevelEnum.EXCLUDED)])
    result = match_job(profile, MatchJob(company_name="GoodCorp"))

    assert _criterion(result, "company").state is MatchState.MATCH
    assert result.eligible is True


def test_excluded_unknown_job_value_is_unknown_without_hard_fail() -> None:
    profile = MatchProfile(preferred_companies=[_pref("BadCorp", PreferenceLevelEnum.EXCLUDED)])
    result = match_job(profile, MatchJob(company_name=None))

    assert _criterion(result, "company").state is MatchState.UNKNOWN
    assert result.eligible is True


# --- AVOID ---------------------------------------------------------------------


def test_avoid_present_value_is_soft_mismatch_but_stays_eligible() -> None:
    profile = MatchProfile(industries=[_pref("finance", PreferenceLevelEnum.AVOID)])
    result = match_job(profile, MatchJob(industry="finance"))

    criterion = _criterion(result, "industry")
    assert criterion.state is MatchState.MISMATCH
    assert criterion.weight > 0
    assert result.eligible is True
    assert result.score == 0.0


def test_avoid_different_value_is_match() -> None:
    profile = MatchProfile(industries=[_pref("finance", PreferenceLevelEnum.AVOID)])
    result = match_job(profile, MatchJob(industry="healthcare"))

    assert _criterion(result, "industry").state is MatchState.MATCH
    assert result.eligible is True
    assert result.score == 100.0


def test_avoid_unknown_job_value_is_unknown() -> None:
    profile = MatchProfile(industries=[_pref("finance", PreferenceLevelEnum.AVOID)])
    result = match_job(profile, MatchJob(industry=None))

    assert _criterion(result, "industry").state is MatchState.UNKNOWN
    assert result.score is None


# --- Positive weights --------------------------------------------------------


def test_positive_weight_ordering_bonus_important_very_important() -> None:
    bonus = _criterion(
        match_job(
            MatchProfile(job_types=[_pref("full_time", PreferenceLevelEnum.BONUS)]),
            MatchJob(job_type="full_time"),
        ),
        "job_type",
    )
    important = _criterion(
        match_job(
            MatchProfile(job_types=[_pref("full_time", PreferenceLevelEnum.IMPORTANT)]),
            MatchJob(job_type="full_time"),
        ),
        "job_type",
    )
    very_important = _criterion(
        match_job(
            MatchProfile(job_types=[_pref("full_time", PreferenceLevelEnum.VERY_IMPORTANT)]),
            MatchJob(job_type="full_time"),
        ),
        "job_type",
    )

    assert bonus.weight < important.weight < very_important.weight


# --- UNKNOWN excluded from the score denominator ------------------------------


def test_unknown_criteria_are_excluded_from_score_denominator() -> None:
    profile = MatchProfile(
        job_types=[_pref("full_time", PreferenceLevelEnum.IMPORTANT)],
        industries=[_pref("tech", PreferenceLevelEnum.IMPORTANT)],
    )

    with_unknown = match_job(profile, MatchJob(job_type="full_time", industry=None))
    only_known = match_job(
        MatchProfile(job_types=[_pref("full_time", PreferenceLevelEnum.IMPORTANT)]),
        MatchJob(job_type="full_time"),
    )

    assert with_unknown.score == only_known.score == 100.0


# --- No known criteria ---------------------------------------------------------


def test_no_known_criteria_returns_none_score() -> None:
    profile = MatchProfile(job_types=[_pref("full_time", PreferenceLevelEnum.IMPORTANT)])
    result = match_job(profile, MatchJob(job_type=None))

    assert result.score is None


def test_no_preferences_expressed_returns_empty_criteria_and_none_score() -> None:
    result = match_job(MatchProfile(), MatchJob(job_type="full_time"))

    assert result.criteria == []
    assert result.score is None
    assert result.eligible is True


# --- Company normalization -----------------------------------------------------


def test_company_matching_is_case_and_whitespace_insensitive() -> None:
    profile = MatchProfile(preferred_companies=[_pref(" OpenAI ", PreferenceLevelEnum.BONUS)])
    result = match_job(profile, MatchJob(company_name="openai"))

    assert _criterion(result, "company").state is MatchState.MATCH


def test_company_matching_does_not_use_fuzzy_similarity() -> None:
    profile = MatchProfile(preferred_companies=[_pref("OpenAI", PreferenceLevelEnum.BONUS)])
    result = match_job(profile, MatchJob(company_name="Open AI"))

    assert _criterion(result, "company").state is MatchState.MISMATCH


# --- Contract type / job type / industry match & mismatch ----------------------


def test_contract_type_match_and_mismatch() -> None:
    profile = MatchProfile(contract_types=[_pref("cdi", PreferenceLevelEnum.IMPORTANT)])

    assert _criterion(match_job(profile, MatchJob(contract_type="cdi")), "contract_type").state is (
        MatchState.MATCH
    )
    assert _criterion(match_job(profile, MatchJob(contract_type="cdd")), "contract_type").state is (
        MatchState.MISMATCH
    )


def test_job_type_match_and_mismatch() -> None:
    profile = MatchProfile(job_types=[_pref("full_time", PreferenceLevelEnum.IMPORTANT)])

    assert _criterion(match_job(profile, MatchJob(job_type="full_time")), "job_type").state is (
        MatchState.MATCH
    )
    assert _criterion(match_job(profile, MatchJob(job_type="part_time")), "job_type").state is (
        MatchState.MISMATCH
    )


def test_industry_match_and_mismatch() -> None:
    profile = MatchProfile(industries=[_pref("tech", PreferenceLevelEnum.IMPORTANT)])

    assert _criterion(match_job(profile, MatchJob(industry="tech")), "industry").state is (
        MatchState.MATCH
    )
    assert _criterion(match_job(profile, MatchJob(industry="retail")), "industry").state is (
        MatchState.MISMATCH
    )


# --- Location --------------------------------------------------------------------


def test_location_matches_on_exact_city() -> None:
    result = match_job(MatchProfile(location="Paris"), MatchJob(city="Paris"))
    assert _criterion(result, "location").state is MatchState.MATCH


def test_location_matches_on_exact_country() -> None:
    result = match_job(MatchProfile(location="France"), MatchJob(country="France"))
    assert _criterion(result, "location").state is MatchState.MATCH


def test_location_is_unknown_when_job_has_no_location_data() -> None:
    result = match_job(MatchProfile(location="Paris"), MatchJob())
    assert _criterion(result, "location").state is MatchState.UNKNOWN


def test_location_ambiguous_free_text_is_unknown_not_guessed() -> None:
    result = match_job(
        MatchProfile(location="Paris"),
        MatchJob(location_text="Remote - Europe based"),
    )
    assert _criterion(result, "location").state is MatchState.UNKNOWN


def test_location_not_evaluated_when_profile_has_no_preference() -> None:
    result = match_job(MatchProfile(location=None), MatchJob(city="Paris"))
    assert [c for c in result.criteria if c.criterion == "location"] == []


# --- Remote ------------------------------------------------------------------------


def test_remote_match_mismatch_unknown() -> None:
    profile = MatchProfile(remote_preference="remote")

    assert _criterion(match_job(profile, MatchJob(remote_type="remote")), "remote").state is (
        MatchState.MATCH
    )
    assert _criterion(match_job(profile, MatchJob(remote_type="on_site")), "remote").state is (
        MatchState.MISMATCH
    )
    assert _criterion(match_job(profile, MatchJob(remote_type=None)), "remote").state is (
        MatchState.UNKNOWN
    )


# --- Global score --------------------------------------------------------------------


def test_global_score_mixes_match_mismatch_and_unknown() -> None:
    profile = MatchProfile(
        remote_preference="remote",
        contract_types=[_pref("cdi", PreferenceLevelEnum.IMPORTANT)],
        industries=[_pref("finance", PreferenceLevelEnum.IMPORTANT)],
        location="Paris",
    )
    job = MatchJob(
        remote_type="remote",  # MATCH, weight 2
        contract_type="cdi",  # MATCH, weight 2
        industry="retail",  # MISMATCH, weight 2
        city=None,
        region=None,
        country=None,
        location_text=None,  # UNKNOWN, ignored
    )

    result = match_job(profile, job)

    # matched_weight = 4 (remote + contract_type), known_weight = 6 (+ industry)
    assert result.score == round(100 * 4 / 6, 2)


# --- Hard eligibility can coexist with an explainable score ---------------------------


def test_ineligible_offer_still_has_an_explainable_score() -> None:
    profile = MatchProfile(
        contract_types=[_pref("internship", PreferenceLevelEnum.REQUIRED)],
        job_types=[_pref("full_time", PreferenceLevelEnum.IMPORTANT)],
    )
    job = MatchJob(contract_type="cdi", job_type="full_time")

    result = match_job(profile, job)

    assert result.eligible is False
    assert result.score == 100.0


# --- Determinism -----------------------------------------------------------------------


def test_matching_is_deterministic_across_calls() -> None:
    profile = MatchProfile(
        location="Paris",
        remote_preference="remote",
        contract_types=[_pref("internship", PreferenceLevelEnum.REQUIRED)],
        industries=[_pref("finance", PreferenceLevelEnum.AVOID)],
    )
    job = MatchJob(
        city="Paris",
        remote_type="remote",
        contract_type="internship",
        industry="finance",
    )

    first = match_job(profile, job)
    second = match_job(profile, job)

    assert first == second


# --- Version -----------------------------------------------------------------------------


def test_matching_version_is_v1() -> None:
    result = match_job(MatchProfile(), MatchJob())
    assert result.matching_version == "v1"
    assert MATCHING_VERSION == "v1"
