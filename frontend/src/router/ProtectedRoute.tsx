import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingSpinner } from '../components/common/LoadingSpinner'; // Optional, for loading state

export const ProtectedRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    // Show a loading spinner or a simple message while checking auth status
    return <LoadingSpinner />;
    // Or return <div>Loading authentication status...</div>;
  }

  if (!isAuthenticated) {
    // User is not authenticated, redirect to login page
    // Pass the current location in state so we can redirect back after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // User is authenticated, render the child route's component
  return <Outlet />;
};

export default ProtectedRoute;
