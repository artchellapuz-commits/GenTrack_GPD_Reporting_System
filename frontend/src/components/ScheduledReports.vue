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
              <option value="GENERATION_SUMMARY">Generation Summary</option>
              <option value="CAPACITY_FACTOR">Capacity Factor Analysis</option>
              <option value="AVAILABILITY">Availability Report</option>
              <option value="PERFORMANCE_METRICS">Performance Metrics</option>
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
    </div>
  </AppLayout>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AppLayout from './AppLayout.vue';

export default {
  name: 'ScheduledReports',
  setup() {
    const scheduledReports = ref([]);
    const showCreateDialog = ref(false);
    const editingReport = ref(null);
    const formData = ref({
      name: '',
      report_type: 'GENERATION_SUMMARY',
      frequency: 'DAILY',
      schedule_time: '08:00',
      format: 'EXCEL',
      date_range_days: 30
    });

    const loadReports = async () => {
      try {
        const response = await axios.get('/api/scheduled-reports/');
        // Ensure response.data is an array
        const data = Array.isArray(response.data) ? response.data : [];
        // Ensure each report has required fields
        scheduledReports.value = data.map(report => ({
          id: report.id || null,
          name: report.name || 'Unnamed Report',
          report_type: report.report_type || 'GENERATION_SUMMARY',
          report_type_display: report.report_type_display || 'Generation Summary',
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
      } catch (error) {
        console.error('Failed to load reports:', error);
        // Set empty array on error
        scheduledReports.value = [];
      }
    };

    const saveReport = async () => {
      try {
        if (editingReport.value) {
          await axios.put(`/api/scheduled-reports/${editingReport.value.id}/`, formData.value);
        } else {
          await axios.post('/api/scheduled-reports/', formData.value);
        }
        showCreateDialog.value = false;
        loadReports();
      } catch (error) {
        console.error('Failed to save report:', error);
        alert('Failed to save report. Please check if the backend API is running.');
      }
    };

    const toggleStatus = async (report) => {
      if (!report || !report.id) {
        console.error('Invalid report object');
        return;
      }
      try {
        const newStatus = report.status === 'ACTIVE' ? 'PAUSED' : 'ACTIVE';
        await axios.patch(`/api/scheduled-reports/${report.id}/`, { status: newStatus });
        loadReports();
      } catch (error) {
        console.error('Failed to toggle status:', error);
        alert('Failed to update report status. Please check if the backend API is running.');
      }
    };

    const runNow = async (report) => {
      if (!report || !report.id) {
        console.error('Invalid report object');
        return;
      }
      try {
        await axios.post(`/api/scheduled-reports/${report.id}/run/`);
        alert('Report execution started');
      } catch (error) {
        console.error('Failed to run report:', error);
        alert('Failed to run report. Please check if the backend API is running.');
      }
    };

    const editReport = (report) => {
      if (!report) {
        console.error('Invalid report object');
        return;
      }
      editingReport.value = report;
      formData.value = {
        name: report.name || '',
        report_type: report.report_type || 'GENERATION_SUMMARY',
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
        const response = await axios.get(`/api/scheduled-reports/${report.id}/executions/`);
        console.log('Executions:', response.data);
        // You can show this in a modal or navigate to a new page
        const count = Array.isArray(response.data) ? response.data.length : 0;
        alert(`Report has ${count} executions. Check console for details.`);
      } catch (error) {
        console.error('Failed to load executions:', error);
        alert('Failed to load execution history. Please check if the backend API is running.');
      }
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
      editingReport,
      formData,
      saveReport,
      toggleStatus,
      runNow,
      editReport,
      viewExecutions,
      formatDate
    };
  },
  components: {
    AppLayout
  }
};
</script>

<style scoped>
.scheduled-reports {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.reports-list {
  display: grid;
  gap: 20px;
}

.report-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
}

.report-header h3 {
  margin: 0 0 5px 0;
  color: #1e293b;
}

.report-type {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.active {
  background: #dcfce7;
  color: #16a34a;
}

.status-badge.paused {
  background: #fef3c7;
  color: #d97706;
}

.status-badge.unknown {
  background: #f1f5f9;
  color: #64748b;
}

.report-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 0.9rem;
}

.detail-item i {
  color: #3b82f6;
}

.report-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-primary, .btn-secondary {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #1e293b;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}
</style>
