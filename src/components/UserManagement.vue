<template>
  <AppLayout>
    <div class="user-management-container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>User Management</h1>
        <button @click="showCreateModal = true" class="btn-primary">
          <i class="pi pi-user-plus"></i>
          <span>Create New User</span>
        </button>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon blue">
            <i class="pi pi-users"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ users.length }}</div>
            <div class="stat-label">Total Users</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon green">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ users.filter(u => u.is_active).length }}</div>
            <div class="stat-label">Active Users</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon orange">
            <i class="pi pi-shield"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ users.filter(u => u.profile?.role === 'ADMIN').length }}</div>
            <div class="stat-label">Admins</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon purple">
            <i class="pi pi-briefcase"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ users.filter(u => u.profile?.role === 'MANAGER').length }}</div>
            <div class="stat-label">Managers</div>
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
              v-model="searchQuery" 
              placeholder="Search by username or email..."
              class="search-input"
            >
          </div>
          
          <div class="filter-group">
            <label>Role</label>
            <select v-model="filterRole">
              <option value="">All Roles</option>
              <option value="ADMIN">Admin</option>
              <option value="MANAGER">Manager</option>
              <option value="OPERATOR">Operator</option>
              <option value="VIEWER">Viewer</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Status</label>
            <select v-model="filterStatus">
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="table-container">
        <div v-if="loading" class="loading-state">
          <i class="pi pi-spin pi-spinner"></i> Loading users...
        </div>

        <table v-else-if="filteredUsers.length > 0" class="users-table">
          <thead>
            <tr>
              <th class="sortable" @click="sortBy('username')">
                Username
                <i :class="['pi', getSortIcon('username'), 'sort-icon']"></i>
              </th>
              <th class="sortable" @click="sortBy('email')">
                Email
                <i :class="['pi', getSortIcon('email'), 'sort-icon']"></i>
              </th>
              <th class="sortable" @click="sortBy('role')">
                Role
                <i :class="['pi', getSortIcon('role'), 'sort-icon']"></i>
              </th>
              <th class="sortable" @click="sortBy('status')">
                Status
                <i :class="['pi', getSortIcon('status'), 'sort-icon']"></i>
              </th>
              <th class="sortable nowrap" @click="sortBy('date_joined')">
                Date Joined
                <i :class="['pi', getSortIcon('date_joined'), 'sort-icon']"></i>
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td>
                <div class="user-info">
                  <i class="pi pi-user"></i>
                  <span>{{ user.username }}</span>
                </div>
              </td>
              <td>{{ user.email || 'N/A' }}</td>
              <td>
                <span class="role-badge" :class="`role-${getRoleBadgeClass(user.profile?.role)}`">
                  {{ user.profile?.role || 'VIEWER' }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>{{ formatDate(user.date_joined) }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="editUser(user)" class="btn-icon btn-edit" title="Edit">
                    <i class="pi pi-pencil"></i>
                  </button>
                  <button 
                    @click="toggleUserStatus(user)" 
                    class="btn-icon" 
                    :class="user.is_active ? 'btn-deactivate' : 'btn-activate'"
                    :title="user.is_active ? 'Deactivate' : 'Activate'"
                  >
                    <i :class="user.is_active ? 'pi pi-ban' : 'pi pi-check'"></i>
                  </button>
                  <button @click="deleteUser(user)" class="btn-icon btn-delete" title="Delete">
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- Pagination -->
        <Paginator 
          v-if="filteredUsers.length > 0"
          :rows="itemsPerPage" 
          :totalRecords="filteredUsers.length" 
          :first="(currentPage - 1) * itemsPerPage"
          @page="onPageChange($event)"
          template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
          :pageLinkSize="5"
        />

        <div v-else class="empty-state">
          <i class="pi pi-users"></i>
          <p>No users found</p>
        </div>
      </div>

      <!-- Create/Edit User Modal -->
      <div v-if="showCreateModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ editMode ? 'Edit User' : 'Create New User' }}</h3>
            <button @click="closeModal" class="btn-close">&times;</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label>Username *</label>
              <input 
                type="text" 
                v-model="formData.username" 
                :disabled="editMode"
                placeholder="Enter username (letters, numbers, @.+-_ only)"
                required
              >
              <small class="field-hint">Username can only contain letters, numbers, and @.+-_ characters (no spaces)</small>
            </div>

            <div class="form-group">
              <label>First Name</label>
              <input 
                type="text" 
                v-model="formData.first_name" 
                placeholder="Enter first name"
              >
            </div>

            <div class="form-group">
              <label>Last Name</label>
              <input 
                type="text" 
                v-model="formData.last_name" 
                placeholder="Enter last name"
              >
            </div>

            <div class="form-group">
              <label>Email</label>
              <input 
                type="email" 
                v-model="formData.email" 
                placeholder="Enter email address"
              >
            </div>

            <div class="form-group" v-if="!editMode">
              <label>Password *</label>
              <input 
                type="password" 
                v-model="formData.password" 
                placeholder="Enter password"
                required
              >
            </div>

            <div class="form-group" v-if="!editMode">
              <label>Confirm Password *</label>
              <input 
                type="password" 
                v-model="formData.confirmPassword" 
                placeholder="Confirm password"
                required
              >
            </div>

            <div class="form-group">
              <label>Role *</label>
              <select v-model="formData.role" required>
                <option value="VIEWER">Viewer</option>
                <option value="OPERATOR">Operator</option>
                <option value="MANAGER">Manager</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>

            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="formData.is_active">
                <span>Active User</span>
              </label>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="btn-secondary">Cancel</button>
            <button @click="saveUser" class="btn-primary">
              {{ editMode ? 'Update User' : 'Create User' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import axios from 'axios';
import AppLayout from './AppLayout.vue';
import Paginator from 'primevue/paginator';

export default {
  name: 'UserManagement',
  components: {
    AppLayout,
    Paginator
  },
  data() {
    return {
      users: [],
      loading: false,
      showCreateModal: false,
      editMode: false,
      searchQuery: '',
      filterRole: '',
      filterStatus: '',
      // Pagination
      currentPage: 1,
      itemsPerPage: 10,
      // Sorting
      sortField: 'username',
      sortOrder: 1, // -1 for descending, 1 for ascending
      formData: {
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: 'VIEWER',
        is_active: true
      }
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const matchesSearch = !this.searchQuery || 
          user.username.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (user.email && user.email.toLowerCase().includes(this.searchQuery.toLowerCase()));
        
        const matchesRole = !this.filterRole || user.profile?.role === this.filterRole;
        
        const matchesStatus = !this.filterStatus || 
          (this.filterStatus === 'active' && user.is_active) ||
          (this.filterStatus === 'inactive' && !user.is_active);
        
        return matchesSearch && matchesRole && matchesStatus;
      });
    },
    sortedUsers() {
      return [...this.filteredUsers].sort((a, b) => {
        let aVal, bVal;
        
        switch(this.sortField) {
          case 'username':
            aVal = a.username?.toLowerCase() || '';
            bVal = b.username?.toLowerCase() || '';
            break;
          case 'email':
            aVal = a.email?.toLowerCase() || '';
            bVal = b.email?.toLowerCase() || '';
            break;
          case 'role':
            aVal = a.profile?.role?.toLowerCase() || 'viewer';
            bVal = b.profile?.role?.toLowerCase() || 'viewer';
            break;
          case 'status':
            aVal = a.is_active ? 1 : 0;
            bVal = b.is_active ? 1 : 0;
            break;
          case 'date_joined':
            aVal = new Date(a.date_joined);
            bVal = new Date(b.date_joined);
            break;
          default:
            return 0;
        }
        
        if (aVal < bVal) return -1 * this.sortOrder;
        if (aVal > bVal) return 1 * this.sortOrder;
        return 0;
      });
    },
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedUsers.slice(start, end);
    }
  },
  mounted() {
    this.loadUsers();
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
    
    changeItemsPerPage() {
      this.currentPage = 1; // Reset to first page when changing items per page
    },
    
    onPageChange(event) {
      this.currentPage = event.page + 1; // PrimeVue uses 0-based page index
    },
    
    async loadUsers() {
      this.loading = true;
      try {
        const response = await api.getUsers();
        this.users = response.data.results || response.data || [];
      } catch (error) {
        // Silently fail if not authenticated or no permission
        if (error.response?.status === 403 || error.response?.status === 401) {
          this.users = [];
          // Don't log error for authentication issues
        } else {
          console.error('Error loading users:', error);
          alert('Failed to load users');
        }
      } finally {
        this.loading = false;
      }
    },
    async saveUser() {
      try {
        // Validation
        if (!this.formData.username) {
          alert('Username is required');
          return;
        }

        // Validate username format
        const usernameRegex = /^[a-zA-Z0-9@.+_-]+$/;
        if (!usernameRegex.test(this.formData.username)) {
          alert('Username can only contain letters, numbers, and @.+-_ characters (no spaces)');
          return;
        }

        if (!this.editMode) {
          if (!this.formData.password) {
            alert('Password is required');
            return;
          }
          if (this.formData.password !== this.formData.confirmPassword) {
            alert('Passwords do not match');
            return;
          }
        }

        const userData = {
          username: this.formData.username,
          first_name: this.formData.first_name,
          last_name: this.formData.last_name,
          email: this.formData.email,
          is_active: this.formData.is_active,
          role: this.formData.role
        };

        if (!this.editMode) {
          userData.password = this.formData.password;
        }

        if (this.editMode) {
          await api.updateUser(this.formData.id, userData);
          alert('User updated successfully');
        } else {
          await api.createUser(userData);
          alert('User created successfully');
        }

        this.closeModal();
        this.loadUsers();
      } catch (error) {
        // Handle authentication errors silently
        if (error.response?.status === 403 || error.response?.status === 401) {
          alert('You do not have permission to manage users. Please log in as an administrator.');
        } else {
          console.error('Error saving user:', error);
          const errorMsg = error.response?.data?.error || error.response?.data?.detail || 'Failed to save user';
          alert(errorMsg);
        }
      }
    },
    editUser(user) {
      this.editMode = true;
      this.formData = {
        id: user.id,
        username: user.username,
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        role: user.profile?.role || 'VIEWER',
        is_active: user.is_active,
        password: '',
        confirmPassword: ''
      };
      this.showCreateModal = true;
    },
    async toggleUserStatus(user) {
      const action = user.is_active ? 'deactivate' : 'activate';
      if (!confirm(`Are you sure you want to ${action} ${user.username}?`)) return;

      try {
        await api.patchUser(user.id, {
          is_active: !user.is_active
        });
        alert(`User ${action}d successfully`);
        this.loadUsers();
      } catch (error) {
        if (error.response?.status === 403 || error.response?.status === 401) {
          alert('You do not have permission to manage users.');
        } else {
          console.error('Error toggling user status:', error);
          alert('Failed to update user status');
        }
      }
    },
    async deleteUser(user) {
      if (!confirm(`Are you sure you want to delete ${user.username}? This action cannot be undone.`)) return;

      try {
        await api.deleteUser(user.id);
        alert('User deleted successfully');
        this.loadUsers();
      } catch (error) {
        if (error.response?.status === 403 || error.response?.status === 401) {
          alert('You do not have permission to delete users.');
        } else {
          console.error('Error deleting user:', error);
          alert('Failed to delete user');
        }
      }
    },
    closeModal() {
      this.showCreateModal = false;
      this.editMode = false;
      this.formData = {
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: 'VIEWER',
        is_active: true
      };
    },
    getRoleBadgeClass(role) {
      const roleMap = {
        'ADMIN': 'danger',
        'MANAGER': 'warning',
        'OPERATOR': 'success',
        'VIEWER': 'info'
      };
      return roleMap[role] || 'info';
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.user-management-container {
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

/* Stats Grid */
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
.stat-icon.purple { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

/* Filters */
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

/* Table */
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: #f8fafc;
}

.users-table th {
  padding: 15px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Sortable Table Headers */
.users-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  position: relative;
}

.users-table th.sortable.nowrap {
  white-space: nowrap;
}

.users-table th.sortable:hover {
  background-color: #e2e8f0;
}

.users-table th .sort-icon {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 6px;
  transition: color 0.2s ease;
  display: inline-block;
  vertical-align: middle;
}

.users-table th.sortable:hover .sort-icon {
  color: #64748b;
}

.users-table th .pi-sort-amount-up,
.users-table th .pi-sort-amount-down {
  color: #667eea;
  font-weight: bold;
}

.users-table td {
  padding: 15px;
  border-top: 1px solid #e2e8f0;
}

.users-table tbody tr:hover {
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

.role-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.role-badge.role-danger {
  background: #fee2e2;
  color: #991b1b;
}

.role-badge.role-warning {
  background: #fef3c7;
  color: #92400e;
}

.role-badge.role-success {
  background: #d1fae5;
  color: #065f46;
}

.role-badge.role-info {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #991b1b;
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

.btn-edit {
  background: #fef3c7;
  color: #92400e;
}

.btn-edit:hover {
  background: #fde047;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fca5a5;
}

.btn-activate {
  background: #d1fae5;
  color: #065f46;
}

.btn-activate:hover {
  background: #6ee7b7;
}

.btn-deactivate {
  background: #e2e8f0;
  color: #475569;
}

.btn-deactivate:hover {
  background: #cbd5e1;
}

/* Buttons */
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

.btn-secondary {
  padding: 10px 20px;
  background: #e2e8f0;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

/* Modal */
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
  max-width: 500px;
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

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.field-hint {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #64748b;
  font-style: italic;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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
</style>
