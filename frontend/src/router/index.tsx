import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './ProtectedRoute';

// Placeholder Page Components
// These would ideally be in frontend/src/pages/
// For now, defined inline for simplicity of this routing task.

const PlaceholderComponent = ({ name }: { name: string }) => (
  <div>
    <h2>{name} Page</h2>
    <p>This is a placeholder for the {name} page.</p>
    {name === "Home" && <p>This is a protected area.</p>}
    {name === "Profile" && <p>This is another protected area.</p>}
  </div>
);

// const LoginPage = () => <PlaceholderComponent name="Login" />; // Replaced by actual import
import LoginPage from '../pages/LoginPage'; // Import the actual LoginPage
// const RegisterPage = () => <PlaceholderComponent name="Register" />; // Replaced by actual import
import RegisterPage from '../pages/RegisterPage'; // Import the actual RegisterPage
// const HomePage = () => <PlaceholderComponent name="Home" />; // Replaced by actual import
import HomePage from '../pages/HomePage'; // Import the actual HomePage
// const ProfilePage = () => <PlaceholderComponent name="Profile" />; // Replaced by actual import
import ProfilePage from '../pages/ProfilePage'; // Import the actual ProfilePage
const NotFoundPage = () => <PlaceholderComponent name="404 Not Found" />;


export const AppRouter: React.FC = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected Routes */}
      {/* All routes nested under this <Route> will use ProtectedRoute */}
      <Route path="/" element={<ProtectedRoute />}>
        {/* Outlet in ProtectedRoute will render these children based on path */}
        <Route index element={<HomePage />} /> {/* Default child for "/" */}
        <Route path="profile" element={<ProfilePage />} />
        {/* Example: <Route path="dashboard" element={<DashboardPage />} /> */}
      </Route>

      {/* Optional: Not Found Route - Catches any path not matched above */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

// Note: BrowserRouter itself should wrap this AppRouter in a higher-level component
// like App.tsx or main.tsx.
export default AppRouter; // Default export is also common for the main router config
