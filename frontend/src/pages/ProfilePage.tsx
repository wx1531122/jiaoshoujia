import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div style={{ padding: '20px' }}>
      <h1>User Profile</h1>
      {user ? (
        <>
          <p><strong>ID:</strong> {user.id}</p>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Active:</strong> {user.is_active ? 'Yes' : 'No'}</p>
          <p><strong>Joined:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
        </>
      ) : (
        <p>Loading user data or not logged in (this should not typically be seen if ProtectedRoute is working).</p>
      )}
      <div style={{ marginTop: '20px' }}>
        <Link to="/">Back to Home</Link>
      </div>
    </div>
  );
};

export default ProfilePage;
