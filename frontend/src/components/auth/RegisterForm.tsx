import React, { useState } from 'react';
import type { FormEvent } from 'react'; // 将 FormEvent 标记为仅类型导入
import AuthService from '../../services/authService'; // 假设路径已修正
import type { RegistrationData } from '../../services/authService'; // 假设路径已修正
// Optional: import { useNavigate } from 'react-router-dom';
// Optional: import { useAuth } from '../../../contexts/AuthContext';

export const RegisterForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Optional: const navigate = useNavigate();
  // Optional: const auth = useAuth(); // If auto-login is desired

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!username || !email || !password || !confirmPassword) {
      setError('All fields are required.');
      setSuccessMessage(null);
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      setSuccessMessage(null);
      return;
    }

    setError(null);
    setSuccessMessage(null);
    setIsLoading(true);

    try {
      const registrationData: RegistrationData = { username, email, password };
      await AuthService.register(registrationData);

      setSuccessMessage('Registration successful! You can now log in.');
      setUsername('');
      setEmail('');
      setPassword('');
      setConfirmPassword('');
      // Optional: navigate('/login');
      // Or if auto-login is implemented:
      // const token = await AuthService.login({username, password}); // Assuming register doesn't return token
      // auth.loginWithToken(token, registeredUser); // Need to adapt AuthContext for this
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Registration failed. Please try again.');
      }
      console.error('Registration error in component:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <div>
        <label htmlFor="register-username">Username:</label>
        <input
          id="register-username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
          disabled={isLoading}
        />
      </div>
      <div>
        <label htmlFor="register-email">Email:</label>
        <input
          id="register-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          disabled={isLoading}
        />
      </div>
      <div>
        <label htmlFor="register-password">Password:</label>
        <input
          id="register-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          disabled={isLoading}
        />
      </div>
      <div>
        <label htmlFor="register-confirm-password">Confirm Password:</label>
        <input
          id="register-confirm-password"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          required
          disabled={isLoading}
        />
      </div>
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
};

export default RegisterForm;
