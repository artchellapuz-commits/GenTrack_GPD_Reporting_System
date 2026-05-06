/**
 * Authentication Utilities
 * Handles token management, user state, and auth helpers
 */

import axios from 'axios';

let API_URL = import.meta.env.VITE_APP_API_URL || process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

// Force production URL if running on Netlify domain
if (window.location.hostname.includes('netlify.app')) {
  API_URL = 'https://npc-reporting-backend.onrender.com/api';
}

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
  // For session-based auth, check if user data exists
  const user = getUser();
  const sessionId = localStorage.getItem('session_id');
  return !!(user && sessionId);
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
  localStorage.removeItem('session_id');
  sessionStorage.removeItem('generateReportState');
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
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

export function setupAxiosInterceptors() {
  // Request interceptor - for session-based auth, axios will automatically send cookies
  axios.interceptors.request.use(
    (config) => {
      // Enable credentials for session-based auth
      config.withCredentials = true;
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor to handle authentication errors
  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      // If error is 401, redirect to login
      if (error.response?.status === 401) {
        clearAuth();
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
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
  
  // Fetch full profile with permissions
  try {
    const profileResponse = await axios.get(`${API_URL}/auth/profile/`, {
      headers: { Authorization: `Bearer ${response.data.access}` }
    });
    setUser(profileResponse.data);
  } catch (error) {
    // Fallback to basic user data
    setUser(response.data.user);
  }

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
 * Get user role from profile
 */
export function getUserRole() {
  const user = getUser();
  if (!user) return null;
  
  // Check if profile data is available
  if (user.profile && user.profile.role) {
    return user.profile.role;
  }
  
  // Fallback: admin check
  if (user.is_staff) return 'ADMIN';
  
  return 'VIEWER'; // Default role
}

/**
 * Get user permissions from profile
 */
export function getUserPermissions() {
  const user = getUser();
  if (!user || !user.profile) return {};
  
  return user.profile.permissions || {};
}

/**
 * Check if user has specific permission
 */
export function hasPermission(permissionName) {
  const user = getUser();
  if (!user) return false;
  
  // Admin has all permissions
  if (user.is_staff) return true;
  
  // Check profile permissions
  const permissions = getUserPermissions();
  return permissions[permissionName] === true;
}

/**
 * Check if user is admin
 */
export function isAdmin() {
  const user = getUser();
  return user && (user.is_staff || getUserRole() === 'ADMIN');
}

/**
 * Check if user is manager or above
 */
export function isManagerOrAbove() {
  const role = getUserRole();
  return role === 'MANAGER' || role === 'ADMIN' || isAdmin();
}

/**
 * Check if user is operator or above
 */
export function isOperatorOrAbove() {
  const role = getUserRole();
  return role === 'OPERATOR' || role === 'MANAGER' || role === 'ADMIN' || isAdmin();
}

/**
 * Check if user is viewer (read-only)
 */
export function isViewer() {
  const role = getUserRole();
  return role === 'VIEWER';
}

/**
 * Check if user can upload data
 */
export function canUploadData() {
  return hasPermission('can_upload_data') || isOperatorOrAbove();
}

/**
 * Check if user can approve data
 */
export function canApproveData() {
  return hasPermission('can_approve_data') || isManagerOrAbove();
}

/**
 * Check if user can export data
 */
export function canExportData() {
  return hasPermission('can_export_data') || true; // All authenticated users
}

/**
 * Check if user can manage users
 */
export function canManageUsers() {
  return hasPermission('can_manage_users') || isAdmin();
}

/**
 * Get user's assigned plant
 */
export function getUserPlant() {
  const user = getUser();
  if (!user || !user.profile) return null;
  
  return user.profile.plant || null;
}

/**
 * Get role display name
 */
export function getRoleDisplayName(role) {
  const roleNames = {
    'VIEWER': 'Viewer',
    'OPERATOR': 'Data Encoder',
    'MANAGER': 'Data Manager',
    'ADMIN': 'System Admin'
  };
  
  // Also check if role is passed in lowercase or mixed case
  if (role && typeof role === 'string') {
    const upperRole = role.toUpperCase();
    return roleNames[upperRole] || role;
  }
  
  return roleNames[role] || 'Unknown';
}

/**
 * Get role badge color
 */
export function getRoleBadgeColor(role) {
  const colors = {
    'VIEWER': 'info',
    'OPERATOR': 'success',
    'MANAGER': 'warning',
    'ADMIN': 'danger'
  };
  return colors[role] || 'secondary';
}
