/**
 * Authentication service functions for the Todo application
 */

// Store token in local storage
export const setAuthToken = (token: string): void => {
  localStorage.setItem('auth-token', token);
};

// Get token from local storage
export const getAuthToken = (): string | null => {
  return localStorage.getItem('auth-token');
};

// Remove token from local storage
export const removeAuthToken = (): void => {
  localStorage.removeItem('auth-token');
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  return !!token;
};

// Decode JWT token to get user info
export const decodeToken = (token: string): any => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Get user ID from token
export const getUserIdFromToken = (): string | null => {
  const token = getAuthToken();
  if (!token) {
    return null;
  }

  const decoded = decodeToken(token);
  return decoded?.user_id || null;
};