// frontend/src/pages/ResetPasswordPage.tsx
import React from 'react';
import { Link, useParams, useSearchParams } from 'react-router-dom'; // useParams and useSearchParams imported
import { AuthLayout } from '../components/layout/AuthLayout'; // Corrected path
import { ResetPasswordForm } from '../components/auth/ResetPasswordForm'; // Corrected path
// import { Notification } from '../components/common/Notification';
// import { useNotificationHandler } from '../hooks/useNotificationHandler';

export const ResetPasswordPage: React.FC = () => {
  // const { notification, showNotification, hideNotification } = useNotificationHandler();
  
  // The ResetPasswordForm component itself handles token extraction from query params.
  // If token were part of the path (e.g., /reset-password/:token), we'd use useParams here.
  // For example: const { token: pathToken } = useParams<{ token: string }>();
  // And then pass it to the form: <ResetPasswordForm token={pathToken} />

  // For this setup, ResetPasswordForm internally uses useSearchParams, so no explicit token passing is needed here
  // unless we wanted to override or prioritize a token from a path param.

  return (
    <AuthLayout title="Set Your New Password">
      {/* {notification && (
        <Notification 
          message={notification.message} 
          type={notification.type} 
          onClose={hideNotification} 
        />
      )} */}
      <ResetPasswordForm /> 
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <p>
          Password reset? <Link to="/login">Login here</Link>
        </p>
      </div>
    </AuthLayout>
  );
};

export default ResetPasswordPage;
