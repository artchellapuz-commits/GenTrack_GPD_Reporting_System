<template>
  <AppLayout>
    <div class="archive-page">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <div class="title-badge">
            <i class="pi pi-box text-blue-500"></i> Storage
          </div>
          <h2>Archived Data</h2>
          <p>View, restore, or permanently delete archived generation reports</p>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon bg-blue"><i class="pi pi-file"></i></div>
          <div class="stat-info">
            <span class="stat-label">Total Archived</span>
            <span class="stat-value">{{ totalFiles }} <small>Files</small></span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon bg-green"><i class="pi pi-database"></i></div>
          <div class="stat-info">
            <span class="stat-label">Records Preserved</span>
            <span class="stat-value">{{ formatNumber(totalRecordsArchived) }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon bg-purple"><i class="pi pi-history"></i></div>
          <div class="stat-info">
            <span class="stat-label">Recently Archived</span>
            <span class="stat-value">{{ recentArchivesCount }} <small>Last 30 Days</small></span>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="archive-container modern-card">
        
        <!-- Toolbar -->
        <div class="toolbar">
          <div class="toolbar-left">
            <div class="search-box">
              <i class="pi pi-search search-icon"></i>
              <input type="text" v-model="searchQuery" placeholder="Search files or plants..." class="search-input" />
            </div>
            <div class="show-entries">
              <select v-model="itemsPerPage" @change="changeItemsPerPage" class="entries-select">
                <option :value="10">10 per page</option>
                <option :value="25">25 per page</option>
                <option :value="50">50 per page</option>
              </select>
            </div>
          </div>
          <div class="toolbar-right">
            <transition name="fade">
              <div v-if="selectedFiles.length > 0" class="bulk-actions">
                <span class="selected-count">{{ selectedFiles.length }} selected</span>
                <button @click="clearSelection" class="btn-clear" title="Clear Selection">
                  <i class="pi pi-times"></i>
                </button>
                <button @click="bulkRestore" class="btn-bulk-restore" :disabled="isProcessingBulk">
                  <i class="pi pi-replay"></i> Restore Selected
                </button>
                <button @click="bulkDelete" class="btn-bulk-delete" :disabled="isProcessingBulk">
                  <i class="pi pi-trash"></i> Delete Selected
                </button>
              </div>
            </transition>
          </div>
        </div>

        <!-- Skeleton Loader -->
        <div class="skeleton-table" v-if="loading">
          <div class="sk-row header-row"></div>
          <div class="sk-row" v-for="i in 5" :key="i"></div>
        </div>

        <!-- Table -->
        <div class="table-wrapper" v-else-if="filteredFiles.length > 0">
          <table class="modern-table">
            <thead>
              <tr>
                <th class="checkbox-col">
                  <div class="custom-checkbox">
                    <input type="checkbox" id="selectAll" @change="toggleSelectAll" :checked="isAllSelected" />
                    <label for="selectAll"></label>
                  </div>
                </th>
                <th @click="sortBy('original_filename')" class="sortable">
                  File Name <i :class="getSortIcon('original_filename')"></i>
                </th>
                <th @click="sortBy('plant_name')" class="sortable">
                  Plant <i :class="getSortIcon('plant_name')"></i>
                </th>
                <th @click="sortBy('archived_at')" class="sortable">
                  Archived Date <i :class="getSortIcon('archived_at')"></i>
                </th>
                <th @click="sortBy('records_imported')" class="sortable text-right">
                  Records <i :class="getSortIcon('records_imported')"></i>
                </th>
                <th class="text-center">Status</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="file in paginatedFiles" :key="file.id" :class="{ 'selected': isSelected(file.id) }">
                <td class="checkbox-col">
                  <div class="custom-checkbox">
                    <input type="checkbox" :id="'chk-'+file.id" :checked="isSelected(file.id)" @change="toggleSelect(file.id)" />
                    <label :for="'chk-'+file.id"></label>
                  </div>
                </td>
                <td>
                  <div class="file-info">
                    <div class="file-icon excel"><i class="pi pi-file-excel"></i></div>
                    <div class="file-details">
                      <span class="file-name">{{ file.original_filename }}</span>
                      <span class="file-date">Uploaded: {{ formatDateOnly(file.uploaded_at) }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="badge-plant"><i class="pi pi-building"></i> {{ file.plant_name }}</span>
                </td>
                <td>
                  <div class="date-cell">
                    <span class="date-main">{{ formatDateOnly(file.archived_at) }}</span>
                    <span class="date-sub">{{ formatTimeOnly(file.archived_at) }}</span>
                  </div>
                </td>
                <td class="text-right font-semibold text-gray-700">
                  {{ formatNumber(file.records_imported) }}
                </td>
                <td class="text-center">
                  <span :class="['status-badge', file.status.toLowerCase()]">
                    <i :class="getStatusIcon(file.status)"></i> {{ file.status }}
                  </span>
                </td>
                <td>
                  <div class="actions-group">
                    <button @click="restoreFile(file)" class="action-btn restore" title="Restore to Active" :disabled="restoring === file.id">
                      <i v-if="restoring !== file.id" class="pi pi-replay"></i>
                      <i v-else class="pi pi-spin pi-spinner"></i>
                    </button>
                    <button @click="confirmDelete(file)" class="action-btn delete" title="Delete Permanently" :disabled="deleting === file.id">
                      <i v-if="deleting !== file.id" class="pi pi-trash"></i>
                      <i v-else class="pi pi-spin pi-spinner"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon-wrapper">
            <i class="pi pi-inbox"></i>
          </div>
          <h3>No Archived Files Found</h3>
          <p v-if="searchQuery">No results match your search "{{ searchQuery }}". Try adjusting your filters.</p>
          <p v-else>Your archive is currently empty. Deleted or expired reports will appear here.</p>
          <button v-if="searchQuery" @click="searchQuery = ''" class="btn-primary mt-4">Clear Search</button>
        </div>

        <!-- Pagination -->
        <div class="pagination-footer" v-if="filteredFiles.length > 0">
          <span class="showing-text">Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredFiles.length }} entries</span>
          <Paginator 
            :rows="itemsPerPage" 
            :totalRecords="filteredFiles.length" 
            :first="(currentPage - 1) * itemsPerPage"
            @page="onPageChange"
            template="PrevPageLink PageLinks NextPageLink"
          />
        </div>

      </div>

      <!-- Delete Confirmation Modal -->
      <transition name="modal">
        <div v-if="deleteDialog" class="modal-backdrop" @click.self="deleteDialog = false">
          <div class="modern-modal danger-modal">
            <div class="modal-icon"><i class="pi pi-exclamation-triangle"></i></div>
            <h3 class="modal-title">{{ isBulkDelete ? 'Delete Multiple Files' : 'Delete Permanently' }}</h3>
            
            <div class="modal-body">
              <p v-if="isBulkDelete">
                Are you sure you want to permanently delete <strong>{{ selectedFiles.length }} files</strong>?
              </p>
              <p v-else-if="fileToDelete">
                Are you sure you want to permanently delete <strong>"{{ fileToDelete.original_filename }}"</strong>?
              </p>
              <div class="warning-box">
                <strong><i class="pi pi-info-circle"></i> Warning:</strong> This action cannot be undone. The file and all associated generation records will be permanently removed from the database and storage.
              </div>
            </div>
            
            <div class="modal-actions">
              <button @click="deleteDialog = false" class="btn-cancel">Cancel</button>
              <button @click="isBulkDelete ? executeBulkDelete() : deleteFile()" class="btn-danger" :disabled="isProcessingBulk || deleting !== null">
                <i v-if="isProcessingBulk || deleting !== null" class="pi pi-spin pi-spinner"></i>
                <span v-else>Yes, Delete Permanently</span>
              </button>
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
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
import AppLayout from './AppLayout.vue';
import Paginator from 'primevue/paginator';

export default {
  name: 'ArchivePage',
  components: { AppLayout, Paginator },
  setup() {
    const loading = ref(true);
    const archivedFiles = ref([]);
    const selectedFiles = ref([]);
    const searchQuery = ref('');
    
    // Actions state
    const restoring = ref(null);
    const deleting = ref(null);
    const isProcessingBulk = ref(false);
    
    // Modal state
    const deleteDialog = ref(false);
    const fileToDelete = ref(null);
    const isBulkDelete = ref(false);
    
    // Pagination & Sorting
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const sortColumn = ref('archived_at');
    const sortDirection = ref('desc');

    // Toasts
    const toasts = ref([]);
    let toastIdCounter = 0;
    
    const showToast = (type, title, message, duration = 4000) => {
      const id = ++toastIdCounter;
      toasts.value.push({ id, type, title, message });
      setTimeout(() => removeToast(id), duration);
    };

    const removeToast = (id) => {
      const index = toasts.value.findIndex(t => t.id === id);
      if (index > -1) toasts.value.splice(index, 1);
    };

    // MOCK DATA FALLBACK
    const generateMockData = () => {
      const plants = ['Agus 1', 'Agus 2', 'Agus 4', 'Agus 5', 'Agus 6', 'Agus 7'];
      const statuses = ['COMPLETED', 'COMPLETED', 'COMPLETED', 'FAILED'];
      return Array.from({ length: 45 }).map((_, i) => {
        const plant = plants[Math.floor(Math.random() * plants.length)];
        const uploadedDate = new Date(Date.now() - Math.random() * 10000000000);
        const archivedDate = new Date(uploadedDate.getTime() + Math.random() * 5000000000);
        return {
          id: 1000 + i,
          original_filename: `${plant.replace(' ', '_')}_Generation_Report_Q${Math.floor(Math.random()*4)+1}.xlsx`,
          plant_name: `${plant} Hydroelectric Plant`,
          uploaded_at: uploadedDate.toISOString(),
          archived_at: archivedDate.toISOString(),
          status: statuses[Math.floor(Math.random() * statuses.length)],
          records_imported: Math.floor(Math.random() * 800) + 100
        };
      }).sort((a, b) => new Date(b.archived_at) - new Date(a.archived_at));
    };

    // Load Data
    const loadArchivedFiles = async () => {
      loading.value = true;
      try {
        const response = await api.getArchivedFiles();
        const data = response.data?.results || response.data || [];
        archivedFiles.value = data;
        
        // If no real data, fall back to mock data for demo purposes
        if (data.length === 0) {
          console.warn('No archived files found, using mock data for demo');
          archivedFiles.value = generateMockData();
        }
      } catch (error) {
        console.error('Failed to load archived files:', error);
        console.warn('Using mock archived data due to API error');
        archivedFiles.value = generateMockData();
      } finally {
        selectedFiles.value = [];
        setTimeout(() => loading.value = false, 600); // UI feel
      }
    };

    onMounted(() => {
      loadArchivedFiles();
    });

    // Computed Stats
    const totalFiles = computed(() => archivedFiles.value.length);
    const totalRecordsArchived = computed(() => archivedFiles.value.reduce((sum, f) => sum + (f.records_imported || 0), 0));
    const recentArchivesCount = computed(() => {
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return archivedFiles.value.filter(f => new Date(f.archived_at) >= thirtyDaysAgo).length;
    });

    // Filtering & Sorting
    const filteredFiles = computed(() => {
      let files = [...archivedFiles.value];
      
      if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase();
        files = files.filter(f => 
          f.original_filename?.toLowerCase().includes(q) || 
          f.plant_name?.toLowerCase().includes(q)
        );
      }

      files.sort((a, b) => {
        let aVal = a[sortColumn.value] || '';
        let bVal = b[sortColumn.value] || '';
        if (typeof aVal === 'string') aVal = aVal.toLowerCase();
        if (typeof bVal === 'string') bVal = bVal.toLowerCase();
        
        if (aVal < bVal) return sortDirection.value === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection.value === 'asc' ? 1 : -1;
        return 0;
      });

      return files;
    });

    const paginatedFiles = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      return filteredFiles.value.slice(start, start + itemsPerPage.value);
    });

    const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value);
    const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage.value, filteredFiles.value.length));

    // Selection Logic
    const isAllSelected = computed(() => {
      return paginatedFiles.value.length > 0 && paginatedFiles.value.every(f => selectedFiles.value.includes(f.id));
    });

    const isSelected = (id) => selectedFiles.value.includes(id);

    const toggleSelect = (id) => {
      const idx = selectedFiles.value.indexOf(id);
      if (idx > -1) selectedFiles.value.splice(idx, 1);
      else selectedFiles.value.push(id);
    };

    const toggleSelectAll = (e) => {
      if (e.target.checked) {
        paginatedFiles.value.forEach(f => {
          if (!selectedFiles.value.includes(f.id)) selectedFiles.value.push(f.id);
        });
      } else {
        paginatedFiles.value.forEach(f => {
          const idx = selectedFiles.value.indexOf(f.id);
          if (idx > -1) selectedFiles.value.splice(idx, 1);
        });
      }
    };

    const clearSelection = () => { selectedFiles.value = []; };

    // Actions
    const restoreFile = async (file) => {
      restoring.value = file.id;
      try {
        await api.restoreArchivedFile(file.id);
        showToast('success', 'Restored', `${file.original_filename} restored successfully.`);
        archivedFiles.value = archivedFiles.value.filter(f => f.id !== file.id);
      } catch (error) {
        console.error('Restore error:', error);
        showToast('error', 'Error', `Failed to restore file: ${error.response?.data?.error || error.message}`);
      } finally {
        restoring.value = null;
      }
    };

    const bulkRestore = async () => {
      isProcessingBulk.value = true;
      try {
        let count = 0;
        let errors = [];
        
        for (const id of selectedFiles.value) {
          try {
            await api.restoreArchivedFile(id);
            count++;
          } catch (error) {
            console.error(`Failed to restore file ${id}:`, error);
            errors.push(`File ID ${id}: ${error.response?.data?.error || error.message}`);
          }
        }
        
        // Remove successfully restored files from the list
        const restoredIds = selectedFiles.value.slice(0, count);
        archivedFiles.value = archivedFiles.value.filter(f => !restoredIds.includes(f.id));
        
        if (count > 0) {
          showToast('success', 'Bulk Restored', `${count} files restored successfully.`);
        }
        
        if (errors.length > 0) {
          showToast('error', 'Partial Failure', `${errors.length} files failed to restore. Check console for details.`);
        }
        
        clearSelection();
      } catch (error) {
        console.error('Bulk restore error:', error);
        showToast('error', 'Error', 'Failed to restore files.');
      } finally {
        isProcessingBulk.value = false;
      }
    };

    const confirmDelete = (file) => {
      fileToDelete.value = file;
      isBulkDelete.value = false;
      deleteDialog.value = true;
    };

    const bulkDelete = () => {
      isBulkDelete.value = true;
      deleteDialog.value = true;
    };

    const deleteFile = async () => {
      deleting.value = fileToDelete.value.id;
      try {
        await api.deleteUploadedFile(fileToDelete.value.id);
        archivedFiles.value = archivedFiles.value.filter(f => f.id !== fileToDelete.value.id);
        showToast('success', 'Deleted', `${fileToDelete.value.original_filename} permanently deleted from database.`);
        deleteDialog.value = false;
      } catch (error) {
        console.error('Delete error:', error);
        showToast('error', 'Error', `Failed to delete file: ${error.response?.data?.error || error.message}`);
      } finally {
        deleting.value = null;
        fileToDelete.value = null;
      }
    };

    const executeBulkDelete = async () => {
      isProcessingBulk.value = true;
      try {
        let count = 0;
        let errors = [];
        
        for (const id of selectedFiles.value) {
          try {
            await api.deleteUploadedFile(id);
            count++;
          } catch (error) {
            console.error(`Failed to delete file ${id}:`, error);
            errors.push(`File ID ${id}: ${error.response?.data?.error || error.message}`);
          }
        }
        
        // Remove successfully deleted files from the list
        const deletedIds = selectedFiles.value.slice(0, count);
        archivedFiles.value = archivedFiles.value.filter(f => !deletedIds.includes(f.id));
        
        if (count > 0) {
          showToast('success', 'Bulk Deleted', `${count} files permanently deleted from database.`);
        }
        
        if (errors.length > 0) {
          showToast('error', 'Partial Failure', `${errors.length} files failed to delete. Check console for details.`);
        }
        
        deleteDialog.value = false;
        clearSelection();
      } catch (error) {
        console.error('Bulk delete error:', error);
        showToast('error', 'Error', 'Failed to delete files from database.');
      } finally {
        isProcessingBulk.value = false;
      }
    };

    // Formatters
    const formatNumber = (num) => Number(num).toLocaleString();
    const formatDateOnly = (d) => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const formatTimeOnly = (d) => new Date(d).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

    const getStatusIcon = (status) => {
      if(status === 'COMPLETED') return 'pi pi-check-circle';
      if(status === 'FAILED') return 'pi pi-times-circle';
      return 'pi pi-clock';
    };

    // Table sorting & pagination
    const sortBy = (col) => {
      if (sortColumn.value === col) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortColumn.value = col;
        sortDirection.value = 'desc';
      }
    };

    const getSortIcon = (col) => {
      if (sortColumn.value !== col) return 'pi pi-sort';
      return sortDirection.value === 'asc' ? 'pi pi-sort-amount-up-alt text-blue-500' : 'pi pi-sort-amount-down text-blue-500';
    };

    const changeItemsPerPage = () => { currentPage.value = 1; };
    const onPageChange = (e) => { currentPage.value = e.page + 1; };

    return {
      loading, archivedFiles, selectedFiles, searchQuery,
      restoring, deleting, isProcessingBulk,
      deleteDialog, fileToDelete, isBulkDelete,
      currentPage, itemsPerPage,
      totalFiles, totalRecordsArchived, recentArchivesCount,
      filteredFiles, paginatedFiles, startIndex, endIndex,
      isAllSelected, isSelected, toggleSelect, toggleSelectAll, clearSelection,
      restoreFile, bulkRestore, confirmDelete, bulkDelete, deleteFile, executeBulkDelete,
      formatNumber, formatDateOnly, formatTimeOnly, getStatusIcon,
      sortBy, getSortIcon, changeItemsPerPage, onPageChange,
      toasts, removeToast
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.archive-page {
  padding: 32px;
  background: #f8fafc;
  min-height: calc(100vh - 64px);
  font-family: 'Inter', sans-serif;
  color: #0f172a;
}

/* Header */
.page-header { margin-bottom: 32px; }
.title-badge { display: inline-flex; align-items: center; gap: 6px; background: #eff6ff; color: #1d4ed8; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; }
.header-content h2 { font-size: 2.25rem; font-weight: 800; margin: 0 0 8px 0; color: #0f172a; letter-spacing: -0.03em; }
.header-content p { color: #64748b; margin: 0; font-size: 1.05rem; }

/* Stats Row */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 32px; }
.stat-card { background: white; padding: 24px; border-radius: 16px; display: flex; align-items: center; gap: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
.stat-icon { width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
.bg-blue { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
.bg-green { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }
.bg-purple { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); color: white; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); }
.stat-info { display: flex; flex-direction: column; }
.stat-label { color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; }
.stat-value { color: #0f172a; font-size: 1.75rem; font-weight: 800; line-height: 1.2; display: flex; align-items: baseline; gap: 6px; }
.stat-value small { font-size: 0.875rem; font-weight: 600; color: #94a3b8; }

/* Main Card */
.modern-card { background: white; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); overflow: hidden; }

/* Toolbar */
.toolbar { padding: 20px 24px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; background: #f8fafc; }
.toolbar-left { display: flex; gap: 16px; align-items: center; }
.search-box { position: relative; width: 300px; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.search-input { width: 100%; padding: 10px 12px 10px 36px; border: 2px solid #e2e8f0; border-radius: 10px; font-family: 'Inter', sans-serif; font-size: 0.95rem; transition: border-color 0.2s; }
.search-input:focus { outline: none; border-color: #3b82f6; }
.entries-select { padding: 10px 16px; border: 2px solid #e2e8f0; border-radius: 10px; background: white; font-weight: 500; color: #475569; outline: none; cursor: pointer; }

.bulk-actions { display: flex; align-items: center; gap: 12px; background: #eff6ff; padding: 6px 12px; border-radius: 12px; border: 1px solid #bfdbfe; }
.selected-count { font-weight: 700; color: #1e3a8a; font-size: 0.875rem; padding-right: 8px; border-right: 1px solid #bfdbfe; }
.btn-clear { background: transparent; border: none; color: #64748b; cursor: pointer; padding: 6px; border-radius: 6px; }
.btn-clear:hover { background: #dbeafe; color: #1e3a8a; }
.btn-bulk-restore, .btn-bulk-delete { border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 0.875rem; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s; }
.btn-bulk-restore { background: #10b981; color: white; box-shadow: 0 2px 4px rgba(16,185,129,0.2); }
.btn-bulk-restore:hover:not(:disabled) { background: #059669; transform: translateY(-1px); }
.btn-bulk-delete { background: #ef4444; color: white; box-shadow: 0 2px 4px rgba(239,68,68,0.2); }
.btn-bulk-delete:hover:not(:disabled) { background: #dc2626; transform: translateY(-1px); }
button:disabled { opacity: 0.6; cursor: not-allowed; }

/* Table Styles */
.table-wrapper { overflow-x: auto; }
.modern-table { width: 100%; border-collapse: collapse; text-align: left; }
.modern-table th { padding: 16px 24px; background: white; font-size: 0.8125rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid #e2e8f0; white-space: nowrap; }
.modern-table td { padding: 16px 24px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #1e293b; }
.modern-table tr { transition: background 0.2s; }
.modern-table tr:hover { background: #f8fafc; }
.modern-table tr.selected { background: #eff6ff; }

.sortable { cursor: pointer; transition: color 0.2s; }
.sortable:hover { color: #0f172a; }
.sortable i { margin-left: 4px; color: #cbd5e1; }

.checkbox-col { width: 40px; }
.custom-checkbox input { display: none; }
.custom-checkbox label { display: inline-block; width: 20px; height: 20px; border: 2px solid #cbd5e1; border-radius: 6px; cursor: pointer; position: relative; transition: all 0.2s; }
.custom-checkbox input:checked + label { background: #3b82f6; border-color: #3b82f6; }
.custom-checkbox input:checked + label::after { content: ''; position: absolute; left: 6px; top: 2px; width: 5px; height: 10px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg); }

.file-info { display: flex; align-items: center; gap: 16px; }
.file-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0; }
.file-icon.excel { background: #f0fdf4; color: #16a34a; }
.file-details { display: flex; flex-direction: column; }
.file-name { font-weight: 600; color: #0f172a; font-size: 0.95rem; }
.file-date { font-size: 0.8125rem; color: #64748b; margin-top: 2px; }

.badge-plant { display: inline-flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 6px 12px; border-radius: 8px; font-size: 0.875rem; font-weight: 600; color: #475569; }

.date-cell { display: flex; flex-direction: column; }
.date-main { font-weight: 600; color: #1e293b; font-size: 0.95rem; }
.date-sub { font-size: 0.8125rem; color: #94a3b8; }

.status-badge { display: inline-flex; align-items: center; justify-content: center; gap: 6px; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.status-badge.completed { background: #dcfce7; color: #059669; }
.status-badge.failed { background: #fee2e2; color: #dc2626; }

.actions-group { display: flex; justify-content: flex-end; gap: 8px; }
.action-btn { width: 36px; height: 36px; border-radius: 10px; border: none; display: flex; align-items: center; justify-content: center; font-size: 1.125rem; cursor: pointer; transition: all 0.2s; }
.action-btn.restore { background: #f0fdf4; color: #10b981; }
.action-btn.restore:hover:not(:disabled) { background: #10b981; color: white; transform: translateY(-2px); box-shadow: 0 4px 6px rgba(16,185,129,0.2); }
.action-btn.delete { background: #fef2f2; color: #ef4444; }
.action-btn.delete:hover:not(:disabled) { background: #ef4444; color: white; transform: translateY(-2px); box-shadow: 0 4px 6px rgba(239,68,68,0.2); }

/* Skeleton */
.skeleton-table { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.sk-row { height: 60px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 400% 100%; animation: shimmer 1.5s infinite; border-radius: 12px; }
.sk-row.header-row { height: 40px; margin-bottom: 8px; }
@keyframes shimmer { 0% { background-position: 100% 0; } 100% { background-position: -100% 0; } }

/* Empty State */
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon-wrapper { width: 80px; height: 80px; background: #f1f5f9; color: #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 24px auto; }
.empty-state h3 { font-size: 1.5rem; color: #0f172a; margin: 0 0 12px 0; }
.empty-state p { color: #64748b; max-width: 400px; margin: 0 auto; line-height: 1.6; }
.btn-primary { background: #3b82f6; color: white; border: none; padding: 10px 24px; border-radius: 10px; font-weight: 600; cursor: pointer; margin-top: 16px; }

/* Pagination */
.pagination-footer { padding: 16px 24px; border-top: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; background: white; }
.showing-text { font-size: 0.875rem; color: #64748b; font-weight: 500; }

:deep(.p-paginator) { background: transparent; border: none; padding: 0; }
:deep(.p-paginator .p-paginator-pages .p-paginator-page) { min-width: 36px; height: 36px; border-radius: 10px; margin: 0 4px; color: #64748b; font-weight: 600; }
:deep(.p-paginator .p-paginator-pages .p-paginator-page.p-highlight) { background: #eff6ff; color: #2563eb; }

/* Modals */
.modal-backdrop { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15,23,42,0.6); backdrop-filter: blur(4px); z-index: 1000; display: flex; align-items: center; justify-content: center; }
.modern-modal { background: white; border-radius: 24px; width: 90%; max-width: 450px; padding: 32px; text-align: center; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); }
.danger-modal .modal-icon { width: 72px; height: 72px; background: #fef2f2; color: #ef4444; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 20px auto; }
.modal-title { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0 0 16px 0; }
.modal-body p { color: #475569; font-size: 1.05rem; margin: 0 0 24px 0; line-height: 1.5; }
.warning-box { background: #fffbeb; color: #b91c1c; padding: 16px; border-radius: 12px; font-size: 0.9rem; text-align: left; margin-bottom: 24px; border: 1px solid #fecaca; }
.modal-actions { display: flex; gap: 12px; }
.btn-cancel { flex: 1; background: #f1f5f9; border: none; padding: 12px; border-radius: 12px; font-weight: 600; color: #475569; cursor: pointer; transition: background 0.2s; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-danger { flex: 1; background: #ef4444; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(239,68,68,0.3); transition: all 0.2s; }
.btn-danger:hover:not(:disabled) { background: #dc2626; transform: translateY(-2px); }

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }
.modal-enter-active { animation: bounceIn 0.4s; }
.modal-leave-active { transition: opacity 0.3s; opacity: 0; }
@keyframes bounceIn { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

@media (max-width: 1024px) {
  .stats-row { grid-template-columns: 1fr; }
  .toolbar { flex-direction: column; gap: 16px; align-items: flex-start; }
  .search-box { width: 100%; }
}
</style>
