// frontend/src/components/layout/Navbar.tsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext'; // Adjust path as needed

export const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login after logout
  };

  return (
    <nav style={{ 
      backgroundColor: '#333', 
      color: 'white', 
      padding: '10px 20px', 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center' 
    }}>
      <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.5em' }}>
        MyApp
      </Link>
      <div>
        {isAuthenticated && user ? (
          <>
            <span style={{ marginRight: '15px' }}>
              Hello, {user.username || user.email}
            </span>
            <Link to="/profile" style={{ color: 'white', marginRight: '15px', textDecoration: 'none' }}>
              Profile
            </Link>
            <button onClick={handleLogout} style={{ cursor: 'pointer' }}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: 'white', marginRight: '10px', textDecoration: 'none' }}>
              Login
            </Link>
            <Link to="/register" style={{ color: 'white', textDecoration: 'none' }}>
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};
