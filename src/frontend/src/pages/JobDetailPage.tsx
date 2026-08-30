import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router';
import { ApiError } from '../api/client';
import { getJob } from '../api/jobs';
import { StatusMessage } from '../components/StatusMessage';
import type { JobOfferDetail } from '../types/jobs';

function formatDate(value: string | null): string | null {
  if (!value) {
    return null;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date.toLocaleString();
}

function formatSalary(job: JobOfferDetail): string | null {
  if (job.salary_min == null && job.salary_max == null) {
    return null;
  }
  const range = [job.salary_min, job.salary_max].filter((value) => value != null).join(' \u2013 ');
  const unit = [job.salary_currency, job.salary_period].filter(Boolean).join(' / ');
  return unit ? `${range} ${unit}` : range;
}

type PageStatus = 'loading' | 'loaded' | 'not-found' | 'error';

export function JobDetailPage() {
  const params = useParams<{ id: string }>();
  const jobId = Number(params.id);

  const [job, setJob] = useState<JobOfferDetail | null>(null);
  const [status, setStatus] = useState<PageStatus>('loading');
  const [errorMessage, setErrorMessage] = useState('');
  const [reloadToken, setReloadToken] = useState(0);

  useEffect(() => {
    if (!Number.isInteger(jobId) || jobId <= 0) {
      setStatus('not-found');
      return;
    }

    let cancelled = false;
    setStatus('loading');

    getJob(jobId)
      .then((response) => {
        if (cancelled) {
          return;
        }
        setJob(response);
        setStatus('loaded');
      })
      .catch((error: unknown) => {
        if (cancelled) {
          return;
        }
        if (error instanceof ApiError && error.status === 404) {
          setStatus('not-found');
          return;
        }
        setErrorMessage(
          error instanceof ApiError ? error.message : 'Unexpected error while loading the offer.',
        );
        setStatus('error');
      });

    return () => {
      cancelled = true;
    };
  }, [jobId, reloadToken]);

  const location = job ? [job.city, job.country].filter(Boolean).join(', ') : '';
  const salary = job ? formatSalary(job) : null;

  return (
    <section className="job-detail-page">
      <p>
        <Link to="/jobs">&larr; Back to offers</Link>
      </p>

      {status === 'loading' && <StatusMessage kind="loading" message="Loading offer\u2026" />}
      {status === 'not-found' && (
        <StatusMessage kind="not-found" message="This offer was not found." />
      )}
      {status === 'error' && (
        <StatusMessage
          kind="error"
          message={errorMessage}
          onRetry={() => setReloadToken((token) => token + 1)}
        />
      )}

      {status === 'loaded' && job && (
        <article className="job-detail">
          <h1>{job.title}</h1>
          {job.company_name && <p className="job-detail__company">{job.company_name}</p>}
          {job.company_description && <p className="job-detail__company-about">{job.company_description}</p>}

          <ul className="job-detail__meta">
            {(location || job.location_text) && <li>{location || job.location_text}</li>}
            {job.contract_type && <li>{job.contract_type}</li>}
            {job.job_type && <li>{job.job_type}</li>}
            {job.remote_type && <li>{job.remote_type}</li>}
            {job.experience_level && <li>{job.experience_level}</li>}
            {job.education_level && <li>{job.education_level}</li>}
            {job.industry && <li>{job.industry}</li>}
            {job.job_category && <li>{job.job_category}</li>}
            {job.duration && <li>{job.duration}</li>}
            {salary && <li>{salary}</li>}
            {formatDate(job.publication_date) && <li>Published {formatDate(job.publication_date)}</li>}
            {formatDate(job.expiration_date) && <li>Expires {formatDate(job.expiration_date)}</li>}
          </ul>

          {job.description && (
            <div className="job-detail__description">
              <h2>Description</h2>
              <p>{job.description}</p>
            </div>
          )}

          <div className="job-detail__provenance">
            <h2>Provenance</h2>
            {job.occurrences.length === 0 && <p>No source information available.</p>}
            {job.occurrences.length > 0 && (
              <ul>
                {job.occurrences.map((occurrence) => (
                  <li key={occurrence.id}>
                    <span>{occurrence.source_name ?? 'Unknown source'}</span>
                    {occurrence.is_primary && <span className="badge">primary</span>}
                    {occurrence.external_job_id && <span> &middot; ref {occurrence.external_job_id}</span>}
                    {formatDate(occurrence.collected_at) && (
                      <span> &middot; collected {formatDate(occurrence.collected_at)}</span>
                    )}
                    {occurrence.source_url && (
                      <span>
                        {' '}
                        &middot;{' '}
                        <a href={occurrence.source_url} target="_blank" rel="noopener noreferrer">
                          View source
                        </a>
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </article>
      )}
    </section>
  );
}
