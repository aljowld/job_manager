import { Link } from 'react-router';
import type { JobOfferSummary } from '../types/jobs';

function formatDate(value: string | null): string | null {
  if (!value) {
    return null;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date.toLocaleDateString();
}

export function JobCard({ job }: { job: JobOfferSummary }) {
  const location = [job.city, job.country].filter(Boolean).join(', ');
  const publicationDate = formatDate(job.publication_date);

  return (
    <article className="job-card">
      <h2 className="job-card__title">
        <Link to={`/jobs/${job.id}`}>{job.title}</Link>
      </h2>
      {job.company_name && <p className="job-card__company">{job.company_name}</p>}
      <ul className="job-card__meta">
        {location && <li>{location}</li>}
        {job.contract_type && <li>{job.contract_type}</li>}
        {job.job_type && <li>{job.job_type}</li>}
        {job.remote_type && <li>{job.remote_type}</li>}
        {publicationDate && <li>{publicationDate}</li>}
      </ul>
    </article>
  );
}
