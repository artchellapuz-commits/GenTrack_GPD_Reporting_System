<template>
  <AppLayout>
    <div class="water-nomination-container">
      <!-- Page Header -->
      <div class="page-header-simple">
        <h1>Water Nomination Management</h1>
        <button @click="showCreateModal = true" class="btn-primary">
          <i class="pi pi-plus-circle"></i>
          <span>New Nomination</span>
        </button>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon blue">
            <i class="pi pi-file"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ nominations.length }}</div>
            <div class="stat-label">Total Nominations</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon orange">
            <i class="pi pi-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ nominations.filter(n => n.status === 'DRAFT').length }}</div>
            <div class="stat-label">Draft</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon green">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ nominations.filter(n => n.status === 'APPROVED').length }}</div>
            <div class="stat-label">Approved</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon purple">
            <i class="pi pi-send"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ nominations.filter(n => n.status === 'SUBMITTED').length }}</div>
            <div class="stat-label">Pending Approval</div>
          </div>
        </div>
      </div>

      <!-- Filters Section with Modern Design -->
    <div class="content-section">
      <div class="section-header">
        <h3><i class="pi pi-filter"></i> Filter Nominations</h3>
        <div class="section-actions">
          <button @click="loadNominations" class="btn-icon" :class="{ 'spin-icon': loading }" title="Refresh">
            <i class="pi pi-refresh"></i>
          </button>
        </div>
      </div>
      
      <div class="filters-section glass-card">
        <div class="filters-grid">
        <div class="filter-group">
          <label>Plant</label>
          <select v-model="filters.plant_code" @change="loadNominations">
            <option value="">All Plants</option>
            <option v-for="plant in plants" :key="plant.code" :value="plant.code">
              {{ plant.name }}
            </option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Status</label>
          <select v-model="filters.status" @change="loadNominations">
            <option value="">All Status</option>
            <option value="DRAFT">Draft</option>
            <option value="SUBMITTED">Submitted</option>
            <option value="APPROVED">Approved</option>
            <option value="REJECTED">Rejected</option>
          </select>
        </div>

        <div class="filter-group date-range-group">
          <label>Date Range</label>
          <div class="date-inputs">
            <input type="date" v-model="filters.start_date" @change="loadNominations" placeholder="Start Date">
            <span class="date-separator">to</span>
            <input type="date" v-model="filters.end_date" @change="loadNominations" placeholder="End Date">
          </div>
        </div>

        <div class="filter-actions">
          <button @click="clearFilters" class="btn-clear">
            <i class="pi pi-times"></i> Clear
          </button>
          <button @click="loadNominations" class="btn-apply">
            <i class="pi pi-filter"></i> Apply
          </button>
        </div>
      </div>
      </div>
    </div>

    <!-- Nominations List with Modern Cards -->
    <div class="content-section">
      <div class="section-header">
        <h3><i class="pi pi-list"></i> Nominations</h3>
        <div class="view-toggle">
          <button @click="viewMode = 'grid'" class="toggle-btn" :class="{ active: viewMode === 'grid' }">
            <i class="pi pi-th-large"></i>
          </button>
          <button @click="viewMode = 'list'" class="toggle-btn" :class="{ active: viewMode === 'list' }">
            <i class="pi pi-bars"></i>
          </button>
        </div>
      </div>
      <div class="nominations-list">
      <div v-if="loading" class="loading-state">
        <i class="pi pi-spin pi-spinner"></i> Loading nominations...
      </div>

      <div v-else-if="nominations.length === 0" class="empty-state">
        <i class="pi pi-inbox"></i>
        <p>No nominations found</p>
      </div>

      <div v-else :class="viewMode === 'grid' ? 'nominations-grid' : 'nominations-list-view'">
        <div 
          v-for="nomination in nominations" 
          :key="nomination.id" 
          class="nomination-card glass-card"
          @click="viewDetails(nomination)"
        >
          <div class="card-header">
            <div class="plant-info">
              <h3>{{ nomination.plant_name }}</h3>
              <span class="date">{{ formatDate(nomination.nomination_date) }}</span>
            </div>
            <span :class="['status-badge', nomination.status ? nomination.status.toLowerCase() : 'draft']">
              {{ nomination.status || 'DRAFT' }}
            </span>
          </div>

          <div class="card-body">
            <div class="info-row">
              <span class="label">Type:</span>
              <span class="value">{{ nomination.nomination_type }}</span>
            </div>
            <div class="info-row highlight-row">
              <span class="label">Total Nominated:</span>
              <span class="value energy-value">{{ nomination.total_nominated_mwh }} MWh</span>
            </div>
            <div class="info-row" v-if="nomination.submitted_by_username">
              <span class="label">Submitted by:</span>
              <span class="value">{{ nomination.submitted_by_username }}</span>
            </div>
          </div>

          <div class="mini-chart">
            <div 
              v-for="(hourData, index) in (nomination.hourly_data || []).slice(0, 24)" 
              :key="index" 
              class="mini-bar"
              :style="{ height: getMiniBarHeight(hourData.nominated_mw, nomination.hourly_data) }"
              :title="`Hour ${index}: ${hourData.nominated_mw} MW`"
            ></div>
          </div>

          <div class="card-actions" @click.stop>
            <button @click.stop="viewDetails(nomination)" class="btn-view">
              <i class="pi pi-eye"></i> View
            </button>
            <button v-if="nomination.status === 'DRAFT'" @click.stop="editNomination(nomination)" class="btn-edit">
              <i class="pi pi-pencil"></i> Edit
            </button>
            <button v-if="nomination.status === 'DRAFT'" @click.stop="deleteNomination(nomination.id)" class="btn-delete">
              <i class="pi pi-trash"></i> Delete
            </button>
            <button v-if="nomination.status === 'DRAFT'" @click.stop="submitNomination(nomination.id)" class="btn-submit">
              <i class="pi pi-send"></i> Submit
            </button>
            <button v-if="canApproveNomination(nomination)" @click.stop="approveNomination(nomination.id)" class="btn-approve">
              <i class="pi pi-check"></i> Approve
            </button>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content glass-card">
        <div class="modal-header">
          <h3>{{ editMode ? 'Edit' : 'Create' }} Water Nomination</h3>
          <button @click="closeModal" class="btn-close">&times;</button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>Plant *</label>
            <select v-model="formData.plant" required>
              <option value="">Select Plant</option>
              <option v-for="plant in plants" :key="plant.id" :value="plant.id">
                {{ plant.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Nomination Date *</label>
            <input type="date" v-model="formData.nomination_date" required>
          </div>

          <div class="form-group">
            <label>Nomination Type *</label>
            <select v-model="formData.nomination_type" required>
              <option value="DAY_AHEAD">Day-Ahead</option>
              <option value="HOUR_AHEAD">Hour-Ahead</option>
              <option value="REAL_TIME">Real-Time</option>
            </select>
          </div>

          <div class="hourly-section">
            <h4>Hourly Nomination (MW)</h4>
            <div class="quick-fill-buttons">
              <button @click="fillAllHours(50)" class="quick-btn" type="button">Fill 50 MW</button>
              <button @click="fillAllHours(75)" class="quick-btn" type="button">Fill 75 MW</button>
              <button @click="fillAllHours(100)" class="quick-btn" type="button">Fill 100 MW</button>
              <button @click="clearAllHours" class="quick-btn danger" type="button">Clear All</button>
              <button @click="copyPreviousDay" class="quick-btn" type="button">Copy Previous Day</button>
            </div>
            <div class="hourly-grid">
              <div v-for="hour in 24" :key="hour" class="hour-input" :class="{ 'has-value': formData[`hour_${String(hour - 1).padStart(2, '0')}`] > 0 }">
                <label>{{ formatHour(hour - 1) }}</label>
                <input 
                  type="number" 
                  step="0.01" 
                  v-model.number="formData[`hour_${String(hour - 1).padStart(2, '0')}`]"
                  @input="calculateTotal"
                  @focus="highlightHour(hour - 1)"
                  @blur="unhighlightHour"
                >
                <div class="hour-bar" :style="{ width: getHourBarWidth(hour - 1) + '%' }"></div>
              </div>
            </div>
            <div class="total-display">
              <div class="total-label">Total Energy:</div>
              <div class="total-value">{{ calculatedTotal.toFixed(2) }} MWh</div>
              <div class="total-avg">Avg: {{ (calculatedTotal / 24).toFixed(2) }} MW/hr</div>
            </div>
          </div>

          <div class="form-group">
            <label>Remarks</label>
            <textarea v-model="formData.remarks" rows="3"></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="btn-secondary">Cancel</button>
          <button @click="saveNomination" class="btn-primary">
            {{ editMode ? 'Update' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click.self="showDetailsModal = false">
      <div class="modal-content glass-card large-modal">
        <div class="modal-header">
          <h3>Nomination Details</h3>
          <button @click="showDetailsModal = false" class="btn-close">&times;</button>
        </div>

        <div class="modal-body" v-if="selectedNomination">
          <div class="details-grid">
            <div class="detail-item">
              <span class="label">Plant:</span>
              <span class="value">{{ selectedNomination.plant_name }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Date:</span>
              <span class="value">{{ formatDate(selectedNomination.nomination_date) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Type:</span>
              <span class="value">{{ selectedNomination.nomination_type }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Status:</span>
              <span :class="['status-badge', selectedNomination.status ? selectedNomination.status.toLowerCase() : 'draft']">
                {{ selectedNomination.status || 'DRAFT' }}
              </span>
            </div>
          </div>

          <div class="hourly-chart">
            <h4>Hourly Nomination Profile</h4>
            <div class="chart-container">
              <div class="chart-bars">
                <div v-for="(hourData, index) in selectedNomination.hourly_data" :key="index" class="bar-item">
                  <div class="bar-container">
                    <div 
                      class="bar animated-bar" 
                      :style="{ 
                        height: (hourData.nominated_mw / maxHourlyValue * 100) + '%',
                        animationDelay: (index * 0.02) + 's'
                      }"
                      @mouseenter="showTooltip(index, hourData.nominated_mw)"
                      @mouseleave="hideTooltip"
                    ></div>
                  </div>
                  <span class="bar-label">{{ index }}</span>
                  <span class="bar-value">{{ hourData.nominated_mw }}</span>
                </div>
              </div>
              <div class="chart-stats">
                <div class="stat-item">
                  <span class="stat-label">Peak:</span>
                  <span class="stat-value">{{ getPeakHour() }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Average:</span>
                  <span class="stat-value">{{ getAverageValue() }} MW</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Total:</span>
                  <span class="stat-value">{{ selectedNomination.total_nominated_mwh }} MWh</span>
                </div>
              </div>
            </div>
          </div>

          <div class="remarks-section" v-if="selectedNomination.remarks">
            <h4>Remarks</h4>
            <p>{{ selectedNomination.remarks }}</p>
          </div>
        </div>
      </div>
    </div>
    </div>
  </AppLayout>
</template>

<script>
import axios from 'axios';
import AppLayout from './AppLayout.vue';
import { canApproveData, getUsername } from '../utils/auth';

export default {
  name: 'WaterNomination',
  components: {
    AppLayout
  },
  data() {
    return {
      nominations: [],
      currentUsername: getUsername(),
      plants: [],
      loading: false,
      showCreateModal: false,
      showDetailsModal: false,
      showStatsModal: false,
      editMode: false,
      selectedNomination: null,
      highlightedHour: null,
      viewMode: 'grid', // 'grid' or 'list'
      filters: {
        plant_code: '',
        status: '',
        start_date: '',
        end_date: ''
      },
      formData: {
        plant: '',
        nomination_date: '',
        nomination_type: 'DAY_AHEAD',
        remarks: ''
      },
      calculatedTotal: 0
    };
  },
  computed: {
    maxHourlyValue() {
      if (!this.selectedNomination || !this.selectedNomination.hourly_data) return 100;
      return Math.max(...this.selectedNomination.hourly_data.map(h => h.nominated_mw), 100);
    }
  },
  mounted() {
    this.loadPlants();
    this.loadNominations();
    this.initializeHourlyFields();
  },
  methods: {
    canApprove() {
      return canApproveData();
    },
    canApproveNomination(nomination) {
      // Can approve if:
      // 1. User has approve permission
      // 2. Nomination is submitted (not draft or already approved)
      // 3. User didn't submit it (can't approve own submission)
      return this.canApprove() && 
             nomination.status === 'SUBMITTED' &&
             nomination.submitted_by_username !== this.currentUsername;
    },
    initializeHourlyFields() {
      for (let i = 0; i < 24; i++) {
        const field = `hour_${String(i).padStart(2, '0')}`;
        this.formData[field] = 0;
      }
    },
    async loadPlants() {
      try {
        const response = await axios.get('http://localhost:8000/api/plants/');
        this.plants = response.data.results || response.data || [];
      } catch (error) {
        console.error('Error loading plants:', error);
        this.plants = [];
      }
    },
    async loadNominations() {
      this.loading = true;
      try {
        const params = {};
        if (this.filters.plant_code) params.plant_code = this.filters.plant_code;
        if (this.filters.status) params.status = this.filters.status;
        if (this.filters.start_date) params.start_date = this.filters.start_date;
        if (this.filters.end_date) params.end_date = this.filters.end_date;

        const response = await axios.get('http://localhost:8000/api/water-nominations/', { params });
        
        // Ensure each nomination has required fields with defaults
        this.nominations = (response.data.results || response.data || []).map(nom => ({
          ...nom,
          status: nom.status || 'DRAFT',
          nomination_type: nom.nomination_type || 'DAY_AHEAD',
          total_nominated_mwh: nom.total_nominated_mwh || 0,
          plant_name: nom.plant_name || 'Unknown Plant',
          hourly_data: nom.hourly_data || []
        }));
      } catch (error) {
        console.error('Error loading nominations:', error);
        alert('Failed to load nominations: ' + (error.response?.data?.error || error.message));
        this.nominations = [];
      } finally {
        this.loading = false;
      }
    },
    async saveNomination() {
      try {
        // Validate required fields
        if (!this.formData.plant) {
          alert('Please select a plant');
          return;
        }
        if (!this.formData.nomination_date) {
          alert('Please select a nomination date');
          return;
        }

        // Prepare data for API
        const nominationData = {
          plant: this.formData.plant,
          nomination_date: this.formData.nomination_date,
          nomination_type: this.formData.nomination_type || 'DAY_AHEAD',
          remarks: this.formData.remarks || ''
        };

        // Add all hourly fields
        for (let i = 0; i < 24; i++) {
          const field = `hour_${String(i).padStart(2, '0')}`;
          nominationData[field] = parseFloat(this.formData[field] || 0);
        }

        console.log('Sending nomination data:', nominationData);

        if (this.editMode) {
          const response = await axios.put(
            `http://localhost:8000/api/water-nominations/${this.formData.id}/`,
            nominationData
          );
          console.log('Update response:', response.data);
          alert('Nomination updated successfully');
        } else {
          const response = await axios.post('http://localhost:8000/api/water-nominations/', nominationData);
          console.log('Create response:', response.data);
          alert('Nomination created successfully');
        }
        this.closeModal();
        this.loadNominations();
      } catch (error) {
        console.error('Full error:', error);
        console.error('Error response:', error.response);
        
        // Build user-friendly error message
        let errorMsg = '';
        
        if (error.response?.data) {
          const data = error.response.data;
          
          // Handle unique constraint error
          if (data.non_field_errors) {
            const errors = Array.isArray(data.non_field_errors) ? data.non_field_errors : [data.non_field_errors];
            if (errors.some(e => String(e).includes('unique set'))) {
              alert('A nomination already exists for this plant, date, and type combination.\n\nPlease either:\n1. Choose a different date\n2. Edit the existing nomination\n3. Delete the existing nomination first');
              return;
            }
            errorMsg = errors.join(', ');
          }
          // Handle field-specific errors
          else if (typeof data === 'object' && !Array.isArray(data)) {
            const fieldErrors = [];
            for (const [field, messages] of Object.entries(data)) {
              const msgArray = Array.isArray(messages) ? messages : [messages];
              fieldErrors.push(`${field}: ${msgArray.join(', ')}`);
            }
            errorMsg = fieldErrors.join('\n');
          }
          // Handle string error
          else if (data.error || data.detail) {
            errorMsg = data.error || data.detail;
          }
          // Fallback to JSON string
          else {
            errorMsg = JSON.stringify(data);
          }
        } else {
          errorMsg = error.message || 'Unknown error occurred';
        }
        
        alert('Failed to save nomination:\n\n' + errorMsg);
      }
    },
    async submitNomination(id) {
      if (!confirm('Submit this nomination for approval?')) return;
      
      try {
        await axios.post(`http://localhost:8000/api/water-nominations/${id}/submit/`);
        alert('Nomination submitted successfully');
        this.loadNominations();
      } catch (error) {
        console.error('Error submitting nomination:', error);
        alert('Failed to submit nomination');
      }
    },
    async deleteNomination(id) {
      if (!confirm('Are you sure you want to delete this draft nomination?')) return;
      
      try {
        await axios.delete(`http://localhost:8000/api/water-nominations/${id}/`);
        alert('Nomination deleted successfully');
        this.loadNominations();
      } catch (error) {
        console.error('Error deleting nomination:', error);
        alert('Failed to delete nomination: ' + (error.response?.data?.error || error.message));
      }
    },
    async approveNomination(id) {
      if (!confirm('Approve this nomination?')) return;
      
      try {
        await axios.post(`http://localhost:8000/api/water-nominations/${id}/approve/`);
        alert('Nomination approved successfully');
        this.loadNominations();
      } catch (error) {
        console.error('Error approving nomination:', error);
        alert('Failed to approve nomination');
      }
    },
    editNomination(nomination) {
      this.editMode = true;
      this.formData = { ...nomination };
      this.showCreateModal = true;
      this.calculateTotal();
    },
    viewDetails(nomination) {
      // Ensure nomination has all required fields
      this.selectedNomination = {
        ...nomination,
        status: nomination.status || 'DRAFT',
        nomination_type: nomination.nomination_type || 'DAY_AHEAD',
        hourly_data: nomination.hourly_data || [],
        remarks: nomination.remarks || ''
      };
      this.showDetailsModal = true;
    },
    closeModal() {
      this.showCreateModal = false;
      this.editMode = false;
      this.formData = {
        plant: '',
        nomination_date: '',
        nomination_type: 'DAY_AHEAD',
        remarks: ''
      };
      this.initializeHourlyFields();
      this.calculatedTotal = 0;
    },
    calculateTotal() {
      let total = 0;
      for (let i = 0; i < 24; i++) {
        const field = `hour_${String(i).padStart(2, '0')}`;
        total += parseFloat(this.formData[field] || 0);
      }
      this.calculatedTotal = total;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    formatHour(hour) {
      return `${String(hour).padStart(2, '0')}:00`;
    },
    getMiniBarHeight(value, hourlyData) {
      if (!hourlyData || hourlyData.length === 0) return '0%';
      const maxValue = Math.max(...hourlyData.map(h => h.nominated_mw || 0), 1);
      return ((value || 0) / maxValue * 100) + '%';
    },
    getHourBarWidth(hour) {
      const field = `hour_${String(hour).padStart(2, '0')}`;
      const value = this.formData[field] || 0;
      if (this.calculatedTotal === 0) return 0;
      return (value / this.calculatedTotal * 100);
    },
    fillAllHours(value) {
      for (let i = 0; i < 24; i++) {
        const field = `hour_${String(i).padStart(2, '0')}`;
        this.formData[field] = value;
      }
      this.calculateTotal();
    },
    clearAllHours() {
      for (let i = 0; i < 24; i++) {
        const field = `hour_${String(i).padStart(2, '0')}`;
        this.formData[field] = 0;
      }
      this.calculateTotal();
    },
    async copyPreviousDay() {
      try {
        if (!this.formData.plant) {
          alert('Please select a plant first');
          return;
        }
        
        if (!this.formData.nomination_date) {
          alert('Please select a nomination date first');
          return;
        }

        // Calculate previous day
        const currentDate = new Date(this.formData.nomination_date);
        const previousDate = new Date(currentDate);
        previousDate.setDate(previousDate.getDate() - 1);
        const previousDateStr = previousDate.toISOString().split('T')[0];

        // Fetch nominations for the previous day
        const response = await axios.get('http://localhost:8000/api/water-nominations/', {
          params: {
            plant: this.formData.plant,
            nomination_date: previousDateStr
          }
        });

        const nominations = response.data.results || response.data || [];
        
        if (nominations.length === 0) {
          alert(`No nomination found for ${previousDateStr}. Cannot copy data.`);
          return;
        }

        // Get the first nomination from previous day
        const previousNomination = nominations[0];
        
        // Copy hourly data
        for (let i = 0; i < 24; i++) {
          const field = `hour_${String(i).padStart(2, '0')}`;
          this.formData[field] = previousNomination[field] || 0;
        }
        
        this.calculateTotal();
        alert(`Successfully copied data from ${previousDateStr}`);
      } catch (error) {
        console.error('Error copying previous day:', error);
        alert('Failed to copy data from previous day: ' + (error.response?.data?.error || error.message));
      }
    },
    highlightHour(hour) {
      this.highlightedHour = hour;
    },
    unhighlightHour() {
      this.highlightedHour = null;
    },
    showTooltip(hour, value) {
      // Could implement a tooltip system here
      console.log(`Hour ${hour}: ${value} MW`);
    },
    hideTooltip() {
      // Hide tooltip
    },
    clearFilters() {
      this.filters = {
        plant_code: '',
        status: '',
        start_date: '',
        end_date: ''
      };
      this.loadNominations();
    },
    getPeakHour() {
      if (!this.selectedNomination || !this.selectedNomination.hourly_data) return 'N/A';
      const hourlyData = this.selectedNomination.hourly_data;
      const maxValue = Math.max(...hourlyData.map(h => h.nominated_mw || 0));
      const peakHour = hourlyData.findIndex(h => h.nominated_mw === maxValue);
      return `${String(peakHour).padStart(2, '0')}:00 (${maxValue} MW)`;
    },
    getAverageValue() {
      if (!this.selectedNomination || !this.selectedNomination.hourly_data) return '0.00';
      const hourlyData = this.selectedNomination.hourly_data;
      const sum = hourlyData.reduce((acc, h) => acc + (h.nominated_mw || 0), 0);
      return (sum / 24).toFixed(2);
    }
  }
};
</script>

<style scoped>
/* Modern Container */
.water-nomination-container {
  padding: 20px;
  max-width: 100%;
  margin: 0;
  background: transparent;
  min-height: 100vh;
}

/* Simple Page Header */
.page-header-simple {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e2e8f0;
}

.page-header-simple h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

/* Page Header with Gradient */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px 40px;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 4px;
}

.breadcrumb-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.breadcrumb-item.active {
  color: white;
  font-weight: 600;
}

.breadcrumb-separator {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

.header-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.header-title-section h1 {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 14px;
  color: #ffffff !important;
  margin: 0;
  text-shadow: none;
  font-weight: 500;
  opacity: 1 !important;
  background: none;
  padding: 0;
  border-radius: 0;
  display: block;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-large {
  padding: 14px 28px;
  font-size: 15px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-large i {
  font-size: 18px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  max-width: 100%;
  margin: 0 0 30px 0;
  padding: 0;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.green {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.purple {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* Content Sections */
.content-section {
  max-width: 100%;
  margin: 0 0 30px 0;
  padding: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.section-header h3 i {
  color: #667eea;
}

.section-actions {
  display: flex;
  gap: 10px;
}

.btn-icon {
  width: 40px;
  height: 40px;
  border: none;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  color: #64748b;
}

.btn-icon:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.view-toggle {
  display: flex;
  gap: 4px;
  background: white;
  padding: 4px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.toggle-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748b;
}

.toggle-btn.active {
  background: #667eea;
  color: white;
}

.toggle-btn:hover:not(.active) {
  background: #f1f5f9;
}

/* Filters Section - Enhanced */
.filters-section {
  padding: 28px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.btn-primary, .btn-secondary, .btn-view, .btn-edit, .btn-delete, .btn-submit, .btn-approve, .btn-info {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary::before, .btn-secondary::before, .btn-view::before, .btn-edit::before, .btn-delete::before,
.btn-submit::before, .btn-approve::before, .btn-info::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn-primary:hover::before, .btn-secondary:hover::before, .btn-view:hover::before, 
.btn-edit:hover::before, .btn-delete:hover::before, .btn-submit:hover::before, .btn-approve:hover::before, .btn-info:hover::before {
  width: 300px;
  height: 300px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-secondary {
  background: #ecf0f1;
  color: #2c3e50;
}

.btn-secondary:hover {
  background: #d5dbdb;
  transform: translateY(-2px);
}

.btn-info {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
}

.btn-info:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(52, 152, 219, 0.6);
}

.pulse-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }
  50% {
    box-shadow: 0 4px 25px rgba(102, 126, 234, 0.8);
  }
}

.spin-icon i {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.btn-view {
  background: #3498db;
  color: white;
  padding: 8px 16px;
}

.btn-edit {
  background: #f39c12;
  color: white;
  padding: 8px 16px;
}

.btn-delete {
  background: #e74c3c;
  color: white;
  padding: 8px 16px;
}

.btn-delete:hover {
  background: #c0392b;
}

.btn-submit {
  background: #27ae60;
  color: white;
  padding: 8px 16px;
}

.btn-approve {
  background: #2ecc71;
  color: white;
  padding: 8px 16px;
}

.filters-section {
  padding: 25px;
  margin-bottom: 25px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.filters-grid {
  display: grid;
  grid-template-columns: 200px 200px 1fr auto;
  gap: 20px;
  align-items: end;
}

@media (max-width: 1200px) {
  .filters-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .date-range-group {
    grid-column: span 2;
  }
  
  .filter-actions {
    grid-column: span 2;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .date-range-group {
    grid-column: span 1;
  }
  
  .filter-actions {
    grid-column: span 1;
  }
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 13px;
  color: #475569;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-group select,
.filter-group input[type="date"] {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  color: #1e293b;
  transition: all 0.3s ease;
  font-family: inherit;
}

.filter-group select:hover,
.filter-group input[type="date"]:hover {
  border-color: #cbd5e1;
}

.filter-group select:focus,
.filter-group input[type="date"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.date-range-group {
  grid-column: span 1;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-inputs input {
  flex: 1;
}

.date-separator {
  color: #94a3b8;
  font-size: 13px;
  font-weight: 600;
  padding: 0 5px;
}

.filter-actions {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.btn-clear,
.btn-apply {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-clear {
  background: #f1f5f9;
  color: #64748b;
  border: 2px solid #e2e8f0;
}

.btn-clear:hover {
  background: #e2e8f0;
  color: #475569;
  transform: translateY(-2px);
}

.btn-apply {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-apply:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* Responsive Filters */
@media (max-width: 1200px) {
  .page-header {
    padding: 25px 30px;
  }
  
  .stats-grid,
  .content-section {
    padding: 0 30px;
  }
  
  .header-title-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .btn-large {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 20px;
  }
  
  .stats-grid,
  .content-section {
    padding: 0 20px;
  }
  
  .header-title-section h1 {
    font-size: 24px;
  }
  
  .icon-wrapper {
    width: 50px;
    height: 50px;
    font-size: 24px;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 20px;
  }
  
  .stat-value {
    font-size: 28px;
  }
}

.nominations-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.nominations-list-view {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.nominations-list-view .nomination-card {
  display: grid;
  grid-template-columns: 200px 1fr auto;
  gap: 20px;
  align-items: center;
}

.nominations-list-view .card-header {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.nominations-list-view .card-body {
  display: flex;
  gap: 30px;
  margin-bottom: 0;
}

.nominations-list-view .mini-chart {
  width: 200px;
  margin: 0;
}

.nominations-list-view .card-actions {
  justify-content: flex-end;
}

@media (max-width: 1400px) {
  .nominations-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .nominations-list-view .nomination-card {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

@media (max-width: 900px) {
  .nominations-grid {
    grid-template-columns: 1fr;
  }
}

.nomination-card {
  padding: 20px;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.nomination-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  transition: left 0.5s;
}

.nomination-card:hover::before {
  left: 100%;
}

.nomination-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.plant-info h3 {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 5px;
}

.date {
  font-size: 13px;
  color: #7f8c8d;
}

.status-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.draft {
  background: #ecf0f1;
  color: #7f8c8d;
}

.status-badge.submitted {
  background: #fff3cd;
  color: #856404;
}

.status-badge.approved {
  background: #d4edda;
  color: #155724;
}

.status-badge.rejected {
  background: #f8d7da;
  color: #721c24;
}

.card-body {
  margin-bottom: 15px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.info-row .label {
  color: #7f8c8d;
}

.info-row .value {
  font-weight: 600;
  color: #2c3e50;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 15px;
  display: block;
}

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
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.large-modal {
  max-width: 1000px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ecf0f1;
}

.modal-header h3 {
  font-size: 20px;
  color: #2c3e50;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #7f8c8d;
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
  font-weight: 600;
  color: #2c3e50;
  font-size: 14px;
}

.form-group select,
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.hourly-section {
  margin: 20px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.hourly-section h4 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.hourly-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.hour-input {
  display: flex;
  flex-direction: column;
  gap: 5px;
  position: relative;
  transition: all 0.3s ease;
}

.hour-input:hover {
  transform: scale(1.05);
  z-index: 10;
}

.hour-input.has-value {
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
  padding: 5px;
}

.hour-input label {
  font-size: 12px;
  color: #7f8c8d;
  font-weight: 600;
}

.hour-input input {
  padding: 8px;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 13px;
  transition: all 0.3s ease;
}

.hour-input input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  transform: scale(1.05);
}

.hour-bar {
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
  transition: width 0.3s ease;
  margin-top: 2px;
}

.quick-fill-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.quick-btn {
  padding: 8px 16px;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.quick-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.quick-btn.danger {
  border-color: #e74c3c;
  color: #e74c3c;
}

.quick-btn.danger:hover {
  background: #e74c3c;
  color: white;
}

.total-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.total-label {
  font-size: 14px;
  opacity: 0.9;
}

.total-value {
  font-size: 24px;
  font-weight: 700;
}

.total-avg {
  font-size: 13px;
  opacity: 0.9;
}

.mini-chart {
  display: flex;
  gap: 2px;
  height: 40px;
  align-items: flex-end;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  margin: 15px 0;
}

.mini-bar {
  flex: 1;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px 2px 0 0;
  min-height: 2px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.mini-bar:hover {
  background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
  transform: scaleY(1.1);
}

.highlight-row {
  background: rgba(102, 126, 234, 0.05);
  padding: 8px;
  border-radius: 6px;
  margin: 5px 0;
}

.energy-value {
  font-size: 18px;
  font-weight: 700;
  color: #667eea;
}

.animated-bar {
  animation: growBar 0.6s ease forwards;
}

@keyframes growBar {
  from {
    height: 0;
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.chart-container {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.chart-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.stat-label {
  font-size: 12px;
  color: #7f8c8d;
  font-weight: 600;
}

.stat-value {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 700;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #ecf0f1;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-item .label {
  font-size: 12px;
  color: #7f8c8d;
  font-weight: 600;
}

.detail-item .value {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 600;
}

.hourly-chart {
  margin: 30px 0;
}

.hourly-chart h4 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.chart-bars {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  height: 200px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
}

.bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.bar-container {
  width: 100%;
  height: 150px;
  display: flex;
  align-items: flex-end;
}

.bar {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
}

.bar-label {
  font-size: 10px;
  color: #7f8c8d;
}

.bar-value {
  font-size: 11px;
  font-weight: 600;
  color: #2c3e50;
}

.remarks-section {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.remarks-section h4 {
  margin-bottom: 10px;
  color: #2c3e50;
}

.remarks-section p {
  color: #7f8c8d;
  line-height: 1.6;
}

.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Header Icon Button */
.btn-icon-header {
  width: 48px;
  height: 48px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-size: 20px;
}

.btn-icon-header:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Palette Button with Theme Color Background */
.btn-palette {
  border: none !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.btn-palette:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.btn-palette i {
  color: white !important;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

/* Dark Mode Styles */
.dark-mode {
  background: #1a1a2e !important;
  color: #eee !important;
}

.dark-mode .page-header {
  background: linear-gradient(135deg, #2d3561 0%, #1f1f3a 100%) !important;
}

.dark-mode .stat-card,
.dark-mode .glass-card,
.dark-mode .modal-content {
  background: rgba(30, 30, 46, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #eee !important;
}

.dark-mode .stat-value,
.dark-mode .stat-label,
.dark-mode h1, .dark-mode h2, .dark-mode h3, .dark-mode h4,
.dark-mode .plant-info h3,
.dark-mode .detail-item .value {
  color: #eee !important;
}

.dark-mode .info-row .label,
.dark-mode .stat-label,
.dark-mode .date,
.dark-mode .detail-item .label {
  color: #aaa !important;
}

.dark-mode .nomination-card {
  background: rgba(30, 30, 46, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.dark-mode .nomination-card:hover {
  background: rgba(40, 40, 60, 0.95) !important;
}

.dark-mode input,
.dark-mode select,
.dark-mode textarea {
  background: rgba(20, 20, 30, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #eee !important;
}

.dark-mode .btn-icon {
  background: rgba(30, 30, 46, 0.95) !important;
  color: #aaa !important;
}

.dark-mode .btn-icon:hover {
  background: #667eea !important;
  color: white !important;
}

.dark-mode .section-header h3 {
  color: #eee !important;
}

.dark-mode .mini-chart {
  background: rgba(20, 20, 30, 0.5) !important;
}

.dark-mode .chart-container,
.dark-mode .hourly-section {
  background: rgba(20, 20, 30, 0.5) !important;
}
</style>

