// frontend/src/components/auth/RequestPasswordResetForm.tsx
import React, { useState, FormEvent } from 'react';
import AuthService from '../../services/authService'; // Adjust path as needed
// import { useNotifications } from '../../contexts/NotificationContext'; // If a notification system is ready

export const RequestPasswordResetForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  // const { addNotification } = useNotifications(); // If using NotificationContext

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setMessage(null);
    setError(null);

    try {
      // This assumes authService.requestPasswordReset exists and handles API call
      // It should be added in a later step to authService.ts
      // For now, we can mock its existence or expect it to be added soon.
      // To make this component testable standalone, we'll simulate the call for now.
      
      // Placeholder for actual API call:
      // await AuthService.requestPasswordReset(email); 
      // Simulate API call for now:
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay
      console.log('Password reset requested for:', email); 
      // End of placeholder

      setMessage('If an account with that email exists, a password reset link has been sent.');
      // addNotification({ type: 'success', message: 'Password reset link sent!' }); // Example notification
      setEmail(''); // Clear email field on success
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to request password reset.';
      setError(errorMessage);
      // addNotification({ type: 'error', message: errorMessage }); // Example notification
      console.error("Request password reset error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Reset Password</h2>
      {message && <p style={{ color: 'green', textAlign: 'center' }}>{message}</p>}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
      
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email Address:</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
          disabled={isLoading}
          style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>
      
      <button 
        type="submit" 
        disabled={isLoading}
        style={{ 
          width: '100%', 
          padding: '10px', 
          backgroundColor: isLoading ? '#ccc' : '#007bff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '4px', 
          cursor: 'pointer' 
        }}
      >
        {isLoading ? 'Sending...' : 'Send Password Reset Link'}
      </button>
    </form>
  );
};
