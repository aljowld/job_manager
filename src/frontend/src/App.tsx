import { Link, Navigate, Route, Routes } from 'react-router';
import { StatusMessage } from './components/StatusMessage';
import { JobDetailPage } from './pages/JobDetailPage';
import { JobsListPage } from './pages/JobsListPage';

export function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <Link to="/jobs" className="app-header__brand">
          Job Manager
        </Link>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Navigate to="/jobs" replace />} />
          <Route path="/jobs" element={<JobsListPage />} />
          <Route path="/jobs/:id" element={<JobDetailPage />} />
          <Route path="*" element={<StatusMessage kind="not-found" message="Page not found." />} />
        </Routes>
      </main>
    </div>
  );
}
