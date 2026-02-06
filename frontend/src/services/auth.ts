/**
 * Authentication service functions for the Todo application
 */

// Store token in local storage
export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth-token', token);
  }
};

// Get token from local storage
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth-token');
  }
  return null;
};

// Remove token from local storage
export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth-token');
  }
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') {
    return false;
  }
  const token = getAuthToken();
  return !!token;
};

// Create a simple JWT token for demo purposes
// In production, this would come from your backend auth service
export const createDemoToken = (email: string): string => {
  // Generate a simple user ID from email
  const userId = `user_${email.split('@')[0]}_${Date.now().toString(36)}`;

  // Create JWT payload
  const header = { alg: 'HS256', typ: 'JWT' };
  const payload = {
    user_id: userId,
    email: email,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
  };

  // Base64 encode (for demo - in production, backend creates real signed tokens)
  const base64Header = btoa(JSON.stringify(header));
  const base64Payload = btoa(JSON.stringify(payload));
  const signature = btoa(`demo_signature_${email}`);

  return `${base64Header}.${base64Payload}.${signature}`;
};

// Decode JWT token to get user info
export const decodeToken = (token: string): any => {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      return null;
    }

    const base64Url = parts[1];
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

// Get user email from token
export const getUserEmailFromToken = (): string | null => {
  const token = getAuthToken();
  if (!token) {
    return null;
  }

  const decoded = decodeToken(token);
  return decoded?.email || null;
};