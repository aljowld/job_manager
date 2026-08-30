import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router';
import { ApiError } from '../api/client';
import { getJobs } from '../api/jobs';
import { JobCard } from '../components/JobCard';
import { JobFilters, type JobFiltersValue } from '../components/JobFilters';
import { Pagination } from '../components/Pagination';
import { StatusMessage } from '../components/StatusMessage';
import type {
  JobOfferListResponse,
  JobRemoteType,
  JobSortField,
  JobSortOrder,
} from '../types/jobs';

const PAGE_SIZE = 20;
const DEFAULT_SORT_BY: JobSortField = 'publication_date';
const DEFAULT_SORT_ORDER: JobSortOrder = 'desc';

function readFilters(searchParams: URLSearchParams): JobFiltersValue {
  return {
    company_name: searchParams.get('company_name') ?? '',
    city: searchParams.get('city') ?? '',
    remote_type: (searchParams.get('remote_type') as JobRemoteType | null) ?? '',
    sort_by: (searchParams.get('sort_by') as JobSortField | null) ?? DEFAULT_SORT_BY,
    sort_order: (searchParams.get('sort_order') as JobSortOrder | null) ?? DEFAULT_SORT_ORDER,
  };
}

function readPage(searchParams: URLSearchParams): number {
  const raw = Number(searchParams.get('page') ?? '1');
  return Number.isInteger(raw) && raw > 0 ? raw : 1;
}

export function JobsListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const filters = readFilters(searchParams);
  const page = readPage(searchParams);

  const [data, setData] = useState<JobOfferListResponse | null>(null);
  const [status, setStatus] = useState<'loading' | 'loaded' | 'error'>('loading');
  const [errorMessage, setErrorMessage] = useState('');
  const [reloadToken, setReloadToken] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setStatus('loading');

    getJobs({
      page,
      page_size: PAGE_SIZE,
      company_name: filters.company_name || undefined,
      city: filters.city || undefined,
      remote_type: filters.remote_type || undefined,
      sort_by: filters.sort_by,
      sort_order: filters.sort_order,
    })
      .then((response) => {
        if (cancelled) {
          return;
        }
        setData(response);
        setStatus('loaded');
      })
      .catch((error: unknown) => {
        if (cancelled) {
          return;
        }
        setErrorMessage(
          error instanceof ApiError ? error.message : 'Unexpected error while loading offers.',
        );
        setStatus('error');
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    page,
    filters.company_name,
    filters.city,
    filters.remote_type,
    filters.sort_by,
    filters.sort_order,
    reloadToken,
  ]);

  function applySearchParams(next: JobFiltersValue, nextPage: number) {
    const params = new URLSearchParams();
    if (next.company_name) {
      params.set('company_name', next.company_name);
    }
    if (next.city) {
      params.set('city', next.city);
    }
    if (next.remote_type) {
      params.set('remote_type', next.remote_type);
    }
    if (next.sort_by !== DEFAULT_SORT_BY) {
      params.set('sort_by', next.sort_by);
    }
    if (next.sort_order !== DEFAULT_SORT_ORDER) {
      params.set('sort_order', next.sort_order);
    }
    if (nextPage > 1) {
      params.set('page', String(nextPage));
    }
    setSearchParams(params);
  }

  function handleFiltersChange(nextFilters: JobFiltersValue) {
    applySearchParams(nextFilters, 1);
  }

  function handlePageChange(nextPage: number) {
    applySearchParams(filters, nextPage);
  }

  return (
    <section className="jobs-list-page">
      <h1>Job offers</h1>
      <JobFilters value={filters} onChange={handleFiltersChange} />

      {status === 'loading' && <StatusMessage kind="loading" message="Loading offers…" />}

      {status === 'error' && (
        <StatusMessage
          kind="error"
          message={errorMessage}
          onRetry={() => setReloadToken((token) => token + 1)}
        />
      )}

      {status === 'loaded' && data && data.items.length === 0 && (
        <StatusMessage kind="empty" message="No offers match your filters." />
      )}

      {status === 'loaded' && data && data.items.length > 0 && (
        <>
          <ul className="job-list">
            {data.items.map((job) => (
              <li key={job.id}>
                <JobCard job={job} />
              </li>
            ))}
          </ul>
          <Pagination
            page={data.page}
            pageSize={data.page_size}
            total={data.total}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </section>
  );
}
