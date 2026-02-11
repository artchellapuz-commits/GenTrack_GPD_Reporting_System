<template>
  <div class="view-reports-page">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">
        <i class="pi pi-chart-line"></i>
        View Generation Reports
      </h2>
      <p class="page-description">
        View and analyze generation reports for Agus Hydro-electric Power Plants
      </p>
    </div>

    <!-- Filters Card -->
    <div class="card">
      <div class="card-body">
        <div class="filters-form">
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
                :class="{ 'selected': filters.plantCodes.includes(plant.code) }"
              >
                <input 
                  type="checkbox" 
                  :value="plant.code" 
                  v-model="filters.plantCodes"
                  class="checkbox-input"
                />
                <div class="plant-info">
                  <span class="plant-name">{{ plant.name }}</span>
                  <span class="plant-code">{{ plant.code }}</span>
                </div>
                <i v-if="filters.plantCodes.includes(plant.code)" class="pi pi-check check-icon"></i>
              </label>
            </div>
          </div>

          <!-- Date Range -->
          <div class="form-row">
            <div class="form-field">
              <label class="field-label">
                <i class="pi pi-calendar"></i>
                Start Date
              </label>
              <input 
                type="date" 
                v-model="filters.startDate" 
                class="date-input"
              />
            </div>

            <div class="form-field">
              <label class="field-label">
                <i class="pi pi-calendar"></i>
                End Date
              </label>
              <input 
                type="date" 
                v-model="filters.endDate" 
                class="date-input"
              />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="filter-actions">
            <button @click="loadReports" class="btn btn-primary">
              <i class="pi pi-filter"></i>
              Apply Filters
            </button>
            <button @click="loadSummary" class="btn btn-secondary">
              <i class="pi pi-chart-bar"></i>
              View Summary
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Statistics -->
    <div v-if="summary" class="card summary-card">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-chart-bar"></i>
          Summary Statistics
        </h3>
      </div>
      <div class="card-body">
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-bolt"></i>
            </div>
            <div class="summary-content">
              <label>Total Generation</label>
              <span class="summary-value">{{ formatNumber(summary.total_generation) }} kWh</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-percentage"></i>
            </div>
            <div class="summary-content">
              <label>Avg Capacity Factor</label>
              <span class="summary-value">{{ formatNumber(summary.avg_capacity_factor) }}%</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-check-circle"></i>
            </div>
            <div class="summary-content">
              <label>Avg Availability</label>
              <span class="summary-value">{{ formatNumber(summary.avg_availability_factor) }}%</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-clock"></i>
            </div>
            <div class="summary-content">
              <label>Total Operating Hours</label>
              <span class="summary-value">{{ formatNumber(summary.total_operating_hours) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <i class="pi pi-spin pi-spinner"></i>
      <p>Loading reports...</p>
    </div>

    <!-- Reports Table -->
    <div v-else-if="reports.length" class="card">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-table"></i>
          Generation Reports
        </h3>
      </div>
      <div class="card-body p-0">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Plant</th>
                <th>Unit</th>
                <th>Generation (kWh)</th>
                <th>Operating Hours</th>
                <th>Capacity Factor (%)</th>
                <th>Availability (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in reports" :key="report.id">
                <td>{{ report.report_date }}</td>
                <td>
                  <span class="plant-badge">{{ report.plant_code }}</span>
                </td>
                <td class="text-center">{{ report.unit_number }}</td>
                <td class="text-right">{{ formatNumber(report.generation_kwh) }}</td>
                <td class="text-center">{{ report.operating_hours }}</td>
                <td class="text-right">{{ formatNumber(report.capacity_factor) }}</td>
                <td class="text-right">{{ formatNumber(report.availability_factor) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="pagination">
          <button @click="previousPage" :disabled="!hasPrevious" class="btn-pagination">
            <i class="pi pi-chevron-left"></i>
            Previous
          </button>
          <span class="pagination-info">Page {{ currentPage }}</span>
          <button @click="nextPage" :disabled="!hasNext" class="btn-pagination">
            Next
            <i class="pi pi-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- No Data State -->
    <div v-else class="empty-state">
      <i class="pi pi-inbox"></i>
      <h3>No Reports Found</h3>
      <p>Try adjusting your filters to see generation reports</p>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'ViewReports',
  data() {
    return {
      plants: [],
      reports: [],
      summary: null,
      loading: false,
      filters: {
        plantCodes: [],
        startDate: '',
        endDate: '',
      },
      currentPage: 1,
      hasNext: false,
      hasPrevious: false,
    };
  },
  mounted() {
    this.loadPlants();
    this.loadReports();
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
      }
    },
    async loadReports() {
      this.loading = true;
      try {
        const params = {
          plant_code: this.filters.plantCodes,
          start_date: this.filters.startDate,
          end_date: this.filters.endDate,
          page: this.currentPage,
        };

        const response = await api.getGenerationReports(params);
        this.reports = response.data.results || response.data;
        this.hasNext = !!response.data.next;
        this.hasPrevious = !!response.data.previous;
      } catch (error) {
        console.error('Error loading reports:', error);
      } finally {
        this.loading = false;
      }
    },
    async loadSummary() {
      try {
        const params = {
          plant_code: this.filters.plantCodes,
          start_date: this.filters.startDate,
          end_date: this.filters.endDate,
        };

        const response = await api.getReportSummary(params);
        this.summary = response.data;
      } catch (error) {
        console.error('Error loading summary:', error);
      }
    },
    nextPage() {
      this.currentPage++;
      this.loadReports();
    },
    previousPage() {
      this.currentPage--;
      this.loadReports();
    },
    formatNumber(value) {
      return value ? parseFloat(value).toFixed(2) : '0.00';
    },
  },
};
</script>

<style scoped>
.view-reports-page {
  max-width: 1400px;
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
  font-size: 1.75rem;
}

.page-description {
  color: var(--gray-600);
  font-size: 1rem;
}

/* Filters */
.filters-form {
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

.filter-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding-top: 0.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.btn i {
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, var(--npc-primary), #004a9f);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #002d5f, #003d82);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background: linear-gradient(135deg, var(--npc-secondary), #008a42);
  color: white;
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #007a38, #00a651);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* Summary Card */
.summary-card {
  margin-bottom: var(--spacing-xl);
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.summary-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, rgba(0, 61, 130, 0.03), rgba(0, 166, 81, 0.03));
  border-radius: var(--radius-lg);
  border: 1px solid var(--gray-200);
  transition: all 0.2s ease;
}

.summary-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--npc-primary);
}

.summary-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--npc-primary), #004a9f);
  color: white;
  border-radius: var(--radius-lg);
  font-size: 1.25rem;
  flex-shrink: 0;
}

.summary-content {
  flex: 1;
  min-width: 0;
}

.summary-content label {
  display: block;
  font-size: 0.8125rem;
  color: var(--gray-600);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.summary-value {
  display: block;
  font-size: 1.5rem;
  color: var(--npc-primary);
  font-weight: 700;
  line-height: 1.2;
}

/* Table */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th, td {
  padding: var(--spacing-md);
  text-align: left;
  border-bottom: 1px solid var(--gray-200);
}

th {
  background: linear-gradient(135deg, rgba(0, 61, 130, 0.05), rgba(0, 166, 81, 0.05));
  font-weight: 600;
  color: var(--gray-700);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

tbody tr {
  transition: background 0.2s ease;
}

tbody tr:hover {
  background: var(--gray-50);
}

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.plant-badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  background: linear-gradient(135deg, var(--npc-primary), #004a9f);
  color: white;
  border-radius: var(--radius-md);
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.05em;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-top: 1px solid var(--gray-200);
}

.btn-pagination {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 0.625rem 1rem;
  background: white;
  color: var(--npc-primary);
  border: 2px solid var(--npc-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.btn-pagination:hover:not(:disabled) {
  background: var(--npc-primary);
  color: white;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn-pagination:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 500;
  color: var(--gray-700);
  padding: 0 var(--spacing-md);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  gap: var(--spacing-md);
}

.loading-state i {
  font-size: 3rem;
  color: var(--npc-primary);
}

.loading-state p {
  color: var(--gray-600);
  font-size: 1.125rem;
  margin: 0;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  text-align: center;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.empty-state i {
  font-size: 4rem;
  color: var(--gray-300);
  margin-bottom: var(--spacing-lg);
}

.empty-state h3 {
  color: var(--gray-700);
  font-size: 1.5rem;
  margin: 0 0 var(--spacing-sm) 0;
}

.empty-state p {
  color: var(--gray-500);
  font-size: 1rem;
  margin: 0;
}
</style>
