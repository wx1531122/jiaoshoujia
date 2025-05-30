// frontend/src/pages/RequestPasswordResetPage.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { AuthLayout } from '../components/layout/AuthLayout'; // Corrected path
import { RequestPasswordResetForm } from '../components/auth/RequestPasswordResetForm'; // Corrected path
// import { Notification } from '../components/common/Notification'; // For standalone notification display
// import { useNotificationHandler } from '../hooks/useNotificationHandler'; // If using a hook for notifications

export const RequestPasswordResetPage: React.FC = () => {
  // const { notification, showNotification, hideNotification } = useNotificationHandler(); // If using hook

  return (
    <AuthLayout title="Forgot Your Password?">
      {/* {notification && (
        <Notification 
          message={notification.message} 
          type={notification.type} 
          onClose={hideNotification} 
        />
      )} */}
      <RequestPasswordResetForm />
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <p>
          Remembered your password? <Link to="/login">Login</Link>
        </p>
        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </AuthLayout>
  );
};

// Default export is good practice for page components
export default RequestPasswordResetPage;
