import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router';
import { JobsListPage } from './JobsListPage';
import { getJobs } from '../api/jobs';
import { ApiError } from '../api/client';

vi.mock('../api/jobs', () => ({
  getJobs: vi.fn(),
}));

const mockedGetJobs = vi.mocked(getJobs);

function renderPage(initialEntries: string[] = ['/jobs']) {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      <Routes>
        <Route path="/jobs" element={<JobsListPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  mockedGetJobs.mockReset();
});

describe('JobsListPage', () => {
  it('shows a loading state before the response resolves', () => {
    mockedGetJobs.mockReturnValue(new Promise(() => {}));

    renderPage();

    expect(screen.getByText(/loading offers/i)).toBeInTheDocument();
  });

  it('renders the returned offers', async () => {
    mockedGetJobs.mockResolvedValue({
      page: 1,
      page_size: 20,
      total: 1,
      items: [
        {
          id: 1,
          title: 'Backend Engineer',
          company_name: 'Acme',
          city: 'Paris',
          country: 'France',
          contract_type: 'cdi',
          job_type: 'full_time',
          remote_type: 'remote',
          status: 'active',
          publication_date: '2026-01-01',
        },
      ],
    });

    renderPage();

    expect(await screen.findByText('Backend Engineer')).toBeInTheDocument();
  });

  it('shows an empty state when there are no results', async () => {
    mockedGetJobs.mockResolvedValue({ page: 1, page_size: 20, total: 0, items: [] });

    renderPage();

    expect(await screen.findByText(/no offers match/i)).toBeInTheDocument();
  });

  it('shows an error state when the request fails', async () => {
    mockedGetJobs.mockRejectedValue(new ApiError('Boom', 500));

    renderPage();

    expect(await screen.findByText('Boom')).toBeInTheDocument();
  });

  it('requests the next page when Next is clicked', async () => {
    mockedGetJobs.mockResolvedValue({
      page: 1,
      page_size: 20,
      total: 40,
      items: [
        {
          id: 1,
          title: 'Backend Engineer',
          company_name: null,
          city: null,
          country: null,
          contract_type: null,
          job_type: null,
          remote_type: null,
          status: 'active',
          publication_date: null,
        },
      ],
    });

    renderPage();
    await screen.findByText('Backend Engineer');

    fireEvent.click(screen.getByRole('button', { name: 'Next' }));

    await waitFor(() => {
      expect(mockedGetJobs).toHaveBeenLastCalledWith(expect.objectContaining({ page: 2 }));
    });
  });

  it('requests filtered results when the company filter changes', async () => {
    mockedGetJobs.mockResolvedValue({ page: 1, page_size: 20, total: 0, items: [] });

    renderPage();
    await screen.findByText(/no offers match/i);

    fireEvent.change(screen.getByLabelText('Company'), { target: { value: 'Acme' } });

    await waitFor(() => {
      expect(mockedGetJobs).toHaveBeenLastCalledWith(
        expect.objectContaining({ company_name: 'Acme', page: 1 }),
      );
    });
  });

  it('links each offer to its detail page', async () => {
    mockedGetJobs.mockResolvedValue({
      page: 1,
      page_size: 20,
      total: 1,
      items: [
        {
          id: 42,
          title: 'Backend Engineer',
          company_name: null,
          city: null,
          country: null,
          contract_type: null,
          job_type: null,
          remote_type: null,
          status: 'active',
          publication_date: null,
        },
      ],
    });

    renderPage();

    const link = await screen.findByRole('link', { name: 'Backend Engineer' });
    expect(link).toHaveAttribute('href', '/jobs/42');
  });
});
