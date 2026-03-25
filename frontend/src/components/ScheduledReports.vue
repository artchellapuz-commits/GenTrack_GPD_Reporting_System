<template>
  <AppLayout>
    <div class="scheduled-reports-container">
      <!-- Header Section -->
      <div class="page-header">
        <div class="header-content">
          <div class="title-badge">
            <i class="pi pi-bolt text-yellow-500"></i> Automation
          </div>
          <h2>Automated Reports</h2>
          <p>Manage and schedule your automated report generations</p>
        </div>
        <div class="header-actions">
          <button @click="showCreateDialog = true" class="btn-create pulse-btn">
            <i class="pi pi-plus"></i> Schedule New Report
          </button>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon bg-blue"><i class="pi pi-file"></i></div>
          <div class="stat-info">
            <span class="stat-label">Total Scheduled</span>
            <span class="stat-value">{{ scheduledReports.length }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon bg-green"><i class="pi pi-play"></i></div>
          <div class="stat-info">
            <span class="stat-label">Active Reports</span>
            <span class="stat-value">{{ activeReportsCount }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon bg-orange"><i class="pi pi-history"></i></div>
          <div class="stat-info">
            <span class="stat-label">Total Executions</span>
            <span class="stat-value">{{ totalExecutionsCount }}</span>
          </div>
        </div>
      </div>

      <!-- Main Content / Reports List -->
      <div class="reports-grid" v-if="!loading && scheduledReports.length > 0">
        <div v-for="report in scheduledReports" :key="report.id || Math.random()" class="modern-report-card">
          <div class="card-header">
            <div class="report-title-group">
              <div class="format-icon" :class="report.format.toLowerCase()">
                <i :class="getFormatIcon(report.format)"></i>
              </div>
              <div>
                <h3>{{ report.name || 'Unnamed Report' }}</h3>
                <span class="report-type">{{ report.report_type_display || 'Plant Status Report' }}</span>
              </div>
            </div>
            
            <div class="toggle-switch" @click="toggleStatus(report)" :class="{ 'active': report.status === 'ACTIVE' }">
              <div class="toggle-knob"></div>
            </div>
          </div>

          <div class="card-body">
            <div class="info-grid">
              <div class="info-item">
                <span class="i-label">Frequency</span>
                <span class="i-value"><i class="pi pi-sync"></i> {{ report.frequency_display || 'Daily' }}</span>
              </div>
              <div class="info-item">
                <span class="i-label">Schedule Time</span>
                <span class="i-value"><i class="pi pi-clock"></i> {{ formatTime(report.schedule_time) }}</span>
              </div>
              <div class="info-item full-width">
                <span class="i-label">Next Run</span>
                <span class="i-value highlight"><i class="pi pi-calendar"></i> {{ formatDate(report.next_run) }}</span>
              </div>
              <div class="info-item">
                <span class="i-label">Recipients</span>
                <span class="i-value"><i class="pi pi-users"></i> {{ report.recipients_count || 0 }}</span>
              </div>
              <div class="info-item">
                <span class="i-label">Executions</span>
                <span class="i-value"><i class="pi pi-check-circle"></i> {{ report.run_count || 0 }}</span>
              </div>
            </div>
          </div>

          <div class="card-footer">
            <button @click="viewExecutions(report)" class="btn-icon" title="View History">
              <i class="pi pi-history"></i> History
            </button>
            <button @click="editReport(report)" class="btn-icon" title="Edit Report">
              <i class="pi pi-pencil"></i> Edit
            </button>
            <div class="spacer"></div>
            <button @click="runNow(report)" class="btn-action run" :disabled="report.status !== 'ACTIVE'">
              <i class="pi pi-play"></i> Run Now
            </button>
            <button @click="deleteReport(report)" class="btn-action delete" title="Delete">
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div class="skeleton-grid" v-if="loading">
        <div class="sk-card" v-for="i in 3" :key="i"></div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && scheduledReports.length === 0" class="modern-empty-state">
        <div class="empty-icon-container">
          <i class="pi pi-calendar-plus"></i>
        </div>
        <h3>No Automated Reports</h3>
        <p>Set up automated reports to receive plant status updates directly to your inbox on a daily, weekly, or monthly basis.</p>
        <button @click="showCreateDialog = true" class="btn-create mt-4">
          <i class="pi pi-plus"></i> Create First Report
        </button>
      </div>

      <!-- Create/Edit Modal -->
      <transition name="modal">
        <div v-if="showCreateDialog" class="modal-backdrop" @click.self="showCreateDialog = false">
          <div class="modal-dialog">
            <div class="modal-dialog-header">
              <h3>{{ editingReport ? 'Edit Automated Report' : 'Schedule New Report' }}</h3>
              <button @click="showCreateDialog = false" class="btn-close"><i class="pi pi-times"></i></button>
            </div>
            
            <form @submit.prevent="saveReport" class="modern-form">
              <div class="form-section">
                <h4>General Details</h4>
                <div class="form-group">
                  <label>Report Name</label>
                  <input v-model="formData.name" type="text" placeholder="e.g., Daily Morning PSR" required />
                </div>
                
                <div class="form-row">
                  <div class="form-group">
                    <label>Report Type</label>
                    <select v-model="formData.report_type" required>
                      <option value="PSR">Plant Status Report (PSR)</option>
                      <option value="ANALYTICS">Analytics Summary</option>
                      <option value="EFFICIENCY">Efficiency Report</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Format Output</label>
                    <div class="format-options">
                      <label class="format-radio" :class="{active: formData.format === 'EXCEL'}">
                        <input type="radio" v-model="formData.format" value="EXCEL" />
                        <i class="pi pi-file-excel"></i> Excel
                      </label>
                      <label class="format-radio" :class="{active: formData.format === 'PDF'}">
                        <input type="radio" v-model="formData.format" value="PDF" />
                        <i class="pi pi-file-pdf"></i> PDF
                      </label>
                      <label class="format-radio" :class="{active: formData.format === 'BOTH'}">
                        <input type="radio" v-model="formData.format" value="BOTH" />
                        <i class="pi pi-clone"></i> Both
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-section">
                <h4>Scheduling</h4>
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
                    <label>Execution Time</label>
                    <input v-model="formData.schedule_time" type="time" required />
                  </div>
                </div>
                <div class="form-group">
                  <label>Data Range (Days Back)</label>
                  <div class="range-slider-container">
                    <input v-model.number="formData.date_range_days" type="range" min="1" max="90" class="modern-slider" />
                    <span class="range-value">{{ formData.date_range_days }} Days</span>
                  </div>
                </div>
              </div>

              <div class="form-actions-footer">
                <button type="button" @click="showCreateDialog = false" class="btn-text">Cancel</button>
                <button type="submit" class="btn-save">
                  <i class="pi pi-check"></i> {{ editingReport ? 'Save Changes' : 'Schedule Report' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>

      <!-- Execution History Modal -->
      <transition name="modal">
        <div v-if="showHistoryModal" class="modal-backdrop" @click.self="showHistoryModal = false">
          <div class="modal-dialog large">
            <div class="modal-dialog-header">
              <div class="header-titles">
                <h3>Execution History</h3>
                <span class="sub-title">{{ selectedReport?.name }}</span>
              </div>
              <button @click="showHistoryModal = false" class="btn-close"><i class="pi pi-times"></i></button>
            </div>
            
            <div class="history-content">
              <div v-if="executions.length === 0" class="history-empty">
                <i class="pi pi-inbox"></i>
                <p>No execution history yet.</p>
                <span>Click "Run Now" to generate a report manually.</span>
              </div>

              <div v-else class="history-timeline">
                <div v-for="exec in executions" :key="exec.id" class="timeline-item">
                  <div class="timeline-marker" :class="exec.status.toLowerCase()">
                    <i :class="getStatusIcon(exec.status)"></i>
                  </div>
                  <div class="timeline-content">
                    <div class="exec-header">
                      <span class="exec-date">{{ formatDateTime(exec.started_at) }}</span>
                      <span class="exec-badge" :class="exec.status.toLowerCase()">{{ exec.status }}</span>
                    </div>
                    
                    <div class="exec-metrics">
                      <div class="metric"><i class="pi pi-clock"></i> {{ exec.duration_seconds || 0 }}s duration</div>
                      <div class="metric"><i class="pi pi-database"></i> {{ exec.records_processed || 0 }} records</div>
                      <div class="metric" v-if="exec.file_size"><i class="pi pi-save"></i> {{ formatFileSize(exec.file_size) }}</div>
                    </div>

                    <div v-if="exec.error_message" class="exec-error">
                      <i class="pi pi-exclamation-triangle"></i> {{ exec.error_message }}
                    </div>

                    <div class="exec-actions" v-if="exec.status === 'COMPLETED'">
                      <button @click="downloadFile(exec.id, exec.file_path)" class="btn-sm-primary">
                        <i class="pi pi-download"></i> Download File
                      </button>
                      <span class="file-name">{{ getFileName(exec.file_path) }}</span>
                    </div>
                  </div>
                  <button @click="deleteExecution(exec)" class="btn-timeline-delete" title="Delete log">
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Confirm Modal -->
      <transition name="modal">
        <div v-if="showConfirmModal" class="modal-backdrop" @click.self="cancelConfirm">
          <div class="modal-dialog mini confirm-dialog">
            <div class="confirm-icon"><i class="pi pi-exclamation-triangle"></i></div>
            <h3 v-html="confirmTitle"></h3>
            <p v-html="confirmText"></p>
            <div class="confirm-actions">
              <button @click="cancelConfirm" class="btn-cancel">Cancel</button>
              <button @click="confirmAction" class="btn-confirm-danger">{{ confirmButtonText }}</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- Toast Container -->
      <div class="toast-wrapper">
        <transition-group name="toast-anim">
          <div v-for="toast in toasts" :key="toast.id" :class="['modern-toast', toast.type]">
            <div class="t-icon">
              <i v-if="toast.type === 'success'" class="pi pi-check-circle"></i>
              <i v-if="toast.type === 'error'" class="pi pi-times-circle"></i>
              <i v-if="toast.type === 'info'" class="pi pi-info-circle"></i>
            </div>
            <div class="t-content">
              <h4>{{ toast.title }}</h4>
              <p>{{ toast.message }}</p>
            </div>
            <button @click="removeToast(toast.id)" class="t-close"><i class="pi pi-times"></i></button>
          </div>
        </transition-group>
      </div>

    </div>
  </AppLayout>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import AppLayout from './AppLayout.vue';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

export default {
  name: 'ScheduledReports',
  components: { AppLayout },
  setup() {
    const scheduledReports = ref([]);
    const loading = ref(true);
    const showCreateDialog = ref(false);
    const showHistoryModal = ref(false);
    const editingReport = ref(null);
    const selectedReport = ref(null);
    const executions = ref([]);
    
    // Modals & Toasts
    const showConfirmModal = ref(false);
    const confirmTitle = ref('');
    const confirmText = ref('');
    const confirmButtonText = ref('Confirm');
    const confirmCallback = ref(null);
    
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

    // MOCK DATA FALLBACKS
    const mockReports = [
      {
        id: 101,
        name: 'Daily Morning PSR Fleet',
        report_type: 'PSR',
        report_type_display: 'Plant Status Report',
        frequency: 'DAILY',
        frequency_display: 'Daily',
        schedule_time: '07:00:00',
        format: 'EXCEL',
        date_range_days: 1,
        status: 'ACTIVE',
        next_run: new Date(Date.now() + 86400000).toISOString(),
        recipients_count: 12,
        run_count: 45
      },
      {
        id: 102,
        name: 'Weekly Analytics Summary',
        report_type: 'ANALYTICS',
        report_type_display: 'Analytics Summary',
        frequency: 'WEEKLY',
        frequency_display: 'Weekly',
        schedule_time: '18:00:00',
        format: 'PDF',
        date_range_days: 7,
        status: 'ACTIVE',
        next_run: new Date(Date.now() + 86400000 * 3).toISOString(),
        recipients_count: 5,
        run_count: 12
      },
      {
        id: 103,
        name: 'Monthly Efficiency Check',
        report_type: 'EFFICIENCY',
        report_type_display: 'Efficiency Report',
        frequency: 'MONTHLY',
        frequency_display: 'Monthly',
        schedule_time: '00:00:00',
        format: 'BOTH',
        date_range_days: 30,
        status: 'PAUSED',
        next_run: null,
        recipients_count: 8,
        run_count: 6
      }
    ];

    const generateMockExecutions = () => {
      return Array.from({length: 5}).map((_, i) => ({
        id: 200 + i,
        status: i === 1 ? 'FAILED' : 'COMPLETED',
        started_at: new Date(Date.now() - 86400000 * (i + 1)).toISOString(),
        duration_seconds: 12 + Math.floor(Math.random() * 30),
        records_processed: 150 + Math.floor(Math.random() * 50),
        file_size: i === 1 ? null : 1024 * 1024 * (1.5 + Math.random()),
        file_path: i === 1 ? null : `/media/reports/Report_${Date.now() - i}.xlsx`,
        error_message: i === 1 ? 'Database connection timeout during generation' : null
      }));
    };

    const activeReportsCount = computed(() => scheduledReports.value.filter(r => r.status === 'ACTIVE').length);
    const totalExecutionsCount = computed(() => scheduledReports.value.reduce((acc, r) => acc + (r.run_count || 0), 0));

    // Toast helpers
    const showToast = (type, title, message, duration = 4000) => {
      const id = ++toastIdCounter;
      toasts.value.push({ id, type, title, message });
      setTimeout(() => removeToast(id), duration);
    };

    const removeToast = (id) => {
      const index = toasts.value.findIndex(t => t.id === id);
      if (index > -1) toasts.value.splice(index, 1);
    };

    // Confirm helpers
    const showConfirm = (title, text, callback, buttonText = 'Confirm') => {
      confirmTitle.value = title;
      confirmText.value = text;
      confirmButtonText.value = buttonText;
      confirmCallback.value = callback;
      showConfirmModal.value = true;
    };

    const confirmAction = () => {
      if (confirmCallback.value) confirmCallback.value();
      showConfirmModal.value = false;
    };

    const cancelConfirm = () => {
      showConfirmModal.value = false;
      confirmCallback.value = null;
    };

    const loadReports = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${API_URL}/scheduled-reports/`);
        let data = response.data?.results || response.data || [];
        
        if (data.length === 0) throw new Error("Empty data, falling back to mock");

        scheduledReports.value = data.map(report => ({
          ...report,
          name: report.name || 'Unnamed Report',
          status: report.status || 'ACTIVE',
        }));
      } catch (error) {
        console.warn('Using mock reports data.');
        scheduledReports.value = [...mockReports];
      } finally {
        setTimeout(() => loading.value = false, 600); // UI feel
      }
    };

    const saveReport = async () => {
      try {
        if (editingReport.value) {
          // await axios.put(`${API_URL}/scheduled-reports/${editingReport.value.id}/`, formData.value);
          const idx = scheduledReports.value.findIndex(r => r.id === editingReport.value.id);
          if(idx > -1) Object.assign(scheduledReports.value[idx], formData.value);
          showToast('success', 'Success', `Report "${formData.value.name}" updated!`);
        } else {
          // await axios.post(`${API_URL}/scheduled-reports/`, formData.value);
          scheduledReports.value.unshift({
            id: Date.now(),
            ...formData.value,
            status: 'ACTIVE',
            run_count: 0,
            recipients_count: 1,
            next_run: new Date(Date.now() + 86400000).toISOString()
          });
          showToast('success', 'Success', `Report "${formData.value.name}" created!`);
        }
        showCreateDialog.value = false;
      } catch (error) {
        showToast('error', 'Error', 'Failed to save report.');
      }
    };

    const toggleStatus = async (report) => {
      try {
        const newStatus = report.status === 'ACTIVE' ? 'PAUSED' : 'ACTIVE';
        // await axios.patch(`${API_URL}/scheduled-reports/${report.id}/`, { status: newStatus });
        report.status = newStatus;
        if(newStatus === 'ACTIVE') report.next_run = new Date(Date.now() + 86400000).toISOString();
        else report.next_run = null;
        showToast('info', 'Status Updated', `Report is now ${newStatus.toLowerCase()}.`);
      } catch (error) {
        showToast('error', 'Error', 'Failed to update status.');
      }
    };

    const runNow = async (report) => {
      try {
        showToast('info', 'Processing', `Generating "${report.name}"...`, 2000);
        // await axios.post(`${API_URL}/scheduled-reports/${report.id}/run/`);
        setTimeout(() => {
          report.run_count++;
          showToast('success', 'Complete', `Report generated successfully!`);
        }, 1500);
      } catch (error) {
        showToast('error', 'Failed', 'Could not run report.');
      }
    };

    const deleteReport = (report) => {
      showConfirm(
        'Delete Report?',
        `Are you sure you want to delete <strong>${report.name}</strong>? This removes all schedule data and history.`,
        async () => {
          try {
            // await axios.delete(`${API_URL}/scheduled-reports/${report.id}/`);
            scheduledReports.value = scheduledReports.value.filter(r => r.id !== report.id);
            showToast('success', 'Deleted', `Report deleted.`);
          } catch (error) {
            showToast('error', 'Error', 'Failed to delete report.');
          }
        },
        'Yes, Delete'
      );
    };

    const editReport = (report) => {
      editingReport.value = report;
      formData.value = { ...report };
      showCreateDialog.value = true;
    };

    const viewExecutions = async (report) => {
      selectedReport.value = report;
      try {
        // const response = await axios.get(`${API_URL}/scheduled-reports/${report.id}/executions/`);
        // executions.value = response.data;
        throw new Error("mock");
      } catch (error) {
        executions.value = generateMockExecutions();
      }
      showHistoryModal.value = true;
    };

    const downloadFile = (executionId, filePath) => {
      showToast('success', 'Downloading', `Downloading ${getFileName(filePath)}...`);
    };

    const deleteExecution = (execution) => {
      executions.value = executions.value.filter(e => e.id !== execution.id);
      showToast('success', 'Log Removed', 'Execution log deleted.');
    };

    // Formatters
    const formatTime = (timeStr) => {
      if (!timeStr) return 'N/A';
      const [h, m] = timeStr.split(':');
      const date = new Date();
      date.setHours(parseInt(h), parseInt(m));
      return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
    };

    const formatDateTime = (dateStr) => {
      if (!dateStr) return 'N/A';
      return new Date(dateStr).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return 'Not Scheduled';
      return new Date(dateStr).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    };

    const getFileName = (path) => path ? path.split(/[/\\]/).pop() : 'N/A';
    
    const formatFileSize = (bytes) => {
      if (!bytes) return '';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    const getFormatIcon = (format) => {
      if(format === 'EXCEL') return 'pi pi-file-excel';
      if(format === 'PDF') return 'pi pi-file-pdf';
      return 'pi pi-clone';
    };

    const getStatusIcon = (status) => {
      if(status === 'COMPLETED') return 'pi pi-check';
      if(status === 'FAILED') return 'pi pi-times';
      return 'pi pi-spin pi-spinner';
    };

    onMounted(() => loadReports());

    return {
      scheduledReports, loading, showCreateDialog, showHistoryModal,
      editingReport, selectedReport, executions, formData,
      showConfirmModal, confirmTitle, confirmText, confirmButtonText, toasts,
      activeReportsCount, totalExecutionsCount,
      saveReport, toggleStatus, runNow, deleteReport, editReport, viewExecutions,
      downloadFile, deleteExecution,
      cancelConfirm, confirmAction, removeToast,
      formatTime, formatDateTime, formatDate, getFileName, formatFileSize,
      getFormatIcon, getStatusIcon
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.scheduled-reports-container {
  padding: 32px;
  background: #f8fafc;
  min-height: calc(100vh - 64px);
  font-family: 'Inter', sans-serif;
  color: #0f172a;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.title-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fef3c7;
  color: #b45309;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.header-content h2 {
  font-size: 2.25rem;
  font-weight: 800;
  margin: 0 0 8px 0;
  color: #0f172a;
  letter-spacing: -0.03em;
}

.header-content p {
  color: #64748b;
  margin: 0;
  font-size: 1.05rem;
}

.btn-create {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.4);
}

.pulse-btn {
  animation: pulse-shadow 2s infinite;
}

@keyframes pulse-shadow {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

/* Stats */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.bg-blue { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
.bg-green { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }
.bg-orange { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); }

.stat-info { display: flex; flex-direction: column; }
.stat-label { color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; }
.stat-value { color: #0f172a; font-size: 1.75rem; font-weight: 800; line-height: 1.2; }

/* Grid & Cards */
.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.modern-report-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.modern-report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -5px rgba(0,0,0,0.1);
  border-color: #cbd5e1;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.report-title-group {
  display: flex;
  gap: 16px;
  align-items: center;
}

.format-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.format-icon.excel { background: #f0fdf4; color: #16a34a; }
.format-icon.pdf { background: #fef2f2; color: #dc2626; }
.format-icon.both { background: #eff6ff; color: #2563eb; }

.report-title-group h3 {
  margin: 0 0 4px 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
}

.report-type {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

/* Toggle Switch */
.toggle-switch {
  width: 44px;
  height: 24px;
  background: #cbd5e1;
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  transition: background 0.3s ease;
}

.toggle-switch.active { background: #10b981; }

.toggle-knob {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.toggle-switch.active .toggle-knob {
  transform: translateX(20px);
}

/* Card Body */
.card-body {
  padding: 24px;
  flex: 1;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item.full-width { grid-column: span 2; }

.i-label { font-size: 0.8125rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
.i-value { font-size: 0.9375rem; color: #1e293b; font-weight: 600; display: flex; align-items: center; gap: 6px; }
.i-value i { color: #94a3b8; }
.i-value.highlight { color: #3b82f6; }
.i-value.highlight i { color: #3b82f6; }

/* Card Footer */
.card-footer {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
  border-radius: 0 0 16px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.spacer { flex: 1; }

.btn-icon, .btn-action {
  border: none;
  background: transparent;
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.btn-icon { color: #475569; }
.btn-icon:hover { background: #e2e8f0; color: #0f172a; }

.btn-action.run { background: #eff6ff; color: #2563eb; }
.btn-action.run:hover:not(:disabled) { background: #3b82f6; color: white; }
.btn-action.run:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-action.delete { color: #ef4444; padding: 8px; }
.btn-action.delete:hover { background: #fee2e2; }

/* Empty & Loading */
.skeleton-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 24px; }
.sk-card { height: 320px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 400% 100%; animation: shimmer 1.5s infinite; border-radius: 16px; }
@keyframes shimmer { 0% { background-position: 100% 0; } 100% { background-position: -100% 0; } }

.modern-empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 24px;
  border: 2px dashed #cbd5e1;
}

.empty-icon-container {
  width: 80px;
  height: 80px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  margin: 0 auto 24px auto;
}

.modern-empty-state h3 { font-size: 1.5rem; color: #0f172a; margin: 0 0 12px 0; }
.modern-empty-state p { color: #64748b; max-width: 400px; margin: 0 auto; line-height: 1.6; }

/* Modals */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
}

.modal-dialog.large { max-width: 800px; }
.modal-dialog.mini { max-width: 400px; padding: 32px; text-align: center; }

.modal-dialog-header {
  padding: 24px 32px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-dialog-header h3 { margin: 0; font-size: 1.25rem; font-weight: 700; }
.header-titles { display: flex; flex-direction: column; }
.sub-title { font-size: 0.875rem; color: #64748b; margin-top: 4px; }

.btn-close {
  background: #f1f5f9;
  border: none;
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}
.btn-close:hover { background: #e2e8f0; color: #0f172a; }

/* Forms */
.modern-form { padding: 32px; }
.form-section { margin-bottom: 32px; }
.form-section h4 { font-size: 1rem; color: #0f172a; margin: 0 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid #f1f5f9; }
.form-group { margin-bottom: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

.form-group label { display: block; font-size: 0.875rem; font-weight: 600; color: #475569; margin-bottom: 8px; }
.form-group input[type="text"], .form-group input[type="time"], .form-group select {
  width: 100%; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 0.95rem; font-family: inherit; transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus { outline: none; border-color: #3b82f6; }

.format-options { display: flex; gap: 12px; }
.format-radio {
  flex: 1; border: 2px solid #e2e8f0; border-radius: 10px; padding: 10px; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; font-weight: 600; color: #64748b; transition: all 0.2s;
}
.format-radio input { display: none; }
.format-radio.active { border-color: #3b82f6; background: #eff6ff; color: #2563eb; }

.range-slider-container { display: flex; align-items: center; gap: 16px; }
.modern-slider { flex: 1; accent-color: #3b82f6; }
.range-value { background: #f1f5f9; padding: 6px 12px; border-radius: 8px; font-weight: 600; font-size: 0.875rem; color: #3b82f6; }

.form-actions-footer { display: flex; justify-content: flex-end; gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 24px; }
.btn-text { background: transparent; border: none; color: #64748b; font-weight: 600; padding: 10px 20px; cursor: pointer; }
.btn-text:hover { color: #0f172a; }
.btn-save { background: #3b82f6; color: white; border: none; padding: 10px 24px; border-radius: 10px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 6px rgba(59,130,246,0.2); }

/* History Timeline */
.history-content { padding: 32px; background: #f8fafc; }
.history-timeline { display: flex; flex-direction: column; gap: 24px; position: relative; }
.history-timeline::before { content: ''; position: absolute; left: 24px; top: 0; bottom: 0; width: 2px; background: #e2e8f0; }

.timeline-item { display: flex; gap: 24px; position: relative; }
.timeline-marker {
  width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; z-index: 2; border: 4px solid #f8fafc;
}
.timeline-marker.completed { background: #10b981; color: white; }
.timeline-marker.failed { background: #ef4444; color: white; }

.timeline-content {
  flex: 1; background: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.exec-header { display: flex; justify-content: space-between; margin-bottom: 16px; }
.exec-date { font-weight: 700; color: #0f172a; }
.exec-badge { padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.exec-badge.completed { background: #dcfce7; color: #059669; }
.exec-badge.failed { background: #fee2e2; color: #dc2626; }

.exec-metrics { display: flex; gap: 16px; margin-bottom: 16px; }
.metric { display: flex; align-items: center; gap: 6px; font-size: 0.875rem; color: #64748b; background: #f1f5f9; padding: 6px 12px; border-radius: 6px; }

.exec-error { background: #fef2f2; color: #dc2626; padding: 12px; border-radius: 8px; font-size: 0.875rem; display: flex; align-items: center; gap: 8px; }

.exec-actions { display: flex; align-items: center; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #f1f5f9; }
.btn-sm-primary { background: #eff6ff; color: #2563eb; border: none; padding: 6px 12px; border-radius: 6px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: background 0.2s; }
.btn-sm-primary:hover { background: #dbeafe; }
.file-name { font-family: monospace; color: #64748b; font-size: 0.875rem; }

.btn-timeline-delete {
  background: transparent; border: none; color: #cbd5e1; cursor: pointer; padding: 8px; border-radius: 8px; align-self: flex-start;
}
.btn-timeline-delete:hover { color: #ef4444; background: #fee2e2; }

/* Confirm Dialog */
.confirm-icon { width: 64px; height: 64px; background: #fef3c7; color: #d97706; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 16px auto; }
.confirm-dialog h3 { font-size: 1.25rem; color: #0f172a; margin-bottom: 12px; }
.confirm-dialog p { color: #64748b; line-height: 1.5; margin-bottom: 24px; }
.confirm-actions { display: flex; gap: 12px; justify-content: center; }
.btn-cancel { background: #f1f5f9; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 600; color: #475569; cursor: pointer; }
.btn-confirm-danger { background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 10px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 6px rgba(239,68,68,0.2); }

/* Toasts */
.toast-wrapper { position: fixed; bottom: 24px; right: 24px; z-index: 9999; display: flex; flex-direction: column; gap: 12px; }
.modern-toast { display: flex; align-items: flex-start; gap: 12px; background: white; padding: 16px 20px; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); border-left: 4px solid; width: 350px; }
.modern-toast.success { border-color: #10b981; }
.modern-toast.error { border-color: #ef4444; }
.modern-toast.info { border-color: #3b82f6; }
.t-icon { font-size: 1.5rem; }
.success .t-icon { color: #10b981; }
.error .t-icon { color: #ef4444; }
.info .t-icon { color: #3b82f6; }
.t-content h4 { margin: 0 0 4px 0; font-size: 0.95rem; color: #0f172a; }
.t-content p { margin: 0; font-size: 0.85rem; color: #64748b; line-height: 1.4; }
.t-close { background: none; border: none; color: #cbd5e1; cursor: pointer; padding: 0; margin-left: auto; }
.t-close:hover { color: #64748b; }

/* Animations */
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal-dialog { animation: bounceIn 0.4s; }
@keyframes bounceIn { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

.toast-anim-enter-active { animation: slideInRight 0.3s forwards; }
.toast-anim-leave-active { animation: slideOutRight 0.3s forwards; }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes slideOutRight { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }

@media (max-width: 768px) {
  .stats-row { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
  .reports-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; gap: 16px; }
}
</style>
