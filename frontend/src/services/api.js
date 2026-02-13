import axios from 'axios';

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
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
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
    return apiClient.post('/generation-reports/generate-report/', data, {
      responseType: 'blob',
    });
  },
};
