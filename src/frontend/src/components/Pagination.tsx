interface PaginationProps {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ page, pageSize, total, onPageChange }: PaginationProps) {
  const totalPages = pageSize > 0 ? Math.max(1, Math.ceil(total / pageSize)) : 1;
  const canGoPrevious = page > 1;
  const canGoNext = page < totalPages;

  return (
    <nav className="pagination" aria-label="Pagination">
      <button type="button" onClick={() => onPageChange(page - 1)} disabled={!canGoPrevious}>
        Previous
      </button>
      <span className="pagination__status">
        Page {page} / {totalPages} &middot; {total} offer{total === 1 ? '' : 's'}
      </span>
      <button type="button" onClick={() => onPageChange(page + 1)} disabled={!canGoNext}>
        Next
      </button>
    </nav>
  );
}
