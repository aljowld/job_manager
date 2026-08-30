import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ApiError } from '../api/client';
import { getProfile, updateProfile } from '../api/profile';
import { App } from '../App';
import { ProfilePage } from './ProfilePage';

vi.mock('../api/profile');

const mockGetProfile = vi.mocked(getProfile);
const mockUpdateProfile = vi.mocked(updateProfile);

describe('ProfilePage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(window, 'alert').mockImplementation(() => {});
  });

  const validProfile = {
    id: 1,
    full_name: 'John Doe',
    email: 'john@example.com',
    phone: null,
    location: null,
    mobility: null,
    remote_preference: 'hybrid',
    desired_salary_min: 50000,
    desired_salary_max: null,
    availability_date: null,
    internship_duration_weeks: null,
    contract_types: [{ contract_type: 'cdi', preference_level: 'REQUIRED' as const }],
    job_types: [],
    job_roles: [],
    industries: [],
    skills: [{ skill_name: 'React', proficiency_level: 'advanced', years_experience: 3 }],
    technologies: [{ technology_name: 'Node', proficiency_level: 'intermediate', years_experience: null }],
    languages: [{ language_name: 'English', proficiency_level: 'fluent' }],
    preferred_companies: [],
  };

  it('shows loading state initially', () => {
    mockGetProfile.mockReturnValue(new Promise(() => {})); // Never resolves
    render(<ProfilePage />);
    expect(screen.getByText('Loading profile…')).toBeInTheDocument();
  });

  it('renders correctly on successful GET', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Full Name/i)).toHaveValue('John Doe');
    });
    expect(screen.getByLabelText(/Email/i)).toHaveValue('john@example.com');
    expect(screen.getByLabelText(/Minimum Salary/i)).toHaveValue(50000);
    expect(screen.getByText('cdi')).toBeInTheDocument();
    expect(screen.getByText('React')).toBeInTheDocument();
  });

  it('initializes empty form on PROFILE_NOT_FOUND', async () => {
    mockGetProfile.mockRejectedValueOnce(new ApiError('Not found', 404, 'PROFILE_NOT_FOUND'));
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Full Name/i)).toHaveValue('');
    });
    expect(screen.getByLabelText(/Minimum Salary/i)).toHaveValue(null);
  });

  it('shows error message on other GET errors', async () => {
    mockGetProfile.mockRejectedValueOnce(new ApiError('Server Error', 500));
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByText('Server Error')).toBeInTheDocument();
    });
  });

  it('modifies a simple string field', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Full Name/i)).toHaveValue('John Doe');
    });

    const input = screen.getByLabelText(/Full Name/i);
    fireEvent.change(input, { target: { value: 'Jane Doe' } });
    expect(input).toHaveValue('Jane Doe');
  });

  it('handles empty nullable string as null', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    mockUpdateProfile.mockResolvedValueOnce({ ...validProfile, email: null });
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    });

    const input = screen.getByLabelText(/Email/i);
    fireEvent.change(input, { target: { value: '' } });

    fireEvent.click(screen.getByRole('button', { name: /Save Profile/i }));
    
    expect(mockUpdateProfile).toHaveBeenCalledWith(expect.objectContaining({ email: null }));
  });

  it('handles empty nullable number as null', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    mockUpdateProfile.mockResolvedValueOnce({ ...validProfile, desired_salary_min: null });
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Minimum Salary/i)).toBeInTheDocument();
    });

    const input = screen.getByLabelText(/Minimum Salary/i);
    fireEvent.change(input, { target: { value: '' } });

    fireEvent.click(screen.getByRole('button', { name: /Save Profile/i }));
    
    expect(mockUpdateProfile).toHaveBeenCalledWith(expect.objectContaining({ desired_salary_min: null }));
  });

  it('adds a contract type, changes level and removes it', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByText('cdi')).toBeInTheDocument();
    });

    // Add cdd
    const contractFieldset = screen.getByRole('group', { name: 'Contract Types' });
    const addInput = contractFieldset.querySelector('input[name="value"]') as HTMLInputElement;
    const addSelect = contractFieldset.querySelector('select[name="preference_level"]') as HTMLSelectElement;
    const addButton = contractFieldset.querySelector('button[type="submit"]') as HTMLButtonElement;
    const form = contractFieldset.querySelector('form') as HTMLFormElement;

    fireEvent.change(addInput, { target: { value: 'cdd' } });
    fireEvent.change(addSelect, { target: { value: 'BONUS' } });
    fireEvent.submit(form);

    expect(screen.getByText('cdd')).toBeInTheDocument();
    
    // Check level of new item
    const selects = screen.getAllByRole('combobox');
    const cddSelect = selects.find(s => s.getAttribute('aria-label') === 'Preference level for cdd');
    expect(cddSelect).toHaveValue('BONUS');

    // Change level
    fireEvent.change(cddSelect!, { target: { value: 'AVOID' } });
    expect(cddSelect).toHaveValue('AVOID');

    // Remove it
    const removeBtn = screen.getByRole('button', { name: 'Remove cdd' });
    fireEvent.click(removeBtn);
    expect(screen.queryByText('cdd')).not.toBeInTheDocument();
  });

  it('prevents case-insensitive duplicates in collections', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile); // has 'cdi'
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByText('cdi')).toBeInTheDocument();
    });

    const contractFieldset = screen.getByRole('group', { name: 'Contract Types' });
    const addInput = contractFieldset.querySelector('input[name="value"]') as HTMLInputElement;
    const form = contractFieldset.querySelector('form') as HTMLFormElement;

    fireEvent.change(addInput, { target: { value: 'CDI ' } });
    fireEvent.submit(form);

    expect(window.alert).toHaveBeenCalledWith('This item already exists.');
  });

  it('edits a skill, tech, and language', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByText('React')).toBeInTheDocument();
    });

    // Add Skill
    const skillFieldset = screen.getByRole('group', { name: 'Skills' });
    fireEvent.change(skillFieldset.querySelector('input[name="skill_name"]')!, { target: { value: 'TypeScript' } });
    fireEvent.submit(skillFieldset.querySelector('form')!);
    expect(screen.getByText('TypeScript')).toBeInTheDocument();

    // Add Tech
    const techFieldset = screen.getByRole('group', { name: 'Technologies' });
    fireEvent.change(techFieldset.querySelector('input[name="technology_name"]')!, { target: { value: 'FastAPI' } });
    fireEvent.submit(techFieldset.querySelector('form')!);
    expect(screen.getByText('FastAPI')).toBeInTheDocument();

    // Add Language
    const langFieldset = screen.getByRole('group', { name: 'Languages' });
    fireEvent.change(langFieldset.querySelector('input[name="language_name"]')!, { target: { value: 'Spanish' } });
    fireEvent.change(langFieldset.querySelector('input[name="proficiency_level"]')!, { target: { value: 'Beginner' } });
    fireEvent.submit(langFieldset.querySelector('form')!);
    expect(screen.getByText('Spanish')).toBeInTheDocument();
  });

  it('sends the correct PUT payload and handles saving states', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    
    // Simulate delay for saving
    mockUpdateProfile.mockImplementation(() => {
      return new Promise((resolve) => setTimeout(() => resolve(validProfile), 50));
    });

    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Full Name/i)).toHaveValue('John Doe');
    });

    const saveBtn = screen.getByRole('button', { name: 'Save Profile' });
    fireEvent.click(saveBtn);

    expect(screen.getByText('Saving...')).toBeInTheDocument();
    expect(saveBtn).toBeDisabled();

    // Verify ID is NOT in payload
    const payload = mockUpdateProfile.mock.calls[0][0];
    expect(payload).not.toHaveProperty('id');
    expect(payload).toHaveProperty('full_name', 'John Doe');

    // Wait for success
    await waitFor(() => {
      expect(screen.getByText('Profile saved successfully.')).toBeInTheDocument();
    });
    expect(saveBtn).not.toBeDisabled();
    expect(screen.getByText('Save Profile')).toBeInTheDocument();
  });

  it('handles PUT error without losing draft', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    mockUpdateProfile.mockRejectedValueOnce(new ApiError('Validation Error', 422));
    
    render(<ProfilePage />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Full Name/i)).toHaveValue('John Doe');
    });

    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'Jane Changed' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save Profile' }));

    await waitFor(() => {
      expect(screen.getByText('Validation Error')).toBeInTheDocument();
    });

    // Draft is kept
    expect(screen.getByLabelText(/Full Name/i)).toHaveValue('Jane Changed');
  });

  it('navigates to /profile successfully via router', async () => {
    mockGetProfile.mockResolvedValueOnce(validProfile);
    render(
      <MemoryRouter initialEntries={['/profile']}>
        <App />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('My Profile')).toBeInTheDocument();
    });
  });
});
