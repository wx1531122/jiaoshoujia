// 文件: frontend/src/App.tsx
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext'; // 假设路径已修正
import { AppRouter } from './router'; // 假设路径已修正
import './App.css';

function App() {
  return (
    // <React.StrictMode> // <-- 移除这一行
      <BrowserRouter>
        <AuthProvider>
          <AppRouter />
        </AuthProvider>
      </BrowserRouter>
    // </React.StrictMode> // <-- 移除这一行
  );
}

export default App;