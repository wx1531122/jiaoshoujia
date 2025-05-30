// frontend/src/components/auth/ResetPasswordForm.tsx
import React, { useState, FormEvent, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom'; // Removed useParams as it's not used for query params
import AuthService from '../../services/authService'; // Adjust path as needed
// import { useNotifications } from '../../contexts/NotificationContext'; // If a notification system is ready

interface ResetPasswordFormProps {
  token?: string; // Allow token to be passed as a prop, e.g. from page component reading URL
}

export const ResetPasswordForm: React.FC<ResetPasswordFormProps> = ({ token: propToken }) => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Attempt to get token from URL query param if not passed as prop
  // This is common if the link is like /reset-password?token=YOUR_TOKEN
  const [searchParams] = useSearchParams();
  const queryToken = searchParams.get('token');

  const token = propToken || queryToken;

  // const { addNotification } = useNotifications(); // If using NotificationContext

  useEffect(() => {
    if (!token) {
      setError("No reset token found. Please ensure you've used the correct link.");
      // addNotification({ type: 'error', message: 'No reset token found.' });
    }
  }, [token]); // Removed addNotification from dependency array as it's commented out

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token) {
      setError("No reset token available. Cannot reset password.");
      // addNotification({ type: 'error', message: 'Reset token is missing.' });
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      // addNotification({ type: 'error', message: 'Passwords do not match.' });
      return;
    }
    if (password.length < 8) { // Example basic validation
        setError('Password must be at least 8 characters long.');
        // addNotification({ type: 'error', message: 'Password must be at least 8 characters long.' });
        return;
    }

    setIsLoading(true);
    setMessage(null);
    setError(null);

    try {
      // This assumes authService.resetPassword exists
      // For now, we can mock its existence or expect it to be added soon.
      // Placeholder for actual API call:
      // await AuthService.resetPassword(token, password);
      // Simulate API call for now:
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log('Password reset submitted for token:', token, 'with new password.');
      // End of placeholder

      setMessage('Your password has been reset successfully! You can now log in with your new password.');
      // addNotification({ type: 'success', message: 'Password reset successfully!' });
      setPassword('');
      setConfirmPassword('');
      // Optionally, redirect to login page:
      // navigate('/login'); 
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to reset password.';
      setError(errorMessage);
      // addNotification({ type: 'error', message: errorMessage });
      console.error("Reset password error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Set New Password</h2>
      {message && <p style={{ color: 'green', textAlign: 'center' }}>{message}</p>}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
      
      {!token && !error && <p style={{ color: 'orange', textAlign: 'center' }}>Loading token or token not found in URL. Please use the link from your email.</p>}

      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>New Password:</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter new password"
          required
          disabled={isLoading || !token}
          style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="confirmPassword" style={{ display: 'block', marginBottom: '5px' }}>Confirm New Password:</label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm new password"
          required
          disabled={isLoading || !token}
          style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>
      
      <button 
        type="submit" 
        disabled={isLoading || !token}
        style={{ 
          width: '100%', 
          padding: '10px', 
          backgroundColor: (isLoading || !token) ? '#ccc' : '#007bff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '4px', 
          cursor: (isLoading || !token) ? 'default' : 'pointer'
        }}
      >
        {isLoading ? 'Resetting...' : 'Reset Password'}
      </button>
    </form>
  );
};
