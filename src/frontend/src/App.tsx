import { Link, Navigate, Route, Routes } from 'react-router';
import { StatusMessage } from './components/StatusMessage';
import { JobDetailPage } from './pages/JobDetailPage';
import { JobsListPage } from './pages/JobsListPage';
import { ProfilePage } from './pages/ProfilePage';

export function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <Link to="/jobs" className="app-header__brand">
          Job Manager
        </Link>
        <nav className="app-header__nav" style={{ marginLeft: 'auto', paddingRight: '1rem' }}>
          <Link to="/profile" style={{ color: 'white', textDecoration: 'none' }}>Profile</Link>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Navigate to="/jobs" replace />} />
          <Route path="/jobs" element={<JobsListPage />} />
          <Route path="/jobs/:id" element={<JobDetailPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="*" element={<StatusMessage kind="not-found" message="Page not found." />} />
        </Routes>
      </main>
    </div>
  );
}
