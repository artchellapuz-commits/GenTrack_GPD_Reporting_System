<template>
  <AppLayout>
    <Toast />
    <div class="upload-page glass-background">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">Upload Excel Report</h2>
      <p class="page-description">
        Upload generation reports for Agus and Pulangi Hydro-electric Power Plants. Supported formats: .xlsx, .xls, .csv (Max: 100MB)
      </p>
    </div>

    <!-- Upload Form Card -->
    <div class="card glass-card glass-fade-in">
      <div class="card-body">
        <form @submit.prevent="uploadFile" class="upload-form">
          <!-- Plant Selection -->
          <div class="form-group">
            <label class="form-label">
              <i class="pi pi-building"></i>
              Select Hydro-Electric Power Plant
              <span class="label-required">*</span>
            </label>
            
            <!-- Custom Dropdown -->
            <div class="custom-select-wrapper">
              <div 
                class="custom-select-trigger"
                @click="toggleDropdown"
                :class="{ 'active': dropdownOpen }"
              >
                <div v-if="selectedPlant" class="selected-plant-display">
                  <div class="selected-plant-info">
                    <div class="selected-plant-name">{{ getSelectedPlant().name }}</div>
                    <div class="selected-plant-meta">
                      {{ getSelectedPlant().code }} • {{ getSelectedPlant().location }} • {{ getSelectedPlant().capacity_mw }} MW
                    </div>
                  </div>
                </div>
                <div v-else class="placeholder-text">
                  Select a hydro-electric power plant...
                </div>
                <i class="pi pi-chevron-down dropdown-arrow"></i>
              </div>
              
              <transition name="dropdown">
                <div v-if="dropdownOpen" class="custom-select-dropdown">
                  <div class="dropdown-search">
                    <div class="search-input-wrapper">
                      <i class="pi pi-search search-icon"></i>
                      <input 
                        type="text" 
                        v-model="searchQuery"
                        placeholder="Search plants..."
                        class="dropdown-search-input"
                        @click.stop
                      />
                    </div>
                  </div>
                  <div class="dropdown-options">
                    <div 
                      v-for="plant in filteredPlants" 
                      :key="plant.code"
                      class="dropdown-option"
                      :class="{ 'selected': selectedPlant === plant.code }"
                      @click="selectPlant(plant.code)"
                    >
                      <div class="option-content">
                        <div class="option-header">
                          <span class="option-name">{{ plant.name }}</span>
                          <span class="option-code">{{ plant.code }}</span>
                        </div>
                        <div class="option-details">
                          <span class="option-detail">
                            <i class="pi pi-map-marker"></i>
                            {{ plant.location }}
                          </span>
                          <span class="option-detail">
                            <i class="pi pi-bolt"></i>
                            {{ plant.capacity_mw }} MW
                          </span>
                        </div>
                      </div>
                      <i v-if="selectedPlant === plant.code" class="pi pi-check option-check"></i>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
            
            <p class="form-help">Select the hydro-electric power plant for this report</p>
          </div>

          <!-- File Selection -->
          <div class="form-group">
            <label class="form-label">
              <i class="pi pi-file-excel"></i>
              Excel File
              <span class="label-required">*</span>
            </label>
            
            <!-- Drag and Drop Zone -->
            <div 
              class="drag-drop-zone"
              :class="{ 
                'drag-over': isDragging,
                'has-file': selectedFile,
                'error': fileError
              }"
              @dragover.prevent="handleDragOver"
              @dragleave.prevent="handleDragLeave"
              @drop.prevent="handleDrop"
              @click="triggerFileInput"
            >
              <input 
                type="file" 
                @change="handleFileSelect" 
                accept=".xlsx,.xls,.csv"
                class="file-input"
                id="file-upload"
                ref="fileInput"
                required
              />
              
              <!-- No File State -->
              <div v-if="!selectedFile" class="drop-zone-content">
                <div class="drop-zone-icon">
                  <i class="pi pi-cloud-upload"></i>
                </div>
                <div class="drop-zone-text">
                  <p class="drop-zone-title">
                    <span v-if="!isDragging">Drag & drop your Excel file here</span>
                    <span v-else class="dragging-text">Drop file to upload</span>
                  </p>
                  <p class="drop-zone-subtitle">or click to browse</p>
                </div>
                <div class="drop-zone-specs">
                  <span class="spec-item">
                    <i class="pi pi-file-excel"></i>
                    .xlsx / .xls / .csv
                  </span>
                  <span class="spec-item">
                    <i class="pi pi-database"></i>
                    Max 100MB
                  </span>
                </div>
              </div>
              
              <!-- File Selected State -->
              <div v-else class="file-preview">
                <div class="file-preview-icon">
                  <i class="pi pi-file-excel"></i>
                </div>
                <div class="file-preview-info">
                  <div class="file-preview-name">{{ selectedFile.name }}</div>
                  <div class="file-preview-meta">
                    <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
                    <span class="file-type">{{ selectedFile.type || 'Excel File' }}</span>
                  </div>
                  <div v-if="fileValidation" class="file-validation">
                    <i class="pi pi-check-circle"></i>
                    Valid Excel file
                  </div>
                </div>
                <button 
                  type="button"
                  @click.stop="removeFile" 
                  class="btn-remove-file"
                  title="Remove file"
                >
                  <i class="pi pi-times"></i>
                </button>
              </div>
            </div>
            
            <p v-if="fileError" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ fileError }}
            </p>
            <p v-else class="form-help">
              Supported formats: .xlsx, .xls, .csv (Excel & CSV files) • Maximum file size: 100MB
            </p>
          </div>

          <!-- Upload Progress -->
          <div v-if="uploading" class="upload-progress-section">
            <div class="progress-header">
              <span class="progress-label">Uploading...</span>
              <span class="progress-percentage">{{ uploadProgress }}%</span>
            </div>
            <div class="progress-bar-container">
              <div class="progress-bar-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <div class="progress-status">
              <i class="pi pi-spin pi-spinner"></i>
              {{ uploadStatus }}
            </div>
          </div>

          <!-- Upload Button -->
          <div class="form-actions">
            <button 
              type="submit"
              :disabled="!selectedPlant || !selectedFile || uploading"
              class="btn btn-primary btn-lg glass-button"
            >
              <span v-if="!uploading">
                <i class="pi pi-upload btn-icon"></i>
                Upload Report
              </span>
              <span v-else class="uploading-state">
                <span class="spinner"></span>
                Uploading...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Alert Messages -->
    <div v-if="message" :class="['alert', `alert-${messageType}`]">
      <i :class="['alert-icon', messageType === 'success' ? 'pi pi-check-circle' : 'pi pi-times-circle']"></i>
      <div class="alert-content">
        <strong v-if="messageType === 'success'">Success!</strong>
        <strong v-else>Error</strong>
        <p>{{ message }}</p>
      </div>
    </div>

    <!-- Upload History -->
    <div class="card glass-card mt-5 glass-fade-in">
      <div class="card-header">
        <div class="header-content">
          <h3 class="card-title">
            <i class="pi pi-history title-icon"></i>
            Recent Uploads
          </h3>
          <div v-if="uploadHistory.length > 0" class="show-entries">
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
      </div>
      <div class="card-body p-0">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th @click="sortBy('filename')" class="sortable">
                  File Name
                  <i :class="['pi', getSortIcon('filename'), 'sort-icon']"></i>
                </th>
                <th @click="sortBy('plant')" class="sortable">
                  Plant
                  <i :class="['pi', getSortIcon('plant'), 'sort-icon']"></i>
                </th>
                <th @click="sortBy('uploaded_at')" class="sortable nowrap">
                  Uploaded At
                  <i :class="['pi', getSortIcon('uploaded_at'), 'sort-icon']"></i>
                </th>
                <th @click="sortBy('status')" class="sortable">
                  Status
                  <i :class="['pi', getSortIcon('status'), 'sort-icon']"></i>
                </th>
                <th @click="sortBy('records')" class="sortable nowrap">
                  Records
                  <i :class="['pi', getSortIcon('records'), 'sort-icon']"></i>
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="upload in paginatedUploadHistory" :key="upload.id" class="upload-row">
                <td>
                  <div class="file-cell">
                    <i class="pi pi-file file-icon-sm"></i>
                    <span class="filename clickable" @click="viewFile(upload)">{{ upload.original_filename }}</span>
                  </div>
                </td>
                <td>
                  <span class="plant-badge">{{ upload.plant_name }}</span>
                </td>
                <td class="text-sm text-muted">
                  {{ formatDate(upload.uploaded_at) }}
                </td>
                <td>
                  <span :class="['badge', `badge-${getStatusClass(upload.status)}`]">
                    {{ upload.status }}
                  </span>
                </td>
                <td class="font-semibold">
                  {{ upload.records_imported || 0 }}
                </td>
                <td>
                  <button @click="archiveFile(upload)" class="btn-archive" title="Archive">
                    <i class="pi pi-inbox"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <!-- Empty State -->
          <div v-if="uploadHistory.length === 0" class="empty-state">
            <div class="empty-state-content">
              <i class="pi pi-inbox empty-state-icon"></i>
              <h4>No Recent Uploads</h4>
              <p>Upload your first Excel file to see it here.</p>
            </div>
          </div>
        </div>
        
        <!-- Pagination -->
        <Paginator 
          v-if="uploadHistory.length > itemsPerPage"
          :rows="itemsPerPage" 
          :totalRecords="uploadHistory.length" 
          :first="(currentPage - 1) * itemsPerPage"
          @page="onPageChange($event)"
          template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
          :pageLinkSize="5"
        />
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <div v-if="deleteDialog" class="modal-overlay" @click.self="deleteDialog = false">
      <div class="modal-delete-content">
        <!-- Orange Header with Icon -->
        <div class="modal-delete-header">
          <div class="header-left">
            <div class="warning-icon-box">
              <i class="pi pi-exclamation-triangle"></i>
            </div>
            <h3 class="modal-title">Delete Report</h3>
          </div>
          <button class="close-btn" @click="deleteDialog = false">
            <i class="pi pi-times"></i>
          </button>
        </div>
        
        <!-- White Body -->
        <div class="modal-delete-body">
          <p class="delete-question" v-if="uploadToDelete">
            Are you sure you want to delete <strong>"{{ uploadToDelete.original_filename }}"</strong>?
          </p>
          
          <div class="delete-info">
            <p class="info-title">This will:</p>
            <ul class="info-list">
              <li>Delete the uploaded file</li>
              <li>Delete all generation report records</li>
              <li>This action cannot be undone</li>
            </ul>
          </div>
        </div>
        
        <!-- Footer with Buttons -->
        <div class="modal-delete-footer">
          <button 
            @click="deleteDialog = false" 
            class="btn-cancel"
          >
            Cancel
          </button>
          <button 
            @click="deleteUpload" 
            class="btn-delete"
            :disabled="deleting !== null"
          >
            <i v-if="deleting === null" class="pi pi-trash"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            {{ deleting !== null ? 'Deleting...' : 'Delete' }}
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
  name: 'UploadExcel',
  components: {
    AppLayout,
    Toast,
    Paginator,
  },
  data() {
    return {
      plants: [],
      selectedPlant: '',
      selectedFile: null,
      uploading: false,
      uploadProgress: 0,
      uploadStatus: 'Preparing upload...',
      message: '',
      messageType: '',
      uploadHistory: [],
      dropdownOpen: false,
      searchQuery: '',
      deleting: null,
      deleteDialog: false,
      uploadToDelete: null,
      isDragging: false,
      fileError: '',
      fileValidation: false,
      // Pagination
      currentPage: 1,
      itemsPerPage: 10,
      // Sorting
      sortField: 'uploaded_at',
      sortOrder: -1, // -1 for descending, 1 for ascending
    };
  },
  computed: {
    filteredPlants() {
      if (!this.searchQuery) return this.plants;
      const query = this.searchQuery.toLowerCase();
      return this.plants.filter(plant => 
        plant.name.toLowerCase().includes(query) ||
        plant.code.toLowerCase().includes(query) ||
        plant.location.toLowerCase().includes(query)
      );
    },
    paginatedUploadHistory() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedUploadHistory.slice(start, end);
    },
    sortedUploadHistory() {
      const sorted = [...this.uploadHistory].sort((a, b) => {
        let aVal, bVal;
        
        switch(this.sortField) {
          case 'filename':
            aVal = a.original_filename?.toLowerCase() || '';
            bVal = b.original_filename?.toLowerCase() || '';
            break;
          case 'plant':
            aVal = a.plant_name?.toLowerCase() || '';
            bVal = b.plant_name?.toLowerCase() || '';
            break;
          case 'uploaded_at':
            aVal = new Date(a.uploaded_at);
            bVal = new Date(b.uploaded_at);
            break;
          case 'status':
            aVal = a.status?.toLowerCase() || '';
            bVal = b.status?.toLowerCase() || '';
            break;
          case 'records':
            aVal = a.records_imported || 0;
            bVal = b.records_imported || 0;
            break;
          default:
            return 0;
        }
        
        if (aVal < bVal) return -1 * this.sortOrder;
        if (aVal > bVal) return 1 * this.sortOrder;
        return 0;
      });
      
      return sorted;
    }
  },
  mounted() {
    this.loadPlants();
    this.loadUploadHistory();
    document.addEventListener('click', this.closeDropdown);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdown);
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
    
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    closeDropdown(e) {
      if (!e.target.closest('.custom-select-wrapper')) {
        this.dropdownOpen = false;
      }
    },
    selectPlant(plantCode) {
      this.selectedPlant = plantCode;
      this.dropdownOpen = false;
      this.searchQuery = '';
    },
    getSelectedPlant() {
      return this.plants.find(p => p.code === this.selectedPlant) || {};
    },
    async loadPlants() {
      try {
        console.log('Loading plants from API...');
        const response = await api.getPlants();
        console.log('API Response:', response);
        console.log('Response data:', response.data);
        this.plants = response.data.results || response.data;
        console.log('Loaded plants:', this.plants);
        console.log('Number of plants:', this.plants.length);
      } catch (error) {
        console.error('Error loading plants:', error);
        console.error('Error response:', error.response);
        console.error('Error message:', error.message);
        this.showMessage('Error loading plants: ' + (error.message || 'Unknown error'), 'error');
      }
    },
    async loadUploadHistory() {
      try {
        console.log('🔄 Loading upload history...');
        const response = await api.getUploadedFiles();
        console.log('📊 Upload history API response:', response);
        console.log('📊 Response data:', response.data);
        
        this.uploadHistory = response.data.results || response.data;
        console.log('📊 Upload history loaded:', this.uploadHistory);
        console.log('📊 Upload history length:', this.uploadHistory.length);
        
        if (this.uploadHistory.length === 0) {
          console.log('⚠️ No upload history found');
        } else {
          console.log('✅ Upload history loaded successfully');
        }
      } catch (error) {
        console.error('❌ Error loading upload history:', error);
        console.error('❌ Error response:', error.response);
        console.error('❌ Error message:', error.message);
      }
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      this.validateAndSetFile(file);
    },
    
    handleDragOver(event) {
      this.isDragging = true;
    },
    
    handleDragLeave(event) {
      this.isDragging = false;
    },
    
    handleDrop(event) {
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      this.validateAndSetFile(file);
    },
    
    triggerFileInput() {
      if (!this.selectedFile && this.$refs.fileInput) {
        this.$refs.fileInput.click();
      }
    },
    
    validateAndSetFile(file) {
      this.fileError = '';
      this.fileValidation = false;
      
      if (!file) return;
      
      // Check file type - accept .xlsx, .xls, and .csv
      const validExtensions = ['.xlsx', '.xls', '.csv'];
      const fileName = file.name.toLowerCase();
      const isValidType = validExtensions.some(ext => fileName.endsWith(ext));
      
      if (!isValidType) {
        this.fileError = 'Invalid file type. Please upload an Excel file (.xlsx, .xls) or CSV file (.csv)';
        return;
      }
      
      // Check file size (100MB limit)
      const maxSize = 100 * 1024 * 1024; // 100MB in bytes
      if (file.size > maxSize) {
        this.fileError = 'File size exceeds 100MB limit';
        return;
      }
      
      // File is valid
      this.selectedFile = file;
      this.fileValidation = true;
    },
    
    removeFile() {
      this.selectedFile = null;
      this.fileError = '';
      this.fileValidation = false;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },
    async uploadFile() {
      if (!this.selectedPlant || !this.selectedFile) {
        this.$toast.warning('Please select both a plant and a file');
        return;
      }

      this.uploading = true;
      this.uploadProgress = 0;
      this.uploadStatus = 'Preparing upload...';
      this.message = '';
      
      this.$toast.info('Starting upload...');

      // Simulate progress
      const progressInterval = setInterval(() => {
        if (this.uploadProgress < 90) {
          this.uploadProgress += Math.random() * 15;
          if (this.uploadProgress > 90) this.uploadProgress = 90;
          
          if (this.uploadProgress < 30) {
            this.uploadStatus = 'Uploading file...';
          } else if (this.uploadProgress < 60) {
            this.uploadStatus = 'Processing Excel data...';
          } else {
            this.uploadStatus = 'Importing records...';
          }
        }
      }, 300);

      try {
        const response = await api.uploadExcel(this.selectedFile, this.selectedPlant);
        
        clearInterval(progressInterval);
        this.uploadProgress = 100;
        this.uploadStatus = 'Upload complete!';
        
        setTimeout(() => {
          this.$toast.success(`${response.data.records_imported} records imported successfully!`);
          this.showMessage(
            `${response.data.records_imported} records imported successfully.`,
            'success'
          );
          this.selectedFile = null;
          this.selectedPlant = '';
          this.fileValidation = false;
          if (this.$refs.fileInput) {
            this.$refs.fileInput.value = '';
          }
          this.loadUploadHistory();
          this.uploading = false;
          this.uploadProgress = 0;
        }, 1000);
      } catch (error) {
        clearInterval(progressInterval);
        this.uploading = false;
        this.uploadProgress = 0;
        
        let errorMsg = error.response?.data?.error || 'Upload failed';
        
        // Make error message more helpful
        if (errorMsg.includes('Missing required columns') || errorMsg.includes('Cannot import')) {
          // Show the actual error message from backend which is now more helpful
          this.$toast.error(errorMsg, 8000);
        } else {
          this.$toast.error(errorMsg);
        }
        
        this.showMessage(errorMsg, 'error');
      }
    },
    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = '';
      }, 5000);
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
    confirmDelete(upload) {
      this.uploadToDelete = upload;
      this.deleteDialog = true;
    },
    
    downloadFile(upload) {
      // Force download with "Save As" dialog
      if (upload.file && upload.file.startsWith('http')) {
        const link = document.createElement('a');
        link.href = upload.file;
        link.download = upload.original_filename || 'download.xlsx';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else if (upload.file) {
        const baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000';
        const link = document.createElement('a');
        link.href = `${baseURL}${upload.file}`;
        link.download = upload.original_filename || 'download.xlsx';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        this.showMessage('File not available for download', 'error');
      }
    },
    
    viewFile(upload) {
      // Open file in new tab - for Excel files, browser will download and open in Excel
      if (upload.file && upload.file.startsWith('http')) {
        window.open(upload.file, '_blank', 'noopener,noreferrer');
      } else if (upload.file) {
        const baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000';
        window.open(`${baseURL}${upload.file}`, '_blank', 'noopener,noreferrer');
      } else {
        this.showMessage('File not available for viewing', 'error');
      }
    },
    
    async deleteUpload() {
      if (!this.uploadToDelete) return;
      
      this.deleting = this.uploadToDelete.id;
      
      try {
        const response = await api.deleteUploadedFile(this.uploadToDelete.id);
        this.$toast.success(
          `File deleted successfully. ${response.data.reports_deleted || 0} records removed.`
        );
        this.deleteDialog = false;
        this.uploadToDelete = null;
        this.loadUploadHistory();
      } catch (error) {
        const errorMsg = error.response?.data?.error || 'Failed to delete file';
        this.$toast.error(errorMsg);
      } finally {
        this.deleting = null;
      }
    },
    
    async downloadTemplate(templateType) {
      try {
        this.$toast.info('Downloading template...');
        
        // Construct URL - VUE_APP_API_URL already includes /api
        const baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';
        const url = `${baseURL}/uploaded-files/download-template/${templateType}/`;
        
        // Use fetch to download the file
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error('Failed to download template');
        }
        
        // Get the blob from response
        const blob = await response.blob();
        
        // Create object URL and trigger download
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `${templateType.replace(/-/g, '_')}_template.xlsx`;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up the object URL
        window.URL.revokeObjectURL(downloadUrl);
        
        this.$toast.success('Template downloaded successfully!');
      } catch (error) {
        console.error('Error downloading template:', error);
        this.$toast.error('Failed to download template');
      }
    },
    
    async archiveFile(upload) {
      try {
        this.$toast.info('Archiving file...');
        await api.archiveUploadedFile(upload.id);
        this.$toast.success('File archived successfully!');
        this.loadUploadHistory();
      } catch (error) {
        const errorMsg = error.response?.data?.error || 'Failed to archive file';
        this.$toast.error(errorMsg);
      }
    },
  },
};
</script>

<style scoped>
/* Delete Modal with Blur Background */
.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  background: rgba(75, 85, 99, 0.75) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 9999 !important;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-delete-content {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-width: 550px;
  width: 90%;
  position: relative;
  z-index: 10000;
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

.upload-page {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: 2rem;
  color: var(--gray-900);
  margin-bottom: var(--spacing-sm);
}

.page-description {
  color: var(--gray-600);
  font-size: 1rem;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-weight: 500;
  color: var(--gray-700);
  margin-bottom: var(--spacing-sm);
}

.form-label i {
  color: var(--npc-primary);
  font-size: 1rem;
}

.label-icon {
  margin-right: var(--spacing-xs);
  color: var(--npc-primary);
}

.label-required {
  color: var(--error);
  margin-left: var(--spacing-xs);
}

.form-help {
  margin-top: var(--spacing-xs);
  font-size: 0.8125rem;
  color: var(--gray-500);
}

/* File Input Styling */
.file-input-wrapper {
  position: relative;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

/* Drag and Drop Zone */
.drag-drop-zone {
  position: relative;
  min-height: 200px;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 3px dashed var(--gray-300);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drag-drop-zone:hover {
  border-color: var(--npc-primary);
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 61, 130, 0.1);
}

.drag-drop-zone.drag-over {
  border-color: var(--npc-primary);
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border-style: solid;
  box-shadow: 0 0 0 4px rgba(0, 61, 130, 0.1);
  transform: scale(1.02);
}

.drag-drop-zone.has-file {
  border-color: #16a34a;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-style: solid;
}

.drag-drop-zone.error {
  border-color: #dc2626;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.drop-zone-content {
  text-align: center;
  width: 100%;
}

.drop-zone-icon {
  font-size: 4rem;
  color: var(--npc-primary);
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.drag-drop-zone.drag-over .drop-zone-icon {
  animation: bounce 0.5s ease-in-out infinite;
  color: var(--npc-secondary);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.drop-zone-text {
  margin-bottom: 1.5rem;
}

.drop-zone-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: 0.5rem;
}

.dragging-text {
  color: var(--npc-primary);
  font-weight: 700;
}

.drop-zone-subtitle {
  font-size: 0.9375rem;
  color: var(--gray-500);
  margin: 0;
}

.drop-zone-specs {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 500;
}

.spec-item i {
  color: var(--npc-primary);
}

/* File Preview */
.file-preview {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  width: 100%;
  padding: 1rem;
  background: white;
  border-radius: var(--radius-md);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.file-preview-icon {
  font-size: 3rem;
  color: #16a34a;
  flex-shrink: 0;
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.file-preview-info {
  flex: 1;
  min-width: 0;
}

.file-preview-name {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 1rem;
  margin-bottom: 0.5rem;
  word-break: break-word;
}

.file-preview-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-bottom: 0.5rem;
}

.file-size {
  font-weight: 500;
}

.file-type {
  color: var(--gray-500);
}

.file-validation {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #16a34a;
  font-size: 0.875rem;
  font-weight: 500;
}

.file-validation i {
  font-size: 1rem;
}

.btn-remove-file {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #fee2e2;
  color: #dc2626;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.btn-remove-file:hover {
  background: #dc2626;
  color: white;
  transform: rotate(90deg) scale(1.1);
}

.form-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: var(--spacing-sm);
  font-size: 0.875rem;
  color: #dc2626;
  font-weight: 500;
}

.form-error i {
  font-size: 1rem;
}

/* Upload Progress */
.upload-progress-section {
  padding: 1.5rem;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #93c5fd;
  border-radius: var(--radius-lg);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.progress-label {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 1rem;
}

.progress-percentage {
  font-weight: 700;
  color: var(--npc-primary);
  font-size: 1.125rem;
}

.progress-bar-container {
  height: 12px;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.75rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--npc-primary), var(--npc-secondary));
  border-radius: 6px;
  transition: width 0.3s ease;
  position: relative;
  overflow: hidden;
}

.progress-bar-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--gray-700);
  font-weight: 500;
}

.progress-status i {
  color: var(--npc-primary);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: var(--spacing-md);
}

.btn-icon {
  margin-right: var(--spacing-xs);
  font-size: 1rem;
}

.uploading-state {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.alert-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.alert-content strong {
  display: block;
  margin-bottom: var(--spacing-xs);
}

.alert-content p {
  margin: 0;
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

.filename.clickable {
  color: var(--npc-primary);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;
}

.filename.clickable:hover {
  color: var(--npc-secondary);
  text-decoration: underline;
}

.filename.clickable:visited {
  color: #8b5cf6;
}

.filename.clickable:visited:hover {
  color: #7c3aed;
  text-decoration: underline;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  width: auto;
  height: auto;
  border-radius: 0.375rem;
}

.btn-action i {
  font-size: 1.125rem;
}

.btn-view {
  color: var(--npc-primary);
}

.btn-view:hover:not(:disabled) {
  color: #ffffff;
  background-color: var(--npc-primary);
  padding: 0.375rem;
  transform: scale(1.05);
}

.btn-download {
  color: var(--npc-secondary);
}

.btn-download:hover:not(:disabled) {
  color: #ffffff;
  background-color: var(--npc-secondary);
  padding: 0.375rem;
  transform: scale(1.05);
}

.btn-delete-action {
  color: var(--error);
}

.btn-delete-action:hover:not(:disabled) {
  color: #ffffff;
  background-color: #ff0000;
  padding: 0.375rem;
  transform: scale(1.05);
}

.btn-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.btn-delete {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  background-color: transparent;
  color: var(--error);
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  width: auto;
  height: auto;
}

.btn-delete:hover:not(:disabled) {
  color: #ffffff;
  background-color: #ff0000;
  padding: 0.375rem;
  transform: scale(1.05);
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-delete i {
  font-size: 1.25rem;
}

/* Remove padding from delete button cell */
td:has(.btn-delete) {
  padding: 0.5rem;
  text-align: center;
  width: 50px;
}

/* Custom Dropdown Styles */
.custom-select-wrapper {
  position: relative;
  width: 100%;
}

.custom-select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 60px;
}

.custom-select-trigger:hover {
  border-color: var(--npc-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.05);
}

.custom-select-trigger.active {
  border-color: var(--npc-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.1);
}

.selected-plant-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex: 1;
}

.selected-plant-info {
  flex: 1;
  min-width: 0;
}

.selected-plant-name {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 0.9375rem;
  margin-bottom: 0.125rem;
}

.selected-plant-meta {
  font-size: 0.8125rem;
  color: var(--gray-600);
}

.placeholder-text {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--gray-500);
  font-size: 0.9375rem;
}

.dropdown-arrow {
  color: var(--gray-400);
  transition: transform 0.2s ease;
  flex-shrink: 0;
  font-size: 0.875rem;
}

.custom-select-trigger.active .dropdown-arrow {
  transform: rotate(180deg);
  color: var(--npc-primary);
}

.custom-select-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  z-index: 1000;
  max-height: 360px; /* Increased more to show all 6 plants */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dropdown-search {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.875rem;
  color: var(--gray-400);
  font-size: 0.875rem;
  pointer-events: none;
}

.dropdown-search-input {
  width: 100%;
  padding: 0.625rem 0.875rem 0.625rem 2.5rem;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.dropdown-search-input:focus {
  outline: none;
  border-color: var(--npc-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.1);
}

.dropdown-options {
  overflow-y: scroll; /* Always show scrollbar */
  max-height: 480px; /* Increased more to show all 6 plants */
  padding-bottom: 4rem; /* Much more padding to prevent cutoff */
  margin-bottom: 0.5rem; /* Add margin to create space from parent border */
}

/* Ensure scrollbar is always visible */
.dropdown-options::-webkit-scrollbar {
  width: 8px;
}

.dropdown-options::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.dropdown-options::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.dropdown-options::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.dropdown-option {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  cursor: pointer;
  transition: background-color 0.2s ease, border-left 0.2s ease, padding-left 0.2s ease;
  border-bottom: 1px solid var(--gray-100);
  border-left: 5px solid transparent;
  background-color: white;
}

.dropdown-option:last-child {
  border-bottom: none;
}

.custom-select-dropdown .dropdown-option:hover {
  background-color: #d4e3f7 !important;
  border-left-color: #003d82 !important;
  padding-left: var(--spacing-md);
  box-shadow: 0 2px 8px rgba(0, 61, 130, 0.2);
}

.custom-select-dropdown .dropdown-option:hover .option-name {
  color: #003d82;
  font-weight: 700;
}

.custom-select-dropdown .dropdown-option:hover .option-detail {
  color: #003d82;
}

.dropdown-option.selected {
  background-color: #e8f4f8;
  border-left-color: #00a651;
}

.custom-select-dropdown .dropdown-option.selected:hover {
  background-color: #c8dff0 !important;
  border-left-color: #003d82 !important;
  box-shadow: 0 2px 8px rgba(0, 61, 130, 0.25);
}

.option-content {
  flex: 1;
  min-width: 0;
}

.option-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-sm);
  margin-bottom: 0.25rem;
}

.option-name {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 0.9375rem;
}

.option-code {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--npc-primary);
  background: rgba(0, 61, 130, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  letter-spacing: 0.05em;
}

.option-details {
  display: flex;
  gap: var(--spacing-md);
  font-size: 0.8125rem;
  color: var(--gray-600);
}

.option-detail {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.option-detail i {
  font-size: 0.75rem;
  color: var(--gray-500);
}

.option-check {
  color: var(--npc-primary);
  font-size: 1.25rem;
  font-weight: bold;
  flex-shrink: 0;
}

/* Dropdown Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Delete Button Hover Effect in Recent Uploads */
.action-buttons :deep(.p-button-rounded) {
  transition: all 0.25s ease;
  width: 2.5rem;
  height: 2.5rem;
}

.action-buttons :deep(.p-button-rounded:hover) {
  background-color: #dc2626 !important;
  color: white !important;
  transform: scale(1.08);
  box-shadow: 0 3px 8px rgba(220, 38, 38, 0.3);
}

.action-buttons :deep(.p-button-rounded:active) {
  transform: scale(1.02);
}

.action-buttons :deep(.p-button-rounded .p-button-icon) {
  font-size: 1.125rem;
  transition: all 0.25s ease;
}

/* Empty State Styles */
.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #6c757d;
}

.empty-state-content {
  max-width: 300px;
  margin: 0 auto;
}

.empty-state-icon {
  font-size: 48px;
  color: #dee2e6;
  margin-bottom: 16px;
}

.empty-state h4 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #495057;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
}

/* Template Download Section */
.template-description {
  color: var(--gray-600);
  margin-bottom: 1.5rem;
  font-size: 0.9375rem;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.template-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px solid #e2e8f0;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.template-btn:hover {
  border-color: var(--npc-primary);
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 61, 130, 0.15);
}

.template-btn i {
  font-size: 2rem;
  color: var(--npc-secondary);
  flex-shrink: 0;
}

.template-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.template-name {
  font-weight: 600;
  color: var(--gray-900);
  font-size: 1rem;
}

.template-desc {
  font-size: 0.8125rem;
  color: var(--gray-600);
}

/* Delete Confirmation Modal - Matching Screenshot Design */
.modal-delete-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 2rem;
  background: linear-gradient(135deg, #ff9a3c 0%, #ff8c00 100%);
  position: relative;
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
  flex-shrink: 0;
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
  letter-spacing: -0.02em;
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
  flex-shrink: 0;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.close-btn i {
  font-size: 1.5rem;
  color: white;
  font-weight: bold;
}

/* White Body */
.modal-delete-body {
  padding: 2.5rem 2rem 2rem 2rem;
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
  line-height: 1.5;
}

.info-list li::before {
  content: '•';
  position: absolute;
  left: 0.5rem;
  color: #a0aec0;
  font-size: 1.25rem;
  line-height: 1.2;
}

.info-list li:last-child {
  color: #718096;
  font-weight: 500;
}

/* Footer with Buttons */
.modal-delete-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem 2rem 2rem;
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
  border: none;
}

.btn-cancel:hover {
  background: #f7fafc;
  color: #4a5568;
}

.btn-delete {
  background: #ef4444;
  color: white;
  min-width: 120px;
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
  transform: none;
}

.btn-delete i {
  font-size: 1rem;
}
.btn-archive {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: transparent;
  color: #f59e0b;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-archive:hover {
  background-color: #f59e0b;
  color: white;
  transform: scale(1.1);
}

.btn-archive i {
  font-size: 1.125rem;
}

/* Show Entries in Card Header */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.show-entries {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
}

.show-entries select {
  padding: 6px 10px;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.3s;
  background: white;
}

.show-entries select:focus {
  outline: none;
  border-color: #667eea;
}

/* Sortable Table Headers */
.table-container th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
  position: relative;
}

.table-container th.sortable.nowrap {
  white-space: nowrap;
}

.table-container th.sortable:hover {
  background-color: #f1f5f9;
}

.table-container th .sort-icon {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 6px;
  transition: color 0.2s ease;
  display: inline-block;
  vertical-align: middle;
}

.table-container th.sortable:hover .sort-icon {
  color: #64748b;
}

.table-container th .pi-sort-amount-up,
.table-container th .pi-sort-amount-down {
  color: #667eea;
  font-weight: bold;
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


/* Archive Button Styles */
.btn-archive {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: transparent;
  color: #f59e0b;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-archive:hover {
  background-color: #f59e0b;
  color: white;
  transform: scale(1.1);
}

.btn-archive i {
  font-size: 1.125rem;
}
