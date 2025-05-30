# Frontend Application for Secure User Authentication

This frontend application is built with React, TypeScript, and Vite. It implements the core user authentication features outlined as Phase 1 in the main project README.

## Key Features (Phase 1 Complete)

*   **User Registration:** New users can register with a username, email, and password.
*   **User Login:** Registered users can log in to access protected resources.
*   **JWT Authentication:** Uses JSON Web Tokens (JWT) for managing user sessions. Tokens are stored in localStorage.
*   **Protected Routes:** Certain routes (e.g., Home, Profile) are protected and require authentication.
*   **User Profile:** Authenticated users can view their basic profile information.
*   **API Client:** A dedicated API client (`src/services/apiClient.ts`) using Axios is configured with interceptors to attach JWT tokens to requests and handle basic API errors.
*   **State Management:** User authentication state is managed globally using React Context (`src/contexts/AuthContext.tsx`).

## Tech Stack

*   React
*   TypeScript
*   Vite
*   React Router DOM for navigation
*   Axios for API communication

## Project Structure

The `frontend/src` directory is organized as follows:

*   **`App.tsx`**: The main application component that sets up routing and context providers.
*   **`main.tsx`**: The entry point of the application.
*   **`assets/`**: Static assets like images.
*   **`components/`**: Reusable UI components.
    *   `auth/`: Components related to authentication (LoginForm, RegisterForm).
    *   `common/`: Common components like LoadingSpinner.
*   **`contexts/`**: React context for global state management (e.g., `AuthContext.tsx`).
*   **`pages/`**: Top-level page components (LoginPage, RegisterPage, HomePage, ProfilePage).
*   **`router/`**: Routing configuration, including protected route logic (`index.tsx`, `ProtectedRoute.tsx`).
*   **`services/`**: Modules for interacting with the backend API (`apiClient.ts`, `authService.ts`).

## Setup and Running the Project

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or
    # yarn install
    ```

3.  **Set up environment variables:**
    Create a `.env.development` file in the `frontend` directory by copying `.env.development.example` (if one exists) or by creating it manually.
    It should contain the base URL for the backend API:
    ```env
    VITE_API_BASE_URL="http://localhost:8000/api/v1"
    ```
    Ensure the backend server is running and accessible at this URL.

4.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The application will typically be available at `http://localhost:5173`.

## Available Scripts

In the `frontend` directory, you can run the following scripts:

*   **`npm run dev`**: Starts the Vite development server with Hot Module Replacement (HMR).
*   **`npm run build`**: Compiles TypeScript and builds the application for production.
*   **`npm run lint`**: Lints the codebase using ESLint.
*   **`npm run preview`**: Serves the production build locally for preview.
