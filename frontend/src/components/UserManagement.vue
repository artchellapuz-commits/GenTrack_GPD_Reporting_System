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

      <!-- Users Table -->
      <div class="table-container">
        <div v-if="loading" class="loading-state">
          <i class="pi pi-spin pi-spinner"></i> Loading users...
        </div>

        <table v-else-if="filteredUsers.length > 0" class="users-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Date Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
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
                placeholder="Enter username"
                required
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
import axios from 'axios';
import AppLayout from './AppLayout.vue';

export default {
  name: 'UserManagement',
  components: {
    AppLayout
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
      formData: {
        username: '',
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
    }
  },
  mounted() {
    this.loadUsers();
  },
  methods: {
    async loadUsers() {
      this.loading = true;
      try {
        const response = await axios.get('http://localhost:8000/api/users/');
        this.users = response.data.results || response.data || [];
      } catch (error) {
        console.error('Error loading users:', error);
        alert('Failed to load users');
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
          email: this.formData.email,
          is_active: this.formData.is_active,
          role: this.formData.role
        };

        if (!this.editMode) {
          userData.password = this.formData.password;
        }

        if (this.editMode) {
          await axios.put(`http://localhost:8000/api/users/${this.formData.id}/`, userData);
          alert('User updated successfully');
        } else {
          await axios.post('http://localhost:8000/api/users/', userData);
          alert('User created successfully');
        }

        this.closeModal();
        this.loadUsers();
      } catch (error) {
        console.error('Error saving user:', error);
        const errorMsg = error.response?.data?.error || error.response?.data?.detail || 'Failed to save user';
        alert(errorMsg);
      }
    },
    editUser(user) {
      this.editMode = true;
      this.formData = {
        id: user.id,
        username: user.username,
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
        await axios.patch(`http://localhost:8000/api/users/${user.id}/`, {
          is_active: !user.is_active
        });
        alert(`User ${action}d successfully`);
        this.loadUsers();
      } catch (error) {
        console.error('Error toggling user status:', error);
        alert('Failed to update user status');
      }
    },
    async deleteUser(user) {
      if (!confirm(`Are you sure you want to delete ${user.username}? This action cannot be undone.`)) return;

      try {
        await axios.delete(`http://localhost:8000/api/users/${user.id}/`);
        alert('User deleted successfully');
        this.loadUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
        alert('Failed to delete user');
      }
    },
    closeModal() {
      this.showCreateModal = false;
      this.editMode = false;
      this.formData = {
        username: '',
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
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
</style>
