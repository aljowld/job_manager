"""Integration tests for the fake-job collection pipeline."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.collection import FakeJobSource
from app.collection.base import RawJob
from app.collection.pipeline import CollectionPipeline
from app.db.base import Base
from app.db.models import JobOffer, JobSource, JobSourceOccurrence, RawJobSnapshot


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_pipeline_persists_fake_jobs_and_occurrences(db_session: Session) -> None:
    """The pipeline creates raw snapshots and canonical offers from the fake source."""
    pipeline = CollectionPipeline(db_session)
    result = pipeline.run(FakeJobSource())

    assert result.collected == 6
    assert result.persisted == 6
    assert result.failed == 0
    assert db_session.query(JobSource).count() == 1
    assert db_session.query(RawJobSnapshot).count() == 6
    assert db_session.query(JobOffer).count() == 6
    assert db_session.query(JobSourceOccurrence).count() == 6


def test_pipeline_preserves_similar_fake_jobs_as_distinct_offers(db_session: Session) -> None:
    """Fake jobs with only a different city are not conflated by deduplication."""
    pipeline = CollectionPipeline(db_session)
    source = FakeJobSource()

    result = pipeline.run(source)

    assert result.persisted == 6
    assert db_session.query(JobOffer).count() == 6
    assert db_session.query(JobSourceOccurrence).filter_by(external_job_id="fake-1001").count() == 1
    assert db_session.query(JobSourceOccurrence).filter_by(external_job_id="fake-1002").count() == 1


def test_pipeline_exposes_recorded_provenance_in_job_occurrences(db_session: Session) -> None:
    """The persisted occurrence retains the source and external identifiers."""
    pipeline = CollectionPipeline(db_session)
    result = pipeline.run(FakeJobSource())

    occurrence = db_session.query(JobSourceOccurrence).filter_by(external_job_id="fake-2001").one()
    assert result.persisted == 6
    assert occurrence.source.name == "fake_jobs"
    assert occurrence.source_url.startswith("https://fake.example/jobs")
    assert occurrence.external_job_id == "fake-2001"


def test_content_hash_is_deterministic_for_same_payload(db_session: Session) -> None:
    """The snapshot hash is stable across process runs for identical content."""
    raw_job = RawJob(
        source_name="fake_jobs",
        external_job_id="fake-42",
        source_url="https://fake.example/jobs/42",
        title="Python Dev",
        company_name="Acme",
        description="Build services.",
        location_raw="Paris, France",
        contract_type_raw="CDI",
        remote_type_raw="hybrid",
        salary_raw="€70k - €90k",
        publication_date_raw="2026-08-01T12:00:00+02:00",
        experience_level_raw="Senior",
        technologies=["python", "sqlalchemy"],
        metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
    )
    pipeline = CollectionPipeline(db_session)

    first_hash = pipeline._content_hash(raw_job)
    second_hash = pipeline._content_hash(
        RawJob(
            source_name="fake_jobs",
            external_job_id="fake-42",
            source_url="https://fake.example/jobs/42",
            title="Python Dev",
            company_name="Acme",
            description="Build services.",
            location_raw="Paris, France",
            contract_type_raw="CDI",
            remote_type_raw="hybrid",
            salary_raw="€70k - €90k",
            publication_date_raw="2026-08-01T12:00:00+02:00",
            experience_level_raw="Senior",
            technologies=["python", "sqlalchemy"],
            metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
        )
    )

    assert first_hash == second_hash
    assert len(first_hash) == 64


def test_job_fingerprint_is_deterministic_and_conservative() -> None:
    """The fingerprint normalizes whitespace and casing but does not include unstable DB timestamps."""
    from app.deduplication.jobs import JobDeduplicator

    fingerprint_a = JobDeduplicator._job_fingerprint(
        title="  Senior   Python Developer  ",
        company_name="  Acme   Corp ",
        city=" Paris ",
        contract_type=" CDI ",
    )
    fingerprint_b = JobDeduplicator._job_fingerprint(
        title="Senior Python Developer",
        company_name="Acme Corp",
        city="Paris",
        contract_type="CDI",
    )

    assert fingerprint_a == fingerprint_b
    assert fingerprint_a == "senior python developer | acme corp | paris | cdi"


def test_pipeline_reuses_existing_offer_for_same_source_and_external_id(db_session: Session) -> None:
    """Recollecting the same source occurrence resolves to the same canonical job offer."""
    class RepeatedJobSource:
        source_name = "fake_jobs"
        source_url = "https://fake.example/jobs"
        collection_method = "fake"

        def collect(self):
            return [
                RawJob(
                    source_name="fake_jobs",
                    external_job_id="repeat-1",
                    source_url="https://fake.example/jobs/repeat-1",
                    title="Platform Engineer",
                    company_name="Acme",
                    description="Manage infrastructure.",
                    location_raw="Paris, France",
                    contract_type_raw="CDI",
                    remote_type_raw="hybrid",
                    salary_raw="€80k - €100k",
                    publication_date_raw="2026-08-15T10:00:00+00:00",
                    experience_level_raw="Senior",
                    technologies=["kubernetes"],
                    metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
                )
            ]

    pipeline = CollectionPipeline(db_session)

    first = pipeline.run(RepeatedJobSource())
    second = pipeline.run(RepeatedJobSource())

    assert first.persisted == 1
    assert second.persisted == 1
    assert db_session.query(JobOffer).count() == 1
    assert db_session.query(JobSourceOccurrence).count() == 1
    assert db_session.query(RawJobSnapshot).count() == 2


def test_pipeline_confirms_cross_source_duplicate_by_url(db_session: Session) -> None:
    """Two different sources can share one canonical job when their normalized URLs match."""
    class SourceA:
        source_name = "source_a"
        source_url = "https://jobs.example"
        collection_method = "api"

        def collect(self):
            return [
                RawJob(
                    source_name=self.source_name,
                    external_job_id="source-a-42",
                    source_url="https://jobs.example/offers/42#top",
                    title="Backend Engineer",
                    company_name="Acme",
                    description="Build APIs.",
                    location_raw="Paris, France",
                    contract_type_raw="CDI",
                    remote_type_raw="hybrid",
                    salary_raw="€80k - €100k",
                    publication_date_raw="2026-08-10T09:00:00+00:00",
                    experience_level_raw="Senior",
                    technologies=["python"],
                    metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
                )
            ]

    class SourceB:
        source_name = "source_b"
        source_url = "https://mirror.example"
        collection_method = "feed"

        def collect(self):
            return [
                RawJob(
                    source_name=self.source_name,
                    external_job_id="source-b-99",
                    source_url="https://jobs.example/offers/42",
                    title="Backend Engineer",
                    company_name="Acme",
                    description="Build APIs.",
                    location_raw="Paris, France",
                    contract_type_raw="CDI",
                    remote_type_raw="hybrid",
                    salary_raw="€80k - €100k",
                    publication_date_raw="2026-08-10T09:00:00+00:00",
                    experience_level_raw="Senior",
                    technologies=["python"],
                    metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
                )
            ]

    pipeline = CollectionPipeline(db_session)
    pipeline.run(SourceA())
    result = pipeline.run(SourceB())

    assert result.persisted == 1
    assert db_session.query(JobOffer).count() == 1
    assert db_session.query(JobSourceOccurrence).count() == 2


def test_pipeline_keeps_ambiguous_similar_jobs_distinct(db_session: Session) -> None:
    """Ambiguous near-identical offers are not merged aggressively during Step 9."""
    class SourceX:
        source_name = "source_x"
        source_url = "https://source-x.example"
        collection_method = "api"

        def collect(self):
            return [
                RawJob(
                    source_name=self.source_name,
                    external_job_id="x-1",
                    source_url="https://source-x.example/1",
                    title="Senior Python Developer",
                    company_name="Acme",
                    description="Backend work.",
                    location_raw="Paris, France",
                    contract_type_raw="CDI",
                    remote_type_raw="hybrid",
                    salary_raw="€70k - €95k",
                    publication_date_raw="2026-08-12T12:00:00+00:00",
                    experience_level_raw="Senior",
                    technologies=["python"],
                    metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
                )
            ]

    class SourceY:
        source_name = "source_y"
        source_url = "https://source-y.example"
        collection_method = "feed"

        def collect(self):
            return [
                RawJob(
                    source_name=self.source_name,
                    external_job_id="y-1",
                    source_url="https://source-y.example/1",
                    title="Senior Python Developer",
                    company_name="Acme",
                    description="Different marketing backend role.",
                    location_raw="Paris, France",
                    contract_type_raw="CDI",
                    remote_type_raw="hybrid",
                    salary_raw="€80k - €100k",
                    publication_date_raw="2026-08-13T12:00:00+00:00",
                    experience_level_raw="Senior",
                    technologies=["python"],
                    metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
                )
            ]

    pipeline = CollectionPipeline(db_session)
    pipeline.run(SourceX())
    result = pipeline.run(SourceY())

    assert result.persisted == 1
    assert db_session.query(JobOffer).count() == 2
    assert db_session.query(JobSourceOccurrence).count() == 2


def test_salary_normalization_handles_real_fake_formats_conservatively() -> None:
    """Salary parsing accepts only explicit, unambiguous fake-source formats."""
    pipeline = CollectionPipeline(db_session)

    assert pipeline._normalize_salary_min("€70k - €90k") == 70000
    assert pipeline._normalize_salary_max("€70k - €90k") == 90000
    assert pipeline._normalize_salary_min("45 000 - 55 000 €") == 45000
    assert pipeline._normalize_salary_max("45 000 - 55 000 €") == 55000
    assert pipeline._normalize_salary_min("€90k") == 90000
    assert pipeline._normalize_salary_max("€90k") == 90000
    assert pipeline._normalize_salary_min("salary not clear") is None
    assert pipeline._normalize_salary_max("salary not clear") is None


def test_publication_date_handles_naive_and_timezone_aware_values() -> None:
    """The date normalization preserves timezone-aware values in UTC and treats invalid values as absent."""
    pipeline = CollectionPipeline(db_session)

    naive = pipeline._normalize_publication_date("2026-08-01T12:00:00")
    aware = pipeline._normalize_publication_date("2026-08-01T12:00:00+02:00")
    invalid = pipeline._normalize_publication_date("not-a-date")

    assert naive == datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    assert aware == datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
    assert invalid is None


def test_pipeline_rolls_back_a_failed_offer_without_partial_writes(db_session: Session) -> None:
    """A failing raw job is isolated; valid jobs persist and invalid item leaves no partial data."""
    class FailingRawJobSource:
        source_name = "fake_jobs"
        source_url = "https://fake.example/jobs"
        collection_method = "fake"

        def collect(self):
            return [
                RawJob(
                    source_name="fake_jobs",
                    external_job_id="fake-valid-1",
                    source_url="https://fake.example/jobs/valid-1",
                    title="Valid job",
                    company_name="Valid Co",
                    description="This one should persist.",
                    location_raw="Paris, France",
                    contract_type_raw="CDI",
                    remote_type_raw="hybrid",
                    salary_raw="€70k - €90k",
                    publication_date_raw="2026-08-01T10:00:00+00:00",
                    experience_level_raw="Senior",
                    technologies=["python"],
                    metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
                ),
                RawJob(
                    source_name="fake_jobs",
                    external_job_id="",
                    source_url="https://fake.example/jobs/invalid",
                    title="Missing external id",
                    company_name="Broken Co",
                    description="This one should fail.",
                    location_raw="Berlin, Germany",
                    contract_type_raw="CDI",
                    remote_type_raw="remote",
                    salary_raw="€50k - €60k",
                    publication_date_raw="2026-08-02T10:00:00+00:00",
                    experience_level_raw="Mid",
                    technologies=["python"],
                    metadata={"city": "Berlin", "country": "DE", "job_type": "full_time"},
                ),
                RawJob(
                    source_name="fake_jobs",
                    external_job_id="fake-valid-2",
                    source_url="https://fake.example/jobs/valid-2",
                    title="Second valid job",
                    company_name="Other Co",
                    description="This one should also persist.",
                    location_raw="Lyon, France",
                    contract_type_raw="CDD",
                    remote_type_raw="on_site",
                    salary_raw="€45 000 - €55 000",
                    publication_date_raw="2026-08-03T10:00:00+00:00",
                    experience_level_raw="Mid",
                    technologies=["sql"],
                    metadata={"city": "Lyon", "country": "FR", "job_type": "full_time"},
                ),
            ]

    pipeline = CollectionPipeline(db_session)
    result = pipeline.run(FailingRawJobSource())

    assert result.collected == 3
    assert result.persisted == 2
    assert result.failed == 1
    assert db_session.query(JobOffer).count() == 2
    assert db_session.query(JobSourceOccurrence).count() == 2
    assert db_session.query(RawJobSnapshot).filter_by(external_job_id="").count() == 0
    assert db_session.query(JobOffer).filter_by(title="Missing external id").count() == 0
