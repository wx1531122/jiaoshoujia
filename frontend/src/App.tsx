import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { AppRouter } from './router'; // Assuming router/index.tsx exports AppRouter
import './App.css'; // Keep existing global styles from Vite, can be modified later
// import './index.css'; // Or if you prefer to use index.css as the main global stylesheet

function App() {
  return (
    <React.StrictMode>
      <BrowserRouter>
        <AuthProvider>
          {/* 
            Optional: A global layout component could wrap AppRouter here,
            e.g., <Layout><AppRouter /></Layout>
            This might include a navigation bar, footer, etc.
            For now, AppRouter is rendered directly.
          */}
          <AppRouter />
        </AuthProvider>
      </BrowserRouter>
    </React.StrictMode>
  );
}

export default App;
