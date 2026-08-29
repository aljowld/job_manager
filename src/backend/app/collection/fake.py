from __future__ import annotations

from app.collection.base import RawJob


class FakeJobSource:
    """Deterministic offline source used to simulate an external job feed."""

    source_name = "fake_jobs"
    source_url = "https://fake.example/jobs"

    def __init__(self) -> None:
        self._jobs = [
            RawJob(
                source_name=self.source_name,
                external_job_id="fake-1001",
                source_url=f"{self.source_url}/1001",
                title="Senior Python Backend Engineer",
                company_name="Northwind Labs",
                description="Build and maintain backend services in Python and FastAPI.",
                location_raw="Paris, France",
                contract_type_raw="CDI",
                remote_type_raw="hybrid",
                salary_raw="€70k - €95k",
                publication_date_raw="2026-08-01",
                experience_level_raw="Senior",
                technologies=["python", "fastapi", "sqlalchemy"],
                metadata={"city": "Paris", "country": "FR", "job_type": "full_time"},
            ),
            RawJob(
                source_name=self.source_name,
                external_job_id="fake-1002",
                source_url=f"{self.source_url}/1002",
                title="Senior Python Backend Engineer",
                company_name="Northwind Labs",
                description="Work on APIs, services and platform tooling.",
                location_raw="Lyon, France",
                contract_type_raw="CDD",
                remote_type_raw="on_site",
                salary_raw="€60k - €80k",
                publication_date_raw="2026-08-03",
                experience_level_raw="Senior",
                technologies=["python", "postgresql", "docker"],
                metadata={"city": "Lyon", "country": "FR", "job_type": "full_time"},
            ),
            RawJob(
                source_name=self.source_name,
                external_job_id="fake-2001",
                source_url=f"{self.source_url}/2001",
                title="Frontend Engineer",
                company_name="Blue Horizon",
                description="Ship accessible interfaces for an internal product team.",
                location_raw="Berlin, Germany",
                contract_type_raw="full_time",
                remote_type_raw="remote",
                salary_raw=None,
                publication_date_raw="2026-08-05",
                experience_level_raw="Mid",
                technologies=["typescript", "react", "vite"],
                metadata={"city": "Berlin", "country": "DE", "job_type": "full_time"},
            ),
            RawJob(
                source_name=self.source_name,
                external_job_id="fake-3001",
                source_url=f"{self.source_url}/3001",
                title="Data Analyst",
                company_name="Cobalt Research",
                description="Analyze product and marketing metrics with SQL and BI tooling.",
                location_raw="London, United Kingdom",
                contract_type_raw="contract",
                remote_type_raw="hybrid",
                salary_raw="£50k - £70k",
                publication_date_raw="2026-08-07",
                experience_level_raw=None,
                technologies=["sql", "python", "dbt"],
                metadata={"city": "London", "country": "UK", "job_type": "full_time"},
            ),
            RawJob(
                source_name=self.source_name,
                external_job_id="fake-4001",
                source_url=f"{self.source_url}/4001",
                title="Platform Engineer",
                company_name="Oak Systems",
                description="Support cloud-native platform operations and developer tooling.",
                location_raw="Remote",
                contract_type_raw="freelance",
                remote_type_raw="remote",
                salary_raw="€90k - €110k",
                publication_date_raw="2026-08-09",
                experience_level_raw="Senior",
                technologies=["kubernetes", "terraform", "aws"],
                metadata={"city": "remote", "country": "EU", "job_type": "contract"},
            ),
            RawJob(
                source_name=self.source_name,
                external_job_id="fake-5001",
                source_url=f"{self.source_url}/5001",
                title="Product Designer",
                company_name="Studio Vale",
                description="Design internal tools and customer-facing experiences.",
                location_raw="Barcelona, Spain",
                contract_type_raw="internship",
                remote_type_raw="on_site",
                salary_raw=None,
                publication_date_raw="2026-08-11",
                experience_level_raw=None,
                technologies=["figma", "research", "ux"],
                metadata={"city": "Barcelona", "country": "ES", "job_type": "internship"},
            ),
        ]

    def collect(self) -> list[RawJob]:
        """Return a fixed list of raw jobs with no network access or randomness."""
        return list(self._jobs)
