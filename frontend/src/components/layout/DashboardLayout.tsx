// frontend/src/components/layout/DashboardLayout.tsx
import React, { ReactNode } from 'react';
import { Navbar } from './Navbar'; // Assuming Navbar.tsx is in the same directory

interface DashboardLayoutProps {
  children: ReactNode;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <div>
      <Navbar />
      <main style={{ padding: '20px' }}>
        {children}
      </main>
      {/* Optional: Footer component could go here */}
    </div>
  );
};
