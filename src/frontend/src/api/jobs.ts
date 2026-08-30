import { request } from './client';
import type { JobListParams, JobOfferDetail, JobOfferListResponse } from '../types/jobs';

export function getJobs(params: JobListParams = {}): Promise<JobOfferListResponse> {
  return request<JobOfferListResponse>('/jobs', params);
}

export function getJob(id: number): Promise<JobOfferDetail> {
  return request<JobOfferDetail>(`/jobs/${id}`);
}
