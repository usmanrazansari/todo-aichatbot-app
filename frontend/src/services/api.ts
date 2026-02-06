/**
 * API client service for frontend-backend communication
 */

import axios, { AxiosInstance } from 'axios';

// Create axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
});

// Add request interceptor to include JWT token in headers
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors globally
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('auth-token');
      window.location.href = '/login';
    } else if (error.response?.status === 403) {
      // Forbidden access - likely a security issue
      console.error('Forbidden access:', error.response.data);
      alert('Access forbidden. Please contact support if this persists.');
    } else if (error.response?.status === 404) {
      // Resource not found
      console.error('Resource not found:', error.response.data);
      alert('Requested resource not found.');
    } else if (error.response?.status >= 500) {
      // Server error
      console.error('Server error:', error.response.data);
      alert('Server error occurred. Please try again later.');
    } else {
      // Other error
      console.error('API error:', error.message);
    }

    return Promise.reject(error);
  }
);

// Additional task-specific methods can be exported separately if needed
export { apiClient };

// Convenience methods for task operations
export const taskApi = {
  getTasks: (userId: string) => apiClient.get(`/api/${userId}/tasks`),
  createTask: (userId: string, data: any) => apiClient.post(`/api/${userId}/tasks`, data),
  getTask: (userId: string, taskId: string) => apiClient.get(`/api/${userId}/tasks/${taskId}`),
  updateTask: (userId: string, taskId: string, data: any) => apiClient.put(`/api/${userId}/tasks/${taskId}`, data),
  deleteTask: (userId: string, taskId: string) => apiClient.delete(`/api/${userId}/tasks/${taskId}`),
  toggleTaskCompletion: (userId: string, taskId: string) => apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`)
};