import axios from 'axios';
import { getAccessToken } from '../utils/auth';

// AGGRESSIVE FIX: Force localhost API URL
const API_BASE_URL = 'http://localhost:8000/api';

console.log('🔧 API Client Configuration:');
console.log('- Base URL:', API_BASE_URL);
console.log('- Current Location:', window.location.href);

// Create API client with AGGRESSIVE settings for localhost
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,  // Enable cookies for session auth
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// AGGRESSIVE request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      headers: config.headers
    });
    
    // Add auth token if available
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// AGGRESSIVE response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', {
      status: response.status,
      url: response.config.url,
      data: response.data
    });
    return response;
  },
  (error) => {
    // Suppress 404 errors for pending_count endpoint (non-critical)
    if (error.config?.url?.includes('/auth/pending_count/') && error.response?.status === 404) {
      // Silently return default response without logging error
      return Promise.resolve({ data: { count: 0 } });
    }
    
    console.error('❌ API Response Error:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      data: error.response?.data
    });
    
    // Handle 401 errors
    if (error.response?.status === 401) {
      import('../utils/auth').then(({ clearAuth }) => {
        clearAuth();
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      });
    }
    
    return Promise.reject(error);
  }
);

// API METHODS - Complete service functions
export const api = {
  // Authentication
  async login(credentials) {
    const response = await apiClient.post('/auth/login/', credentials);
    return response; // Return full response object
  },

  async logout() {
    const response = await apiClient.post('/auth/logout/');
    return response; // Return full response object
  },

  // Plants
  async getPlants() {
    console.log('📡 Loading plants from API...');
    const response = await apiClient.get('/plants/');
    console.log('✅ Plants loaded:', response.data);
    return response; // Return full response object
  },

  async createPlant(plantData) {
    const response = await apiClient.post('/plants/', plantData);
    return response; // Return full response object
  },

  // Reports
  async getReports(params = {}) {
    const response = await apiClient.get('/reports/', { params });
    return response; // Return full response object
  },

  async getGenerationReports(params = {}) {
    const response = await apiClient.get('/generation-reports/', { params });
    return response; // Return full response object
  },

  async getReportSummary(params = {}) {
    const response = await apiClient.get('/generation-reports/summary/', { params });
    return response; // Return full response object
  },

  async getPlantComparison(params = {}) {
    const response = await apiClient.get('/analytics/comparison/', { params });
    return response; // Return full response object
  },

  async createReport(reportData) {
    const response = await apiClient.post('/reports/', reportData);
    return response; // Return full response object
  },

  async generateReport(reportData) {
    const response = await apiClient.post('/generation-reports/generate_report/', reportData);
    return response; // Return full response object
  },

  async previewReport(reportData) {
    const response = await apiClient.post('/generation-reports/preview-report/', reportData);
    return response; // Return full response object
  },

  async getReport(id) {
    const response = await apiClient.get(`/reports/${id}/`);
    return response; // Return full response object
  },

  async updateReport(id, reportData) {
    const response = await apiClient.put(`/reports/${id}/`, reportData);
    return response; // Return full response object
  },

  async deleteReport(id) {
    const response = await apiClient.delete(`/reports/${id}/`);
    return response; // Return full response object
  },

  // File uploads
  async uploadFile(formData) {
    const response = await apiClient.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response; // Return full response object
  },

  async uploadExcel(file, plantCode) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('plant_code', plantCode); // Changed from 'plant' to 'plant_code'
    
    const response = await apiClient.post('/uploaded-files/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response; // Return full response object
  },

  async getUploadedFiles() {
    console.log('📡 Loading upload history from API...');
    const response = await apiClient.get('/uploaded-files/');
    console.log('✅ Upload history loaded:', response.data);
    return response; // Return full response object
  },

  // Historical data
  async getHistoricalData(params = {}) {
    const response = await apiClient.get('/historical-data/', { params });
    return response; // Return full response object
  },

  async importHistoricalData(formData) {
    const response = await apiClient.post('/import-historical/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response; // Return full response object
  },

  // Analytics
  async getAnalytics(params = {}) {
    const response = await apiClient.get('/analytics/', { params });
    return response; // Return full response object
  },

  // Password reset
  async requestPasswordReset(email) {
    const response = await apiClient.post('/auth/password-reset/', { email });
    return response; // Return full response object
  },

  async getPendingResetCount() {
    try {
      const response = await apiClient.get('/auth/pending_count/');
      return response; // Return full response object
    } catch (error) {
      // Return 0 if endpoint doesn't exist
      if (error.response?.status === 404) {
        return { data: { count: 0 } };
      }
      throw error;
    }
  },

  // User management
  async getCurrentUser() {
    const response = await apiClient.get('/auth/user/');
    return response; // Return full response object
  },

  // Testimonials
  async getTestimonials() {
    const response = await apiClient.get('/testimonials/');
    return response; // Return full response object
  },

  async createTestimonial(testimonialData) {
    const response = await apiClient.post('/testimonials/', testimonialData);
    return response; // Return full response object
  },

  // Scheduled reports
  async getScheduledReports() {
    const response = await apiClient.get('/scheduled-reports/');
    return response; // Return full response object
  },

  async createScheduledReport(reportData) {
    const response = await apiClient.post('/scheduled-reports/', reportData);
    return response; // Return full response object
  },

  // E-signature
  async getSignatoryRequests() {
    const response = await apiClient.get('/signatory-requests/');
    return response; // Return full response object
  },

  async createSignatoryRequest(requestData) {
    const response = await apiClient.post('/signatory-requests/', requestData);
    return response; // Return full response object
  },

  // Audit logs
  async getAuditLogs(params = {}) {
    const response = await apiClient.get('/audit-logs/', { params });
    return response; // Return full response object
  },

  // Monthly targets
  async getMonthlyTargets(params = {}) {
    // Ensure we get all targets by setting a large page size
    const requestParams = { 
      page_size: 100, // Get all targets in one request
      ...params 
    };
    const response = await apiClient.get('/monthly-targets/', { params: requestParams });
    return response; // Return full response object
  },

  async getCurrentMonthlyTarget(plantCode, month, year) {
    const response = await apiClient.get('/monthly-targets/current/', {
      params: { 
        plant_code: plantCode, 
        month, 
        year,
        _t: Date.now() // Cache-busting parameter to force fresh data
      }
    });
    return response; // Return full response object
  },

  async setMonthlyTarget(targetData) {
    const response = await apiClient.post('/monthly-targets/set-current/', targetData);
    return response; // Return full response object
  },

  async bulkSetTargets(targets) {
    const response = await apiClient.post('/monthly-targets/bulk-set/', { targets });
    return response; // Return full response object
  },

  async createMonthlyTarget(targetData) {
    const response = await apiClient.post('/monthly-targets/', targetData);
    return response; // Return full response object
  },

  async updateMonthlyTarget(id, targetData) {
    const response = await apiClient.put(`/monthly-targets/${id}/`, targetData);
    return response; // Return full response object
  },

  async deleteMonthlyTarget(id) {
    const response = await apiClient.delete(`/monthly-targets/${id}/`);
    return response; // Return full response object
  },

  // E-Signature methods
  async getUserSignatoryAuthorizations() {
    const response = await apiClient.get('/signatory-authorizations/my-authorizations/');
    return response; // Return full response object
  },

  async getESignatures(params = {}) {
    const response = await apiClient.get('/e-signatures/', { params });
    return response; // Return full response object
  },

  async getESignaturesBySignatory(signatoryName) {
    const response = await apiClient.get('/e-signatures/by-signatory/', {
      params: { name: signatoryName }
    });
    return response; // Return full response object
  },

  async getReportSignaturesForReport(reportDate, reportType) {
    const response = await apiClient.get('/report-signatures/for-report/', {
      params: { 
        report_date: reportDate,
        report_type: reportType
      }
    });
    return response; // Return full response object
  },

  async createESignature(signatureData) {
    const response = await apiClient.post('/e-signatures/', signatureData);
    return response; // Return full response object
  },

  async createReportSignature(signatureData) {
    const response = await apiClient.post('/report-signatures/', signatureData);
    return response; // Return full response object
  },

  async updateESignature(id, signatureData) {
    const response = await apiClient.put(`/e-signatures/${id}/`, signatureData);
    return response; // Return full response object
  },

  async signReport(signatureData) {
    const response = await apiClient.post('/report-signatures/sign-report/', signatureData);
    return response; // Return full response object
  },

  // Document management
  async createDocument(formData) {
    const response = await apiClient.post('/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response; // Return full response object
  },

  async getDocuments(params = {}) {
    const response = await apiClient.get('/documents/', { params });
    return response; // Return full response object
  }
};

// Export both the client and the API methods
export default api; // Make api the default export

// Also export the client for direct access
export { apiClient };

// Legacy exports for backward compatibility
export const getPlants = api.getPlants;
export const getUploadedFiles = api.getUploadedFiles;
export const uploadFile = api.uploadFile;
export const getReports = api.getReports;
export const createReport = api.createReport;

// Simple API methods for testing
export const testAPI = {
  // Test basic connectivity
  async testConnection() {
    console.log('🧪 Testing API connection...');
    try {
      const response = await apiClient.get('/plants/');
      console.log('✅ API Connection successful:', response.data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ API Connection failed:', error);
      return { success: false, error: error.message };
    }
  },

  // Test authentication
  async testAuth(credentials) {
    console.log('🧪 Testing authentication...');
    try {
      const response = await apiClient.post('/auth/login/', credentials);
      console.log('✅ Authentication successful:', response.data);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('❌ Authentication failed:', error);
      return { success: false, error: error.message };
    }
  }
};
