import React, { useState, FormEvent } from 'react';
import { useAuth } from '../../../contexts/AuthContext';
// Optional: import { useNavigate } from 'react-router-dom';

export const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoadingLocal, setIsLoadingLocal] = useState<boolean>(false);

  const { login, isLoading: authIsLoading } = useAuth();
  // Optional: const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!username || !password) {
      setError('Username and password are required.');
      return;
    }

    setError(null);
    setIsLoadingLocal(true);

    try {
      await login({ username, password });
      // On successful login, AuthContext will set isAuthenticated to true.
      // Navigation is typically handled by a parent component or a router setup
      // that listens to isAuthenticated state.
      // e.g., navigate('/dashboard'); // Or wherever appropriate
      setUsername(''); // Clear fields on success
      setPassword('');
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Login failed. Please try again.');
      }
      console.error('Login error in component:', err);
    } finally {
      setIsLoadingLocal(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <label htmlFor="login-username">Username or Email:</label>
        <input
          id="login-username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username or Email"
          required
          disabled={authIsLoading || isLoadingLocal}
        />
      </div>
      <div>
        <label htmlFor="login-password">Password:</label>
        <input
          id="login-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          disabled={authIsLoading || isLoadingLocal}
        />
      </div>
      <button type="submit" disabled={authIsLoading || isLoadingLocal}>
        {authIsLoading || isLoadingLocal ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

export default LoginForm;
