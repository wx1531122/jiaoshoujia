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
// Ensure this matches the UserRead schema in backend/app/users/schemas.py
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_verified_email: boolean; // Added this field based on model updates
  created_at: string; // Assuming ISO string format from backend
  updated_at: string; // Assuming ISO string format from backend
}

// Corresponds to backend's Token schema
export interface AuthToken {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Optional: If backend returns a specific message structure for some of these new endpoints
// export interface MessageResponse {
//   message: string;
// }

const AuthService = {
  login: async (credentials: LoginCredentials): Promise<AuthToken> => {
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

  // --- New methods for Email Verification and Password Reset ---

  requestEmailVerification: async (email: string): Promise<void> => {
    // Backend for /auth/request-email-verification returns MessageSchema.
    // If we needed to use the message, we could type:
    // await apiClient.post<MessageResponse>('/auth/request-email-verification', { email });
    await apiClient.post('/auth/request-email-verification', { email });
  },

  // verifyEmail: async (token: string): Promise<void> => {
  //   // Backend for /auth/verify-email/{token} is a GET request.
  //   // This might not be strictly needed if verification is primarily navigation
  //   // and the page component handles feedback based on its own loading or backend redirects.
  //   // If an explicit API call is made by the EmailVerificationPage:
  //   await apiClient.get(`/auth/verify-email/${token}`);
  // },

  requestPasswordReset: async (email: string): Promise<void> => {
    // Backend for /auth/request-password-reset returns MessageSchema.
    await apiClient.post('/auth/request-password-reset', { email });
  },

  resetPassword: async (token: string, new_password: string): Promise<void> => {
    // Backend for /auth/reset-password returns MessageSchema.
    await apiClient.post('/auth/reset-password', { token, new_password });
  },

  // Optional: logout function
  // If logout involves clearing localStorage and local state only, it might live in a context/hook.
  // If it needs to invalidate a token on the backend:
  // logout: async (): Promise<void> => {
  //   // Ensure this endpoint exists on your backend if you implement it
  //   await apiClient.post('/auth/logout'); 
  //   // Local cleanup (localStorage, AuthContext state) should be handled separately
  // },
};

export default AuthService;
