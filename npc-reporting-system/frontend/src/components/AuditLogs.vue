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
              <option value="LOGIN">Login</option>
              <option value="LOGOUT">Logout</option>
              <option value="CREATE">Create / Request</option>
              <option value="UPDATE">Update</option>
              <option value="DELETE">Delete</option>
              <option value="UPLOAD">Upload</option>
              <option value="GENERATE">Generate Report</option>
              <option value="EXPORT">Export</option>
              <option value="ARCHIVE">Archive</option>
              <option value="APPROVE">Approve</option>
              <option value="REJECT">Reject</option>
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
            <button @click="exportLogs" class="btn-export">
              <i class="pi pi-download"></i> Export
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

      <div v-else class="table-wrapper">
        <!-- Table Header with Entries Selector -->
        <div class="table-header">
          <div class="entries-selector">
            <label>Show</label>
            <select v-model.number="entriesPerPage" @change="changeEntriesPerPage" class="entries-dropdown">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
            </select>
            <label>entries</label>
          </div>
        </div>

        <!-- Table -->
        <div class="table-container">
          <table class="audit-table">
            <thead>
              <tr>
                <th class="sortable" @click="sortBy('timestamp')">
                  Timestamp
                  <i :class="['pi', getSortIcon('timestamp'), 'sort-icon']"></i>
                </th>
                <th class="sortable" @click="sortBy('user')">
                  User
                  <i :class="['pi', getSortIcon('user'), 'sort-icon']"></i>
                </th>
                <th class="sortable" @click="sortBy('action')">
                  Action
                  <i :class="['pi', getSortIcon('action'), 'sort-icon']"></i>
                </th>
                <th class="sortable" @click="sortBy('model')">
                  Model
                  <i :class="['pi', getSortIcon('model'), 'sort-icon']"></i>
                </th>
                <th class="sortable" @click="sortBy('description')">
                  Description
                  <i :class="['pi', getSortIcon('description'), 'sort-icon']"></i>
                </th>
                <th class="sortable nowrap" @click="sortBy('ip_address')">
                  IP Address
                  <i :class="['pi', getSortIcon('ip_address'), 'sort-icon']"></i>
                </th>
                <th class="sortable" @click="sortBy('location')">
                  Location
                  <i :class="['pi', getSortIcon('location'), 'sort-icon']"></i>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in sortedLogs" :key="log.id">
                <td>{{ formatDateTime(log.timestamp) }}</td>
                <td>
                  <div class="user-cell">
                    <i class="pi pi-user"></i>
                    <div class="user-info">
                      <div class="user-name">{{ log.user_full_name || 'System' }}</div>
                      <div class="user-role" v-if="log.user_role">{{ log.user_role }}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span :class="['action-badge', getActionClass(log.action)]">
                    {{ log.action_display || log.action }}
                  </span>
                </td>
                <td>{{ log.model_display_name || log.model_name || 'N/A' }}</td>
                <td class="description-cell">{{ log.description }}</td>
                <td>{{ log.ip_address || 'N/A' }}</td>
                <td>
                  <div class="location-cell">
                    <i class="pi pi-map-marker"></i>
                    {{ log.location_display || 'Internal Network' }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <Paginator 
          :rows="entriesPerPage" 
          :totalRecords="totalEntries" 
          :first="(currentPage - 1) * entriesPerPage"
          @page="onPageChange($event)"
          template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
          :pageLinkSize="5"
        />
      </div>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import axios from 'axios';
import AppLayout from './AppLayout.vue';
import Paginator from 'primevue/paginator';

export default {
  name: 'AuditLogs',
  components: {
    AppLayout,
    Paginator
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
      },
      // Pagination
      currentPage: 1,
      entriesPerPage: 10,
      totalEntries: 0,
      // Sorting
      sortField: 'timestamp',
      sortOrder: -1, // -1 for descending, 1 for ascending
      refreshInterval: null
    };
  },
  computed: {
    sortedLogs() {
      return [...this.logs].sort((a, b) => {
        let aVal, bVal;
        
        switch(this.sortField) {
          case 'timestamp':
            aVal = new Date(a.timestamp);
            bVal = new Date(b.timestamp);
            break;
          case 'user':
            aVal = (a.user_full_name || 'System').toLowerCase();
            bVal = (b.user_full_name || 'System').toLowerCase();
            break;
          case 'action':
            aVal = (a.action_display || a.action || '').toLowerCase();
            bVal = (b.action_display || b.action || '').toLowerCase();
            break;
          case 'model':
            aVal = (a.model_display_name || a.model_name || '').toLowerCase();
            bVal = (b.model_display_name || b.model_name || '').toLowerCase();
            break;
          case 'description':
            aVal = a.description?.toLowerCase() || '';
            bVal = b.description?.toLowerCase() || '';
            break;
          case 'ip_address':
            aVal = a.ip_address || '';
            bVal = b.ip_address || '';
            break;
          case 'location':
            aVal = (a.location_display || '').toLowerCase();
            bVal = (b.location_display || '').toLowerCase();
            break;
          default:
            return 0;
        }
        
        if (aVal < bVal) return -1 * this.sortOrder;
        if (aVal > bVal) return 1 * this.sortOrder;
        return 0;
      });
    },
    totalPages() {
      return Math.ceil(this.totalEntries / this.entriesPerPage);
    },
    startEntry() {
      return this.logs.length === 0 ? 0 : (this.currentPage - 1) * this.entriesPerPage + 1;
    },
    endEntry() {
      return Math.min(this.currentPage * this.entriesPerPage, this.totalEntries);
    }
  },
  mounted() {
    this.loadLogs();
    // Auto-refresh every 30 seconds
    this.refreshInterval = setInterval(() => {
      this.loadLogs(true); // Pass true to indicate background refresh
    }, 30000);
  },
  beforeUnmount() {
    // Clear interval when component is destroyed to prevent memory leaks
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  methods: {
    sortBy(field) {
      if (this.sortField === field) {
        // Toggle sort order if clicking the same field
        this.sortOrder = this.sortOrder * -1;
      } else {
        // Set new field and default to ascending
        this.sortField = field;
        this.sortOrder = 1;
      }
    },
    
    getSortIcon(field) {
      if (this.sortField !== field) {
        return 'pi-sort-alt'; // Neutral sort icon
      }
      return this.sortOrder === 1 ? 'pi-sort-amount-up' : 'pi-sort-amount-down';
    },
    
    async loadLogs(isBackgroundRefresh = false) {
      // Only show loading spinner if it's not a background refresh
      if (!isBackgroundRefresh) {
        this.loading = true;
      }
      
      try {
        const params = {
          page: this.currentPage,
          page_size: this.entriesPerPage
        };
        if (this.filters.action) params.action = this.filters.action;
        if (this.filters.username) params.username = this.filters.username;
        if (this.filters.date_from) params.date_from = this.filters.date_from;
        if (this.filters.date_to) params.date_to = this.filters.date_to;

        const response = await axios.get('http://localhost:8000/api/audit-logs/', { params });
        
        // Handle paginated response
        if (response.data.results) {
          this.logs = response.data.results;
          this.totalEntries = response.data.count || 0;
        } else {
          // Fallback for non-paginated response
          this.logs = response.data || [];
          this.totalEntries = this.logs.length;
        }
      } catch (error) {
        console.error('Error loading audit logs:', error);
        if (!isBackgroundRefresh) {
          alert('Failed to load audit logs');
        }
        // Don't clear existing logs on background refresh failure
        if (!isBackgroundRefresh) {
          this.logs = [];
          this.totalEntries = 0;
        }
      } finally {
        if (!isBackgroundRefresh) {
          this.loading = false;
        }
      }
    },
    onPageChange(event) {
      this.currentPage = event.page + 1; // PrimeVue uses 0-based index
      this.loadLogs();
    },
    changeEntriesPerPage() {
      this.currentPage = 1; // Reset to first page
      this.loadLogs();
    },
    clearFilters() {
      this.filters = {
        action: '',
        username: '',
        date_from: '',
        date_to: ''
      };
      this.currentPage = 1;
      this.loadLogs();
    },
    async exportLogs() {
      try {
        const params = {};
        if (this.filters.action) params.action = this.filters.action;
        if (this.filters.username) params.username = this.filters.username;
        if (this.filters.date_from) params.start_date = this.filters.date_from;
        if (this.filters.date_to) params.end_date = this.filters.date_to;

        const queryString = new URLSearchParams(params).toString();
        const url = `http://localhost:8000/api/audit-logs/export/?${queryString}`;
        
        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = `Audit_Logs_${new Date().toISOString().split('T')[0]}.xlsx`;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        alert('Audit logs exported successfully!');
      } catch (error) {
        console.error('Error exporting audit logs:', error);
        alert('Failed to export audit logs');
      }
    },
    formatDateTime(datetime) {
      return new Date(datetime).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
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
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  align-items: end;
}

@media (max-width: 1200px) {
  .filters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
  }
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
  flex-wrap: wrap;
  grid-column: 1 / -1;
  justify-content: flex-end;
  margin-top: 10px;
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
  white-space: nowrap;
  flex-shrink: 0;
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

.btn-export {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  background: #00a651;
  color: white;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-export:hover {
  background: #008a42;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
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

/* Sortable Table Headers */
.audit-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  position: relative;
}

.audit-table th.sortable.nowrap {
  white-space: nowrap;
}

.audit-table th.sortable:hover {
  background-color: #e2e8f0;
}

.audit-table th .sort-icon {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 6px;
  transition: color 0.2s ease;
  display: inline-block;
  vertical-align: middle;
}

.audit-table th.sortable:hover .sort-icon {
  color: #64748b;
}

.audit-table th .pi-sort-amount-up,
.audit-table th .pi-sort-amount-down {
  color: #667eea;
  font-weight: bold;
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

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  color: #1e293b;
}

.user-role {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 2px;
}

.location-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
}

.location-cell i {
  color: #667eea;
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

/* Table Wrapper */
.table-wrapper {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Table Header with Entries Selector */
.table-header {
  padding: 20px 25px;
  border-bottom: 1px solid #f1f5f9;
  background: #fafbfc;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.entries-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: #475569;
}

.entries-selector label {
  font-weight: 500;
}

.entries-dropdown {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.entries-dropdown:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.entries-dropdown:hover {
  border-color: #cbd5e1;
}

/* Sakai-Style Pagination */
:deep(.p-paginator) {
  background: white;
  border-top: 1px solid #e2e8f0;
  padding: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

:deep(.p-paginator .p-paginator-first),
:deep(.p-paginator .p-paginator-prev),
:deep(.p-paginator .p-paginator-next),
:deep(.p-paginator .p-paginator-last),
:deep(.p-paginator .p-paginator-page) {
  min-width: 2.5rem;
  height: 2.5rem;
  margin: 0.125rem;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #64748b;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
}

:deep(.p-paginator .p-paginator-first:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-prev:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-next:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-last:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-page:not(.p-highlight):hover) {
  background: #f1f5f9;
  color: #667eea;
}

:deep(.p-paginator .p-paginator-page.p-highlight) {
  background: #667eea;
  color: white;
  font-weight: 600;
}

:deep(.p-paginator .p-disabled) {
  opacity: 0.4;
  cursor: not-allowed;
}

:deep(.p-paginator .p-paginator-icon) {
  font-size: 0.875rem;
}

/* Rows Per Page Dropdown */
:deep(.p-paginator .p-dropdown) {
  margin-left: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  height: 2.5rem;
  min-width: 4rem;
}

:deep(.p-paginator .p-dropdown:hover) {
  border-color: #667eea;
}

:deep(.p-paginator .p-dropdown .p-dropdown-label) {
  padding: 0.5rem;
  font-size: 0.9rem;
}

:deep(.p-paginator .p-dropdown-trigger) {
  width: 2rem;
}

/* Dropdown Panel */
:deep(.p-dropdown-panel) {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-top: 4px;
}

:deep(.p-dropdown-items) {
  padding: 0.25rem 0;
}

:deep(.p-dropdown-item) {
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #475569;
}

:deep(.p-dropdown-item:hover) {
  background: #f1f5f9;
  color: #667eea;
}

:deep(.p-dropdown-item.p-highlight) {
  background: #667eea;
  color: white;
}
</style>
