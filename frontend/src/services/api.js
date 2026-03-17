import axios from 'axios';
import { getAccessToken } from '../utils/auth';

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false,  // Changed to false for simpler setup
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      data: config.data,
      headers: config.headers
    });
    
    // Use the auth utility to get the token
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Import clearAuth dynamically to avoid circular imports
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

export default {
  // Plants
  getPlants() {
    return apiClient.get('/plants/');
  },

  // Units
  getUnits(plantCode = null) {
    const params = plantCode ? { plant_code: plantCode } : {};
    return apiClient.get('/units/', { params });
  },

  // Upload Excel file
  uploadExcel(file, plantCode) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('plant_code', plantCode);

    return apiClient.post('/uploaded-files/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Get uploaded files
  getUploadedFiles(params = {}) {
    return apiClient.get('/uploaded-files/', { params });
  },

  // Delete uploaded file
  deleteUploadedFile(fileId) {
    return apiClient.delete(`/uploaded-files/${fileId}/delete_upload/`);
  },

  // Archive uploaded file
  archiveUploadedFile(fileId) {
    return apiClient.post(`/uploaded-files/${fileId}/archive/`);
  },

  // Restore archived file
  restoreArchivedFile(fileId) {
    return apiClient.post(`/uploaded-files/${fileId}/restore/`);
  },

  // Get archived files
  getArchivedFiles(params = {}) {
    return apiClient.get('/uploaded-files/archived/', { params });
  },

  // Get generation reports
  getGenerationReports(params = {}) {
    // Add timestamp to prevent caching
    const queryParams = { ...params, _t: Date.now() };
    return apiClient.get('/generation-reports/', { params: queryParams });
  },

  // Get summary statistics
  getReportSummary(params = {}) {
    // Add timestamp to prevent caching
    const queryParams = { ...params, _t: Date.now() };
    return apiClient.get('/generation-reports/summary/', { params: queryParams });
  },

  // Generate Excel report
  generateReport(data) {
    console.log('API: Sending generateReport request with data:', data);
    return apiClient.post('/generation-reports/generate-report/', data, {
      responseType: 'blob',
      timeout: 60000, // 60 second timeout
    }).then(response => {
      console.log('API: generateReport response received:', {
        status: response.status,
        statusText: response.statusText,
        headers: response.headers,
        dataType: typeof response.data,
        dataSize: response.data?.size || 'unknown'
      });
      return response;
    }).catch(error => {
      console.error('API: generateReport error:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        config: error.config
      });
      throw error;
    });
  },

  // Preview report data before generating Excel
  previewReport(data) {
    console.log('API: Sending previewReport request with data:', data);
    return apiClient.post('/generation-reports/preview-report/', data, {
      timeout: 30000, // 30 second timeout
    });
  },

  // E-Signatures
  getESignatures(params = {}) {
    return apiClient.get('/e-signatures/', { params });
  },

  getESignaturesBySignatory(signatoryName) {
    return apiClient.get('/e-signatures/by-signatory/', {
      params: { name: signatoryName }
    });
  },

  createESignature(data) {
    return apiClient.post('/e-signatures/create-from-data/', data);
  },

  updateESignature(id, data) {
    return apiClient.put(`/e-signatures/${id}/`, data);
  },

  deleteESignature(id) {
    return apiClient.delete(`/e-signatures/${id}/`);
  },

  // Report Signatures
  getReportSignatures(params = {}) {
    return apiClient.get('/report-signatures/', { params });
  },

  getReportSignaturesForReport(reportDate, reportType = 'PSR') {
    return apiClient.get('/report-signatures/for-report/', {
      params: { report_date: reportDate, report_type: reportType }
    });
  },

  signReport(data) {
    return apiClient.post('/report-signatures/sign-report/', data);
  },

  // Signatory Authorization Requests (User-friendly)
  getUserSignatoryAuthorizations() {
    return apiClient.get('/signatory-authorizations/my-authorizations/');
  },

  getUserAuthorizationRequests() {
    return apiClient.get('/signatory-authorizations/my-requests/');
  },

  requestSignatoryAuthorization(data) {
    return apiClient.post('/signatory-authorizations/request/', data);
  },

  // Admin endpoints for authorization management
  getPendingAuthorizationRequests() {
    return apiClient.get('/signatory-authorizations/pending-requests/');
  },

  approveAuthorizationRequest(requestId, data = {}) {
    return apiClient.post(`/signatory-authorizations/approve-request/${requestId}/`, data);
  },

  rejectAuthorizationRequest(requestId, data = {}) {
    return apiClient.post(`/signatory-authorizations/reject-request/${requestId}/`, data);
  },

  cancelAuthorizationRequest(requestId) {
    return apiClient.post(`/signatory-authorizations/cancel-request/${requestId}/`);
  },

  // 2FA Security Methods
  requestSignatory2FA(data) {
    return apiClient.post('/e-signatures/request-2fa/', data);
  },

  verifySignatory2FA(data) {
    return apiClient.post('/e-signatures/verify-2fa/', data);
  },

  // E-signature workflow methods
  async createDocument(documentData) {
    return apiClient.post('/documents/', documentData);
  },

  async getDocuments() {
    return apiClient.get('/documents/');
  },

  async getDocument(id) {
    return apiClient.get(`/documents/${id}/`);
  },

  async requestSignatures(documentId, signatureData) {
    return apiClient.post(`/documents/${documentId}/request_signatures/`, signatureData);
  },

  async getSignatureRequests() {
    return apiClient.get('/signature-requests/');
  },

  async verifySignatureToken(token) {
    return apiClient.get(`/signing/verify/${token}/`);
  },

  async signDocument(token, signatureData) {
    return apiClient.post(`/signing/sign/${token}/`, signatureData);
  },

  async getDigitalSignatures() {
    return apiClient.get('/digital-signatures/');
  },
};
