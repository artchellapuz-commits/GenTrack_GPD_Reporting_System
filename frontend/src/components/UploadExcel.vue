<template>
  <div class="upload-page">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">Upload Excel Report</h2>
      <p class="page-description">
        Upload generation reports for Agus Hydro-electric Power Plants. Supported format: .xlsx
      </p>
    </div>

    <!-- Upload Form Card -->
    <div class="card">
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
            <div class="file-input-wrapper">
              <input 
                type="file" 
                @change="handleFileSelect" 
                accept=".xlsx"
                class="file-input"
                id="file-upload"
                required
              />
              <label for="file-upload" class="file-input-label">
                <i class="pi pi-paperclip file-icon"></i>
                <span v-if="!selectedFile">Choose Excel file...</span>
                <span v-else class="file-name">{{ selectedFile.name }}</span>
              </label>
            </div>
            <p class="form-help">Maximum file size: 10MB. Format: .xlsx only</p>
          </div>

          <!-- Upload Button -->
          <div class="form-actions">
            <button 
              type="submit"
              :disabled="!selectedPlant || !selectedFile || uploading"
              class="btn btn-primary btn-lg"
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
    <div v-if="uploadHistory.length" class="card mt-5">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-history title-icon"></i>
          Recent Uploads
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
                <th>Status</th>
                <th>Records</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="upload in uploadHistory" :key="upload.id">
                <td>
                  <div class="file-cell">
                    <i class="pi pi-file file-icon-sm"></i>
                    {{ upload.original_filename }}
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
                  <button 
                    @click="confirmDelete(upload)"
                    class="btn-delete"
                    :disabled="deleting === upload.id"
                    title="Delete this upload and all associated records"
                  >
                    <i v-if="deleting !== upload.id" class="pi pi-trash"></i>
                    <i v-else class="pi pi-spin pi-spinner"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'UploadExcel',
  data() {
    return {
      plants: [],
      selectedPlant: '',
      selectedFile: null,
      uploading: false,
      message: '',
      messageType: '',
      uploadHistory: [],
      dropdownOpen: false,
      searchQuery: '',
      deleting: null,
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
        const response = await api.getUploadedFiles();
        this.uploadHistory = response.data.results || response.data;
      } catch (error) {
        console.error('Error loading upload history:', error);
      }
    },
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedPlant || !this.selectedFile) return;

      this.uploading = true;
      this.message = '';

      try {
        const response = await api.uploadExcel(this.selectedFile, this.selectedPlant);
        this.showMessage(
          `${response.data.records_imported} records imported successfully.`,
          'success'
        );
        this.selectedFile = null;
        this.selectedPlant = '';
        document.getElementById('file-upload').value = '';
        this.loadUploadHistory();
      } catch (error) {
        let errorMsg = error.response?.data?.error || 'Upload failed';
        
        // Make error message more helpful
        if (errorMsg.includes('Missing required columns')) {
          errorMsg = 'Invalid Excel file format!\n\n' +
                    'Your file is missing required columns. Please use the correct template.\n\n' +
                    'Required columns:\n' +
                    '• Date\n' +
                    '• Unit Number\n' +
                    '• Generation kWh\n' +
                    '• Operating Hours\n' +
                    '• Availability Hours\n' +
                    '• Forced Outage Hours\n' +
                    '• Scheduled Outage Hours\n\n' +
                    'Use the sample file: CORRECT_SAMPLE_AGUS1.xlsx';
        }
        
        this.showMessage(errorMsg, 'error');
      } finally {
        this.uploading = false;
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
      const confirmMsg = `Are you sure you want to delete "${upload.original_filename}"?\n\n` +
                        `This will permanently delete:\n` +
                        `- The uploaded file\n` +
                        `- ${upload.records_imported || 0} generation report records\n\n` +
                        `This action cannot be undone.`;
      
      if (confirm(confirmMsg)) {
        this.deleteUpload(upload.id);
      }
    },
    async deleteUpload(uploadId) {
      this.deleting = uploadId;
      
      try {
        const response = await api.deleteUploadedFile(uploadId);
        this.showMessage(
          `File deleted successfully. ${response.data.reports_deleted || 0} records removed.`,
          'success'
        );
        this.loadUploadHistory();
      } catch (error) {
        const errorMsg = error.response?.data?.error || 'Failed to delete file';
        this.showMessage(errorMsg, 'error');
      } finally {
        this.deleting = null;
      }
    }
  },
};
</script>

<style scoped>
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
}

.file-input-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background-color: var(--gray-50);
  border: 2px dashed var(--gray-300);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.file-input-label:hover {
  border-color: var(--npc-primary);
  background-color: rgba(0, 61, 130, 0.02);
}

.file-icon {
  font-size: 1.5rem;
  color: var(--npc-primary);
}

.file-name {
  color: var(--npc-primary);
  font-weight: 500;
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
  padding: 0.5rem;
  background-color: transparent;
  color: var(--error);
  border: 1px solid var(--error);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  min-width: 36px;
  min-height: 36px;
}

.btn-delete:hover:not(:disabled) {
  background-color: var(--error);
  color: white;
  transform: scale(1.05);
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-delete i {
  font-size: 1rem;
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
  max-height: 400px;
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
  overflow-y: auto;
  max-height: 320px;
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
</style>
