import React from 'react';
import { Link } from 'react-router-dom'; // Optional, for profile link
import { useAuth } from '../contexts/AuthContext';

const HomePage: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div style={{ padding: '20px' }}>
      <h1>Welcome to the Home Page!</h1>
      {user ? (
        <p>Hello, {user.username || user.email || 'User'}!</p>
      ) : (
        <p>Loading user data or not logged in (this should not typically be seen if ProtectedRoute is working).</p>
      )}
      
      <p>This is your main dashboard area after logging in.</p>

      <div style={{ marginTop: '20px' }}>
        <button onClick={logout} style={{ marginRight: '10px' }}>
          Logout
        </button>
        {/* Optional: Link to profile page */}
        <Link to="/profile">
          <button>View Profile</button>
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
