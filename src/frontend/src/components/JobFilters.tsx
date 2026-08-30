import type { FormEvent } from 'react';
import type { JobRemoteType, JobSortField, JobSortOrder } from '../types/jobs';

export interface JobFiltersValue {
  company_name: string;
  city: string;
  remote_type: JobRemoteType | '';
  sort_by: JobSortField;
  sort_order: JobSortOrder;
}

interface JobFiltersProps {
  value: JobFiltersValue;
  onChange: (value: JobFiltersValue) => void;
}

export function JobFilters({ value, onChange }: JobFiltersProps) {
  function update<K extends keyof JobFiltersValue>(key: K, next: JobFiltersValue[K]) {
    onChange({ ...value, [key]: next });
  }

  return (
    <form
      className="job-filters"
      role="search"
      aria-label="Job filters"
      onSubmit={(event: FormEvent<HTMLFormElement>) => event.preventDefault()}
    >
      <div className="job-filters__field">
        <label htmlFor="filter-company">Company</label>
        <input
          id="filter-company"
          type="text"
          value={value.company_name}
          onChange={(event) => update('company_name', event.target.value)}
        />
      </div>
      <div className="job-filters__field">
        <label htmlFor="filter-city">City</label>
        <input
          id="filter-city"
          type="text"
          value={value.city}
          onChange={(event) => update('city', event.target.value)}
        />
      </div>
      <div className="job-filters__field">
        <label htmlFor="filter-remote">Remote</label>
        <select
          id="filter-remote"
          value={value.remote_type}
          onChange={(event) => update('remote_type', event.target.value as JobFiltersValue['remote_type'])}
        >
          <option value="">Any</option>
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="on_site">On-site</option>
        </select>
      </div>
      <div className="job-filters__field">
        <label htmlFor="filter-sort-by">Sort by</label>
        <select
          id="filter-sort-by"
          value={value.sort_by}
          onChange={(event) => update('sort_by', event.target.value as JobSortField)}
        >
          <option value="publication_date">Publication date</option>
          <option value="created_at">Date added</option>
          <option value="title">Title</option>
        </select>
      </div>
      <div className="job-filters__field">
        <label htmlFor="filter-sort-order">Order</label>
        <select
          id="filter-sort-order"
          value={value.sort_order}
          onChange={(event) => update('sort_order', event.target.value as JobSortOrder)}
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>
    </form>
  );
}
