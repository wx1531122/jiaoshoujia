import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
  Dispatch,
  SetStateAction,
} from 'react';
import AuthService, { User, LoginCredentials, AuthToken } from '../services/authService'; // Assuming AuthToken is exported if needed for token state
import apiClient from '../services/apiClient'; // For direct localStorage interaction in case of token change

// 1. Define AuthState Interface
interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null; // Store only the access token string
  isLoading: boolean;
}

// 2. Define AuthContextType Interface
interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  // Optional: register if you want to handle it via context
  // register: (userData: RegistrationData) => Promise<void>;
  setUser: Dispatch<SetStateAction<User | null>>;
  setToken: Dispatch<SetStateAction<string | null>>;
  setIsAuthenticated: Dispatch<SetStateAction<boolean>>;
}

// 3. Create AuthContext
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 4. Implement AuthProvider Component
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setTokenState] = useState<string | null>(localStorage.getItem('authToken'));
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!localStorage.getItem('authToken'));
  const [isLoading, setIsLoading] = useState<boolean>(true); // Start true for initial check

  // Wrapper for setToken to also update localStorage and apiClient header
  const setToken = (newToken: string | null | ((prevState: string | null) => string | null)) => {
    setTokenState(prevToken => {
      const updatedToken = typeof newToken === 'function' ? newToken(prevToken) : newToken;
      if (updatedToken) {
        localStorage.setItem('authToken', updatedToken);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${updatedToken}`;
      } else {
        localStorage.removeItem('authToken');
        delete apiClient.defaults.headers.common['Authorization'];
      }
      return updatedToken;
    });
  };


  useEffect(() => {
    const checkAuth = async () => {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        setToken(storedToken); // Ensure apiClient header is set
        setIsAuthenticated(true);
        try {
          console.log('AuthProvider: Verifying token and fetching user...');
          const currentUser = await AuthService.getCurrentUser();
          setUser(currentUser);
          console.log('AuthProvider: User fetched successfully', currentUser);
        } catch (error) {
          console.error('AuthProvider: Token verification failed or user fetch failed', error);
          // Token might be invalid or expired
          logout(); // Clear out stale token and user state
        }
      } else {
        // No token, ensure clean state
        setUser(null);
        setToken(null);
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    };

    checkAuth();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array: run only on mount

  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    try {
      const authTokenData: AuthToken = await AuthService.login(credentials);
      setToken(authTokenData.access_token); // This will also update localStorage & apiClient header
      
      // After setting token, fetch user details
      const currentUser = await AuthService.getCurrentUser();
      setUser(currentUser);
      setIsAuthenticated(true);
      console.log('Login successful, user:', currentUser);
    } catch (error) {
      console.error('Login failed:', error);
      // Ensure clean state on login failure
      setUser(null);
      setToken(null); // This will clear localStorage & apiClient header
      setIsAuthenticated(false);
      // Optional: re-throw error or provide error message to UI
      throw error; // Re-throw to allow component to handle UI updates
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    // No need to set isLoading for logout, it's typically fast
    // but can be added if backend logout is slow
    console.log('AuthProvider: Logging out...');
    setUser(null);
    setToken(null); // This will clear localStorage & apiClient header
    setIsAuthenticated(false);
    // Optional: Call backend logout if it exists
    // AuthService.logout().catch(error => console.error("Backend logout failed:", error));
    // No need to redirect here; routing logic should handle that based on isAuthenticated state
  };

  const contextValue: AuthContextType = {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    logout,
    setUser, // Exposing direct setters can be powerful but use with caution
    setToken,
    setIsAuthenticated,
  };

  return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
};

// 5. Implement useAuth Hook
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
