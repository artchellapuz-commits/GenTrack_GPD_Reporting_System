<template>
  <AppLayout>
  <div class="approval-queue-container">
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon purple">
          <i class="pi pi-clock"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ validPendingNominations.length }}</div>
          <div class="stat-label">Pending Nominations</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon blue">
          <i class="pi pi-upload"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">0</div>
          <div class="stat-label">Pending Uploads</div>
        </div>
      </div>
    </div>

    <!-- Water Nominations Section -->
    <div class="content-section">
      <div class="section-header">
        <h3><i class="pi pi-calendar"></i> Pending Water Nominations</h3>
      </div>
      
      <div v-if="loading" class="loading-state">
        <i class="pi pi-spin pi-spinner"></i>
        <p>Loading pending items...</p>
      </div>

      <div v-else-if="validPendingNominations.length === 0" class="empty-state">
        <i class="pi pi-check-circle"></i>
        <h3>All Caught Up!</h3>
        <p>No pending nominations to approve</p>
      </div>

      <div v-else class="approval-cards">
        <div v-for="nomination in validPendingNominations" :key="nomination.id" class="approval-card">
          <div class="card-header">
            <div class="card-title">
              <i class="pi pi-calendar"></i>
              <strong>{{ nomination.plant_name }}</strong>
            </div>
            <span class="status-badge pending">Pending Approval</span>
          </div>
          
          <div class="card-body">
            <div class="info-grid">
              <div class="info-item">
                <label>Nomination Date:</label>
                <span>{{ formatDate(nomination.nomination_date) }}</span>
              </div>
              <div class="info-item">
                <label>Type:</label>
                <span>{{ nomination.nomination_type }}</span>
              </div>
              <div class="info-item">
                <label>Submitted By:</label>
                <span>{{ nomination.submitted_by_username }}</span>
              </div>
              <div class="info-item">
                <label>Submitted At:</label>
                <span>{{ formatDateTime(nomination.submitted_at) }}</span>
              </div>
              <div class="info-item full-width">
                <label>Total Nominated:</label>
                <span class="highlight">{{ nomination.total_nominated_mwh }} MWh</span>
              </div>
            </div>
          </div>
          
          <div class="card-actions">
            <button @click="viewDetails(nomination)" class="btn-view">
              <i class="pi pi-eye"></i> View Details
            </button>
            <button @click="rejectNomination(nomination.id)" class="btn-reject">
              <i class="pi pi-times"></i> Reject
            </button>
            <button @click="approveNomination(nomination.id)" class="btn-approve">
              <i class="pi pi-check"></i> Approve
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click.self="showDetailsModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Nomination Details</h3>
          <button @click="showDetailsModal = false" class="btn-close">&times;</button>
        </div>
        
        <div class="modal-body" v-if="selectedNomination">
          <div class="detail-section">
            <h4>Basic Information</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Plant:</label>
                <span>{{ selectedNomination.plant_name }}</span>
              </div>
              <div class="detail-item">
                <label>Date:</label>
                <span>{{ formatDate(selectedNomination.nomination_date) }}</span>
              </div>
              <div class="detail-item">
                <label>Type:</label>
                <span>{{ selectedNomination.nomination_type }}</span>
              </div>
              <div class="detail-item">
                <label>Status:</label>
                <span>{{ selectedNomination.status }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedNomination.hourly_data && selectedNomination.hourly_data.length > 0">
            <h4>Hourly Schedule</h4>
            <div class="hourly-table">
              <table>
                <thead>
                  <tr>
                    <th>Hour</th>
                    <th>Nominated MW</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(hour, index) in selectedNomination.hourly_data.filter(h => h !== null)" :key="index">
                    <td>{{ formatHour(hour.hour) }}</td>
                    <td>{{ hour.nominated_mw }} MW</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div class="detail-section" v-else>
            <h4>Hourly Schedule</h4>
            <p class="no-data">Hourly data not available</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import axios from 'axios';
import AppLayout from './AppLayout.vue';
import { canApproveData } from '../utils/auth';

export default {
  name: 'ApprovalQueue',
  components: {
    AppLayout
  },
  data() {
    return {
      pendingNominations: [],
      loading: false,
      showDetailsModal: false,
      selectedNomination: null
    };
  },
  computed: {
    validPendingNominations() {
      if (!Array.isArray(this.pendingNominations)) {
        return [];
      }
      return this.pendingNominations.filter(n => n !== null && n && n.id);
    }
  },
  mounted() {
    // Check permission
    if (!canApproveData()) {
      alert('You do not have permission to access this page');
      this.$router.push('/dashboard');
      return;
    }
    this.loadPendingItems();
  },
  methods: {
    async loadPendingItems() {
      this.loading = true;
      try {
        // Load pending water nominations
        const response = await axios.get('http://localhost:8000/api/water-nominations/', {
          params: { status: 'SUBMITTED' }
        });
        
        console.log('API Response:', response.data);
        
        // Handle both paginated and non-paginated responses
        if (response.data.results) {
          this.pendingNominations = response.data.results;
        } else if (Array.isArray(response.data)) {
          this.pendingNominations = response.data;
        } else {
          this.pendingNominations = [];
        }
        
        console.log('Pending nominations loaded:', this.pendingNominations.length);
      } catch (error) {
        console.error('Error loading pending items:', error);
        this.pendingNominations = [];
        alert('Failed to load pending items');
      } finally {
        this.loading = false;
      }
    },
    async approveNomination(id) {
      if (!confirm('Are you sure you want to approve this nomination?')) return;
      
      try {
        await axios.post(`http://localhost:8000/api/water-nominations/${id}/approve/`);
        alert('Nomination approved successfully');
        this.loadPendingItems();
      } catch (error) {
        console.error('Error approving nomination:', error);
        const errorMsg = error.response?.data?.error || 'Failed to approve nomination';
        alert(errorMsg);
      }
    },
    async rejectNomination(id) {
      const reason = prompt('Please provide a reason for rejection:');
      if (!reason) return;
      
      try {
        await axios.post(`http://localhost:8000/api/water-nominations/${id}/reject/`, {
          reason: reason
        });
        alert('Nomination rejected');
        this.loadPendingItems();
      } catch (error) {
        console.error('Error rejecting nomination:', error);
        alert('Failed to reject nomination');
      }
    },
    viewDetails(nomination) {
      // Ensure nomination has all required fields with defaults
      this.selectedNomination = {
        ...nomination,
        hourly_data: nomination.hourly_data || []
      };
      this.showDetailsModal = true;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
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
    formatHour(hour) {
      return `${String(hour).padStart(2, '0')}:00`;
    }
  }
};
</script>

<style scoped>
.approval-queue-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  color: white;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.breadcrumb-item {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb-item.active {
  color: white;
  font-weight: 500;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.6);
}

.header-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.header-title-section h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
}

.subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn-icon-header {
  width: 45px;
  height: 45px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.btn-icon-header:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.spin-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-icon.purple { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-icon.blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: #64748b;
  font-size: 0.9rem;
}

.content-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.section-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.loading-state i, .empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-state i {
  color: #10b981;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
}

.approval-cards {
  display: grid;
  gap: 1.5rem;
}

.approval-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.approval-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-header {
  background: #f8fafc;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #1e293b;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.card-body {
  padding: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.info-item span {
  color: #1e293b;
  font-weight: 500;
}

.info-item .highlight {
  color: #667eea;
  font-size: 1.1rem;
  font-weight: 700;
}

.card-actions {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.btn-view, .btn-reject, .btn-approve {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-view {
  background: #f1f5f9;
  color: #475569;
}

.btn-view:hover {
  background: #e2e8f0;
}

.btn-reject {
  background: #fee2e2;
  color: #991b1b;
}

.btn-reject:hover {
  background: #fecaca;
}

.btn-approve {
  background: #10b981;
  color: white;
}

.btn-approve:hover {
  background: #059669;
}

/* Modal Styles */
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
  border-radius: 16px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1e293b;
}

.btn-close {
  width: 36px;
  height: 36px;
  border: none;
  background: #f1f5f9;
  border-radius: 8px;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.modal-body {
  padding: 1.5rem;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section h4 {
  margin: 0 0 1rem 0;
  color: #1e293b;
  font-size: 1.1rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.detail-item span {
  color: #1e293b;
  font-weight: 500;
}

.hourly-table {
  overflow-x: auto;
}

.hourly-table table {
  width: 100%;
  border-collapse: collapse;
}

.hourly-table th,
.hourly-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.hourly-table th {
  background: #f8fafc;
  color: #64748b;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
}

.hourly-table td {
  color: #1e293b;
}

.hourly-table tr:hover {
  background: #f8fafc;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-style: italic;
}

@media (max-width: 768px) {
  .approval-queue-container {
    padding: 1rem;
  }

  .page-header {
    padding: 1.5rem;
  }

  .header-title-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-title-section h1 {
    font-size: 1.5rem;
  }

  .icon-wrapper {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .btn-view, .btn-reject, .btn-approve {
    width: 100%;
    justify-content: center;
  }
}
</style>
