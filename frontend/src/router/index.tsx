import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './ProtectedRoute';

// Import existing pages
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import HomePage from '../pages/HomePage';
import ProfilePage from '../pages/ProfilePage';

// Import new pages for Phase 2
import RequestPasswordResetPage from '../pages/RequestPasswordResetPage';
import ResetPasswordPage from '../pages/ResetPasswordPage';
import EmailVerificationPage from '../pages/EmailVerificationPage';

// A more descriptive NotFoundPage placeholder
const NotFoundPage = () => (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <h2>404 - Page Not Found</h2>
        <p>Sorry, the page you are looking for does not exist.</p>
    </div>
);

export const AppRouter: React.FC = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      {/* Phase 2 Public Routes for Password Reset and Email Verification */}
      <Route path="/request-password-reset" element={<RequestPasswordResetPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} /> 
      {/* Note: ResetPasswordPage expects token from query param ?token=... */}
      <Route path="/verify-email" element={<EmailVerificationPage />} />
      {/* Note: EmailVerificationPage expects token from query param ?token=... */}

      {/* Protected Routes */}
      <Route path="/" element={<ProtectedRoute />}>
        <Route index element={<HomePage />} />
        <Route path="profile" element={<ProfilePage />} />
        {/* Example: <Route path="dashboard" element={<DashboardPage />} /> */}
      </Route>

      {/* Optional: Not Found Route - Catches any path not matched above */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default AppRouter;
