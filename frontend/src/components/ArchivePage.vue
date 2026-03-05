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
          <div class="header-left">
            <h3 class="card-title">
              <i class="pi pi-history title-icon"></i>
              Archived Uploads ({{ totalFiles }})
            </h3>
          </div>
          <div class="header-actions" v-if="selectedFiles.length > 0">
            <span class="selected-count">{{ selectedFiles.length }} selected</span>
            <button @click="bulkDelete" class="btn-bulk-delete glass-button">
              <i class="pi pi-trash"></i>
              Delete Selected
            </button>
            <button @click="clearSelection" class="btn-clear glass-button">
              <i class="pi pi-times"></i>
              Clear
            </button>
          </div>
        </div>

        <!-- Show Entries Control -->
        <div class="table-controls">
          <div class="show-entries">
            <label for="entries-select">Show</label>
            <select 
              id="entries-select" 
              v-model="itemsPerPage" 
              @change="changeItemsPerPage"
              class="entries-select"
            >
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
            </select>
            <span>entries</span>
          </div>
        </div>

        <div class="card-body p-0">
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th style="width: 50px;">
                    <input 
                      type="checkbox" 
                      @change="toggleSelectAll"
                      :checked="isAllSelected"
                      class="checkbox-input"
                    />
                  </th>
                  <th @click="sortBy('original_filename')" class="sortable">
                    <div class="th-content">
                      <span>File Name</span>
                      <i :class="getSortIcon('original_filename')"></i>
                    </div>
                  </th>
                  <th @click="sortBy('plant_name')" class="sortable">
                    <div class="th-content">
                      <span>Plant</span>
                      <i :class="getSortIcon('plant_name')"></i>
                    </div>
                  </th>
                  <th @click="sortBy('uploaded_at')" class="sortable">
                    <div class="th-content">
                      <span>Uploaded At</span>
                      <i :class="getSortIcon('uploaded_at')"></i>
                    </div>
                  </th>
                  <th @click="sortBy('archived_at')" class="sortable">
                    <div class="th-content">
                      <span>Archived At</span>
                      <i :class="getSortIcon('archived_at')"></i>
                    </div>
                  </th>
                  <th @click="sortBy('status')" class="sortable">
                    <div class="th-content">
                      <span>Status</span>
                      <i :class="getSortIcon('status')"></i>
                    </div>
                  </th>
                  <th @click="sortBy('records_imported')" class="sortable">
                    <div class="th-content">
                      <span>Records</span>
                      <i :class="getSortIcon('records_imported')"></i>
                    </div>
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="file in paginatedFiles" 
                  :key="file.id" 
                  class="archive-row"
                  :class="{ 'selected-row': isSelected(file.id) }"
                >
                  <td>
                    <input 
                      type="checkbox" 
                      :checked="isSelected(file.id)"
                      @change="toggleSelect(file.id)"
                      class="checkbox-input"
                    />
                  </td>
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
          
          <!-- Pagination -->
          <Paginator 
            v-if="archivedFiles.length > 0"
            :rows="itemsPerPage" 
            :totalRecords="totalFiles" 
            :first="(currentPage - 1) * itemsPerPage"
            @page="onPageChange($event)"
            template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
            :pageLinkSize="5"
          />
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
              <h3 class="modal-title">
                {{ isBulkDelete ? 'Delete Multiple Files' : 'Delete Permanently' }}
              </h3>
            </div>
            <button class="close-btn" @click="deleteDialog = false">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-delete-body">
            <p class="delete-question" v-if="isBulkDelete">
              Are you sure you want to permanently delete <strong>{{ selectedFiles.length }} files</strong>?
            </p>
            <p class="delete-question" v-else-if="fileToDelete">
              Are you sure you want to permanently delete <strong>"{{ fileToDelete.original_filename }}"</strong>?
            </p>
            
            <div class="delete-info">
              <p class="info-title">This will:</p>
              <ul class="info-list">
                <li>Permanently delete the uploaded file(s)</li>
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
              @click="isBulkDelete ? executeBulkDelete() : deleteFile()" 
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
import Paginator from 'primevue/paginator';

export default {
  name: 'ArchivePage',
  components: {
    AppLayout,
    Toast,
    Paginator,
  },
  data() {
    return {
      archivedFiles: [],
      selectedFiles: [],
      restoring: null,
      deleting: null,
      deleteDialog: false,
      fileToDelete: null,
      isBulkDelete: false,
      // Pagination
      currentPage: 1,
      itemsPerPage: 10,
      // Sorting
      sortColumn: 'archived_at',
      sortDirection: 'desc',
    };
  },
  computed: {
    isAllSelected() {
      return this.paginatedFiles.length > 0 && 
             this.paginatedFiles.every(file => this.selectedFiles.includes(file.id));
    },
    sortedFiles() {
      const files = [...this.archivedFiles];
      
      files.sort((a, b) => {
        let aVal = a[this.sortColumn];
        let bVal = b[this.sortColumn];
        
        // Handle null/undefined values
        if (aVal === null || aVal === undefined) aVal = '';
        if (bVal === null || bVal === undefined) bVal = '';
        
        // Convert to lowercase for string comparison
        if (typeof aVal === 'string') aVal = aVal.toLowerCase();
        if (typeof bVal === 'string') bVal = bVal.toLowerCase();
        
        // Compare values
        if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
      
      return files;
    },
    paginatedFiles() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedFiles.slice(start, end);
    },
    totalFiles() {
      return this.archivedFiles.length;
    },
    totalPages() {
      return Math.ceil(this.totalFiles / this.itemsPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage;
    },
    endIndex() {
      const end = this.startIndex + this.itemsPerPage;
      return end > this.totalFiles ? this.totalFiles : end;
    },
  },
  mounted() {
    this.loadArchivedFiles();
  },
  methods: {
    async loadArchivedFiles() {
      try {
        const response = await api.getArchivedFiles();
        this.archivedFiles = response.data.results || response.data;
        // Clear selection when reloading
        this.selectedFiles = [];
      } catch (error) {
        console.error('Error loading archived files:', error);
        this.$toast.error('Failed to load archived files');
      }
    },
    
    toggleSelect(fileId) {
      const index = this.selectedFiles.indexOf(fileId);
      if (index > -1) {
        this.selectedFiles.splice(index, 1);
      } else {
        this.selectedFiles.push(fileId);
      }
    },
    
    toggleSelectAll(event) {
      if (event.target.checked) {
        // Select all files on current page
        this.paginatedFiles.forEach(file => {
          if (!this.selectedFiles.includes(file.id)) {
            this.selectedFiles.push(file.id);
          }
        });
      } else {
        // Deselect all files on current page
        this.paginatedFiles.forEach(file => {
          const index = this.selectedFiles.indexOf(file.id);
          if (index > -1) {
            this.selectedFiles.splice(index, 1);
          }
        });
      }
    },
    
    isSelected(fileId) {
      return this.selectedFiles.includes(fileId);
    },
    
    clearSelection() {
      this.selectedFiles = [];
    },
    
    bulkDelete() {
      if (this.selectedFiles.length === 0) {
        this.$toast.warning('Please select files to delete');
        return;
      }
      this.isBulkDelete = true;
      this.deleteDialog = true;
    },
    
    async executeBulkDelete() {
      if (this.selectedFiles.length === 0) return;
      
      this.deleting = 'bulk';
      let successCount = 0;
      let failCount = 0;
      
      try {
        // Delete files one by one
        for (const fileId of this.selectedFiles) {
          try {
            await api.deleteUploadedFile(fileId);
            successCount++;
          } catch (error) {
            console.error(`Failed to delete file ${fileId}:`, error);
            failCount++;
          }
        }
        
        // Show result
        if (successCount > 0) {
          this.$toast.success(`Successfully deleted ${successCount} file(s)`);
        }
        if (failCount > 0) {
          this.$toast.error(`Failed to delete ${failCount} file(s)`);
        }
        
        this.deleteDialog = false;
        this.isBulkDelete = false;
        this.selectedFiles = [];
        this.loadArchivedFiles();
        
      } catch (error) {
        this.$toast.error('Failed to delete files');
      } finally {
        this.deleting = null;
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
      this.isBulkDelete = false;
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
    
    changeItemsPerPage() {
      this.currentPage = 1; // Reset to first page when changing items per page
    },
    
    onPageChange(event) {
      this.currentPage = event.page + 1; // PrimeVue uses 0-based page index
    },
    
    // Sorting methods
    sortBy(column) {
      if (this.sortColumn === column) {
        // Toggle direction if same column
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // New column, default to ascending
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },
    
    getSortIcon(column) {
      if (this.sortColumn !== column) {
        return 'pi pi-sort-alt sort-icon';
      }
      return this.sortDirection === 'asc' 
        ? 'pi pi-sort-amount-up-alt sort-icon active' 
        : 'pi pi-sort-amount-down sort-icon active';
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.selected-count {
  font-size: 0.9375rem;
  color: var(--npc-primary);
  font-weight: 600;
  padding: 0.5rem 1rem;
  background: rgba(0, 61, 130, 0.1);
  border-radius: 0.5rem;
}

.btn-bulk-delete,
.btn-clear {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-bulk-delete {
  background: #ef4444;
  color: white;
}

.btn-bulk-delete:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-clear {
  background: #6b7280;
  color: white;
}

.btn-clear:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--npc-primary);
}

.selected-row {
  background-color: rgba(0, 61, 130, 0.05);
}

.archive-row {
  transition: background-color 0.2s ease;
}

.archive-row:hover {
  background-color: rgba(0, 61, 130, 0.02);
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

/* Table Controls */
.table-controls {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.show-entries {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  color: var(--gray-700);
}

.show-entries label {
  font-weight: 500;
}

.entries-select {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  border: 1px solid #cbd5e0;
  border-radius: 0.5rem;
  background-color: white;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23718096' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
}

.entries-select:hover {
  border-color: var(--npc-primary);
}

.entries-select:focus {
  outline: none;
  border-color: var(--npc-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.1);
}

/* Sortable Headers */
.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
}

.sortable:hover {
  background-color: rgba(0, 61, 130, 0.05);
}

.th-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.sort-icon {
  font-size: 0.875rem;
  color: #cbd5e0;
  transition: color 0.2s ease;
}

.sort-icon.active {
  color: var(--npc-primary);
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

/* Responsive Design */
@media (max-width: 768px) {
  .pagination-container {
    flex-direction: column;
    align-items: center;
  }
  
  .pagination-info {
    position: static;
    text-align: center;
    order: 2;
    margin-top: 0.5rem;
  }
  
  .pagination-controls {
    justify-content: center;
    order: 1;
  }
  
  .table-controls {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
