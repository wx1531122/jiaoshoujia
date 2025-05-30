import React, { useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';
import { useAuth } from '../contexts/AuthContext';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { AuthLayout } from '../components/layout/AuthLayout'; // Import AuthLayout

const LoginPage: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      const from = location.state?.from?.pathname || '/';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, isLoading, navigate, location]);

  if (isLoading || (!isLoading && isAuthenticated)) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <AuthLayout title="Login to Your Account"> {/* Use AuthLayout */}
      <LoginForm />
      <p style={{ marginTop: '20px', textAlign: 'center' }}>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
      <p style={{ marginTop: '10px', textAlign: 'center' }}>
        <Link to="/request-password-reset">Forgot password?</Link>
      </p>
    </AuthLayout>
  );
};

export default LoginPage;
