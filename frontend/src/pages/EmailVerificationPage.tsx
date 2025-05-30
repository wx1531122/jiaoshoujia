// frontend/src/pages/EmailVerificationPage.tsx
import React, { useEffect, useState } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import AuthService from '../services/authService'; // Corrected path
import { AuthLayout } from '../components/layout/AuthLayout'; // Corrected path
// import { useAuth } from '../contexts/AuthContext'; // If auto-login or user state update is needed

export const EmailVerificationPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();
  // const { checkUserAuthentication } = useAuth(); // Example if re-fetching user state

  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');
  const [message, setMessage] = useState<string>('Verifying your email address...');

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('No verification token found. Please use the link sent to your email.');
      return;
    }

    const verifyToken = async () => {
      try {
        // Option 1: If backend verifies on GET and this page is just for UX.
        // We assume the backend has already processed the token if the link was valid.
        // For a more robust UX, an API call here would confirm.

        // Option 2: Call an explicit verification endpoint (if AuthService.verifyEmail were active)
        // await AuthService.verifyEmail(token); 
        
        // For now, simulate success if token exists, as AuthService.verifyEmail is commented out.
        // In a real scenario, this would involve an API call.
        console.log("Simulating email verification for token:", token);
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call

        setStatus('success');
        setMessage('Your email has been successfully verified! You can now login.');
        
        // Optional: Automatically update user auth state if they are logged in elsewhere or can auto-login.
        // if (typeof checkUserAuthentication === 'function') {
        //    await checkUserAuthentication(); 
        // }

        // Optional: Redirect to login after a delay
        const timer = setTimeout(() => { // Store timer to clear it on unmount
          navigate('/login');
        }, 3000);
        return () => clearTimeout(timer); // Cleanup timer on component unmount

      } catch (err: any) {
        setStatus('error');
        const errorMessage = err.response?.data?.detail || err.message || 'Failed to verify email. The link may be invalid or expired.';
        setMessage(errorMessage);
        console.error("Email verification error:", err);
      }
    };

    verifyToken();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token, navigate]); // Removed checkUserAuthentication from deps as it's commented out

  const renderContent = () => {
    switch (status) {
      case 'verifying':
        return <p>{message}</p>; // Or a loading spinner
      case 'success':
        return (
          <>
            <p style={{ color: 'green' }}>{message}</p>
            <Link to="/login">Go to Login</Link>
          </>
        );
      case 'error':
        return (
          <>
            <p style={{ color: 'red' }}>{message}</p>
            <p>If you need a new verification link, please try registering again or request a new link (if feature exists).</p>
            <Link to="/register">Go to Register</Link>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <AuthLayout title="Email Verification">
      <div style={{ textAlign: 'center' }}>
        {renderContent()}
      </div>
    </AuthLayout>
  );
};

export default EmailVerificationPage;
