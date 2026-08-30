"""Deterministic, explainable job-matching engine (v1)."""

from app.matching.jobs import (
    MATCHING_VERSION,
    CriterionMatchResult,
    JobMatchResult,
    MatchJob,
    MatchProfile,
    MatchState,
    PreferenceItem,
    match_job,
)

__all__ = [
    "MATCHING_VERSION",
    "CriterionMatchResult",
    "JobMatchResult",
    "MatchJob",
    "MatchProfile",
    "MatchState",
    "PreferenceItem",
    "match_job",
]
