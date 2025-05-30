import React from 'react';
// Link import might not be needed if profile link is removed in favor of Navbar
// import { Link } from 'react-router-dom'; 
import { useAuth } from '../contexts/AuthContext';
import { DashboardLayout } from '../components/layout/DashboardLayout'; // Import DashboardLayout

const HomePage: React.FC = () => {
  const { user } = useAuth(); // Logout function no longer directly called here

  return (
    <DashboardLayout> {/* Use DashboardLayout */}
      <h1>Welcome to the Home Page!</h1>
      {user ? (
        <p>Hello, {user.username || user.email || 'User'}!</p>
      ) : (
        <p>Loading user data or not logged in (this should not typically be seen if ProtectedRoute is working).</p>
      )}
      
      <p>This is your main dashboard area after logging in.</p>

      {/* 
        Logout and Profile buttons/links removed from here as they are now part of the Navbar 
        provided by DashboardLayout.
      */}
      {/* 
      <div style={{ marginTop: '20px' }}>
        <button onClick={logout} style={{ marginRight: '10px' }}>
          Logout
        </button>
        <Link to="/profile">
          <button>View Profile</button>
        </Link>
      </div> 
      */}
    </DashboardLayout>
  );
};

export default HomePage;
