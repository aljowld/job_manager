/** Mirrors the backend Pydantic schemas exposed by `GET /api/v1/jobs*`. */

export interface JobSourceOccurrenceSummary {
  id: number;
  source_name: string | null;
  source_url: string | null;
  external_job_id: string | null;
  collected_at: string | null;
  is_primary: boolean;
}

export interface JobOfferSummary {
  id: number;
  title: string;
  company_name: string | null;
  city: string | null;
  country: string | null;
  contract_type: string | null;
  job_type: string | null;
  remote_type: string | null;
  status: string;
  publication_date: string | null;
}

export interface JobOfferDetail {
  id: number;
  title: string;
  company_name: string | null;
  company_description: string | null;
  description: string | null;
  normalized_description: string | null;
  job_type: string | null;
  contract_type: string | null;
  location_text: string | null;
  city: string | null;
  region: string | null;
  country: string | null;
  remote_type: string | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string | null;
  salary_period: string | null;
  duration: string | null;
  experience_level: string | null;
  education_level: string | null;
  industry: string | null;
  job_category: string | null;
  publication_date: string | null;
  expiration_date: string | null;
  status: string;
  occurrences: JobSourceOccurrenceSummary[];
}

export interface JobOfferListResponse {
  page: number;
  page_size: number;
  total: number;
  items: JobOfferSummary[];
}

export type JobSortField = 'publication_date' | 'created_at' | 'title';
export type JobSortOrder = 'asc' | 'desc';
export type JobRemoteType = 'remote' | 'hybrid' | 'on_site';

/** Query params accepted by `GET /api/v1/jobs` that the V1 frontend exposes. */
export interface JobListParams {
  page?: number;
  page_size?: number;
  company_name?: string;
  city?: string;
  remote_type?: JobRemoteType;
  sort_by?: JobSortField;
  sort_order?: JobSortOrder;
  [key: string]: string | number | undefined;
}
