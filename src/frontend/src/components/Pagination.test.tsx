import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { Pagination } from './Pagination';

describe('Pagination', () => {
  it('disables Previous on the first page and Next on the last page', () => {
    render(<Pagination page={1} pageSize={20} total={15} onPageChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Previous' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Next' })).toBeDisabled();
  });

  it('calls onPageChange with the next page when Next is clicked', () => {
    const onPageChange = vi.fn();
    render(<Pagination page={1} pageSize={20} total={45} onPageChange={onPageChange} />);

    fireEvent.click(screen.getByRole('button', { name: 'Next' }));

    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it('calls onPageChange with the previous page when Previous is clicked', () => {
    const onPageChange = vi.fn();
    render(<Pagination page={2} pageSize={20} total={45} onPageChange={onPageChange} />);

    fireEvent.click(screen.getByRole('button', { name: 'Previous' }));

    expect(onPageChange).toHaveBeenCalledWith(1);
  });
});
