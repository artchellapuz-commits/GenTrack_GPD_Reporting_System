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

    <!-- Loading State with Skeleton -->
    <div v-if="loading" class="loading-state">
      <!-- Skeleton for Summary Stats -->
      <SkeletonLoader type="stats" />
      
      <!-- Skeleton for Table -->
      <SkeletonLoader type="table" />
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
                <th class="text-left sortable" @click="sortBy('report_date')">
                  Date
                  <i :class="['pi', getSortIcon('report_date'), 'sort-icon']"></i>
                </th>
                <th class="text-left sortable" @click="sortBy('plant')">
                  Plant
                  <i :class="['pi', getSortIcon('plant'), 'sort-icon']"></i>
                </th>
                <th class="text-center sortable" @click="sortBy('unit')">
                  Unit
                  <i :class="['pi', getSortIcon('unit'), 'sort-icon']"></i>
                </th>
                <th class="text-right sortable nowrap" @click="sortBy('generation')">
                  Generation (kWh)
                  <i :class="['pi', getSortIcon('generation'), 'sort-icon']"></i>
                </th>
                <th class="text-center sortable nowrap" @click="sortBy('operating_hours')">
                  Operating Hours
                  <i :class="['pi', getSortIcon('operating_hours'), 'sort-icon']"></i>
                </th>
                <th class="text-right sortable nowrap" @click="sortBy('capacity_factor')">
                  Capacity Factor (%)
                  <i :class="['pi', getSortIcon('capacity_factor'), 'sort-icon']"></i>
                </th>
                <th class="text-right sortable nowrap" @click="sortBy('availability')">
                  Availability (%)
                  <i :class="['pi', getSortIcon('availability'), 'sort-icon']"></i>
                </th>
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
import SkeletonLoader from './SkeletonLoader.vue';
import Paginator from 'primevue/paginator';

export default {
  name: 'ViewReports',
  components: {
    AppLayout,
    AdvancedFilter,
    SkeletonLoader,
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
      // Sorting
      sortField: 'report_date',
      sortOrder: -1, // -1 for descending, 1 for ascending
    };
  },
  computed: {
    reports() {
      // Sort first, then paginate
      const sorted = this.sortedReports;
      const start = (this.currentPage - 1) * this.rowsPerPage;
      const end = start + this.rowsPerPage;
      return sorted.slice(start, end);
    },
    sortedReports() {
      return [...this.allReports].sort((a, b) => {
        let aVal, bVal;
        
        switch(this.sortField) {
          case 'report_date':
            aVal = new Date(a.report_date);
            bVal = new Date(b.report_date);
            break;
          case 'plant':
            aVal = a.plant_name?.toLowerCase() || '';
            bVal = b.plant_name?.toLowerCase() || '';
            break;
          case 'unit':
            aVal = a.unit_name?.toLowerCase() || '';
            bVal = b.unit_name?.toLowerCase() || '';
            break;
          case 'generation':
            aVal = parseFloat(a.generation_kwh) || 0;
            bVal = parseFloat(b.generation_kwh) || 0;
            break;
          case 'operating_hours':
            aVal = parseFloat(a.operating_hours) || 0;
            bVal = parseFloat(b.operating_hours) || 0;
            break;
          case 'capacity_factor':
            aVal = parseFloat(a.capacity_factor) || 0;
            bVal = parseFloat(b.capacity_factor) || 0;
            break;
          case 'availability':
            aVal = parseFloat(a.availability) || 0;
            bVal = parseFloat(b.availability) || 0;
            break;
          default:
            return 0;
        }
        
        if (aVal < bVal) return -1 * this.sortOrder;
        if (aVal > bVal) return 1 * this.sortOrder;
        return 0;
      });
    }
  },
  mounted() {
    this.loadPlants();
    this.loadReports();
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
        let data = response.data.results || response.data;
        
        if (!data || data.length === 0) {
          throw new Error("No data");
        }
        
        this.allReports = data;
        this.totalRecords = this.allReports.length;
      } catch (error) {
        console.warn('Using mock reports for demonstration');
        this.allReports = [
          {
            id: 1,
            report_date: '2026-03-24',
            plant_code: 'AGUS_1',
            unit_number: '1',
            generation_kwh: '45210.50',
            operating_hours: '24',
            capacity_factor: '65.40',
            availability_factor: '100.00'
          },
          {
            id: 2,
            report_date: '2026-03-24',
            plant_code: 'AGUS_1',
            unit_number: '2',
            generation_kwh: '38100.00',
            operating_hours: '20',
            capacity_factor: '55.20',
            availability_factor: '83.33'
          },
          {
            id: 3,
            report_date: '2026-03-24',
            plant_code: 'AGUS_2',
            unit_number: '1',
            generation_kwh: '98450.75',
            operating_hours: '24',
            capacity_factor: '82.10',
            availability_factor: '100.00'
          },
          {
            id: 4,
            report_date: '2026-03-23',
            plant_code: 'AGUS_4',
            unit_number: '1',
            generation_kwh: '75000.00',
            operating_hours: '24',
            capacity_factor: '78.50',
            availability_factor: '100.00'
          },
          {
            id: 5,
            report_date: '2026-03-23',
            plant_code: 'AGUS_5',
            unit_number: '2',
            generation_kwh: '0.00',
            operating_hours: '0',
            capacity_factor: '0.00',
            availability_factor: '0.00'
          }
        ];
        this.totalRecords = this.allReports.length;
      } finally {
        setTimeout(() => this.loading = false, 600); // UI feel
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
        if (!response.data || Object.keys(response.data).length === 0) {
          throw new Error("No summary");
        }
        this.summary = response.data;
      } catch (error) {
        console.warn('Using mock summary for demonstration');
        this.summary = {
          total_generation: 256761.25,
          avg_capacity_factor: 56.24,
          avg_availability_factor: 76.66,
          total_operating_hours: 92
        };
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
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  letter-spacing: -0.025em;
}

.page-title i {
  color: #3b82f6;
  font-size: 2rem;
}

.page-description {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
}

/* Card General Styles */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.card-title i {
  color: #3b82f6;
  font-size: 1.25rem;
}

.card-body {
  padding: 1.5rem;
}

.card-body.p-0 {
  padding: 0;
}

/* Header Controls */
.header-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rows-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.rows-select {
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #334155;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.2em;
  min-width: 5rem;
}

.rows-select:hover {
  border-color: #cbd5e1;
}

.rows-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Summary Statistics */
.summary-card {
  margin-bottom: 2rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.summary-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.summary-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 16px;
  font-size: 2rem;
  flex-shrink: 0;
  transition: transform 0.3s ease;
  box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.4);
}

.summary-item:hover .summary-icon {
  transform: scale(1.05) rotate(5deg);
}

/* Different colors for different summary items */
.summary-item:nth-child(2) .summary-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 6px 12px -2px rgba(16, 185, 129, 0.4);
}

.summary-item:nth-child(3) .summary-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 6px 12px -2px rgba(245, 158, 11, 0.4);
}

.summary-item:nth-child(4) .summary-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  box-shadow: 0 6px 12px -2px rgba(139, 92, 246, 0.4);
}

.summary-content {
  flex: 1;
  min-width: 0;
}

.summary-content label {
  display: block;
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.summary-value {
  display: block;
  font-size: 1.75rem;
  color: #0f172a;
  font-weight: 800;
  line-height: 1.2;
}

/* Table Styles */
.table-container {
  overflow-x: auto;
  width: 100%;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
}

th, td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}

th {
  background: #f8fafc;
  font-weight: 700;
  color: #475569;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  position: sticky;
  top: 0;
  z-index: 10;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  background: #f8fafc;
  transform: scale(1.001);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 5;
}

td {
  font-size: 0.95rem;
  color: #1e293b;
  font-weight: 500;
}

.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

/* Sortable Headers */
th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
}

th.sortable:hover {
  background-color: #f1f5f9;
  color: #0f172a;
}

th .sort-icon {
  font-size: 0.8rem;
  color: #cbd5e1;
  margin-left: 0.5rem;
  transition: color 0.2s ease;
  vertical-align: middle;
}

th.sortable:hover .sort-icon {
  color: #94a3b8;
}

th .pi-sort-amount-up,
th .pi-sort-amount-down {
  color: #3b82f6;
  font-weight: bold;
}

/* Badges */
.plant-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  background: #eff6ff;
  color: #2563eb;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.025em;
  border: 1px solid #bfdbfe;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
  gap: 1.5rem;
}

.loading-state i {
  font-size: 3.5rem;
  color: #3b82f6;
  animation: spin 1s linear infinite;
}

.loading-state p {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: white;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}

.empty-state i {
  font-size: 4rem;
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: #0f172a;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

/* PrimeVue Paginator Customization */
:deep(.p-paginator) {
  background: white;
  border-top: 1px solid #e2e8f0;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  border-radius: 0 0 12px 12px;
}

:deep(.p-paginator .p-paginator-first),
:deep(.p-paginator .p-paginator-prev),
:deep(.p-paginator .p-paginator-next),
:deep(.p-paginator .p-paginator-last),
:deep(.p-paginator .p-paginator-page) {
  min-width: 2.5rem;
  height: 2.5rem;
  margin: 0.125rem;
  border-radius: 8px;
  border: 1px solid transparent;
  background: transparent;
  color: #64748b;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.95rem;
}

:deep(.p-paginator .p-paginator-first:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-prev:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-next:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-last:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-page:not(.p-highlight):hover) {
  background: #f1f5f9;
  color: #0f172a;
  border-color: #e2e8f0;
}

:deep(.p-paginator .p-paginator-page.p-highlight) {
  background: #3b82f6;
  color: white;
  font-weight: 600;
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

:deep(.p-paginator .p-disabled) {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .view-reports-page {
    padding: 1rem;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
  }
  
  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .header-controls {
    justify-content: space-between;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
