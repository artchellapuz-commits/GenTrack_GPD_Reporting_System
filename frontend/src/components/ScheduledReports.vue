<template>
  <AppLayout>
    <div class="scheduled-reports">
      <div class="header">
        <h2>Automated Reports</h2>
      <button @click="showCreateDialog = true" class="btn-primary">
        <i class="pi pi-plus"></i> Schedule New Report
      </button>
    </div>

    <div class="reports-list">
      <div v-for="report in scheduledReports" :key="report.id || Math.random()" class="report-card">
        <div class="report-header">
          <div>
            <h3>{{ report.name || 'Unnamed Report' }}</h3>
            <p class="report-type">{{ report.report_type_display || 'Unknown Type' }}</p>
          </div>
          <span :class="['status-badge', report.status ? report.status.toLowerCase() : 'unknown']">
            {{ report.status || 'Unknown' }}
          </span>
        </div>

        <div class="report-details">
          <div class="detail-item">
            <i class="pi pi-clock"></i>
            <span>{{ report.frequency_display || 'Unknown' }} at {{ report.schedule_time || 'N/A' }}</span>
          </div>
          <div class="detail-item">
            <i class="pi pi-calendar"></i>
            <span>Next run: {{ formatDate(report.next_run) }}</span>
          </div>
          <div class="detail-item">
            <i class="pi pi-send"></i>
            <span>{{ report.recipients_count || 0 }} recipients</span>
          </div>
          <div class="detail-item">
            <i class="pi pi-check-circle"></i>
            <span>{{ report.run_count || 0 }} executions</span>
          </div>
        </div>

        <div class="report-actions">
          <button @click="viewExecutions(report)" class="btn-secondary">
            <i class="pi pi-history"></i> History
          </button>
          <button @click="editReport(report)" class="btn-secondary">
            <i class="pi pi-pencil"></i> Edit
          </button>
          <button @click="toggleStatus(report)" class="btn-secondary">
            <i :class="report.status === 'ACTIVE' ? 'pi pi-pause' : 'pi pi-play'"></i>
            {{ report.status === 'ACTIVE' ? 'Pause' : 'Activate' }}
          </button>
          <button @click="runNow(report)" class="btn-primary">
            <i class="pi pi-play"></i> Run Now
          </button>
          <button @click="deleteReport(report)" class="btn-danger">
            <i class="pi pi-trash"></i> Delete
          </button>
        </div>
      </div>

      <div v-if="scheduledReports.length === 0" class="empty-state">
        <i class="pi pi-inbox" style="font-size: 3rem; color: #94a3b8;"></i>
        <p>No scheduled reports yet</p>
        <button @click="showCreateDialog = true" class="btn-primary">
          Create Your First Report
        </button>
      </div>
    </div>

    <!-- Execution History Modal -->
    <div v-if="showHistoryModal" class="modal-overlay" @click.self="showHistoryModal = false">
      <div class="modal-content large">
        <div class="modal-header">
          <h2>Execution History - {{ selectedReport?.name }}</h2>
          <button @click="showHistoryModal = false" class="btn-close">×</button>
        </div>
        
        <div v-if="executions.length === 0" class="empty-state">
          <i class="pi pi-inbox" style="font-size: 2rem; color: #94a3b8;"></i>
          <p>No execution history yet</p>
          <p style="font-size: 0.9rem; color: #64748b;">Click "Run Now" to generate a report</p>
        </div>

        <div v-else class="executions-list">
          <div v-for="exec in executions" :key="exec.id" class="execution-card">
            <div class="execution-header">
              <div>
                <span :class="['status-badge', exec.status.toLowerCase()]">
                  {{ exec.status }}
                </span>
                <span class="execution-date">{{ formatDateTime(exec.started_at) }}</span>
              </div>
              <div class="execution-actions">
                <button 
                  v-if="exec.status === 'COMPLETED' && exec.file_path" 
                  @click="downloadFile(exec.id)"
                  class="btn-download"
                >
                  <i class="pi pi-download"></i> Download
                </button>
                <button 
                  @click="deleteExecution(exec)"
                  class="btn-delete-exec"
                  title="Delete execution"
                >
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>

            <div class="execution-details">
              <div class="detail-row">
                <span class="label">Duration:</span>
                <span class="value">{{ exec.duration_seconds || 0 }}s</span>
              </div>
              <div class="detail-row">
                <span class="label">Records:</span>
                <span class="value">{{ exec.records_processed || 0 }}</span>
              </div>
              <div class="detail-row">
                <span class="label">File Size:</span>
                <span class="value">{{ formatFileSize(exec.file_size) }}</span>
              </div>
              <div v-if="exec.file_path" class="detail-row">
                <span class="label">File:</span>
                <span class="value filename">{{ getFileName(exec.file_path) }}</span>
              </div>
              <div v-if="exec.error_message" class="detail-row error">
                <span class="label">Error:</span>
                <span class="value">{{ exec.error_message }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Dialog -->
    <div v-if="showCreateDialog" class="modal-overlay" @click.self="showCreateDialog = false">
      <div class="modal-content">
        <h2>{{ editingReport ? 'Edit' : 'Schedule New' }} Report</h2>
        
        <form @submit.prevent="saveReport">
          <div class="form-group">
            <label>Report Name</label>
            <input v-model="formData.name" type="text" required />
          </div>

          <div class="form-group">
            <label>Report Type</label>
            <select v-model="formData.report_type" required>
              <option value="PSR">Plant Status Report (PSR)</option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Frequency</label>
              <select v-model="formData.frequency" required>
                <option value="DAILY">Daily</option>
                <option value="WEEKLY">Weekly</option>
                <option value="MONTHLY">Monthly</option>
                <option value="QUARTERLY">Quarterly</option>
              </select>
            </div>

            <div class="form-group">
              <label>Time</label>
              <input v-model="formData.schedule_time" type="time" required />
            </div>
          </div>

          <div class="form-group">
            <label>Format</label>
            <select v-model="formData.format" required>
              <option value="PDF">PDF</option>
              <option value="EXCEL">Excel</option>
              <option value="BOTH">Both</option>
            </select>
          </div>

          <div class="form-group">
            <label>Date Range (days)</label>
            <input v-model.number="formData.date_range_days" type="number" min="1" max="365" required />
          </div>

          <div class="form-actions">
            <button type="button" @click="showCreateDialog = false" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              {{ editingReport ? 'Update' : 'Create' }} Report
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Message Modal (Success/Error/Info) -->
    <div v-if="showMessageModal" class="modal-overlay" @click.self="closeMessageModal">
      <div class="modal-content message-modal">
        <div class="modal-header" :class="messageType">
          <div class="modal-icon">
            <i v-if="messageType === 'success'" class="pi pi-check-circle"></i>
            <i v-if="messageType === 'error'" class="pi pi-times-circle"></i>
            <i v-if="messageType === 'info'" class="pi pi-info-circle"></i>
          </div>
          <h2>{{ messageTitle }}</h2>
          <button @click="closeMessageModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <p v-html="messageText"></p>
        </div>
        <div class="modal-footer">
          <button @click="closeMessageModal" class="btn-primary">OK</button>
        </div>
      </div>
    </div>

    <!-- Confirm Modal (Yes/No) -->
    <div v-if="showConfirmModal" class="modal-overlay" @click.self="cancelConfirm">
      <div class="modal-content confirm-modal">
        <div class="modal-header warning">
          <div class="modal-icon">
            <i class="pi pi-exclamation-triangle"></i>
          </div>
          <h2>{{ confirmTitle }}</h2>
          <button @click="cancelConfirm" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <p v-html="confirmText"></p>
        </div>
        <div class="modal-footer">
          <button @click="cancelConfirm" class="btn-secondary">Cancel</button>
          <button @click="confirmAction" class="btn-danger">{{ confirmButtonText }}</button>
        </div>
      </div>
    </div>

    <!-- Toast Notifications Container -->
    <div class="toast-container">
      <transition-group name="toast">
        <div 
          v-for="toast in toasts" 
          :key="toast.id" 
          :class="['toast', `toast-${toast.type}`]"
        >
          <div class="toast-icon">
            <i v-if="toast.type === 'success'" class="pi pi-check-circle"></i>
            <i v-if="toast.type === 'error'" class="pi pi-times-circle"></i>
            <i v-if="toast.type === 'warning'" class="pi pi-exclamation-triangle"></i>
            <i v-if="toast.type === 'info'" class="pi pi-info-circle"></i>
          </div>
          <div class="toast-content">
            <div class="toast-title">{{ toast.title }}</div>
            <div class="toast-message">{{ toast.message }}</div>
          </div>
          <button @click="removeToast(toast.id)" class="toast-close">
            <i class="pi pi-times"></i>
          </button>
        </div>
      </transition-group>
    </div>
    </div>
  </AppLayout>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AppLayout from './AppLayout.vue';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

export default {
  name: 'ScheduledReports',
  setup() {
    const scheduledReports = ref([]);
    const showCreateDialog = ref(false);
    const showHistoryModal = ref(false);
    const editingReport = ref(null);
    const selectedReport = ref(null);
    const executions = ref([]);
    
    // Message Modal
    const showMessageModal = ref(false);
    const messageType = ref('info'); // 'success', 'error', 'info'
    const messageTitle = ref('');
    const messageText = ref('');
    
    // Confirm Modal
    const showConfirmModal = ref(false);
    const confirmTitle = ref('');
    const confirmText = ref('');
    const confirmButtonText = ref('Confirm');
    const confirmCallback = ref(null);
    
    // Toast Notifications
    const toasts = ref([]);
    let toastIdCounter = 0;
    
    const formData = ref({
      name: '',
      report_type: 'PSR',
      frequency: 'DAILY',
      schedule_time: '08:00',
      format: 'EXCEL',
      date_range_days: 30
    });

    // Modal helper functions
    const showMessage = (type, title, text) => {
      messageType.value = type;
      messageTitle.value = title;
      messageText.value = text;
      showMessageModal.value = true;
    };

    const closeMessageModal = () => {
      showMessageModal.value = false;
    };

    const showConfirm = (title, text, callback, buttonText = 'Confirm') => {
      confirmTitle.value = title;
      confirmText.value = text;
      confirmButtonText.value = buttonText;
      confirmCallback.value = callback;
      showConfirmModal.value = true;
    };

    const confirmAction = () => {
      if (confirmCallback.value) {
        confirmCallback.value();
      }
      showConfirmModal.value = false;
    };

    const cancelConfirm = () => {
      showConfirmModal.value = false;
      confirmCallback.value = null;
    };

    // Toast helper functions
    const showToast = (type, title, message, duration = 4000) => {
      const id = ++toastIdCounter;
      const toast = { id, type, title, message };
      toasts.value.push(toast);
      
      // Auto remove after duration
      setTimeout(() => {
        removeToast(id);
      }, duration);
    };

    const removeToast = (id) => {
      const index = toasts.value.findIndex(t => t.id === id);
      if (index > -1) {
        toasts.value.splice(index, 1);
      }
    };

    const loadReports = async () => {
      try {
        console.log('Loading reports from:', `${API_URL}/scheduled-reports/`);
        const response = await axios.get(`${API_URL}/scheduled-reports/`);
        console.log('API Response:', response);
        console.log('Response data:', response.data);
        
        // Handle paginated response (DRF returns {results: [...], count: N})
        let data = [];
        if (response.data.results && Array.isArray(response.data.results)) {
          data = response.data.results;
        } else if (Array.isArray(response.data)) {
          data = response.data;
        }
        console.log('Processed data:', data);
        
        // Ensure each report has required fields
        scheduledReports.value = data.map(report => ({
          id: report.id || null,
          name: report.name || 'Unnamed Report',
          report_type: report.report_type || 'PSR',
          report_type_display: report.report_type_display || 'Plant Status Report (PSR)',
          frequency: report.frequency || 'DAILY',
          frequency_display: report.frequency_display || 'Daily',
          schedule_time: report.schedule_time || '08:00',
          format: report.format || 'EXCEL',
          date_range_days: report.date_range_days || 30,
          status: report.status || 'ACTIVE',
          next_run: report.next_run || null,
          recipients_count: report.recipients_count || 0,
          run_count: report.run_count || 0,
          ...report
        }));
        
        console.log('Final scheduledReports:', scheduledReports.value);
      } catch (error) {
        console.error('Failed to load reports:', error);
        console.error('Error details:', error.response);
        // Set empty array on error
        scheduledReports.value = [];
      }
    };

    const saveReport = async () => {
      try {
        if (editingReport.value) {
          await axios.put(`${API_URL}/scheduled-reports/${editingReport.value.id}/`, formData.value);
          showToast('success', 'Success!', `Report "${formData.value.name}" updated successfully!`);
        } else {
          await axios.post(`${API_URL}/scheduled-reports/`, formData.value);
          showToast('success', 'Success!', `Report "${formData.value.name}" created successfully!`);
        }
        showCreateDialog.value = false;
        loadReports();
      } catch (error) {
        console.error('Failed to save report:', error);
        showMessage('error', 'Error', 'Failed to save report. Please check if the backend API is running.');
      }
    };

    const toggleStatus = async (report) => {
      if (!report || !report.id) {
        console.error('Invalid report object');
        return;
      }
      try {
        const newStatus = report.status === 'ACTIVE' ? 'PAUSED' : 'ACTIVE';
        await axios.patch(`${API_URL}/scheduled-reports/${report.id}/`, { status: newStatus });
        loadReports();
        showToast('success', 'Status Updated', `Report "${report.name}" is now ${newStatus.toLowerCase()}.`);
      } catch (error) {
        console.error('Failed to toggle status:', error);
        showToast('error', 'Error', 'Failed to update report status.');
      }
    };

    const runNow = async (report) => {
      if (!report || !report.id) {
        console.error('Invalid report object');
        return;
      }
      try {
        console.log('Running report:', report.id, report.name);
        const response = await axios.post(`${API_URL}/scheduled-reports/${report.id}/run/`);
        console.log('Run response:', response.data);
        
        if (response.data.success) {
          showToast('success', 'Report Generated!', `"${response.data.report_name}" generated successfully! Check execution history.`, 5000);
          loadReports();
        } else {
          showToast('error', 'Error', response.data.error || 'Report execution failed');
        }
      } catch (error) {
        console.error('Failed to run report:', error);
        const errorMsg = error.response?.data?.error || error.response?.data?.details || error.message;
        showToast('error', 'Failed to Run Report', errorMsg, 6000);
      }
    };

    const deleteReport = async (report) => {
      if (!report || !report.id) {
        console.error('Invalid report object');
        return;
      }
      
      // Show confirm modal
      showConfirm(
        'Delete Report',
        `Are you sure you want to delete "<strong>${report.name}</strong>"?<br><br>This will:<br>• Delete the scheduled report<br>• Delete all execution history<br>• This action cannot be undone`,
        async () => {
          try {
            console.log('Deleting report:', report.id, report.name);
            await axios.delete(`${API_URL}/scheduled-reports/${report.id}/`);
            
            showToast('success', 'Deleted!', `Report "${report.name}" has been deleted successfully.`);
            loadReports();
          } catch (error) {
            console.error('Failed to delete report:', error);
            const errorMsg = error.response?.data?.error || error.message;
            showToast('error', 'Failed to Delete', errorMsg);
          }
        },
        'Delete'
      );
    };

    const editReport = (report) => {
      if (!report) {
        console.error('Invalid report object');
        return;
      }
      editingReport.value = report;
      formData.value = {
        name: report.name || '',
        report_type: report.report_type || 'PSR',
        frequency: report.frequency || 'DAILY',
        schedule_time: report.schedule_time || '08:00',
        format: report.format || 'EXCEL',
        date_range_days: report.date_range_days || 30
      };
      showCreateDialog.value = true;
    };

    const viewExecutions = async (report) => {
      if (!report || !report.id) {
        console.error('Invalid report object');
        return;
      }
      try {
        selectedReport.value = report;
        const response = await axios.get(`${API_URL}/scheduled-reports/${report.id}/executions/`);
        executions.value = Array.isArray(response.data) ? response.data : [];
        showHistoryModal.value = true;
      } catch (error) {
        console.error('Failed to load executions:', error);
        showMessage('error', 'Error', 'Failed to load execution history. Please check if the backend API is running.');
      }
    };

    const downloadFile = async (executionId) => {
      if (!executionId) return;
      
      try {
        console.log('Downloading execution:', executionId);
        
        // Use the proper API endpoint for download
        const downloadUrl = `${API_URL}/report-executions/${executionId}/download/`;
        
        console.log('Download URL:', downloadUrl);
        
        // Fetch the file
        const response = await axios.get(downloadUrl, {
          responseType: 'blob'
        });
        
        // Create blob and download
        const blob = new Blob([response.data], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
        
        // Get filename from Content-Disposition header or use default
        let filename = 'PSR_Report.xlsx';
        const contentDisposition = response.headers['content-disposition'];
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
          if (filenameMatch) {
            filename = filenameMatch[1];
          }
        }
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        
        console.log('Download successful:', filename);
      } catch (error) {
        console.error('Download failed:', error);
        showMessage('error', 'Download Failed', 'Failed to download file. Please check if the file exists and try again.');
      }
    };

    const deleteExecution = async (execution) => {
      if (!execution || !execution.id) {
        console.error('Invalid execution object');
        return;
      }
      
      // Show confirm modal
      showConfirm(
        'Delete Execution',
        `Are you sure you want to delete this execution?<br><br>` +
        `<strong>File:</strong> ${getFileName(execution.file_path) || 'N/A'}<br>` +
        `<strong>Date:</strong> ${formatDateTime(execution.started_at)}<br><br>` +
        `This will permanently delete the execution record and the generated file.<br>` +
        `This action cannot be undone.`,
        async () => {
          try {
            console.log('Deleting execution:', execution.id);
            await axios.delete(`${API_URL}/report-executions/${execution.id}/`);
            
            showToast('success', 'Deleted!', 'Execution record has been deleted successfully.');
            
            // Refresh executions list
            if (selectedReport.value) {
              await viewExecutions(selectedReport.value);
            }
            
            // Reload reports list to update execution count
            await loadReports();
          } catch (error) {
            console.error('Failed to delete execution:', error);
            const errorMsg = error.response?.data?.error || error.message;
            showToast('error', 'Failed to Delete', errorMsg);
          }
        },
        'Delete'
      );
    };

    const getFileName = (filePath) => {
      if (!filePath) return 'N/A';
      // Handle both forward slashes and backslashes
      return filePath.split(/[/\\]/).pop();
    };

    const formatFileSize = (bytes) => {
      if (!bytes) return 'N/A';
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    const formatDateTime = (dateStr) => {
      if (!dateStr) return 'N/A';
      const date = new Date(dateStr);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return 'Not scheduled';
      return new Date(dateStr).toLocaleString();
    };

    onMounted(() => {
      loadReports();
    });

    return {
      scheduledReports,
      showCreateDialog,
      showHistoryModal,
      editingReport,
      selectedReport,
      executions,
      formData,
      showMessageModal,
      messageType,
      messageTitle,
      messageText,
      showConfirmModal,
      confirmTitle,
      confirmText,
      confirmButtonText,
      toasts,
      saveReport,
      toggleStatus,
      runNow,
      deleteReport,
      editReport,
      viewExecutions,
      downloadFile,
      deleteExecution,
      getFileName,
      formatFileSize,
      formatDateTime,
      formatDate,
      closeMessageModal,
      confirmAction,
      cancelConfirm,
      showToast,
      removeToast
    };
  },
  components: {
    AppLayout
  }
};
</script>

<style scoped>
.scheduled-reports {
  padding: 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #e2e8f0;
}

.header h2 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.reports-list {
  display: grid;
  gap: 24px;
}

.report-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.report-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.report-card:hover::before {
  opacity: 1;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 20px;
}

.report-header h3 {
  margin: 0 0 8px 0;
  color: #0f172a;
  font-size: 1.375rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.report-type {
  color: #64748b;
  font-size: 0.9375rem;
  margin: 0;
  font-weight: 500;
}

.status-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-badge.active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-badge.paused {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.status-badge.unknown {
  background: #e2e8f0;
  color: #64748b;
}

.report-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #475569;
  font-size: 0.9375rem;
  font-weight: 500;
}

.detail-item i {
  color: #3b82f6;
  font-size: 1.125rem;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #dbeafe;
  border-radius: 8px;
  padding: 4px;
}

.report-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.btn-primary, .btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9375rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-secondary {
  background: white;
  color: #475569;
  border: 2px solid #e2e8f0;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  transform: translateY(-2px);
}

.btn-danger {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9375rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-danger:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.btn-danger:active {
  transform: translateY(0);
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #cbd5e1;
}

.empty-state i {
  font-size: 4rem;
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-state p {
  color: #64748b;
  font-size: 1.125rem;
  margin: 12px 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-content.large {
  max-width: 900px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e2e8f0;
}

.modal-header h2 {
  margin: 0;
  color: #0f172a;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.btn-close {
  background: #f1f5f9;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  transition: all 0.2s;
  font-weight: 300;
}

.btn-close:hover {
  background: #e2e8f0;
  color: #1e293b;
  transform: rotate(90deg);
}

.executions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.execution-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
}

.execution-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.execution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.execution-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.execution-date {
  margin-left: 12px;
  color: #64748b;
  font-size: 0.9375rem;
  font-weight: 500;
}

.btn-download {
  padding: 8px 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9375rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.btn-download:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-delete-exec {
  padding: 8px 12px;
  background: white;
  color: #ef4444;
  border: 2px solid #fecaca;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
}

.btn-delete-exec:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-color: #ef4444;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.btn-delete-exec:active {
  transform: translateY(0) scale(1);
}

.execution-details {
  display: grid;
  gap: 12px;
  background: white;
  padding: 16px;
  border-radius: 10px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-row .label {
  color: #64748b;
  font-size: 0.9375rem;
  font-weight: 600;
}

.detail-row .value {
  color: #0f172a;
  font-size: 0.9375rem;
  font-weight: 500;
}

.detail-row .filename {
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  color: #3b82f6;
  background: #dbeafe;
  padding: 4px 8px;
  border-radius: 6px;
}

.detail-row.error {
  background: #fef2f2;
  padding: 12px;
  border-radius: 8px;
  border-bottom: none;
  border-left: 4px solid #ef4444;
}

.detail-row.error .value {
  color: #dc2626;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.completed {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-badge.running {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.status-badge.failed {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.status-badge.pending {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  color: #0f172a;
  font-weight: 600;
  font-size: 0.9375rem;
  letter-spacing: -0.01em;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s;
  background: white;
  color: #0f172a;
  font-weight: 500;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid #e2e8f0;
}

/* Message and Confirm Modals */
.message-modal,
.confirm-modal {
  max-width: 520px;
}

.modal-header.success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
}

.modal-header.error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.3);
}

.modal-header.info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

.modal-header.warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.3);
}

.modal-header.success,
.modal-header.error,
.modal-header.info,
.modal-header.warning {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 32px;
  border-radius: 20px 20px 0 0;
  margin: -32px -32px 24px -32px;
  border-bottom: none;
}

.modal-header.success h2,
.modal-header.error h2,
.modal-header.info h2,
.modal-header.warning h2 {
  flex: 1;
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.modal-header.success .btn-close,
.modal-header.error .btn-close,
.modal-header.info .btn-close,
.modal-header.warning .btn-close {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.modal-header.success .btn-close:hover,
.modal-header.error .btn-close:hover,
.modal-header.info .btn-close:hover,
.modal-header.warning .btn-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.modal-icon {
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 14px;
  backdrop-filter: blur(10px);
}

.modal-body {
  padding: 24px 0;
  color: #475569;
  line-height: 1.7;
  font-size: 1rem;
}

.modal-body p {
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 2px solid #e2e8f0;
}

/* Toast Notifications */
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 420px;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-left: 4px solid;
  min-width: 320px;
  animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

@keyframes slideIn {
  from {
    transform: translateX(450px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast-success {
  border-left-color: #10b981;
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
}

.toast-error {
  border-left-color: #ef4444;
  background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
}

.toast-warning {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
}

.toast-info {
  border-left-color: #3b82f6;
  background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
}

.toast-icon {
  font-size: 1.75rem;
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.toast-success .toast-icon {
  color: #10b981;
  background: #d1fae5;
}

.toast-error .toast-icon {
  color: #ef4444;
  background: #fee2e2;
}

.toast-warning .toast-icon {
  color: #f59e0b;
  background: #fef3c7;
}

.toast-info .toast-icon {
  color: #3b82f6;
  background: #dbeafe;
}

.toast-content {
  flex: 1;
  padding-top: 2px;
}

.toast-title {
  font-weight: 700;
  font-size: 1rem;
  color: #0f172a;
  margin-bottom: 4px;
  letter-spacing: -0.01em;
}

.toast-message {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.5;
  font-weight: 500;
}

.toast-close {
  background: #f1f5f9;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
  flex-shrink: 0;
  font-size: 1rem;
}

.toast-close:hover {
  background: #e2e8f0;
  color: #64748b;
  transform: scale(1.1);
}

/* Toast transitions */
.toast-enter-active {
  animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-leave-active {
  animation: slideOut 0.3s cubic-bezier(0.4, 0, 1, 1);
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(450px);
    opacity: 0;
  }
}

/* Responsive toast */
@media (max-width: 640px) {
  .toast-container {
    left: 12px;
    right: 12px;
    top: 12px;
    max-width: none;
  }
  
  .toast {
    min-width: auto;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .scheduled-reports {
    padding: 20px;
  }

  .header h2 {
    font-size: 1.5rem;
  }

  .report-card {
    padding: 20px;
  }

  .report-details {
    grid-template-columns: 1fr;
  }

  .report-actions {
    flex-direction: column;
  }

  .report-actions button {
    width: 100%;
    justify-content: center;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-content {
    padding: 24px;
    width: 95%;
  }
}
</style>
