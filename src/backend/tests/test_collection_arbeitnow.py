"""Unit tests for the Arbeitnow job source connector (no real network access)."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import httpx
import pytest

from app.collection.arbeitnow import ArbeitnowApiError, ArbeitnowJobSource
from app.collection.base import JobCollector


def _job_item(
    *,
    slug: str = "senior-python-engineer-berlin-123",
    title: str = "Senior Python Engineer",
    company_name: str = "Acme GmbH",
    remote: bool = False,
    location: str = "Berlin",
    job_types: list[str] | None = None,
    tags: list[str] | None = None,
    created_at: int = 1788000000,
) -> dict:
    return {
        "slug": slug,
        "company_name": company_name,
        "title": title,
        "description": "<p>Build great backend systems.</p>",
        "remote": remote,
        "url": f"https://www.arbeitnow.com/jobs/companies/acme/{slug}",
        "tags": tags if tags is not None else ["python", "fastapi"],
        "job_types": job_types if job_types is not None else ["Experienced", "Full time"],
        "location": location,
        "created_at": created_at,
    }


def _make_transport(pages: dict[int, list[dict]]) -> httpx.MockTransport:
    """Build a transport that serves fixture pages keyed by the '?page=' query param."""

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        data = pages.get(page, [])
        return httpx.Response(200, json={"data": data})

    return httpx.MockTransport(handler)


def _source_with_transport(transport: httpx.MockTransport, **kwargs) -> ArbeitnowJobSource:
    client = httpx.Client(transport=transport)
    return ArbeitnowJobSource(client=client, **kwargs)


def test_arbeitnow_source_satisfies_job_collector_protocol() -> None:
    source = ArbeitnowJobSource()
    assert isinstance(source, JobCollector)


def test_collect_maps_a_single_page_job_correctly() -> None:
    transport = _make_transport({1: [_job_item()]})
    source = _source_with_transport(transport, max_pages=1)

    raw_jobs = source.collect()

    assert len(raw_jobs) == 1
    raw_job = raw_jobs[0]
    assert raw_job.source_name == "arbeitnow"
    assert raw_job.external_job_id == "senior-python-engineer-berlin-123"
    assert raw_job.source_url == "https://www.arbeitnow.com/jobs/companies/acme/senior-python-engineer-berlin-123"
    assert raw_job.title == "Senior Python Engineer"
    assert raw_job.company_name == "Acme GmbH"
    assert raw_job.location_raw == "Berlin"
    assert raw_job.contract_type_raw == "Experienced; Full time"
    assert raw_job.remote_type_raw is None
    assert raw_job.technologies == ["python", "fastapi"]
    assert raw_job.metadata == {"job_types": ["Experienced", "Full time"]}


def test_collect_represents_remote_flag_as_raw_string() -> None:
    transport = _make_transport({1: [_job_item(remote=True)]})
    source = _source_with_transport(transport, max_pages=1)

    raw_job = source.collect()[0]

    assert raw_job.remote_type_raw == "remote"


def test_collect_converts_created_at_timestamp_to_iso_string() -> None:
    timestamp = 1788000000
    transport = _make_transport({1: [_job_item(created_at=timestamp)]})
    source = _source_with_transport(transport, max_pages=1)

    raw_job = source.collect()[0]

    assert raw_job.publication_date_raw == datetime.fromtimestamp(timestamp, tz=UTC).isoformat()


def test_collect_paginates_across_multiple_pages_and_stops_on_empty_page() -> None:
    transport = _make_transport(
        {
            1: [_job_item(slug="job-page-1")],
            2: [_job_item(slug="job-page-2")],
            3: [],
        }
    )
    source = _source_with_transport(transport, max_pages=5)

    raw_jobs = source.collect()

    assert [job.external_job_id for job in raw_jobs] == ["job-page-1", "job-page-2"]


def test_collect_stops_at_max_pages_even_if_more_pages_exist() -> None:
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        page = int(request.url.params.get("page", "1"))
        return httpx.Response(200, json={"data": [_job_item(slug=f"job-page-{page}")]})

    source = _source_with_transport(httpx.MockTransport(handler), max_pages=2)

    raw_jobs = source.collect()

    assert call_count == 2
    assert [job.external_job_id for job in raw_jobs] == ["job-page-1", "job-page-2"]


def test_collect_raises_on_non_2xx_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="internal error")

    source = _source_with_transport(httpx.MockTransport(handler), max_pages=1)

    with pytest.raises(ArbeitnowApiError):
        source.collect()


def test_collect_raises_on_invalid_json() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not json")

    source = _source_with_transport(httpx.MockTransport(handler), max_pages=1)

    with pytest.raises(ArbeitnowApiError):
        source.collect()


def test_collect_raises_on_unexpected_response_shape() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"unexpected": "shape"})

    source = _source_with_transport(httpx.MockTransport(handler), max_pages=1)

    with pytest.raises(ArbeitnowApiError):
        source.collect()


def test_collect_raises_on_timeout() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out", request=request)

    source = _source_with_transport(httpx.MockTransport(handler), max_pages=1)

    with pytest.raises(ArbeitnowApiError):
        source.collect()


def test_collect_skips_malformed_item_without_failing_the_batch() -> None:
    malformed = {"title": "Missing slug and url"}
    transport = _make_transport({1: [malformed, _job_item(slug="valid-job")]})
    source = _source_with_transport(transport, max_pages=1)

    raw_jobs = source.collect()

    assert [job.external_job_id for job in raw_jobs] == ["valid-job"]


def test_collect_never_performs_a_real_network_call() -> None:
    """Regression guard: the default client is never constructed in these tests."""
    transport = _make_transport({1: [_job_item()]})
    source = _source_with_transport(transport, max_pages=1)

    # If this test made a real network call it would raise (MockTransport handles it instead).
    raw_jobs = source.collect()
    assert len(raw_jobs) == 1


def test_job_item_fixture_round_trips_through_json() -> None:
    """Sanity check that fixtures mirror the documented API JSON shape."""
    payload = json.dumps({"data": [_job_item()]})
    assert json.loads(payload)["data"][0]["slug"] == "senior-python-engineer-berlin-123"
