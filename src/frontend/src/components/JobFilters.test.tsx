import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { JobFilters, type JobFiltersValue } from './JobFilters';

const baseValue: JobFiltersValue = {
  company_name: '',
  city: '',
  remote_type: '',
  sort_by: 'publication_date',
  sort_order: 'desc',
};

describe('JobFilters', () => {
  it('calls onChange with the updated company name', () => {
    const onChange = vi.fn();
    render(<JobFilters value={baseValue} onChange={onChange} />);

    fireEvent.change(screen.getByLabelText('Company'), { target: { value: 'OpenAI' } });

    expect(onChange).toHaveBeenCalledWith({ ...baseValue, company_name: 'OpenAI' });
  });

  it('calls onChange with the updated remote type', () => {
    const onChange = vi.fn();
    render(<JobFilters value={baseValue} onChange={onChange} />);

    fireEvent.change(screen.getByLabelText('Remote'), { target: { value: 'remote' } });

    expect(onChange).toHaveBeenCalledWith({ ...baseValue, remote_type: 'remote' });
  });
});
