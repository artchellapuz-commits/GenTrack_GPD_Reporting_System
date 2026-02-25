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
    <div class="card glass-card glass-fade-in
    ">
      <div class="card-body">
        <form @submit.prevent="generateReport" class="report-form">
          <!-- Plant Selection -->
          <div class="form-section">
            <label class="section-label">
              <i class="pi pi-building"></i>
              Select Plants
            </label>
            <div class="plants-grid">
              <label 
                v-for="plant in plants" 
                :key="plant.code"
                class="plant-checkbox"
                :class="{ 'selected': selectedPlants.includes(plant.code) }"
              >
                <input 
                  type="checkbox" 
                  :value="plant.code" 
                  v-model="selectedPlants"
                  class="checkbox-input"
                />
                <div class="plant-info">
                  <span class="plant-name">{{ plant.name }}</span>
                  <span class="plant-code">{{ plant.code }}</span>
                </div>
                <i v-if="selectedPlants.includes(plant.code)" class="pi pi-check check-icon"></i>
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

    <!-- Alert Messages -->
    <transition name="fade">
      <div v-if="message" :class="['alert', `alert-${messageType}`]">
        <i :class="['pi', messageType === 'success' ? 'pi-check-circle' : 'pi-times-circle']"></i>
        <span>{{ message }}</span>
      </div>
    </transition>
  </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import AppLayout from './AppLayout.vue';

export default {
  name: 'GenerateReport',
  components: {
    AppLayout,
  },
  data() {
    return {
      plants: [],
      selectedPlants: [],
      startDate: '',
      endDate: '',
      reportType: 'psr',
      generating: false,
      message: '',
      messageType: '',
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
        return this.selectedPlants.length > 0 && this.startDate;
      }
      // For other reports, both dates are required
      return this.selectedPlants.length > 0 && this.startDate && this.endDate;
    },
  },
  mounted() {
    this.loadPlants();
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
        this.showMessage('Error loading plants: ' + (error.message || 'Unknown error'), 'error');
      }
    },
    async generateReport() {
      if (!this.canGenerate) return;

      this.generating = true;
      this.message = '';

      try {
        // For daily status report, automatically set end_date = start_date
        const endDateToUse = this.reportType === 'daily_status' ? this.startDate : this.endDate;
        
        const response = await api.generateReport({
          plant_codes: this.selectedPlants,
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

        this.showMessage('Report generated successfully!', 'success');
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
        
        this.showMessage(errorMsg, 'error');
      } finally {
        this.generating = false;
      }
    },
    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = '';
      }, 5000);
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

.checkbox-input {
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

/* Alert */
.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  margin-top: 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 500;
}

.alert i {
  font-size: 1.25rem;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border-left: 4px solid #28a745;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border-left: 4px solid #dc3545;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
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
</style>
