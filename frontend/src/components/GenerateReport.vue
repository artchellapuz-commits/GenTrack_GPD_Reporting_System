<template>
  <AppLayout>
    <div class="generate-report-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h2 class="page-title">
            <i class="pi pi-file-excel title-icon"></i>
            Generate Excel Report
          </h2>
          <p class="page-description">
            Create and download customized generation reports for all {{ plants.length }} power plants
          </p>
        </div>
        <div class="header-info">
          <div class="info-badge success">
            <i class="pi pi-check-circle"></i>
            <span>All Plants Included</span>
          </div>
          <div class="info-badge primary">
            <i class="pi pi-file-excel"></i>
            <span>PSR Format</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Form Card -->
    <div class="main-card">
      <div class="card-header">
        <div class="card-title">
          <i class="pi pi-calendar-plus"></i>
          <span>Report Configuration</span>
        </div>
        <div class="card-subtitle">
          Select the date for your comprehensive plant status report
        </div>
      </div>
      
      <div class="card-body">
        <form @submit.prevent="generateReport" class="report-form">
          <!-- Date Selection -->
          <div class="form-field">
            <label class="field-label">
              <i class="pi pi-calendar"></i>
              Report Date
            </label>
            <div class="date-input-wrapper">
              <input 
                type="date" 
                v-model="reportDate" 
                class="date-input"
                required
                :class="{ 'has-value': reportDate }"
                style="color: #000000 !important; background: #ffffff !important; border: 2px solid #d1d5db !important;"
              />
              <div class="input-border"></div>
            </div>
            <div class="field-hint">
              <i class="pi pi-info-circle"></i>
              <span>Generate report for the selected date across all power plants</span>
            </div>
          </div>

          <!-- Generate Button -->
          <div class="button-section">
            <button 
              type="submit"
              :disabled="!canGenerate || generating"
              class="btn-generate btn-generate-prominent"
              :class="{ 'generating': generating }"
            >
              <div class="btn-content">
                <div class="btn-icon">
                  <i v-if="!generating" class="pi pi-eye"></i>
                  <i v-else class="pi pi-spin pi-spinner"></i>
                </div>
                <span class="btn-text">{{ generating ? 'Loading Preview...' : 'Preview Report' }}</span>
              </div>
              <div class="btn-ripple"></div>
            </button>
            
            <div v-if="!canGenerate" class="validation-message">
              <i class="pi pi-exclamation-triangle"></i>
              <span v-if="!reportDate">Please select a report date to continue</span>
              <span v-else-if="!selectedPlants || selectedPlants.length === 0">Loading plants... Please wait</span>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Report Preview Section -->
    <div v-if="showPreview && reportPreview" class="preview-card">
      <div class="card-header">
        <div class="card-title">
          <i class="pi pi-file-excel"></i>
          <span>Excel Report Preview</span>
        </div>
        <div class="preview-actions">
          <button @click="downloadExcel" class="btn-download-excel" style="color: #ffffff !important; background: #10b981 !important; border: 2px solid #10b981 !important;">
            <i class="pi pi-download" style="color: #ffffff !important;"></i>
            <span style="color: #ffffff !important; font-weight: 600 !important;">Download Excel</span>
          </button>
          <button @click="closePreview" class="btn-close-preview" style="background: #ffffff !important; color: #000000 !important; border: 3px solid #000000 !important; display: flex !important; visibility: visible !important; opacity: 1 !important;">
            <i class="pi pi-times" style="color: #000000 !important; font-size: 1.4rem !important; font-weight: 900 !important;"></i>
          </button>
        </div>
      </div>
      
      <div class="card-body">
        <!-- Excel-like Header -->
        <div class="excel-header">
          <div class="header-row title-row">
            <div class="header-cell title-cell">{{ reportPreview.header.title }}</div>
          </div>
          <div class="header-row subtitle-row">
            <div class="header-cell subtitle-cell">{{ reportPreview.header.subtitle }}</div>
          </div>
          <div class="header-row portfolio-row">
            <div class="header-cell portfolio-cell">{{ reportPreview.header.portfolio }}</div>
          </div>
          <div class="header-row date-row">
            <div class="header-cell date-cell">{{ reportPreview.header.date_text }}</div>
          </div>
        </div>

        <!-- Excel-like Table -->
        <div class="excel-table-container">
          <table class="excel-table">
            <thead>
              <tr class="excel-header-row">
                <th class="excel-th plant-col">PLANT</th>
                <th class="excel-th capacity-col">CAPACITY<br>(MW)</th>
                <th class="excel-th nominated-col">NOMINATED<br>(MW)</th>
                <th class="excel-th actual-col">ACTUAL<br>(MW)</th>
                <th class="excel-th variance-col">VARIANCE<br>(MW)</th>
                <th class="excel-th hours-col">OPERATING<br>HOURS</th>
                <th class="excel-th outage-col">FORCED<br>OUTAGE</th>
                <th class="excel-th outage-col">SCHEDULED<br>OUTAGE</th>
                <th class="excel-th remarks-col">REMARKS</th>
              </tr>
            </thead>
            <tbody>
              <!-- Plant Data -->
              <template v-for="plant in reportPreview.plants_data" :key="plant.code">
                <!-- Plant Header Row -->
                <tr class="plant-header-row">
                  <td class="excel-td plant-name-cell" :colspan="9">{{ plant.name }}</td>
                </tr>
                <!-- Unit Rows -->
                <tr v-for="unit in plant.units" :key="`${plant.code}-${unit.number}`" class="unit-row">
                  <td class="excel-td unit-cell">{{ unit.label }}</td>
                  <td class="excel-td number-cell">{{ unit.capacity }}</td>
                  <td class="excel-td number-cell">{{ unit.nominated }}</td>
                  <td class="excel-td number-cell">{{ unit.actual }}</td>
                  <td class="excel-td number-cell" :class="{ 'negative': unit.variance < 0 }">{{ unit.variance }}</td>
                  <td class="excel-td number-cell">{{ unit.operating_hours }}</td>
                  <td class="excel-td number-cell">{{ unit.forced_outage }}</td>
                  <td class="excel-td number-cell">{{ unit.scheduled_outage }}</td>
                  <td class="excel-td remarks-cell">{{ unit.remarks || '-' }}</td>
                </tr>
                <!-- Plant Total Row -->
                <tr class="plant-total-row">
                  <td class="excel-td total-label-cell">{{ plant.name }} TOTAL</td>
                  <td class="excel-td total-number-cell">{{ plant.plant_totals.capacity }}</td>
                  <td class="excel-td total-number-cell">{{ plant.plant_totals.nominated }}</td>
                  <td class="excel-td total-number-cell">{{ plant.plant_totals.actual }}</td>
                  <td class="excel-td total-number-cell" :class="{ 'negative': plant.plant_totals.variance < 0 }">{{ plant.plant_totals.variance }}</td>
                  <td class="excel-td total-number-cell" colspan="4">-</td>
                </tr>
              </template>
              
              <!-- Grand Total Row -->
              <tr class="grand-total-row">
                <td class="excel-td grand-total-label">PSALM TOTAL</td>
                <td class="excel-td grand-total-number">{{ reportPreview.totals.total_capacity }}</td>
                <td class="excel-td grand-total-number">{{ reportPreview.totals.total_nominated }}</td>
                <td class="excel-td grand-total-number">{{ reportPreview.totals.total_actual }}</td>
                <td class="excel-td grand-total-number" :class="{ 'negative': reportPreview.totals.total_variance < 0 }">{{ reportPreview.totals.total_variance }}</td>
                <td class="excel-td grand-total-number" colspan="4">-</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Forecasted Load Section -->
        <div class="excel-section forecasted-load-section">
          <h4 class="section-title">FORECASTED LOAD</h4>
          <table class="excel-table small-table">
            <tbody>
              <tr>
                <td class="excel-td label-cell">Mindanao</td>
                <td class="excel-td number-cell">{{ reportPreview.forecasted_load.mindanao_load }} MW</td>
              </tr>
              <tr>
                <td class="excel-td label-cell">Luzon + Visayas</td>
                <td class="excel-td number-cell">{{ reportPreview.forecasted_load.luzon_visayas }} MW</td>
              </tr>
              <tr class="total-row">
                <td class="excel-td total-label-cell">Total Philippines</td>
                <td class="excel-td total-number-cell">{{ reportPreview.forecasted_load.total_philippines }} MW</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- IPP Section -->
        <div class="excel-section ipp-section">
          <h4 class="section-title">INDEPENDENT POWER PRODUCERS (IPP)</h4>
          <table class="excel-table">
            <thead>
              <tr class="excel-header-row">
                <th class="excel-th">IPP PLANT</th>
                <th class="excel-th">CAPACITY (MW)</th>
                <th class="excel-th">NOMINATED (MW)</th>
                <th class="excel-th">ACTUAL (MW)</th>
                <th class="excel-th">VARIANCE (MW)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ipp in reportPreview.ipp_data" :key="ipp.name" class="ipp-row">
                <td class="excel-td">{{ ipp.name }}</td>
                <td class="excel-td number-cell">{{ ipp.capacity }}</td>
                <td class="excel-td number-cell">{{ ipp.nominated }}</td>
                <td class="excel-td number-cell">{{ ipp.actual }}</td>
                <td class="excel-td number-cell" :class="{ 'negative': ipp.variance < 0 }">{{ ipp.variance }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Notes Section -->
        <div class="excel-section notes-section">
          <h4 class="section-title">NOTES</h4>
          <ul class="notes-list">
            <li v-for="note in reportPreview.notes" :key="note">{{ note }}</li>
          </ul>
        </div>

        <!-- Signature Sections -->
        <div class="excel-section signatures-section">
          <h4 class="section-title">AUTHORIZATION</h4>
          
          <!-- First Row of Signatures -->
          <div class="signature-row">
            <table class="signature-table">
              <thead>
                <tr>
                  <th v-for="sig in reportPreview.signatures.first_row" :key="sig.name" class="signature-header">
                    {{ sig.role }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <!-- Signature space -->
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`space-${sig.name}`" class="signature-cell">
                    &nbsp;
                  </td>
                </tr>
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`space2-${sig.name}`" class="signature-cell">
                    &nbsp;
                  </td>
                </tr>
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`space3-${sig.name}`" class="signature-cell">
                    &nbsp;
                  </td>
                </tr>
                <!-- Names -->
                <tr class="signature-names">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`name-${sig.name}`" class="signature-name">
                    {{ sig.name }}
                  </td>
                </tr>
                <!-- Titles -->
                <tr class="signature-titles">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`title-${sig.name}`" class="signature-title">
                    {{ sig.title }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Second Row of Signatures -->
          <div class="signature-row">
            <table class="signature-table">
              <thead>
                <tr>
                  <th v-for="sig in reportPreview.signatures.second_row" :key="sig.name" class="signature-header">
                    {{ sig.role }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <!-- Signature space -->
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`space-${sig.name}`" class="signature-cell">
                    &nbsp;
                  </td>
                </tr>
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`space2-${sig.name}`" class="signature-cell">
                    &nbsp;
                  </td>
                </tr>
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`space3-${sig.name}`" class="signature-cell">
                    &nbsp;
                  </td>
                </tr>
                <!-- Names -->
                <tr class="signature-names">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`name-${sig.name}`" class="signature-name">
                    {{ sig.name }}
                  </td>
                </tr>
                <!-- Titles -->
                <tr class="signature-titles">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`title-${sig.name}`" class="signature-title">
                    {{ sig.title }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Footer Note -->
        <div class="excel-section footer-note-section">
          <p class="footer-note">{{ reportPreview.footer_note }}</p>
        </div>
      </div>
    </div>

    <!-- Generation History -->
    <div v-if="generationHistory.length > 0" class="history-card">
      <div class="card-header">
        <div class="card-title" style="color: #000000 !important;">
          <i class="pi pi-history" style="color: #000000 !important;"></i>
          <span style="color: #000000 !important;">Recent Reports</span>
        </div>
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
            @click="downloadHistoryReport(item)"
          >
            <div class="history-icon">
              <i class="pi pi-file-excel"></i>
            </div>
            <div class="history-details">
              <div class="history-main">
                <span class="history-filename" style="color: #000000 !important;">{{ item.filename }}</span>
                <span class="history-plant-badge" style="color: #000000 !important;">{{ item.plantName }}</span>
              </div>
              <div class="history-meta">
                <span class="history-type" style="color: #000000 !important;">
                  <i class="pi pi-tag" style="color: #000000 !important;"></i>
                  {{ item.reportTypeName }}
                </span>
                <span class="history-exact-time" style="color: #000000 !important;">
                  <i class="pi pi-clock" style="color: #000000 !important;"></i>
                  {{ formatExactTime(item.timestamp) }}
                </span>
              </div>
            </div>
            <div class="history-actions">
              <button 
                @click.stop="downloadHistoryReport(item)" 
                class="btn-download"
                title="Download this report"
              >
                <i class="pi pi-download"></i>
              </button>
              <button 
                @click.stop="regenerateReport(item)" 
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
      selectedPlants: [],
      reportDate: '',
      reportType: 'psr',
      generating: false,
      generationHistory: [],
      showMenu: false,
      reportPreview: null,
      showPreview: false,
      reportTypes: [
        {
          value: 'psr',
          label: 'Plant Status Report (PSR)',
          description: 'Official PSR format for Mindanao plants',
          icon: 'pi pi-file-excel'
        }
      ]
    };
  },
  computed: {
    canGenerate() {
      // Require both report date and plants to be loaded
      return this.reportDate && this.selectedPlants && this.selectedPlants.length > 0;
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
        
        // Always select all plants automatically
        this.selectedPlants = this.plants.map(plant => plant.code);
        console.log('Selected plants:', this.selectedPlants);
        
        // Ensure we have plants selected
        if (this.selectedPlants.length === 0) {
          console.warn('No plants were selected after loading');
          toast.warning('No plants available for report generation');
        } else {
          console.log(`Successfully loaded ${this.selectedPlants.length} plants:`, this.selectedPlants);
        }
      } catch (error) {
        console.error('Error loading plants:', error);
        toast.error('Error loading plants: ' + (error.message || 'Unknown error'));
        
        // Fallback: try to use hardcoded plant codes if API fails
        console.log('Attempting fallback with hardcoded plant codes...');
        this.selectedPlants = ['AGUS1', 'AGUS2', 'AGUS4', 'AGUS5', 'AGUS6', 'AGUS7', 'PULANGI4'];
        this.plants = this.selectedPlants.map(code => ({ code, name: code }));
        toast.info('Using fallback plant codes. Some features may be limited.');
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
      this.selectedPlants = [historyItem.plantCode];
      this.reportDate = historyItem.reportDate;
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
        // Parse plant codes - they might be comma-separated
        const plantCodes = historyItem.plantCode.includes(',') 
          ? historyItem.plantCode.split(',').map(code => code.trim())
          : [historyItem.plantCode];

        console.log('Downloading history report with data:', {
          plant_codes: plantCodes,
          start_date: historyItem.reportDate,
          end_date: historyItem.reportDate,
          report_type: historyItem.reportType,
        });

        const response = await api.generateReport({
          plant_codes: plantCodes,
          start_date: historyItem.reportDate,
          end_date: historyItem.reportDate,
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
        console.error('Error response:', error.response);
        console.error('Error response data:', error.response?.data);
        
        let errorMsg = 'Failed to download report';
        
        // Handle blob response errors
        if (error.response?.data instanceof Blob) {
          try {
            const text = await error.response.data.text();
            console.error('Blob error text:', text);
            const errorData = JSON.parse(text);
            errorMsg = errorData.error || errorMsg;
            
            // Show detailed validation errors if available
            if (errorData.plant_codes) {
              errorMsg = `Plant validation error: ${errorData.plant_codes.join(', ')}`;
            }
            if (errorData.start_date) {
              errorMsg = `Date validation error: ${errorData.start_date.join(', ')}`;
            }
            if (errorData.end_date) {
              errorMsg = `Date validation error: ${errorData.end_date.join(', ')}`;
            }
          } catch (e) {
            console.error('Error parsing blob:', e);
            errorMsg = error.response?.statusText || errorMsg;
          }
        } else if (error.response?.data?.error) {
          errorMsg = error.response.data.error;
        } else if (error.response?.data) {
          // Handle validation errors
          const data = error.response.data;
          console.error('Validation error data:', data);
          
          if (data.plant_codes) {
            errorMsg = `Plant validation error: ${Array.isArray(data.plant_codes) ? data.plant_codes.join(', ') : data.plant_codes}`;
          } else if (data.start_date) {
            errorMsg = `Start date validation error: ${Array.isArray(data.start_date) ? data.start_date.join(', ') : data.start_date}`;
          } else if (data.end_date) {
            errorMsg = `End date validation error: ${Array.isArray(data.end_date) ? data.end_date.join(', ') : data.end_date}`;
          } else if (data.non_field_errors) {
            errorMsg = `Validation error: ${Array.isArray(data.non_field_errors) ? data.non_field_errors.join(', ') : data.non_field_errors}`;
          } else if (data.detail) {
            errorMsg = `API error: ${data.detail}`;
          } else {
            errorMsg = `Validation error: ${JSON.stringify(data)}`;
          }
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 8000);
      } finally {
        this.generating = false;
      }
    },
    
    formatDateRange(reportDate) {
      return new Date(reportDate).toLocaleDateString();
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

      // Ensure we have plants selected
      if (!this.selectedPlants || this.selectedPlants.length === 0) {
        toast.error('No plants selected. Please wait for plants to load or refresh the page.');
        return;
      }

      // Validate date format (should be YYYY-MM-DD)
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateRegex.test(this.reportDate)) {
        toast.error('Invalid date format. Please select a valid date.');
        return;
      }

      console.log('Generating report preview with data:', {
        plant_codes: this.selectedPlants,
        start_date: this.reportDate,
        end_date: this.reportDate,
        report_type: this.reportType,
      });

      this.generating = true;

      try {
        const response = await api.previewReport({
          plant_codes: this.selectedPlants,
          start_date: this.reportDate,
          end_date: this.reportDate,
          report_type: this.reportType,
        });

        this.reportPreview = response.data;
        this.showPreview = true;
        
        // Scroll to preview section
        this.$nextTick(() => {
          const previewElement = document.querySelector('.preview-card');
          if (previewElement) {
            previewElement.scrollIntoView({ behavior: 'smooth' });
          }
        });

        toast.success('Report preview loaded successfully!');
      } catch (error) {
        console.error('Generate report preview error:', error);
        console.error('Error response:', error.response);
        console.error('Error response data:', error.response?.data);
        
        let errorMsg = 'Failed to generate report preview';
        
        // Handle validation errors
        if (error.response?.data) {
          const data = error.response.data;
          console.error('Validation error data:', data);
          
          if (data.plant_codes) {
            errorMsg = `Plant validation error: ${Array.isArray(data.plant_codes) ? data.plant_codes.join(', ') : data.plant_codes}`;
          } else if (data.start_date) {
            errorMsg = `Start date validation error: ${Array.isArray(data.start_date) ? data.start_date.join(', ') : data.start_date}`;
          } else if (data.end_date) {
            errorMsg = `End date validation error: ${Array.isArray(data.end_date) ? data.end_date.join(', ') : data.end_date}`;
          } else if (data.non_field_errors) {
            errorMsg = `Validation error: ${Array.isArray(data.non_field_errors) ? data.non_field_errors.join(', ') : data.non_field_errors}`;
          } else if (data.detail) {
            errorMsg = `API error: ${data.detail}`;
          } else if (data.error) {
            errorMsg = data.error;
            if (errorMsg.includes('No data found')) {
              errorMsg += '. Please upload Excel files first in the Upload Excel Reports page.';
            }
          } else {
            errorMsg = `Validation error: ${JSON.stringify(data)}`;
          }
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 8000);
      } finally {
        this.generating = false;
      }
    },

    async downloadExcel() {
      if (!this.reportPreview) return;

      this.generating = true;
      toast.info('Generating Excel file...');

      try {
        const response = await api.generateReport({
          plant_codes: this.selectedPlants,
          start_date: this.reportDate,
          end_date: this.reportDate,
          report_type: this.reportType,
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        
        // Set filename based on report date
        const dateStr = this.reportDate.replace(/-/g, '');
        const filename = `PLANT_STATUS_${dateStr}.xlsx`;
        
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        // Save to history
        const selectedPlantNames = this.plants
          .filter(p => this.selectedPlants.includes(p.code))
          .map(p => p.name)
          .join(', ');
        const reportTypeName = this.reportTypes.find(t => t.value === this.reportType)?.label || this.reportType;
        
        this.saveToHistory({
          filename,
          plantCode: this.selectedPlants.join(','),
          plantName: selectedPlantNames,
          reportDate: this.reportDate,
          reportType: this.reportType,
          reportTypeName,
        });

        toast.success('Excel file downloaded successfully!');
      } catch (error) {
        console.error('Download Excel error:', error);
        toast.error('Failed to download Excel file: ' + (error.message || 'Unknown error'), 6000);
      } finally {
        this.generating = false;
      }
    },

    closePreview() {
      this.showPreview = false;
      this.reportPreview = null;
    },

    formatNumber(value) {
      if (!value) return '0';
      return new Intl.NumberFormat().format(value);
    },

    formatDate(dateString) {
      if (!dateString) return '-';
      return new Date(dateString).toLocaleDateString();
    },
  },
};
</script>
<style scoped>
/* Variables */
:root {
  --primary-color: #003d82;
  --primary-light: #0056b3;
  --primary-dark: #002a5c;
  --success-color: #10b981;
  --success-light: #34d399;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --border-color: #e5e7eb;
  --border-light: #f3f4f6;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
}

/* Main Container */
.generate-report-page {
  width: 100%;
  margin: 0;
  padding: 1rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* Header */
.page-header {
  margin-bottom: 3rem;
  text-align: center;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.title-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.025em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title-icon {
  font-size: 2.25rem;
  color: var(--primary-color);
  filter: drop-shadow(0 2px 4px rgba(0, 61, 130, 0.2));
}

.page-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
  line-height: 1.6;
}
.header-info {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.info-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-lg);
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--shadow-md);
}

.info-badge.success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  color: var(--success-color);
  border-color: rgba(16, 185, 129, 0.2);
}

.info-badge.primary {
  background: linear-gradient(135deg, rgba(0, 61, 130, 0.1) 0%, rgba(0, 61, 130, 0.05) 100%);
  color: var(--primary-color);
  border-color: rgba(0, 61, 130, 0.2);
}

.info-badge:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.info-badge i {
  font-size: 1rem;
}

/* Main Card */
.main-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  margin-bottom: 2rem;
  border: 1px solid var(--border-light);
  backdrop-filter: blur(20px);
  width: 100%;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

/* When preview is shown, make main card smaller */
.generate-report-page:has(.preview-card) .main-card {
  max-width: 600px;
}

.card-header {
  padding: 2rem 2rem 1rem 2rem;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-bottom: 1px solid var(--border-light);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #000000 !important;
  margin: 0 0 0.5rem 0;
}

.card-title span {
  color: #000000 !important;
}

.card-title i {
  color: #000000 !important;
}

.card-title i {
  color: var(--primary-color);
  font-size: 1.375rem;
}

.card-subtitle {
  font-size: 0.9375rem;
  color: var(--text-secondary);
  margin: 0;
}

.card-body {
  padding: 2rem;
}
/* Form */
.report-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field-label i {
  color: var(--primary-color);
  font-size: 1rem;
}

/* Date Input */
.date-input-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
}

.date-input {
  width: 100%;
  padding: 1rem 1.25rem;
  font-size: 1rem;
  color: #000000 !important;
  background: #ffffff !important;
  border: 2px solid #d1d5db !important;
  border-radius: var(--radius-lg);
  transition: all 0.3s ease;
  outline: none;
  font-family: inherit;
  font-weight: 500;
}

.date-input:hover {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.date-input:focus {
  border-color: #2563eb !important;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
  transform: translateY(-1px);
}

.date-input.has-value {
  border-color: #10b981 !important;
  background: #ffffff !important;
  color: #000000 !important;
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-light) 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}

.date-input:focus + .input-border {
  transform: scaleX(1);
}
.field-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--text-muted);
  font-style: italic;
}

.field-hint i {
  color: var(--primary-color);
  font-size: 0.875rem;
}

/* Button Section */
.button-section {
  display: flex !important;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
  visibility: visible !important;
  margin: 2rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(248, 250, 252, 0.8) 0%, rgba(241, 245, 249, 0.6) 100%);
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  backdrop-filter: blur(10px);
}

.btn-generate {
  position: relative;
  display: flex !important;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 450px;
  padding: 1.25rem 2.5rem;
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
  color: #1f2937 !important;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
  visibility: visible !important;
  opacity: 1 !important;
  text-transform: none;
  letter-spacing: 0.025em;
  backdrop-filter: blur(10px);
}

.btn-generate::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transition: left 0.5s;
}

.btn-generate:hover::before {
  left: 100%;
}

.btn-generate-prominent {
  animation: none;
  border: 2px solid #3b82f6;
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
}

.btn-generate-prominent:hover:not(:disabled) {
  border-color: #2563eb;
  box-shadow: 
    0 10px 15px -3px rgba(59, 130, 246, 0.2),
    0 4px 6px -2px rgba(59, 130, 246, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  border-color: #3b82f6;
  background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
}

.btn-generate:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
}

.btn-generate:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed;
  transform: none;
  display: flex !important;
  visibility: visible !important;
  animation: none;
  background: linear-gradient(145deg, #f3f4f6 0%, #e5e7eb 100%);
  border-color: #d1d5db;
  color: #9ca3af !important;
  box-shadow: 
    0 1px 2px 0 rgba(0, 0, 0, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
}

.btn-generate.generating {
  background: linear-gradient(135deg, var(--text-secondary) 0%, var(--text-muted) 100%);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 2;
  position: relative;
}

.btn-icon {
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  color: #3b82f6 !important;
  transition: color 0.3s ease;
}

.btn-text {
  font-weight: 600;
  letter-spacing: 0.025em;
  font-size: 1.1rem;
  color: #1f2937 !important;
  transition: color 0.3s ease;
}
.btn-ripple {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  transform: scale(0);
  transition: transform 0.6s ease;
  z-index: 1;
}

.btn-generate:active .btn-ripple {
  transform: scale(1);
}

.validation-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
  color: var(--warning-color);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
}

.validation-message i {
  font-size: 1rem;
}

/* History Card */
.history-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.history-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
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
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-menu:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border-color: var(--primary-color);
}
.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 180px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
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
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.menu-item:hover {
  background: var(--bg-secondary);
}

.menu-item-danger {
  color: var(--danger-color);
}

.menu-item-danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

/* History List */
.history-list {
  display: flex;
  flex-direction: column;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border-light);
  transition: all 0.2s ease;
  cursor: pointer;
  color: #000000 !important;
}

.history-item * {
  color: #000000 !important;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background: var(--bg-secondary);
  transform: translateX(4px);
}
.history-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--success-color) 0%, var(--success-light) 100%);
  border-radius: var(--radius-lg);
  flex-shrink: 0;
  box-shadow: var(--shadow-md);
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
  color: #000000 !important;
}

.history-details * {
  color: #000000 !important;
}

.history-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  color: #000000 !important;
}

.history-main * {
  color: #000000 !important;
}

.history-filename {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #000000 !important;
}

.history-plant-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: #000000 !important;
  border-radius: var(--radius-sm);
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
  color: #000000 !important;
}

.history-meta * {
  color: #000000 !important;
}

.history-meta > span {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: #000000 !important;
}

.history-type {
  font-weight: 500;
  color: #000000 !important;
}

.history-exact-time {
  color: #000000 !important;
  background: #f5f5f5 !important;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  border: 1px solid #d0d0d0 !important;
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
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-download {
  color: var(--success-color);
  border-color: var(--success-color);
}

.btn-download:hover {
  background: var(--success-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-regenerate {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-regenerate:hover {
  background: var(--primary-color);
  color: white;
  transform: rotate(180deg);
}

/* Responsive Design */
@media (max-width: 768px) {
  .generate-report-page {
    padding: 1rem 0.5rem;
  }
  
  .page-title {
    font-size: 2rem;
    flex-direction: column;
    text-align: center;
  }
  
  .header-info {
    flex-direction: column;
    width: 100%;
  }
  
  .info-badge {
    justify-content: center;
  }
  
  .card-header,
  .card-body {
    padding: 1.5rem 1rem;
  }
  
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .history-details {
    width: 100%;
  }
  
  .history-actions {
    align-self: flex-end;
  }
  
  .btn-generate {
    font-size: 1rem;
    padding: 1rem 1.5rem;
  }
}
@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  
  .card-title {
    font-size: 1.25rem;
  }
  
  .history-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

/* Animation Classes */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-card,
.history-card,
.preview-card {
  animation: fadeInUp 0.6s ease-out;
}

.history-card {
  animation-delay: 0.2s;
}

.preview-card {
  animation-delay: 0.3s;
}

/* Preview Card Styles */
.preview-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  border: 1px solid var(--border-light);
  margin-bottom: 2rem;
  width: 100%;
}

.preview-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-download-excel {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #10b981 !important;
  color: #ffffff !important;
  border: 2px solid #10b981 !important;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 600 !important;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2) !important;
}

.btn-download-excel:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3) !important;
  background: #059669 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
}

.btn-download-excel i {
  color: #ffffff !important;
  font-size: 1rem !important;
}

.btn-download-excel span {
  color: #ffffff !important;
  font-weight: 600 !important;
}

.btn-close-preview {
  display: flex !important;
  align-items: center;
  justify-content: center;
  width: 44px !important;
  height: 44px !important;
  background: #ffffff !important;
  color: #000000 !important;
  border: 3px solid #000000 !important;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.4rem !important;
  font-weight: 900 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 1000 !important;
}

.btn-close-preview:hover {
  background: #f8f8f8 !important;
  color: #000000 !important;
  border-color: #000000 !important;
  transform: scale(1.15) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
}

.btn-close-preview:active {
  transform: scale(1.05) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
}

/* Excel-like Header */
.excel-header {
  margin-bottom: 2rem;
  text-align: center;
  background: #2F4F4F;
  color: white;
  padding: 1rem;
  border-radius: var(--radius-lg);
}

.header-row {
  margin-bottom: 0.5rem;
}

.header-row:last-child {
  margin-bottom: 0;
}

.title-cell {
  font-size: 1.5rem;
  font-weight: bold;
}

.subtitle-cell {
  font-size: 1.25rem;
  font-weight: bold;
}

.portfolio-cell {
  font-size: 1rem;
  font-weight: bold;
}

.date-cell {
  font-size: 0.9rem;
  font-weight: normal;
}

/* Excel-like Table */
.excel-table-container {
  overflow-x: auto;
  border: 2px solid #000;
  border-radius: 4px;
  margin-bottom: 2rem;
  width: 100%;
}

.excel-table {
  width: 100%;
  min-width: 1200px;
  border-collapse: collapse;
  font-family: 'Calibri', Arial, sans-serif;
  font-size: 11px;
  background: white;
}

.excel-th {
  background: #D9D9D9;
  border: 1px solid #000;
  padding: 8px 4px;
  text-align: center;
  font-weight: bold;
  font-size: 10px;
  vertical-align: middle;
  color: #000;
}

.excel-th.plant-col {
  width: 200px;
  min-width: 200px;
}

.excel-th.capacity-col,
.excel-th.nominated-col,
.excel-th.actual-col,
.excel-th.variance-col {
  width: 100px;
  min-width: 100px;
}

.excel-th.hours-col,
.excel-th.outage-col {
  width: 120px;
  min-width: 120px;
}

.excel-th.remarks-col {
  width: 300px;
  min-width: 300px;
}

.excel-td {
  border: 1px solid #000;
  padding: 4px 6px;
  font-size: 11px;
  color: #000;
  vertical-align: middle;
}

.plant-header-row {
  background: #E6E6E6;
}

.plant-name-cell {
  font-weight: bold;
  text-align: center;
  background: #E6E6E6;
}

.unit-cell {
  padding-left: 20px;
  text-align: left;
}

.number-cell {
  text-align: center;
}

.number-cell.negative {
  color: #FF0000;
}

.plant-total-row {
  background: #F2F2F2;
  font-weight: bold;
}

.total-label-cell {
  font-weight: bold;
  text-align: left;
  padding-left: 10px;
}

.total-number-cell {
  text-align: center;
  font-weight: bold;
}

.grand-total-row {
  background: #D9D9D9;
  font-weight: bold;
  border-top: 2px solid #000;
}

.grand-total-label {
  font-weight: bold;
  text-align: left;
  padding-left: 10px;
}

.grand-total-number {
  text-align: center;
  font-weight: bold;
}

.remarks-cell {
  text-align: left;
  max-width: 150px;
  word-wrap: break-word;
}

/* Excel Sections */
.excel-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  background: #FAFAFA;
  width: 100%;
}

.section-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #000;
  text-align: center;
  background: #D9D9D9;
  padding: 0.5rem;
  border: 1px solid #000;
  border-radius: 4px;
}

.small-table {
  width: 100%;
  max-width: none;
  margin: 0;
}

.label-cell {
  text-align: left;
  font-weight: normal;
  padding-left: 10px;
}

.ipp-row:nth-child(even) {
  background: #F9F9F9;
}

.notes-list {
  list-style-type: disc;
  padding-left: 2rem;
  margin: 0;
}

.notes-list li {
  margin-bottom: 0.5rem;
  color: #000;
  font-size: 0.9rem;
}

/* Signature Sections */
.signatures-section {
  background: white;
  border: 2px solid #000;
}

.signature-row {
  margin-bottom: 2rem;
}

.signature-row:last-child {
  margin-bottom: 0;
}

.signature-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Calibri', Arial, sans-serif;
}

.signature-header {
  background: #F2F2F2;
  border: 1px solid #000;
  padding: 8px;
  text-align: left;
  font-size: 10px;
  font-weight: normal;
  color: #000;
  width: 25%;
}

.signature-cell {
  border: 1px solid #000;
  padding: 8px;
  height: 20px;
  background: white;
}

.signature-space {
  height: 20px;
}

.signature-name {
  border: 1px solid #000;
  padding: 4px 8px;
  font-size: 11px;
  font-weight: bold;
  color: #000;
  text-align: left;
}

.signature-title {
  border: 1px solid #000;
  padding: 4px 8px;
  font-size: 10px;
  font-weight: normal;
  color: #000;
  text-align: left;
}

/* Footer Note */
.footer-note-section {
  background: white;
  border: 1px solid #ccc;
  margin-top: 2rem;
}

.footer-note {
  font-size: 10px;
  color: #000;
  line-height: 1.4;
  margin: 0;
  padding: 1rem;
  font-style: italic;
}
</style>