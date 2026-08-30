import { request } from './client';
import type { ProfileInput, ProfileOutput } from '../types/profile';

export function getProfile(): Promise<ProfileOutput> {
  return request<ProfileOutput>('/profile');
}

export function updateProfile(payload: ProfileInput): Promise<ProfileOutput> {
  return request<ProfileOutput>('/profile', undefined, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
}

