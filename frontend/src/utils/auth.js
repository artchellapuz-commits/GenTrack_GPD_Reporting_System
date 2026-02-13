/**
 * Authentication Utilities
 * Handles token management, user state, and auth helpers
 */

import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

/**
 * Get access token from localStorage
 */
export function getAccessToken() {
  return localStorage.getItem('access_token');
}

/**
 * Get refresh token from localStorage
 */
export function getRefreshToken() {
  return localStorage.getItem('refresh_token');
}

/**
 * Get user data from localStorage
 */
export function getUser() {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

/**
 * Get username from localStorage
 */
export function getUsername() {
  const user = getUser();
  return user ? user.username : null;
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated() {
  return !!getAccessToken();
}

/**
 * Set authentication tokens
 */
export function setTokens(accessToken, refreshToken) {
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
  axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
}

/**
 * Set user data
 */
export function setUser(user) {
  localStorage.setItem('user', JSON.stringify(user));
}

/**
 * Clear authentication data
 */
export function clearAuth() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  delete axios.defaults.headers.common['Authorization'];
}

/**
 * Refresh access token
 */
export async function refreshAccessToken() {
  try {
    const refreshToken = getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API_URL}/auth/refresh/`, {
      refresh: refreshToken
    });

    const newAccessToken = response.data.access;
    localStorage.setItem('access_token', newAccessToken);
    axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;

    return newAccessToken;
  } catch (error) {
    console.error('Token refresh failed:', error);
    clearAuth();
    throw error;
  }
}

/**
 * Setup axios interceptors for automatic token refresh
 */
export function setupAxiosInterceptors() {
  // Request interceptor to add token
  axios.interceptors.request.use(
    (config) => {
      const token = getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor to handle token expiration
  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      // If error is 401 and we haven't retried yet
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        try {
          const newToken = await refreshAccessToken();
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return axios(originalRequest);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }

      return Promise.reject(error);
    }
  );
}

/**
 * Login user
 */
export async function login(username, password) {
  const response = await axios.post(`${API_URL}/auth/login/`, {
    username,
    password
  });

  setTokens(response.data.access, response.data.refresh);
  setUser(response.data.user);

  return response.data;
}

/**
 * Logout user
 */
export async function logout() {
  try {
    const refreshToken = getRefreshToken();
    
    if (refreshToken) {
      await axios.post(`${API_URL}/auth/logout/`, {
        refresh_token: refreshToken
      });
    }
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    clearAuth();
  }
}

/**
 * Register new user
 */
export async function register(userData) {
  const response = await axios.post(`${API_URL}/auth/register/`, userData);

  setTokens(response.data.tokens.access, response.data.tokens.refresh);
  setUser(response.data.user);

  return response.data;
}

/**
 * Get user profile
 */
export async function getUserProfile() {
  const response = await axios.get(`${API_URL}/auth/profile/`);
  setUser(response.data);
  return response.data;
}

/**
 * Update user profile
 */
export async function updateUserProfile(data) {
  const response = await axios.put(`${API_URL}/auth/update_profile/`, data);
  setUser(response.data);
  return response.data;
}

/**
 * Change password
 */
export async function changePassword(oldPassword, newPassword, newPassword2) {
  const response = await axios.post(`${API_URL}/auth/change_password/`, {
    old_password: oldPassword,
    new_password: newPassword,
    new_password2: newPassword2
  });
  return response.data;
}

/**
 * Check if user has permission
 */
export function hasPermission(permissionName) {
  const user = getUser();
  if (!user) return false;
  
  // Admin has all permissions
  if (user.is_staff) return true;
  
  // Add more permission checks as needed
  // You can check permissionName here when you implement permissions
  console.log('Checking permission:', permissionName);
  return false;
}

/**
 * Check if user is admin
 */
export function isAdmin() {
  const user = getUser();
  return user && user.is_staff;
}
