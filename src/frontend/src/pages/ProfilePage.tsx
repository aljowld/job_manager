import { useEffect, useState } from 'react';
import { ApiError } from '../api/client';
import { getProfile, updateProfile } from '../api/profile';
import { StatusMessage } from '../components/StatusMessage';
import type { ProfileInput, ProfileOutput } from '../types/profile';
import { PreferenceCollectionEditor } from '../components/profile/PreferenceCollectionEditor';
import { SkillsEditor } from '../components/profile/SkillsEditor';
import { TechnologiesEditor } from '../components/profile/TechnologiesEditor';
import { LanguagesEditor } from '../components/profile/LanguagesEditor';

function createEmptyProfile(): ProfileInput {
  return {
    full_name: null,
    email: null,
    phone: null,
    location: null,
    mobility: null,
    remote_preference: null,
    desired_salary_min: null,
    desired_salary_max: null,
    availability_date: null,
    internship_duration_weeks: null,
    contract_types: [],
    job_types: [],
    job_roles: [],
    industries: [],
    skills: [],
    technologies: [],
    languages: [],
    preferred_companies: [],
  };
}

export function ProfilePage() {
  const [draft, setDraft] = useState<ProfileInput | null>(null);
  const [status, setStatus] = useState<'loading' | 'loaded' | 'error' | 'saving' | 'saved'>('loading');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    let cancelled = false;
    setStatus('loading');

    getProfile()
      .then((data) => {
        if (cancelled) return;
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const { id, ...editableData } = data;
        setDraft(editableData);
        setStatus('loaded');
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        if (error instanceof ApiError && error.code === 'PROFILE_NOT_FOUND') {
          setDraft(createEmptyProfile());
          setStatus('loaded');
          return;
        }
        setErrorMessage(
          error instanceof ApiError ? error.message : 'Unexpected error while loading profile.',
        );
        setStatus('error');
      });

    return () => {
      cancelled = true;
    };
  }, []);

  function handleSimpleFieldChange(
    field: keyof ProfileInput,
    value: string | number | null
  ) {
    if (!draft) return;
    setDraft({ ...draft, [field]: value });
  }

  function handleStringChange(field: keyof ProfileInput, e: React.ChangeEvent<HTMLInputElement>) {
    const val = e.target.value.trim();
    handleSimpleFieldChange(field, val === '' ? null : val);
  }

  function handleNumberChange(field: keyof ProfileInput, e: React.ChangeEvent<HTMLInputElement>) {
    const val = e.target.value;
    handleSimpleFieldChange(field, val === '' ? null : Number(val));
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!draft) return;

    setStatus('saving');
    setErrorMessage('');

    try {
      const savedData = await updateProfile(draft);
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { id, ...editableData } = savedData;
      setDraft(editableData);
      setStatus('saved');
      setTimeout(() => {
        setStatus((current) => (current === 'saved' ? 'loaded' : current));
      }, 3000);
    } catch (error: unknown) {
      setErrorMessage(
        error instanceof ApiError ? error.message : 'Unexpected error while saving profile.',
      );
      setStatus('loaded'); // Restore form visibility
    }
  }

  if (status === 'loading') {
    return <StatusMessage kind="loading" message="Loading profile…" />;
  }

  if (status === 'error') {
    return (
      <StatusMessage
        kind="error"
        message={errorMessage}
        onRetry={() => window.location.reload()}
      />
    );
  }

  if (!draft) {
    return null;
  }

  return (
    <section className="profile-page">
      <h1>My Profile</h1>
      
      {errorMessage && (
        <div className="status-message status-message--error" role="alert">
          {errorMessage}
        </div>
      )}

      {status === 'saved' && (
        <div className="status-message status-message--success" role="alert">
          Profile saved successfully.
        </div>
      )}

      <form onSubmit={handleSave} className="profile-form">
        <fieldset>
          <legend>Personal Information</legend>
          <div className="form-group">
            <label htmlFor="full_name">Full Name</label>
            <input
              type="text"
              id="full_name"
              value={draft.full_name ?? ''}
              onChange={(e) => handleStringChange('full_name', e)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={draft.email ?? ''}
              onChange={(e) => handleStringChange('email', e)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="phone">Phone</label>
            <input
              type="tel"
              id="phone"
              value={draft.phone ?? ''}
              onChange={(e) => handleStringChange('phone', e)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              type="text"
              id="location"
              value={draft.location ?? ''}
              onChange={(e) => handleStringChange('location', e)}
            />
          </div>
        </fieldset>

        <fieldset>
          <legend>Preferences & Availability</legend>
          <div className="form-group">
            <label htmlFor="mobility">Mobility</label>
            <input
              type="text"
              id="mobility"
              value={draft.mobility ?? ''}
              onChange={(e) => handleStringChange('mobility', e)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="remote_preference">Remote Preference</label>
            <input
              type="text"
              id="remote_preference"
              value={draft.remote_preference ?? ''}
              onChange={(e) => handleStringChange('remote_preference', e)}
              placeholder="e.g. hybrid, remote"
            />
          </div>
          <div className="form-group">
            <label htmlFor="desired_salary_min">Minimum Salary</label>
            <input
              type="number"
              id="desired_salary_min"
              value={draft.desired_salary_min ?? ''}
              onChange={(e) => handleNumberChange('desired_salary_min', e)}
              min="0"
            />
          </div>
          <div className="form-group">
            <label htmlFor="desired_salary_max">Maximum Salary</label>
            <input
              type="number"
              id="desired_salary_max"
              value={draft.desired_salary_max ?? ''}
              onChange={(e) => handleNumberChange('desired_salary_max', e)}
              min="0"
            />
          </div>
          <div className="form-group">
            <label htmlFor="availability_date">Availability Date</label>
            <input
              type="date"
              id="availability_date"
              value={draft.availability_date ?? ''}
              onChange={(e) => handleStringChange('availability_date', e)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="internship_duration_weeks">Internship Duration (weeks)</label>
            <input
              type="number"
              id="internship_duration_weeks"
              value={draft.internship_duration_weeks ?? ''}
              onChange={(e) => handleNumberChange('internship_duration_weeks', e)}
              min="0"
            />
          </div>
        </fieldset>

        <div className="form-actions form-actions--top">
          <button type="submit" disabled={status === 'saving'}>
            {status === 'saving' ? 'Saving...' : 'Save Profile'}
          </button>
        </div>
      </form>

      <div className="profile-collections">
        <PreferenceCollectionEditor
          title="Contract Types"
          items={draft.contract_types}
          itemKey="contract_type"
          onChange={(items) => setDraft({ ...draft, contract_types: items })}
        />
        <PreferenceCollectionEditor
          title="Job Types"
          items={draft.job_types}
          itemKey="job_type"
          onChange={(items) => setDraft({ ...draft, job_types: items })}
        />
        <PreferenceCollectionEditor
          title="Job Roles"
          items={draft.job_roles}
          itemKey="job_role"
          onChange={(items) => setDraft({ ...draft, job_roles: items })}
        />
        <PreferenceCollectionEditor
          title="Industries"
          items={draft.industries}
          itemKey="industry"
          onChange={(items) => setDraft({ ...draft, industries: items })}
        />
        <PreferenceCollectionEditor
          title="Preferred Companies"
          items={draft.preferred_companies}
          itemKey="company_name"
          onChange={(items) => setDraft({ ...draft, preferred_companies: items })}
        />

        <SkillsEditor
          items={draft.skills}
          onChange={(items) => setDraft({ ...draft, skills: items })}
        />
        <TechnologiesEditor
          items={draft.technologies}
          onChange={(items) => setDraft({ ...draft, technologies: items })}
        />
        <LanguagesEditor
          items={draft.languages}
          onChange={(items) => setDraft({ ...draft, languages: items })}
        />
      </div>

    </section>
  );
}

