"""Deterministic deduplication helpers for canonical job offers."""

from app.deduplication.jobs import (
    DeduplicationResult,
    DuplicateDecision,
    JobDeduplicator,
)

__all__ = ["DeduplicationResult", "DuplicateDecision", "JobDeduplicator"]
