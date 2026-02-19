<template>
  <AppLayout>
    <div class="view-reports-page glass-background">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">
        <i class="pi pi-chart-line"></i>
        View Generation Reports
      </h2>
      <p class="page-description">
        View and analyze generation reports for Agus and Pulangi Hydro-electric Power Plants
      </p>
    </div>

    <!-- Advanced Filter Component -->
    <AdvancedFilter 
      :plants="plants"
      :showNumericFilters="true"
      :initialFilters="filters"
      @filter-change="onFilterChange"
    />

    <!-- Summary Statistics -->
    <div v-if="summary" class="card glass-card summary-card glass-fade-in">
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
    <div v-else-if="reports.length" class="card glass-card glass-fade-in">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-table"></i>
          Generation Reports
        </h3>
        <div class="header-controls">
          <label class="rows-label">Show:</label>
          <select v-model="rowsPerPage" @change="onRowsChange" class="rows-select glass-select">
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
            <option :value="200">200</option>
          </select>
          <span class="rows-label">entries</span>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th class="text-left">Date</th>
                <th class="text-left">Plant</th>
                <th class="text-center">Unit</th>
                <th class="text-right">Generation (kWh)</th>
                <th class="text-center">Operating Hours</th>
                <th class="text-right">Capacity Factor (%)</th>
                <th class="text-right">Availability (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in reports" :key="report.id">
                <td class="text-left">{{ report.report_date }}</td>
                <td class="text-left">
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
        <Paginator 
          :rows="rowsPerPage" 
          :totalRecords="totalRecords" 
          :first="(currentPage - 1) * rowsPerPage"
          @page="onPageChange($event)"
          template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
          :pageLinkSize="5"
        />
      </div>
    </div>

    <!-- No Data State -->
    <div v-else class="empty-state">
      <i class="pi pi-inbox"></i>
      <h3>No Reports Found</h3>
      <p>Try adjusting your filters to see generation reports</p>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import AppLayout from './AppLayout.vue';
import AdvancedFilter from './AdvancedFilter.vue';
import Paginator from 'primevue/paginator';

export default {
  name: 'ViewReports',
  components: {
    AppLayout,
    AdvancedFilter,
    Paginator,
  },
  data() {
    return {
      plants: [],
      allReports: [], // Store all reports
      summary: null,
      loading: false,
      filters: {
        plantCodes: [],
        startDate: '',
        endDate: '',
      },
      currentPage: 1,
      totalRecords: 0,
      rowsPerPage: 10,
    };
  },
  computed: {
    reports() {
      // Client-side pagination
      const start = (this.currentPage - 1) * this.rowsPerPage;
      const end = start + this.rowsPerPage;
      return this.allReports.slice(start, end);
    }
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
    onFilterChange(newFilters) {
      this.filters = { ...this.filters, ...newFilters };
      this.loadReports();
      if (newFilters.plantCodes && newFilters.plantCodes.length > 0) {
        this.loadSummary();
      }
    },
    async loadReports() {
      this.loading = true;
      try {
        const params = {
          plant_code: this.filters.plantCodes,
          start_date: this.filters.startDate,
          end_date: this.filters.endDate,
          page_size: 1000, // Get all records (or a large number)
        };

        const response = await api.getGenerationReports(params);
        this.allReports = response.data.results || response.data;
        this.totalRecords = this.allReports.length;
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
    onPageChange(event) {
      this.currentPage = event.page + 1; // PrimeVue uses 0-based index
    },
    onRowsChange() {
      this.currentPage = 1; // Reset to first page when changing rows per page
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

/* Card Header with Controls */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, rgba(0, 61, 130, 0.02), rgba(0, 166, 81, 0.02));
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.card-title i {
  color: var(--npc-primary);
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rows-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.rows-select {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #1e293b;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2364748b' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  min-width: 4rem;
}

.rows-select:hover {
  border-color: var(--npc-primary);
}

.rows-select:focus {
  outline: none;
  border-color: var(--npc-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 130, 0.1);
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
  white-space: nowrap;
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

.text-left {
  text-align: left !important;
}

.text-center {
  text-align: center !important;
}

.text-right {
  text-align: right !important;
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

/* Sakai-Style Pagination */
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

/* Rows Per Page Dropdown */
:deep(.p-paginator .p-dropdown) {
  margin-left: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  height: 2.5rem;
  min-width: 4rem;
}

:deep(.p-paginator .p-dropdown:hover) {
  border-color: var(--npc-primary);
}

:deep(.p-paginator .p-dropdown .p-dropdown-label) {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  color: #1e293b;
}

:deep(.p-paginator .p-dropdown .p-dropdown-trigger) {
  width: 2rem;
  color: #64748b;
}

:deep(.p-dropdown-panel) {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-top: 0.25rem;
}

:deep(.p-dropdown-panel .p-dropdown-items) {
  padding: 0.25rem;
}

:deep(.p-dropdown-panel .p-dropdown-item) {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #1e293b;
  transition: all 0.2s ease;
}

:deep(.p-dropdown-panel .p-dropdown-item:hover) {
  background: #f1f5f9;
  color: var(--npc-primary);
}

:deep(.p-dropdown-panel .p-dropdown-item.p-highlight) {
  background: #fef3c7;
  color: #92400e;
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
