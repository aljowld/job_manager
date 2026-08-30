export type StatusMessageKind = 'loading' | 'empty' | 'error' | 'not-found';

interface StatusMessageProps {
  kind: StatusMessageKind;
  message: string;
  onRetry?: () => void;
}

/** Reusable loading/empty/error/not-found placeholder, used instead of a silent blank screen. */
export function StatusMessage({ kind, message, onRetry }: StatusMessageProps) {
  return (
    <div className={`status-message status-message--${kind}`} role={kind === 'error' ? 'alert' : 'status'}>
      <p>{message}</p>
      {onRetry && (
        <button type="button" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}
