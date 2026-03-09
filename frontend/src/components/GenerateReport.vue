<template>
  <AppLayout>
    <div class="generate-report-page glass-background">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">Generate Excel Report</h2>
      <p class="page-description">
        Create and download customized generation reports
      </p>
    </div>

    <!-- Main Form Card -->
    <div class="card glass-card glass-fade-in">
      <div class="card-body">
        <form @submit.prevent="generateReport" class="report-form">
          <!-- Plant Selection -->
          <div class="form-section">
            <label class="section-label">
              <i class="pi pi-building"></i>
              Select Plant
            </label>
            <div class="plants-grid">
              <label 
                v-for="plant in plants" 
                :key="plant.code"
                class="plant-checkbox"
                :class="{ 'selected': selectedPlant === plant.code }"
              >
                <input 
                  type="radio" 
                  :value="plant.code" 
                  v-model="selectedPlant"
                  class="radio-input"
                />
                <div class="plant-info">
                  <span class="plant-name">{{ plant.name }}</span>
                  <span class="plant-code">{{ plant.code }}</span>
                </div>
                <i v-if="selectedPlant === plant.code" class="pi pi-check check-icon"></i>
              </label>
            </div>
          </div>

          <!-- Date Range -->
          <div class="form-row">
            <div class="form-field">
              <label class="field-label">
                <i class="pi pi-calendar"></i>
                {{ reportType === 'daily_status' ? 'Report Date' : 'Start Date' }}
              </label>
              <input 
                type="date" 
                v-model="startDate" 
                class="date-input glass-input"
                required
              />
              <p v-if="reportType === 'daily_status'" class="field-hint">
                <i class="pi pi-info-circle"></i>
                Daily report will be generated for this specific date
              </p>
            </div>

            <div v-if="reportType !== 'daily_status'" class="form-field">
              <label class="field-label">
                <i class="pi pi-calendar"></i>
                End Date
              </label>
              <input 
                type="date" 
                v-model="endDate" 
                class="date-input glass-input"
                required
              />
            </div>
          </div>

          <!-- Report Type -->
          <div class="form-field">
            <label class="field-label">
              <i class="pi pi-file"></i>
              Report Type
            </label>
            <div class="report-types">
              <label 
                v-for="type in reportTypes" 
                :key="type.value"
                class="report-type-option"
                :class="{ 'active': reportType === type.value }"
              >
                <input 
                  type="radio" 
                  :value="type.value" 
                  v-model="reportType"
                  class="radio-input"
                />
                <div class="type-content">
                  <i :class="type.icon"></i>
                  <div class="type-text">
                    <span class="type-name">{{ type.label }}</span>
                    <span class="type-desc">{{ type.description }}</span>
                  </div>
                </div>
              </label>
            </div>
          </div>

          <!-- Generate Button -->
          <button 
            type="submit"
            :disabled="!canGenerate || generating"
            class="btn-generate glass-button"
          >
            <i v-if="!generating" class="pi pi-download"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            <span>{{ generating ? 'Generating...' : 'Generate Report' }}</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Generation History -->
    <div v-if="generationHistory.length > 0" class="card glass-card glass-fade-in mt-4">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-history"></i>
          Generation History
        </h3>
        <div class="menu-wrapper">
          <button @click="toggleMenu" class="btn-menu" ref="menuButton">
            <i class="pi pi-ellipsis-v"></i>
          </button>
          <transition name="dropdown">
            <div v-if="showMenu" class="dropdown-menu" @click.stop>
              <button @click="clearHistory" class="menu-item menu-item-danger">
                <i class="pi pi-trash"></i>
                <span>Clear History</span>
              </button>
            </div>
          </transition>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="history-list">
          <div 
            v-for="(item, index) in generationHistory" 
            :key="index"
            class="history-item"
          >
            <div class="history-icon">
              <i class="pi pi-file-excel"></i>
            </div>
            <div class="history-details" @click="downloadHistoryReport(item)" style="cursor: pointer;">
              <div class="history-main">
                <span class="history-filename">{{ item.filename }}</span>
                <span class="history-plant-badge">{{ item.plantName }}</span>
              </div>
              <div class="history-meta">
                <span class="history-type">
                  <i class="pi pi-tag"></i>
                  {{ item.reportTypeName }}
                </span>
                <span class="history-exact-time">
                  <i class="pi pi-clock"></i>
                  {{ formatExactTime(item.timestamp) }}
                </span>
              </div>
            </div>
            <div class="history-actions">
              <button 
                @click="downloadHistoryReport(item)" 
                class="btn-download"
                title="Download this report"
              >
                <i class="pi pi-download"></i>
              </button>
              <button 
                @click="regenerateReport(item)" 
                class="btn-regenerate"
                title="Load parameters to regenerate"
              >
                <i class="pi pi-refresh"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import AppLayout from './AppLayout.vue';
import toast from '../utils/toast';

export default {
  name: 'GenerateReport',
  components: {
    AppLayout,
  },
  data() {
    return {
      plants: [],
      selectedPlant: '',
      startDate: '',
      endDate: '',
      reportType: 'psr',
      generating: false,
      generationHistory: [],
      showMenu: false,
      reportTypes: [
        {
          value: 'psr',
          label: 'Plant Status Report (PSR)',
          description: 'Official PSR format for Mindanao plants',
          icon: 'pi pi-file-excel'
        },
        {
          value: 'daily_status',
          label: 'Daily Plant Status Report',
          description: 'Daily status with capacity, load, and lake elevations',
          icon: 'pi pi-calendar'
        }
      ]
    };
  },
  computed: {
    canGenerate() {
      // For daily status report, only start date is required
      if (this.reportType === 'daily_status') {
        return this.selectedPlant && this.startDate;
      }
      // For other reports, both dates are required
      return this.selectedPlant && this.startDate && this.endDate;
    },
  },
  mounted() {
    this.loadPlants();
    this.loadGenerationHistory();
    document.addEventListener('click', this.closeMenu);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeMenu);
  },
  methods: {
    async loadPlants() {
      try {
        const response = await api.getPlants();
        // Handle both paginated and non-paginated responses
        this.plants = response.data.results || response.data;
        console.log('Loaded plants:', this.plants);
      } catch (error) {
        console.error('Error loading plants:', error);
        toast.error('Error loading plants: ' + (error.message || 'Unknown error'));
      }
    },
    
    loadGenerationHistory() {
      try {
        const history = localStorage.getItem('reportGenerationHistory');
        if (history) {
          this.generationHistory = JSON.parse(history);
          // Sort by timestamp descending (newest first)
          this.generationHistory.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        }
      } catch (error) {
        console.error('Error loading generation history:', error);
        this.generationHistory = [];
      }
    },
    
    saveToHistory(reportData) {
      try {
        const historyItem = {
          ...reportData,
          timestamp: new Date().toISOString(),
        };
        
        this.generationHistory.unshift(historyItem);
        
        // Keep only last 50 items
        if (this.generationHistory.length > 50) {
          this.generationHistory = this.generationHistory.slice(0, 50);
        }
        
        localStorage.setItem('reportGenerationHistory', JSON.stringify(this.generationHistory));
      } catch (error) {
        console.error('Error saving to history:', error);
      }
    },
    
    clearHistory() {
      if (confirm('Are you sure you want to clear all generation history?')) {
        this.generationHistory = [];
        localStorage.removeItem('reportGenerationHistory');
        this.showMenu = false;
        toast.success('History cleared successfully');
      }
    },
    
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    
    closeMenu(e) {
      if (this.$refs.menuButton && !this.$refs.menuButton.contains(e.target)) {
        this.showMenu = false;
      }
    },
    
    async regenerateReport(historyItem) {
      this.selectedPlant = historyItem.plantCode;
      this.startDate = historyItem.startDate;
      this.endDate = historyItem.endDate;
      this.reportType = historyItem.reportType;
      
      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
      toast.info('Report parameters loaded. Click "Generate Report" to regenerate.');
    },
    
    async downloadHistoryReport(historyItem) {
      if (this.generating) {
        toast.warning('Please wait for the current report to finish generating');
        return;
      }
      
      this.generating = true;
      toast.info('Downloading report...');

      try {
        const response = await api.generateReport({
          plant_codes: [historyItem.plantCode],
          start_date: historyItem.startDate,
          end_date: historyItem.endDate,
          report_type: historyItem.reportType,
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', historyItem.filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        toast.success('Report downloaded successfully!');
      } catch (error) {
        console.error('Download report error:', error);
        let errorMsg = 'Failed to download report';
        
        // Handle blob response errors
        if (error.response?.data instanceof Blob) {
          try {
            const text = await error.response.data.text();
            const errorData = JSON.parse(text);
            errorMsg = errorData.error || errorMsg;
          } catch (e) {
            errorMsg = error.response?.statusText || errorMsg;
          }
        } else if (error.response?.data?.error) {
          errorMsg = error.response.data.error;
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 6000);
      } finally {
        this.generating = false;
      }
    },
    
    formatDateRange(startDate, endDate) {
      if (startDate === endDate) {
        return new Date(startDate).toLocaleDateString();
      }
      return `${new Date(startDate).toLocaleDateString()} - ${new Date(endDate).toLocaleDateString()}`;
    },
    
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
      if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
      if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
      
      return date.toLocaleDateString();
    },
    
    formatExactTime(timestamp) {
      const date = new Date(timestamp);
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      };
      return date.toLocaleString('en-US', options);
    },
    
    async generateReport() {
      if (!this.canGenerate) return;

      this.generating = true;

      try {
        // For daily status report, automatically set end_date = start_date
        const endDateToUse = this.reportType === 'daily_status' ? this.startDate : this.endDate;
        
        const response = await api.generateReport({
          plant_codes: [this.selectedPlant],
          start_date: this.startDate,
          end_date: endDateToUse,
          report_type: this.reportType,
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        
        // Set filename based on report type
        const dateStr = this.startDate.replace(/-/g, '');
        let filename;
        if (this.reportType === 'daily_status') {
          filename = `DAILY_PLANT_STATUS_${dateStr}.xlsx`;
        } else {
          filename = `PLANT_STATUS_${dateStr}.xlsx`;
        }
        
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();

        // Save to history
        const selectedPlantObj = this.plants.find(p => p.code === this.selectedPlant);
        const reportTypeName = this.reportTypes.find(t => t.value === this.reportType)?.label || this.reportType;
        
        this.saveToHistory({
          filename,
          plantCode: this.selectedPlant,
          plantName: selectedPlantObj?.name || this.selectedPlant,
          startDate: this.startDate,
          endDate: endDateToUse,
          reportType: this.reportType,
          reportTypeName,
        });

        toast.success('Report generated successfully!');
      } catch (error) {
        console.error('Generate report error:', error);
        let errorMsg = 'Failed to generate report';
        
        // Handle blob response errors
        if (error.response?.data instanceof Blob) {
          try {
            const text = await error.response.data.text();
            const errorData = JSON.parse(text);
            errorMsg = errorData.error || errorMsg;
            
            // Add helpful hint if no data found
            if (errorMsg.includes('No data found')) {
              errorMsg += '. Please upload Excel files first in the Upload Excel Reports page.';
            }
          } catch (e) {
            errorMsg = error.response?.statusText || errorMsg;
          }
        } else if (error.response?.data?.error) {
          errorMsg = error.response.data.error;
          if (errorMsg.includes('No data found')) {
            errorMsg += '. Please upload Excel files first in the Upload Excel Reports page.';
          }
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 6000);
      } finally {
        this.generating = false;
      }
    },
  },
};
</script>

<style scoped>
.generate-report-page {
  max-width: 800px;
  margin: 0 auto;
}

/* Header */
.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.page-description {
  color: #718096;
  font-size: 0.9375rem;
  margin: 0;
}

/* Form */
.report-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section,
.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.section-label,
.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #2d3748;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-label i,
.field-label i {
  color: var(--npc-primary);
  font-size: 1rem;
}

/* Plants Grid */
.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.75rem;
}

.plant-checkbox {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.plant-checkbox:hover {
  border-color: var(--npc-primary);
  background: #edf2f7;
}

.plant-checkbox.selected {
  border-color: var(--npc-primary);
  background: rgba(0, 61, 130, 0.04);
}

.checkbox-input,
.radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.plant-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.plant-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #2d3748;
}

.plant-code {
  font-size: 0.75rem;
  color: #718096;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.check-icon {
  color: var(--npc-primary);
  font-size: 1.125rem;
  font-weight: bold;
}

/* Form Row */
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

/* Date Input */
.date-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  color: #2d3748;
  background: white;
  transition: all 0.2s ease;
}

.date-input:hover {
  border-color: #cbd5e0;
}

.date-input:focus {
  outline: none;
  border-color: var(--npc-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.1);
}

/* Field Hint */
.field-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
  font-size: 0.8125rem;
  color: #718096;
  font-style: italic;
}

.field-hint i {
  color: var(--npc-primary);
  font-size: 0.875rem;
}

/* Report Types */
.report-types {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.report-type-option {
  position: relative;
  display: flex;
  align-items: center;
  padding: 1.25rem;
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.report-type-option:hover {
  border-color: var(--npc-primary);
  background: #edf2f7;
}

.report-type-option.active {
  border-color: var(--npc-primary);
  background: rgba(0, 61, 130, 0.04);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.05);
}

.radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.type-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.type-content > i {
  font-size: 1.5rem;
  color: var(--npc-primary);
}

.type-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.type-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2d3748;
}

.type-desc {
  font-size: 0.8125rem;
  color: #718096;
}

/* Generate Button */
.btn-generate {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--npc-primary) 0%, #004a9f 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 61, 130, 0.2);
}

.btn-generate:active:not(:disabled) {
  transform: translateY(0);
}

.btn-generate:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-generate i {
  font-size: 1.125rem;
}

/* Responsive */
@media (max-width: 640px) {
  .plants-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

/* History Section */
.mt-4 {
  margin-top: 2rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.card-title i {
  color: var(--npc-primary);
  font-size: 1.25rem;
}

.menu-wrapper {
  position: relative;
}

.btn-menu {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  color: #718096;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-menu:hover {
  background: #f7fafc;
  color: #2d3748;
  border-color: #cbd5e0;
}

.btn-menu i {
  font-size: 1.125rem;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 180px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 1000;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  color: #2d3748;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.menu-item:hover {
  background: #f7fafc;
}

.menu-item-danger {
  color: #ef4444;
}

.menu-item-danger:hover {
  background: #fef2f2;
  color: #dc2626;
}

.menu-item i {
  font-size: 1rem;
}

.btn-clear-history {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-clear-history:hover {
  background: #ef4444;
  color: white;
}

.history-list {
  display: flex;
  flex-direction: column;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  transition: background-color 0.2s ease;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background-color: #f7fafc;
}

.history-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.history-icon i {
  font-size: 1.5rem;
  color: white;
}

.history-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.history-details:hover {
  color: var(--npc-primary);
}

.history-details:hover .history-filename {
  color: var(--npc-primary);
  text-decoration: underline;
}

.history-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.history-filename {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2d3748;
  transition: all 0.2s ease;
}

.history-plant-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  background: var(--npc-primary);
  color: white;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.025em;
}

.history-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.8125rem;
  color: #718096;
}

.history-meta > span {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.history-meta i {
  font-size: 0.75rem;
  color: #a0aec0;
}

.history-type {
  font-weight: 500;
}

.history-exact-time {
  color: #4a5568;
  font-weight: 500;
  background: #f7fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #e2e8f0;
}

.history-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-download,
.btn-regenerate {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: 1px solid;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-download {
  color: #10b981;
  border-color: #10b981;
}

.btn-download:hover {
  background: #10b981;
  color: white;
  transform: translateY(-2px);
}

.btn-regenerate {
  color: var(--npc-primary);
  border-color: var(--npc-primary);
}

.btn-regenerate:hover {
  background: var(--npc-primary);
  color: white;
  transform: rotate(180deg);
}

.btn-download i,
.btn-regenerate i {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .history-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .history-details {
    width: 100%;
  }
  
  .history-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .history-actions {
    align-self: flex-end;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
