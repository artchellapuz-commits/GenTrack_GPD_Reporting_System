<template>
  <AppLayout>
    <Toast />
    <div class="archive-page glass-background">
      <!-- Page Header -->
      <div class="page-header">
        <h2 class="page-title">
          <i class="pi pi-inbox"></i>
          Archived Files
        </h2>
        <p class="page-description">
          View and manage archived uploaded files. You can restore or permanently delete archived files.
        </p>
      </div>

      <!-- Archived Files List -->
      <div v-if="archivedFiles.length" class="card glass-card glass-fade-in">
        <div class="card-header">
          <h3 class="card-title">
            <i class="pi pi-history title-icon"></i>
            Archived Uploads ({{ archivedFiles.length }})
          </h3>
        </div>
        <div class="card-body p-0">
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>File Name</th>
                  <th>Plant</th>
                  <th>Uploaded At</th>
                  <th>Archived At</th>
                  <th>Status</th>
                  <th>Records</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="file in archivedFiles" :key="file.id" class="archive-row">
                  <td>
                    <div class="file-cell">
                      <i class="pi pi-file file-icon-sm"></i>
                      <span class="filename">{{ file.original_filename }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="plant-badge">{{ file.plant_name }}</span>
                  </td>
                  <td class="text-sm text-muted">
                    {{ formatDate(file.uploaded_at) }}
                  </td>
                  <td class="text-sm text-muted">
                    {{ formatDate(file.archived_at) }}
                  </td>
                  <td>
                    <span :class="['badge', `badge-${getStatusClass(file.status)}`]">
                      {{ file.status }}
                    </span>
                  </td>
                  <td class="font-semibold">
                    {{ file.records_imported || 0 }}
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button 
                        @click="restoreFile(file)" 
                        class="btn-restore" 
                        title="Restore"
                        :disabled="restoring === file.id"
                      >
                        <i v-if="restoring !== file.id" class="pi pi-replay"></i>
                        <i v-else class="pi pi-spin pi-spinner"></i>
                      </button>
                      <button 
                        @click="confirmDelete(file)" 
                        class="btn-delete-action" 
                        title="Delete Permanently"
                        :disabled="deleting === file.id"
                      >
                        <i v-if="deleting !== file.id" class="pi pi-trash"></i>
                        <i v-else class="pi pi-spin pi-spinner"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state glass-card">
        <div class="empty-icon">
          <i class="pi pi-inbox"></i>
        </div>
        <h3 class="empty-title">No Archived Files</h3>
        <p class="empty-description">
          You haven't archived any files yet. Archived files will appear here.
        </p>
        <router-link to="/upload" class="btn btn-primary glass-button">
          <i class="pi pi-upload"></i>
          Go to Upload
        </router-link>
      </div>

      <!-- Delete Confirmation Dialog -->
      <div v-if="deleteDialog" class="modal-overlay" @click.self="deleteDialog = false">
        <div class="modal-delete-content">
          <div class="modal-delete-header">
            <div class="header-left">
              <div class="warning-icon-box">
                <i class="pi pi-exclamation-triangle"></i>
              </div>
              <h3 class="modal-title">Delete Permanently</h3>
            </div>
            <button class="close-btn" @click="deleteDialog = false">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-delete-body">
            <p class="delete-question" v-if="fileToDelete">
              Are you sure you want to permanently delete <strong>"{{ fileToDelete.original_filename }}"</strong>?
            </p>
            
            <div class="delete-info">
              <p class="info-title">This will:</p>
              <ul class="info-list">
                <li>Permanently delete the uploaded file</li>
                <li>Delete all generation report records</li>
                <li>This action cannot be undone</li>
              </ul>
            </div>
          </div>
          
          <div class="modal-delete-footer">
            <button @click="deleteDialog = false" class="btn-cancel">
              Cancel
            </button>
            <button 
              @click="deleteFile" 
              class="btn-delete"
              :disabled="deleting !== null"
            >
              <i v-if="deleting === null" class="pi pi-trash"></i>
              <i v-else class="pi pi-spin pi-spinner"></i>
              {{ deleting !== null ? 'Deleting...' : 'Delete Permanently' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import AppLayout from './AppLayout.vue';
import Toast from 'primevue/toast';

export default {
  name: 'ArchivePage',
  components: {
    AppLayout,
    Toast,
  },
  data() {
    return {
      archivedFiles: [],
      restoring: null,
      deleting: null,
      deleteDialog: false,
      fileToDelete: null,
    };
  },
  mounted() {
    this.loadArchivedFiles();
  },
  methods: {
    async loadArchivedFiles() {
      try {
        const response = await api.getArchivedFiles();
        this.archivedFiles = response.data.results || response.data;
      } catch (error) {
        console.error('Error loading archived files:', error);
        this.$toast.error('Failed to load archived files');
      }
    },
    
    async restoreFile(file) {
      this.restoring = file.id;
      try {
        await api.restoreArchivedFile(file.id);
        this.$toast.success('File restored successfully!');
        this.loadArchivedFiles();
      } catch (error) {
        const errorMsg = error.response?.data?.error || 'Failed to restore file';
        this.$toast.error(errorMsg);
      } finally {
        this.restoring = null;
      }
    },
    
    confirmDelete(file) {
      this.fileToDelete = file;
      this.deleteDialog = true;
    },
    
    async deleteFile() {
      if (!this.fileToDelete) return;
      
      this.deleting = this.fileToDelete.id;
      try {
        const response = await api.deleteUploadedFile(this.fileToDelete.id);
        this.$toast.success(
          `File deleted permanently. ${response.data.reports_deleted || 0} records removed.`
        );
        this.deleteDialog = false;
        this.fileToDelete = null;
        this.loadArchivedFiles();
      } catch (error) {
        const errorMsg = error.response?.data?.error || 'Failed to delete file';
        this.$toast.error(errorMsg);
      } finally {
        this.deleting = null;
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    
    getStatusClass(status) {
      const statusMap = {
        'COMPLETED': 'success',
        'FAILED': 'error',
        'PROCESSING': 'warning',
        'PENDING': 'info'
      };
      return statusMap[status] || 'info';
    },
  },
};
</script>

<style scoped>
.archive-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: 2rem;
  color: var(--gray-900);
  margin-bottom: var(--spacing-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.page-title i {
  color: var(--npc-primary);
}

.page-description {
  color: var(--gray-600);
  font-size: 1rem;
}

.card-title {
  font-size: 1.25rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.title-icon {
  font-size: 1.25rem;
  color: var(--npc-primary);
}

.file-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.filename {
  font-weight: 500;
}

.file-icon-sm {
  font-size: 1rem;
  color: var(--npc-primary);
}

.plant-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: var(--npc-primary);
  color: white;
  border-radius: var(--radius-md);
  font-size: 0.8125rem;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
}

.btn-restore,
.btn-delete-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-restore {
  color: #10b981;
}

.btn-restore:hover:not(:disabled) {
  background-color: #10b981;
  color: white;
  transform: scale(1.1);
}

.btn-delete-action {
  color: #ef4444;
}

.btn-delete-action:hover:not(:disabled) {
  background-color: #ef4444;
  color: white;
  transform: scale(1.1);
}

.btn-restore:disabled,
.btn-delete-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-restore i,
.btn-delete-action i {
  font-size: 1.125rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  color: var(--gray-400);
  margin-bottom: 1.5rem;
}

.empty-title {
  font-size: 1.5rem;
  color: var(--gray-700);
  margin-bottom: 0.5rem;
}

.empty-description {
  color: var(--gray-600);
  margin-bottom: 2rem;
}

/* Delete Modal */
.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  background: rgba(75, 85, 99, 0.75) !important;
  backdrop-filter: blur(12px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 9999 !important;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-delete-content {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-width: 550px;
  width: 90%;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-delete-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  background: linear-gradient(135deg, #ff9a3c 0%, #ff8c00 100%);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.warning-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
}

.warning-icon-box i {
  font-size: 2rem;
  color: white;
}

.modal-title {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.close-btn i {
  font-size: 1.5rem;
  color: white;
}

.modal-delete-body {
  padding: 2.5rem 2rem 2rem;
  background: white;
}

.delete-question {
  font-size: 1.125rem;
  color: #718096;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.delete-question strong {
  color: #2d3748;
  font-weight: 600;
}

.delete-info {
  margin-top: 1.5rem;
}

.info-title {
  font-size: 1rem;
  color: #718096;
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-list li {
  font-size: 0.9375rem;
  color: #718096;
  padding-left: 1.5rem;
  position: relative;
}

.info-list li::before {
  content: '•';
  position: absolute;
  left: 0.5rem;
  color: #a0aec0;
  font-size: 1.25rem;
}

.modal-delete-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem 2rem;
  background: white;
  border-top: 1px solid #e2e8f0;
}

.btn-cancel,
.btn-delete {
  padding: 0.875rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-cancel {
  background: transparent;
  color: #718096;
}

.btn-cancel:hover {
  background: #f7fafc;
  color: #4a5568;
}

.btn-delete {
  background: #ef4444;
  color: white;
  min-width: 180px;
  justify-content: center;
}

.btn-delete:hover:not(:disabled) {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
