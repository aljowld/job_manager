import { beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router';
import { JobDetailPage } from './JobDetailPage';
import { getJob } from '../api/jobs';
import { ApiError } from '../api/client';

vi.mock('../api/jobs', () => ({
  getJob: vi.fn(),
}));

const mockedGetJob = vi.mocked(getJob);

function renderPage(id = '7') {
  return render(
    <MemoryRouter initialEntries={[`/jobs/${id}`]}>
      <Routes>
        <Route path="/jobs/:id" element={<JobDetailPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  mockedGetJob.mockReset();
});

describe('JobDetailPage', () => {
  it('shows a loading state before the response resolves', () => {
    mockedGetJob.mockReturnValue(new Promise(() => {}));

    renderPage();

    expect(screen.getByText(/loading offer/i)).toBeInTheDocument();
  });

  it('renders the offer once loaded, including provenance', async () => {
    mockedGetJob.mockResolvedValue({
      id: 7,
      title: 'Backend Engineer',
      company_name: 'Acme',
      company_description: null,
      description: 'Build things.',
      normalized_description: null,
      job_type: 'full_time',
      contract_type: 'cdi',
      location_text: null,
      city: 'Paris',
      region: null,
      country: 'France',
      remote_type: 'remote',
      salary_min: null,
      salary_max: null,
      salary_currency: null,
      salary_period: null,
      duration: null,
      experience_level: null,
      education_level: null,
      industry: null,
      job_category: null,
      publication_date: null,
      expiration_date: null,
      status: 'active',
      occurrences: [
        {
          id: 1,
          source_name: 'arbeitnow',
          source_url: 'https://example.com/job/7',
          external_job_id: 'ext-7',
          collected_at: '2026-01-01T00:00:00Z',
          is_primary: true,
        },
      ],
    });

    renderPage();

    expect(await screen.findByText('Backend Engineer')).toBeInTheDocument();
    expect(screen.getByText('arbeitnow')).toBeInTheDocument();
    const link = screen.getByRole('link', { name: 'View source' });
    expect(link).toHaveAttribute('href', 'https://example.com/job/7');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');
  });

  it('shows a not-found state on a 404', async () => {
    mockedGetJob.mockRejectedValue(new ApiError('Not found', 404));

    renderPage();

    expect(await screen.findByText('This offer was not found.')).toBeInTheDocument();
  });

  it('shows an error state on other failures', async () => {
    mockedGetJob.mockRejectedValue(new ApiError('Boom', 500));

    renderPage();

    expect(await screen.findByText('Boom')).toBeInTheDocument();
  });
});
