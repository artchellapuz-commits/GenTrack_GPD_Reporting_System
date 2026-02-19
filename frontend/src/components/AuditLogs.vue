<template>
  <AppLayout>
  <div class="audit-logs-container">
    <!-- Filters -->
    <div class="content-section">
      <div class="filters-card">
        <div class="filters-grid">
          <div class="filter-group">
            <label>Action Type</label>
            <select v-model="filters.action">
              <option value="">All Actions</option>
              <option value="CREATE">Create</option>
              <option value="UPDATE">Update</option>
              <option value="DELETE">Delete</option>
              <option value="UPLOAD">Upload</option>
              <option value="EXPORT">Export</option>
              <option value="APPROVE">Approve</option>
              <option value="REJECT">Reject</option>
              <option value="LOGIN">Login</option>
              <option value="LOGOUT">Logout</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>User</label>
            <input type="text" v-model="filters.username" placeholder="Search by username">
          </div>
          
          <div class="filter-group">
            <label>Date From</label>
            <input type="date" v-model="filters.date_from">
          </div>
          
          <div class="filter-group">
            <label>Date To</label>
            <input type="date" v-model="filters.date_to">
          </div>
          
          <div class="filter-actions">
            <button @click="clearFilters" class="btn-secondary">
              <i class="pi pi-times"></i> Clear
            </button>
            <button @click="loadLogs" class="btn-primary">
              <i class="pi pi-search"></i> Search
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Audit Logs Table -->
    <div class="content-section">
      <div v-if="loading" class="loading-state">
        <i class="pi pi-spin pi-spinner"></i>
        <p>Loading audit logs...</p>
      </div>

      <div v-else-if="logs.length === 0" class="empty-state">
        <i class="pi pi-inbox"></i>
        <h3>No Audit Logs Found</h3>
        <p>No activities match your search criteria</p>
      </div>

      <div v-else class="table-container">
        <table class="audit-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>User</th>
              <th>Action</th>
              <th>Model</th>
              <th>Description</th>
              <th>IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id">
              <td>{{ formatDateTime(log.timestamp) }}</td>
              <td>
                <div class="user-cell">
                  <i class="pi pi-user"></i>
                  {{ log.user ? log.user.username : 'System' }}
                </div>
              </td>
              <td>
                <span :class="['action-badge', getActionClass(log.action)]">
                  {{ log.action }}
                </span>
              </td>
              <td>{{ log.model_name }}</td>
              <td class="description-cell">{{ log.description }}</td>
              <td>{{ log.ip_address || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import axios from 'axios';
import AppLayout from './AppLayout.vue';

export default {
  name: 'AuditLogs',
  components: {
    AppLayout
  },
  data() {
    return {
      logs: [],
      loading: false,
      filters: {
        action: '',
        username: '',
        date_from: '',
        date_to: ''
      }
    };
  },
  mounted() {
    this.loadLogs();
  },
  methods: {
    async loadLogs() {
      this.loading = true;
      try {
        const params = {};
        if (this.filters.action) params.action = this.filters.action;
        if (this.filters.username) params.username = this.filters.username;
        if (this.filters.date_from) params.date_from = this.filters.date_from;
        if (this.filters.date_to) params.date_to = this.filters.date_to;

        const response = await axios.get('http://localhost:8000/api/audit-logs/', { params });
        this.logs = response.data.results || response.data || [];
      } catch (error) {
        console.error('Error loading audit logs:', error);
        alert('Failed to load audit logs');
        this.logs = [];
      } finally {
        this.loading = false;
      }
    },
    clearFilters() {
      this.filters = {
        action: '',
        username: '',
        date_from: '',
        date_to: ''
      };
      this.loadLogs();
    },
    formatDateTime(datetime) {
      return new Date(datetime).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    getActionClass(action) {
      const classes = {
        'CREATE': 'success',
        'UPDATE': 'info',
        'DELETE': 'danger',
        'UPLOAD': 'primary',
        'EXPORT': 'secondary',
        'APPROVE': 'success',
        'REJECT': 'danger',
        'LOGIN': 'info',
        'LOGOUT': 'warning'
      };
      return classes[action] || 'secondary';
    }
  }
};
</script>

<style scoped>
.audit-logs-container {
  padding: 0;
  max-width: 100%;
  margin: 0;
  background: #f8fafc;
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px 40px;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 4px;
}

.breadcrumb-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.breadcrumb-item.active {
  color: white;
  font-weight: 600;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

.header-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  color: white;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.subtitle {
  margin: 5px 0 0 0;
  opacity: 0.9;
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-icon-header {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.3s ease;
}

.btn-icon-header:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.spin-icon i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.content-section {
  max-width: 1400px;
  margin: 0 auto 30px;
  padding: 0 40px;
}

.filters-card {
  background: white;
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #334155;
}

.filter-group input,
.filter-group select {
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.btn-primary, .btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #e2e8f0;
  color: #475569;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.loading-state i, .empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  color: #cbd5e1;
}

.table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.audit-table {
  width: 100%;
  border-collapse: collapse;
}

.audit-table thead {
  background: #f8fafc;
}

.audit-table th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  font-size: 0.9rem;
  border-bottom: 2px solid #e2e8f0;
}

.audit-table td {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.9rem;
  color: #334155;
}

.audit-table tbody tr:hover {
  background: #f8fafc;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.action-badge.success {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}

.action-badge.info {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.action-badge.danger {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.action-badge.warning {
  background: rgba(251, 146, 60, 0.1);
  color: #ea580c;
}

.action-badge.primary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.action-badge.secondary {
  background: rgba(100, 116, 139, 0.1);
  color: #475569;
}

.description-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
