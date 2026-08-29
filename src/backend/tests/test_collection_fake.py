"""Tests for the offline fake collection source."""

from __future__ import annotations

from app.collection import FakeJobSource, JobCollector, RawJob


def test_fake_job_source_can_be_created() -> None:
    """The fake source is instantiable and exposes its provenance."""
    source = FakeJobSource()

    assert source.source_name == "fake_jobs"
    assert source.source_url == "https://fake.example/jobs"


def test_fake_job_source_collect_returns_raw_jobs() -> None:
    """The fake source returns a list of in-memory raw jobs."""
    source = FakeJobSource()

    jobs = source.collect()

    assert isinstance(jobs, list)
    assert len(jobs) == 6
    assert all(isinstance(job, RawJob) for job in jobs)


def test_fake_job_source_collect_is_deterministic() -> None:
    """The data is stable between calls and remains fully offline."""
    source = FakeJobSource()

    first = source.collect()
    second = source.collect()

    assert first == second


def test_fake_job_source_exposes_provenance_and_external_identifiers() -> None:
    """Every raw job includes its origin information."""
    source = FakeJobSource()

    jobs = source.collect()
    external_ids = [job.external_job_id for job in jobs]
    urls = [job.source_url for job in jobs]

    assert external_ids == [
        "fake-1001",
        "fake-1002",
        "fake-2001",
        "fake-3001",
        "fake-4001",
        "fake-5001",
    ]
    assert all(job.source_name == source.source_name for job in jobs)
    assert all(job.source_url.startswith(source.source_url) for job in jobs)
    assert all(job.external_job_id.startswith("fake-") for job in jobs)
    assert all(url.endswith(job.external_job_id.replace("fake-", "")) for job, url in zip(jobs, urls))


def test_fake_job_source_includes_missing_and_diverse_cases() -> None:
    """The fake dataset covers several realistic raw-job variants and missing fields."""
    source = FakeJobSource()

    jobs = source.collect()
    remote_types = {job.remote_type_raw for job in jobs}
    salaries = {job.salary_raw for job in jobs}
    experience_levels = {job.experience_level_raw for job in jobs}
    titles = {job.title for job in jobs}

    assert remote_types == {"hybrid", "on_site", "remote"}
    assert None in salaries
    assert None in experience_levels
    assert {"Senior Python Backend Engineer", "Frontend Engineer", "Data Analyst", "Platform Engineer", "Product Designer"}.issubset(titles)


def test_fake_job_source_matches_the_job_collector_contract() -> None:
    """The fake source is compatible with the minimal collector protocol."""
    source = FakeJobSource()

    assert isinstance(source, JobCollector)
    assert callable(source.collect)
