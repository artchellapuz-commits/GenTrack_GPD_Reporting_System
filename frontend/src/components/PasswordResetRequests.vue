<template>
  <AppLayout>
    <div class="password-reset-requests">
      <!-- Page Header -->
      <div class="page-header">
        <h1>Password Reset Requests</h1>
        <button @click="loadRequests" class="btn-primary" :disabled="loading">
          <i class="pi" :class="loading ? 'pi-spin pi-spinner' : 'pi-refresh'"></i>
          <span>Refresh</span>
        </button>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon orange">
            <i class="pi pi-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.pending }}</div>
            <div class="stat-label">Pending</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon green">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.approved }}</div>
            <div class="stat-label">Approved</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon red">
            <i class="pi pi-times-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.rejected }}</div>
            <div class="stat-label">Rejected</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon blue">
            <i class="pi pi-check"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.completed }}</div>
            <div class="stat-label">Completed</div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filter-left">
          <div class="show-entries">
            <span>Show:</span>
            <select v-model.number="itemsPerPage" @change="changeItemsPerPage">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
            </select>
            <span>entries</span>
          </div>
        </div>
        
        <div class="filter-right">
          <div class="filter-group">
            <label>Search</label>
            <input 
              type="text" 
              v-model="filters.search" 
              @input="debounceSearch"
              placeholder="Search by username..."
              class="search-input"
            >
          </div>
          
          <div class="filter-group">
            <label>Status</label>
            <select v-model="filters.status" @change="loadRequests">
              <option value="">All Status</option>
              <option value="PENDING">Pending</option>
              <option value="APPROVED">Approved</option>
              <option value="REJECTED">Rejected</option>
              <option value="COMPLETED">Completed</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Requests Table -->
      <div class="table-container">
        <div v-if="loading" class="loading-state">
          <i class="pi pi-spin pi-spinner"></i> Loading requests...
        </div>

        <table v-else-if="requests.length > 0" class="requests-table">
          <thead>
            <tr>
              <th class="sortable" @click="sortBy('username')">
                Username
                <i :class="['pi', getSortIcon('username'), 'sort-icon']"></i>
              </th>
              <th class="sortable" @click="sortBy('reason')">
                Reason
                <i :class="['pi', getSortIcon('reason'), 'sort-icon']"></i>
              </th>
              <th class="sortable" @click="sortBy('status')">
                Status
                <i :class="['pi', getSortIcon('status'), 'sort-icon']"></i>
              </th>
              <th class="sortable" @click="sortBy('created_at')">
                Requested
                <i :class="['pi', getSortIcon('created_at'), 'sort-icon']"></i>
              </th>
              <th class="sortable nowrap" @click="sortBy('ip_address')">
                IP Address
                <i :class="['pi', getSortIcon('ip_address'), 'sort-icon']"></i>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="request in paginatedRequests" 
              :key="request.id"
              :id="`request-row-${request.id}`"
              :class="{ 'highlighted-row': highlightedRequestId === request.id }"
            >
              <td>
                <div class="user-info">
                  <i class="pi pi-user"></i>
                  <span>{{ request.username }}</span>
                </div>
              </td>
              <td>{{ request.reason || 'No reason provided' }}</td>
              <td>
                <span class="status-badge" :class="getStatusClass(request.status)">
                  {{ request.status || 'N/A' }}
                </span>
              </td>
              <td>{{ formatDate(request.created_at) }}</td>
              <td>{{ request.ip_address || 'N/A' }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="viewRequest(request)" class="btn-icon btn-view" title="View">
                    <i class="pi pi-eye"></i>
                  </button>
                  <button 
                    v-if="request.status === 'PENDING'"
                    @click="openApproveModal(request)" 
                    class="btn-icon btn-approve" 
                    title="Approve"
                  >
                    <i class="pi pi-check"></i>
                  </button>
                  <button 
                    v-if="request.status === 'PENDING'"
                    @click="openRejectModal(request)" 
                    class="btn-icon btn-reject" 
                    title="Reject"
                  >
                    <i class="pi pi-times"></i>
                  </button>
                  <button 
                    v-if="request.status === 'APPROVED'"
                    @click="openResetModal(request)" 
                    class="btn-icon btn-reset" 
                    title="Reset Password"
                  >
                    <i class="pi pi-key"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- y -->
        <Paginator 
          v-if="requests.length > 0"
          :rows="itemsPerPage" 
          :totalRecords="requests.length" 
          :first="(currentPage - 1) * itemsPerPage"
          @page="onPageChange($event)"
          template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
          :pageLinkSize="5"
        />

        <div v-else class="empty-state">
          <i class="pi pi-inbox"></i>
          <p>No password reset requests found</p>
        </div>
      </div>

      <!-- Detail Modal -->
      <div v-if="selectedRequest" class="modal-overlay" @click.self="selectedRequest = null">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Request Details</h3>
            <button @click="selectedRequest = null" class="btn-close">&times;</button>
          </div>

          <div class="modal-body">
            <div class="detail-grid">
              <div class="detail-item">
                <label>Username</label>
                <div class="detail-value">
                  <i class="pi pi-user"></i>
                  {{ selectedRequest.username }}
                </div>
              </div>
              
              <div class="detail-item">
                <label>Status</label>
                <span class="status-badge" :class="getStatusClass(selectedRequest.status)">
                  {{ selectedRequest.status || 'N/A' }}
                </span>
              </div>
              
              <div class="detail-item full-width">
                <label>Reason</label>
                <div class="detail-value">
                  {{ selectedRequest.reason || 'No reason provided' }}
                </div>
              </div>
              
              <div class="detail-item">
                <label>IP Address</label>
                <div class="detail-value">
                  <i class="pi pi-map-marker"></i>
                  {{ selectedRequest.ip_address || 'N/A' }}
                </div>
              </div>
              
              <div class="detail-item">
                <label>Requested At</label>
                <div class="detail-value">
                  <i class="pi pi-calendar"></i>
                  {{ formatDateTime(selectedRequest.created_at) }}
                </div>
              </div>
              
              <div class="detail-item" v-if="selectedRequest.processed_by_username">
                <label>Processed By</label>
                <div class="detail-value">
                  <i class="pi pi-user"></i>
                  {{ selectedRequest.processed_by_username }}
                </div>
              </div>
              
              <div class="detail-item" v-if="selectedRequest.processed_at">
                <label>Processed At</label>
                <div class="detail-value">
                  <i class="pi pi-calendar"></i>
                  {{ formatDateTime(selectedRequest.processed_at) }}
                </div>
              </div>
              
              <div class="detail-item full-width" v-if="selectedRequest.admin_notes">
                <label>Admin Notes</label>
                <div class="detail-value">
                  {{ selectedRequest.admin_notes }}
                </div>
              </div>
            </div>
            
            <div class="modal-actions">
              <button 
                v-if="selectedRequest.status === 'PENDING'"
                @click="openApproveModal(selectedRequest)" 
                class="btn-primary"
              >
                <i class="pi pi-check"></i>
                Approve Request
              </button>
              <button 
                v-if="selectedRequest.status === 'PENDING'"
                @click="openRejectModal(selectedRequest)" 
                class="btn-danger"
              >
                <i class="pi pi-times"></i>
                Reject Request
              </button>
              <button 
                v-if="selectedRequest.status === 'APPROVED'"
                @click="openResetModal(selectedRequest)" 
                class="btn-primary"
              >
                <i class="pi pi-key"></i>
                Reset Password
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Approve Modal -->
      <div v-if="showApproveModal" class="modal-overlay" @click.self="closeModals">
        <div class="action-modal">
          <div class="modal-header">
            <h3>Approve Password Reset Request</h3>
            <button @click="closeModals" class="btn-close">&times;</button>
          </div>
          <div class="modal-body">
            <p>Approve password reset request for <strong>{{ actionRequest?.username }}</strong>?</p>
            <p class="modal-note">This will mark the request as approved. You can then reset the password.</p>
          </div>
          <div class="modal-footer">
            <button @click="closeModals" class="btn-secondary">Cancel</button>
            <button @click="approveRequest" class="btn-primary">
              <i class="pi pi-check"></i>
              Approve
            </button>
          </div>
        </div>
      </div>

      <!-- Reject Modal -->
      <div v-if="showRejectModal" class="modal-overlay" @click.self="closeModals">
        <div class="action-modal">
          <div class="modal-header">
            <h3>Reject Password Reset Request</h3>
            <button @click="closeModals" class="btn-close">&times;</button>
          </div>
          <div class="modal-body">
            <p>Reject password reset request for <strong>{{ actionRequest?.username }}</strong>?</p>
            <div class="form-group">
              <label>Enter rejection reason (optional):</label>
              <textarea 
                v-model="rejectReason" 
                placeholder="Enter reason for rejection..."
                rows="4"
                class="form-textarea"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeModals" class="btn-secondary">Cancel</button>
            <button @click="rejectRequest" class="btn-danger">
              <i class="pi pi-times"></i>
              Reject
            </button>
          </div>
        </div>
      </div>

      <!-- Reset Password Modal -->
      <div v-if="showResetModal" class="modal-overlay" @click.self="resetPasswordData ? null : closeModals">
        <div class="action-modal reset-modal">
          <div class="modal-header">
            <h3>{{ resetPasswordData ? 'Password Reset Successful' : 'Reset Password' }}</h3>
            <button @click="closeResetModal" class="btn-close">&times;</button>
          </div>
          <div class="modal-body">
            <div v-if="!resetPasswordData">
              <p>Reset password for <strong>{{ actionRequest?.username }}</strong>?</p>
              <p class="modal-note">A new temporary password will be generated and sent to the user's email if available.</p>
            </div>
            <div v-else class="password-result">
              <div class="success-message">
                <i class="pi pi-check-circle"></i>
                <p>Password reset successfully for <strong>{{ resetPasswordData.username }}</strong></p>
              </div>
              
              <div class="password-display">
                <label>New Temporary Password:</label>
                <div class="password-box">
                  <code>{{ resetPasswordData.new_password }}</code>
                  <button @click="copyPassword" class="btn-copy" title="Copy">
                    <i class="pi pi-copy"></i>
                  </button>
                </div>
              </div>

              <div class="email-status">
                <div v-if="resetPasswordData.email_sent && resetPasswordData.user_email" class="status-success">
                  <i class="pi pi-check-circle"></i>
                  <span>Password sent to: {{ resetPasswordData.user_email }}</span>
                </div>
                <div v-else-if="resetPasswordData.user_email" class="status-warning">
                  <i class="pi pi-exclamation-triangle"></i>
                  <span>Email failed to send to: {{ resetPasswordData.user_email }}</span>
                </div>
                <div v-else class="status-warning">
                  <i class="pi pi-exclamation-triangle"></i>
                  <span>No email on file for this user</span>
                </div>
              </div>

              <p class="modal-note">Please provide this password to the user securely.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button v-if="!resetPasswordData" @click="closeModals" class="btn-secondary">Cancel</button>
            <button v-if="!resetPasswordData" @click="resetPassword" class="btn-primary">
              <i class="pi pi-key"></i>
              Reset Password
            </button>
            <button v-if="resetPasswordData" @click="closeResetModal" class="btn-primary">
              <i class="pi pi-check"></i>
              Done
            </button>
          </div>
        </div>
      </div>

      <!-- Success Modal -->
      <div v-if="showSuccessModal" class="modal-overlay" @click.self="closeModals">
        <div class="action-modal success-modal">
          <div class="modal-header">
            <h3>Success</h3>
            <button @click="closeModals" class="btn-close">&times;</button>
          </div>
          <div class="modal-body">
            <div class="success-content">
              <i class="pi pi-check-circle"></i>
              <p>{{ successMessage }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeModals" class="btn-primary">
              OK
            </button>
          </div>
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
  name: 'PasswordResetRequests',
  components: {
    AppLayout,
    Paginator
  },
  data() {
    return {
      requests: [],
      selectedRequest: null,
      loading: false,
      filters: {
        status: '',
        search: ''
      },
      stats: {
        pending: 0,
        approved: 0,
        rejected: 0,
        completed: 0
      },
      searchTimeout: null,
      // Pagination
      currentPage: 1,
      itemsPerPage: 10,
      // Sorting
      sortField: 'created_at',
      sortOrder: -1, // -1 for descending, 1 for ascending
      // Modal states
      showApproveModal: false,
      showRejectModal: false,
      showResetModal: false,
      showSuccessModal: false,
      actionRequest: null,
      rejectReason: '',
      resetPasswordData: null,
      successMessage: '',
      // Highlight state
      highlightedRequestId: null
    };
  },
  created() {
    this.loadRequests();
  },
  mounted() {
    // Check if there's a highlight query parameter
    const highlightId = this.$route.query.highlight;
    if (highlightId) {
      this.highlightedRequestId = parseInt(highlightId);
      // Wait for data to load and DOM to update
      this.$nextTick(() => {
        setTimeout(() => {
          this.scrollToHighlightedRow();
        }, 500);
      });
    }
  },
  computed: {
    paginatedRequests() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedRequests.slice(start, end);
    },
    sortedRequests() {
      return [...this.requests].sort((a, b) => {
        let aVal, bVal;
        
        switch(this.sortField) {
          case 'username':
            aVal = a.username?.toLowerCase() || '';
            bVal = b.username?.toLowerCase() || '';
            break;
          case 'reason':
            aVal = a.reason?.toLowerCase() || '';
            bVal = b.reason?.toLowerCase() || '';
            break;
          case 'status':
            aVal = a.status?.toLowerCase() || '';
            bVal = b.status?.toLowerCase() || '';
            break;
          case 'created_at':
            aVal = new Date(a.created_at);
            bVal = new Date(b.created_at);
            break;
          case 'ip_address':
            aVal = a.ip_address || '';
            bVal = b.ip_address || '';
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
      return Math.ceil(this.requests.length / this.itemsPerPage);
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
      this.currentPage = 1; // Reset to first page when sorting
    },
    
    getSortIcon(field) {
      if (this.sortField !== field) {
        return 'pi-sort-alt'; // Neutral sort icon
      }
      return this.sortOrder === 1 ? 'pi-sort-amount-up' : 'pi-sort-amount-down';
    },
    
    async loadRequests() {
      this.loading = true;
      try {
        const params = {};
        if (this.filters.status) params.status = this.filters.status;
        if (this.filters.search) params.search = this.filters.search;
        
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/password-reset-requests/`,
          { 
            params,
            headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
          }
        );
        
        if (Array.isArray(response.data)) {
          this.requests = response.data;
        } else if (response.data && Array.isArray(response.data.results)) {
          this.requests = response.data.results;
        } else {
          this.requests = [];
        }
        
        this.calculateStats();
        this.currentPage = 1; // Reset to first page on new data
        
        // Trigger highlight scroll after data is loaded
        if (this.highlightedRequestId) {
          this.$nextTick(() => {
            setTimeout(() => {
              this.scrollToHighlightedRow();
            }, 300);
          });
        }
      } catch (error) {
        console.error('Error loading requests:', error);
        this.requests = [];
        this.calculateStats();
        alert('Failed to load password reset requests. Please try again.');
      } finally {
        this.loading = false;
      }
    },
    
    calculateStats() {
      if (!Array.isArray(this.requests)) {
        this.stats = { pending: 0, approved: 0, rejected: 0, completed: 0 };
        return;
      }
      this.stats = {
        pending: this.requests.filter(r => r.status === 'PENDING').length,
        approved: this.requests.filter(r => r.status === 'APPROVED').length,
        rejected: this.requests.filter(r => r.status === 'REJECTED').length,
        completed: this.requests.filter(r => r.status === 'COMPLETED').length
      };
    },
    
    debounceSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadRequests();
      }, 500);
    },
    
    changeItemsPerPage() {
      this.currentPage = 1; // Reset to first page when changing items per page
    },
    
    onPageChange(event) {
      this.currentPage = event.page + 1; // PrimeVue uses 0-based page index
    },
    
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    
    viewRequest(request) {
      this.selectedRequest = request;
    },
    
    // Modal handlers
    openApproveModal(request) {
      this.actionRequest = request;
      this.showApproveModal = true;
    },
    
    openRejectModal(request) {
      this.actionRequest = request;
      this.rejectReason = '';
      this.showRejectModal = true;
    },
    
    openResetModal(request) {
      this.actionRequest = request;
      this.showResetModal = true;
    },
    
    closeModals() {
      this.showApproveModal = false;
      this.showRejectModal = false;
      this.showResetModal = false;
      this.showSuccessModal = false;
      this.actionRequest = null;
      this.rejectReason = '';
      this.resetPasswordData = null;
      this.successMessage = '';
    },
    
    showSuccess(message) {
      this.successMessage = message;
      this.showSuccessModal = true;
    },
    
    async approveRequest() {
      if (!this.actionRequest) return;
      
      try {
        console.log('Approving request:', this.actionRequest.id);
        const response = await axios.patch(
          `${process.env.VUE_APP_API_URL}/password-reset-requests/${this.actionRequest.id}/`,
          { status: 'APPROVED' },
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }}
        );
        
        console.log('Approve response:', response.data);
        this.closeModals();
        this.showSuccess('Request approved successfully. You can now reset the password.');
        this.selectedRequest = null;
        this.loadRequests();
        this.notifyParentToRefresh();
      } catch (error) {
        console.error('Error approving request:', error);
        console.error('Error response:', error.response?.data);
        alert(`Failed to approve request: ${error.response?.data?.detail || error.message}`);
      }
    },
    
    async resetPassword() {
      if (!this.actionRequest) return;
      
      try {
        console.log('Resetting password for:', this.actionRequest.username);
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/reset_user_password/`,
          { 
            username: this.actionRequest.username,
            request_id: this.actionRequest.id
          },
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }}
        );
        
        console.log('Reset password response:', response.data);
        this.resetPasswordData = response.data;
        
        // Keep modal open to show the password
      } catch (error) {
        console.error('Error resetting password:', error);
        console.error('Error response:', error.response?.data);
        alert(`Failed to reset password: ${error.response?.data?.error || error.message}`);
      }
    },
    
    closeResetModal() {
      this.closeModals();
      this.selectedRequest = null;
      this.loadRequests();
      this.notifyParentToRefresh();
    },
    
    copyPassword() {
      if (this.resetPasswordData && this.resetPasswordData.new_password) {
        // Try modern clipboard API first
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(this.resetPasswordData.new_password)
            .then(() => {
              this.showSuccess('Password copied to clipboard!');
            })
            .catch(err => {
              console.error('Clipboard API failed:', err);
              // Fallback to textarea method
              this.copyPasswordFallback();
            });
        } else {
          // Fallback for older browsers
          this.copyPasswordFallback();
        }
      }
    },
    
    copyPasswordFallback() {
      try {
        // Create temporary textarea
        const textarea = document.createElement('textarea');
        textarea.value = this.resetPasswordData.new_password;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();
        
        // Try to copy
        const successful = document.execCommand('copy');
        document.body.removeChild(textarea);
        
        if (successful) {
          this.showSuccess('Password copied to clipboard!');
        } else {
          alert('Failed to copy password. Please copy it manually.');
        }
      } catch (err) {
        console.error('Fallback copy failed:', err);
        alert('Failed to copy password. Please copy it manually.');
      }
    },
    
    async rejectRequest() {
      if (!this.actionRequest) return;
      
      try {
        console.log('Rejecting request:', this.actionRequest.id);
        const response = await axios.patch(
          `${process.env.VUE_APP_API_URL}/password-reset-requests/${this.actionRequest.id}/`,
          { 
            status: 'REJECTED',
            admin_notes: this.rejectReason || 'Request rejected'
          },
          { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }}
        );
        
        console.log('Reject response:', response.data);
        this.closeModals();
        this.showSuccess('Request rejected successfully.');
        this.selectedRequest = null;
        this.loadRequests();
        this.notifyParentToRefresh();
      } catch (error) {
        console.error('Error rejecting request:', error);
        console.error('Error response:', error.response?.data);
        alert(`Failed to reject request: ${error.response?.data?.detail || error.message}`);
      }
    },
    
    notifyParentToRefresh() {
      // Trigger a custom event that the parent can listen to
      window.dispatchEvent(new CustomEvent('password-reset-processed'));
    },
    
    scrollToHighlightedRow() {
      if (!this.highlightedRequestId) return;
      
      const rowElement = document.getElementById(`request-row-${this.highlightedRequestId}`);
      if (rowElement) {
        // Scroll to the row with smooth behavior
        rowElement.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'center' 
        });
        
        // Remove highlight after 5 seconds
        setTimeout(() => {
          this.highlightedRequestId = null;
          // Clean up the query parameter
          this.$router.replace({ 
            path: this.$route.path,
            query: {}
          });
        }, 5000);
      }
    },
    
    getStatusClass(status) {
      if (!status) return 'status-unknown';
      const statusMap = {
        'PENDING': 'status-pending',
        'APPROVED': 'status-approved',
        'REJECTED': 'status-rejected',
        'COMPLETED': 'status-completed'
      };
      return statusMap[status] || 'status-unknown';
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    },
    
    formatDateTime(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.password-reset-requests {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: white;
}

.stat-icon.blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-icon.green { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stat-icon.orange { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-icon.red { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

.filters-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-left {
  flex-shrink: 0;
}

.filter-right {
  display: flex;
  gap: 20px;
  flex: 1;
  justify-content: flex-end;
}

.show-entries {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
}

.show-entries select {
  padding: 8px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.3s;
}

.show-entries select:focus {
  outline: none;
  border-color: #667eea;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.search-input,
.filter-group select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #667eea;
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table thead {
  background: #f8fafc;
}

.requests-table th {
  padding: 15px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Sortable Table Headers */
.requests-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  position: relative;
}

.requests-table th.sortable.nowrap {
  white-space: nowrap;
}

.requests-table th.sortable:hover {
  background-color: #e2e8f0;
}

.requests-table th .sort-icon {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 6px;
  transition: color 0.2s ease;
  display: inline-block;
  vertical-align: middle;
}

.requests-table th.sortable:hover .sort-icon {
  color: #64748b;
}

.requests-table th .pi-sort-amount-up,
.requests-table th .pi-sort-amount-down {
  color: #667eea;
  font-weight: bold;
}

.requests-table td {
  padding: 15px;
  border-top: 1px solid #e2e8f0;
}

.requests-table tbody tr:hover {
  background: #f8fafc;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info i {
  color: #667eea;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-approved {
  background: #d1fae5;
  color: #065f46;
}

.status-rejected {
  background: #fee2e2;
  color: #991b1b;
}

.status-completed {
  background: #dbeafe;
  color: #1e40af;
}

.status-unknown {
  background: #e2e8f0;
  color: #475569;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view {
  background: #dbeafe;
  color: #1e40af;
}

.btn-view:hover {
  background: #93c5fd;
}

.btn-approve {
  background: #d1fae5;
  color: #065f46;
}

.btn-approve:hover {
  background: #6ee7b7;
}

.btn-reject {
  background: #fee2e2;
  color: #991b1b;
}

.btn-reject:hover {
  background: #fca5a5;
}

.btn-complete {
  background: #dbeafe;
  color: #1e40af;
}

.btn-complete:hover {
  background: #93c5fd;
}

.btn-reset {
  background: #fef3c7;
  color: #92400e;
}

.btn-reset:hover {
  background: #fde047;
}

.btn-primary {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.btn-danger {
  padding: 12px 24px;
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.3s;
}

.btn-danger:hover {
  transform: translateY(-2px);
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 15px;
  display: block;
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
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 20px;
  color: #1e293b;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #64748b;
}

.modal-body {
  padding: 20px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
}

.detail-value {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1e293b;
  font-weight: 500;
}

.detail-value i {
  color: #667eea;
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

@media (max-width: 768px) {
  .password-reset-requests {
    padding: 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .filters-section {
    grid-template-columns: 1fr;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}

/* Action Modals */
.action-modal {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.action-modal.reset-modal {
  max-width: 600px;
}

.action-modal .modal-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.action-modal .modal-body {
  padding: 24px;
}

.action-modal .modal-body p {
  margin: 0 0 16px 0;
  color: #1e293b;
  font-size: 15px;
}

.modal-note {
  color: #64748b !important;
  font-size: 14px !important;
  margin-top: 12px !important;
}

.form-group {
  margin-top: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s;
}

.form-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-secondary {
  padding: 10px 20px;
  background: #e2e8f0;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

/* Password Reset Result */
.password-result {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #d1fae5;
  border-radius: 8px;
  color: #065f46;
}

.success-message i {
  font-size: 24px;
}

.success-message p {
  margin: 0 !important;
  color: #065f46 !important;
}

.password-display {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.password-display label {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.password-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
}

.password-box code {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
}

.btn-copy {
  padding: 8px 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-copy:hover {
  background: #5568d3;
}

.email-status {
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
}

.status-success {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #065f46;
  background: #d1fae5;
  padding: 12px;
  border-radius: 8px;
}

.status-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #92400e;
  background: #fef3c7;
  padding: 12px;
  border-radius: 8px;
}

.status-success i,
.status-warning i {
  font-size: 18px;
}

/* Success Modal */
.success-modal .modal-body {
  padding: 32px 24px;
}

.success-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.success-content i {
  font-size: 48px;
  color: #4caf50;
}

.success-content p {
  font-size: 16px;
  color: #1e293b;
  margin: 0 !important;
}

/* Pagination */
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
  color: var(--npc-primary);
}

:deep(.p-paginator .p-paginator-page.p-highlight) {
  background: #fef3c7;
  color: #92400e;
  font-weight: 600;
}

:deep(.p-paginator .p-disabled) {
  opacity: 0.4;
  cursor: not-allowed;
}

:deep(.p-paginator .p-paginator-icon) {
  font-size: 0.875rem;
}

/* Highlighted Row Animation */
.highlighted-row {
  animation: highlightFade 5s ease-in-out;
  position: relative;
}

@keyframes highlightFade {
  0% {
    background-color: #fef3c7;
    box-shadow: 0 0 0 3px #fbbf24;
  }
  10% {
    background-color: #fef3c7;
    box-shadow: 0 0 0 3px #fbbf24;
  }
  100% {
    background-color: transparent;
    box-shadow: none;
  }
}

.highlighted-row td {
  position: relative;
}

.highlighted-row td::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #fbbf24 0%, #f59e0b 100%);
  animation: fadeOutBar 5s ease-in-out forwards;
}

@keyframes fadeOutBar {
  0%, 10% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
