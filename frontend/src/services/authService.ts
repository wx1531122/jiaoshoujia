import apiClient from './apiClient';

// Type Definitions
// These should align with backend schemas.

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegistrationData {
  username: string;
  email: string;
  password: string;
}

// Corresponds to backend's UserRead schema
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string; // Assuming ISO string format from backend
  updated_at: string; // Assuming ISO string format from backend
}

// Corresponds to backend's Token schema
export interface AuthToken {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

const AuthService = {
  login: async (credentials: LoginCredentials): Promise<AuthToken> => {
    // The apiClient already has baseURL set to '.../api/v1'
    // So, the path here is relative to that.
    const response = await apiClient.post<AuthToken>('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: RegistrationData): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  // Optional: logout function
  // If logout involves clearing localStorage and local state only, it might live in a context/hook.
  // If it needs to invalidate a token on the backend:
  // logout: async (): Promise<void> => {
  //   await apiClient.post('/auth/logout'); // Assuming a /auth/logout endpoint exists
  // },
};

export default AuthService;
