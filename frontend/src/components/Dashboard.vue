<template>
  <AppLayout>
    <div class="dashboard-page glass-background">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div>
          <h2 class="page-title">
            <i class="pi pi-chart-line"></i>
            Dashboard
          </h2>
          <p class="page-description">
            Overview of Agus and Pulangi Hydroelectric Power Plants Generation Performance
          </p>
        </div>
        <div class="header-actions">
          <button @click="exportDashboardToPDF" class="btn-export-pdf glass-button">
            <i class="pi pi-file-pdf"></i>
            Export PDF
          </button>
          <button @click="exportAllDashboardData" class="btn-export-csv glass-button">
            <i class="pi pi-file-excel"></i>
            Export CSV
          </button>
          <button @click="refreshData" class="btn-refresh glass-button" :disabled="loading">
            <i class="pi" :class="loading ? 'pi-spin pi-spinner' : 'pi-refresh'"></i>
            Refresh
          </button>
          <button @click="toggleAutoRefresh" class="btn-auto-refresh glass-button" :class="{ active: autoRefresh }">
            <i class="pi pi-clock"></i>
            Auto-refresh {{ autoRefresh ? 'ON' : 'OFF' }}
          </button>
        </div>
      </div>
      <div class="last-updated" v-if="lastUpdated">
        Last updated: {{ formatLastUpdated(lastUpdated) }}
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <i class="pi pi-spin pi-spinner"></i>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Summary Cards -->
      <div class="stats-grid">
        <div class="stat-card glass-stat-card glass-float">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <i class="pi pi-bolt"></i>
          </div>
          <div class="stat-content">
            <label>Total Generation</label>
            <span class="stat-value">{{ formatNumber(stats.totalGeneration) }}</span>
            <span class="stat-unit">kWh</span>
          </div>
        </div>

        <div class="stat-card glass-stat-card glass-float">
          <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <i class="pi pi-percentage"></i>
          </div>
          <div class="stat-content">
            <label>Avg Capacity Factor</label>
            <span class="stat-value">{{ formatNumber(stats.avgCapacityFactor) }}</span>
            <span class="stat-unit">%</span>
          </div>
        </div>

        <div class="stat-card glass-stat-card glass-float">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <label>Avg Availability</label>
            <span class="stat-value">{{ formatNumber(stats.avgAvailability) }}</span>
            <span class="stat-unit">%</span>
          </div>
        </div>

        <div class="stat-card glass-stat-card glass-float">
          <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <i class="pi pi-clock"></i>
          </div>
          <div class="stat-content">
            <label>Operating Hours</label>
            <span class="stat-value">{{ formatNumber(stats.totalOperatingHours) }}</span>
            <span class="stat-unit">hrs</span>
          </div>
        </div>
      </div>

      <!-- Plants Overview -->
      <div class="card glass-card">
        <div class="card-header">
          <div class="card-header-content">
            <h3 class="card-title">
              <i class="pi pi-building"></i>
              Plants Overview
            </h3>
            <div class="filter-controls">
              <div class="search-box">
                <i class="pi pi-search"></i>
                <input 
                  v-model="searchQuery" 
                  type="text" 
                  placeholder="Search plants..."
                  @input="filterPlants"
                  class="glass-input"
                />
              </div>
              <select v-model="sortBy" @change="sortPlants" class="sort-select glass-select">
                <option value="name">Sort by Name</option>
                <option value="generation">Sort by Generation</option>
                <option value="capacityFactor">Sort by Capacity Factor</option>
                <option value="availability">Sort by Availability</option>
              </select>
              <button @click="toggleSortOrder" class="btn-sort-order glass-button">
                <i class="pi" :class="sortOrder === 'asc' ? 'pi-sort-amount-up' : 'pi-sort-amount-down'"></i>
              </button>
              <button 
                @click="toggleComparisonMode" 
                class="btn-compare-mode glass-button"
                :class="{ active: comparisonMode }"
              >
                <i class="pi pi-chart-bar"></i>
                {{ comparisonMode ? 'Cancel Compare' : 'Compare Plants' }}
              </button>
              <div class="view-toggle">
                <button 
                  @click="viewMode = 'grid'" 
                  class="btn-view" 
                  :class="{ active: viewMode === 'grid' }"
                >
                  <i class="pi pi-th-large"></i>
                </button>
                <button 
                  @click="viewMode = 'list'" 
                  class="btn-view" 
                  :class="{ active: viewMode === 'list' }"
                >
                  <i class="pi pi-list"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="comparison-bar" v-if="comparisonMode">
            <div class="comparison-info">
              <i class="pi pi-info-circle"></i>
              <span>Select 2-4 plants to compare. {{ selectedForComparison.length }} selected.</span>
            </div>
            <div class="comparison-actions">
              <button 
                @click="openComparison" 
                class="btn-view-comparison glass-button"
                :disabled="selectedForComparison.length < 2"
              >
                <i class="pi pi-eye"></i>
                View Comparison
              </button>
              <button @click="cancelComparison" class="btn-cancel-comparison glass-button">
                <i class="pi pi-times"></i>
                Cancel
              </button>
            </div>
          </div>
          <div class="filter-chips" v-if="activeFilters.length > 0">
            <span class="filter-chip" v-for="filter in activeFilters" :key="filter">
              {{ filter }}
              <i class="pi pi-times" @click="removeFilter(filter)"></i>
            </span>
          </div>
          <div class="plants-grid" :class="{ 'list-view': viewMode === 'list' }">
            <transition-group name="plant-fade">
              <div 
                v-for="plant in filteredPlants" 
                :key="plant.code" 
                class="plant-card" 
                :class="{ 
                  'no-data': !plant.hasData, 
                  'clickable': plant.hasData && !comparisonMode,
                  'comparison-mode': comparisonMode,
                  'selected-for-comparison': isSelectedForComparison(plant)
                }"
                @click="comparisonMode && plant.hasData ? comparePlant(plant) : (plant.hasData && openPlantDetails(plant))"
              >
              <div class="plant-header">
                <h4>{{ plant.name }}</h4>
                <div class="plant-badges">
                  <div class="badge-row">
                    <button 
                      v-if="plant.hasData && !comparisonMode"
                      @click.stop="toggleFavorite(plant)" 
                      class="btn-favorite"
                      :class="{ 'is-favorite': isFavorite(plant.code) }"
                      :title="isFavorite(plant.code) ? 'Remove from favorites' : 'Add to favorites'"
                    >
                      <i class="pi" :class="isFavorite(plant.code) ? 'pi-star-fill' : 'pi-star'"></i>
                    </button>
                    <span class="plant-code">{{ plant.code }}</span>
                    <div v-if="comparisonMode && plant.hasData" class="comparison-checkbox">
                      <i class="pi" :class="isSelectedForComparison(plant) ? 'pi-check-circle' : 'pi-circle'"></i>
                    </div>
                  </div>
                  <span v-if="plant.hasData" class="status-badge active">
                    <i class="pi pi-circle-fill"></i> Active
                  </span>
                  <span v-else class="status-badge inactive">
                    <i class="pi pi-circle"></i> No Data
                  </span>
                </div>
              </div>
              <div v-if="plant.hasData" class="plant-stats">
                <div class="plant-stat" @mouseenter="highlightStat($event)" @mouseleave="unhighlightStat($event)">
                  <i class="pi pi-bolt"></i>
                  <div>
                    <label>Generation</label>
                    <span class="animated-value">{{ formatNumber(plant.generation) }} kWh</span>
                  </div>
                </div>
                <div class="plant-stat" @mouseenter="highlightStat($event)" @mouseleave="unhighlightStat($event)">
                  <i class="pi pi-percentage"></i>
                  <div>
                    <label>Capacity Factor</label>
                    <span class="animated-value">{{ formatNumber(plant.capacityFactor) }}%</span>
                  </div>
                </div>
                <div class="plant-stat" @mouseenter="highlightStat($event)" @mouseleave="unhighlightStat($event)">
                  <i class="pi pi-check-circle"></i>
                  <div>
                    <label>Availability</label>
                    <span class="animated-value">{{ formatNumber(plant.availability) }}%</span>
                  </div>
                </div>
              </div>
              <div v-else class="no-data-message">
                <i class="pi pi-inbox"></i>
                <p>No data uploaded yet</p>
              </div>
              <div v-if="plant.hasData" class="plant-progress">
                <div class="progress-bar">
                  <div 
                    class="progress-fill" 
                    :style="{ 
                      width: plant.capacityFactor + '%',
                      background: getProgressColor(plant.capacityFactor)
                    }"
                  ></div>
                </div>
                <span class="progress-label">{{ formatNumber(plant.capacityFactor) }}%</span>
              </div>
              <div v-if="plant.hasData && !comparisonMode" class="plant-footer">
                <button @click.stop="comparePlant(plant)" class="btn-compare glass-button">
                  <i class="pi pi-chart-bar"></i> Compare
                </button>
                <button 
                  @click.stop="exportPlantDataAsExcel(plant)" 
                  class="btn-export glass-button"
                  :disabled="exportingPlant === plant.code"
                >
                  <i class="pi" :class="exportingPlant === plant.code ? 'pi-spin pi-spinner' : 'pi-download'"></i>
                  {{ exportingPlant === plant.code ? 'Exporting...' : 'Export' }}
                </button>
              </div>
            </div>
            </transition-group>
          </div>
          <div v-if="filteredPlants.length === 0" class="empty-state">
            <i class="pi pi-filter-slash"></i>
            <p>No plants match your filters</p>
            <button @click="clearFilters" class="btn-clear-filters glass-button">Clear Filters</button>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card glass-card glass-fade-in">
        <div class="card-header">
          <h3 class="card-title">
            <i class="pi pi-history"></i>
            Recent Uploads
          </h3>
        </div>
        <div class="card-body">
          <div v-if="recentUploads.length === 0" class="empty-state-small">
            <i class="pi pi-inbox"></i>
            <p>No recent uploads</p>
          </div>
          <div v-else class="activity-list">
            <div v-for="upload in recentUploads" :key="upload.id" class="activity-item">
              <div class="activity-icon" :class="upload.status.toLowerCase()">
                <i :class="getStatusIcon(upload.status)"></i>
              </div>
              <div class="activity-content">
                <h4>{{ upload.original_filename }}</h4>
                <p>{{ upload.plant_name }} • {{ upload.records_imported }} records</p>
              </div>
              <div class="activity-meta">
                <span class="activity-time">{{ formatDate(upload.uploaded_at) }}</span>
                <span class="activity-status" :class="upload.status.toLowerCase()">
                  {{ upload.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h3 class="section-title">
          <i class="pi pi-bolt"></i>
          Quick Actions
        </h3>
        <div class="actions-grid">
          <router-link to="/upload" class="action-card">
            <i class="pi pi-upload"></i>
            <h4>Upload Excel</h4>
            <p>Import generation data</p>
          </router-link>
          <router-link to="/view" class="action-card">
            <i class="pi pi-chart-line"></i>
            <h4>View Reports</h4>
            <p>Browse and analyze data</p>
          </router-link>
          <router-link to="/generate" class="action-card">
            <i class="pi pi-download"></i>
            <h4>Generate Report</h4>
            <p>Export to Excel</p>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Plant Detail Modal -->
    <PlantDetailModal
      :isOpen="showModal"
      :plant="selectedPlant"
      @close="closeModal"
    />

    <!-- Comparison Modal -->
    <div v-if="showComparisonModal" class="modal-overlay glass-overlay" @click="closeComparison">
      <div class="comparison-modal glass-modal" @click.stop>
        <div class="modal-header">
          <h2>
            <i class="pi pi-chart-bar"></i>
            Plant Comparison
          </h2>
          <button @click="closeComparison" class="btn-close-modal glass-button">
            <i class="pi pi-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="comparison-grid">
            <div class="comparison-column header-column">
              <div class="metric-label">Plant</div>
              <div class="metric-label">Code</div>
              <div class="metric-label">Capacity (MW)</div>
              <div class="metric-label">Generation (kWh)</div>
              <div class="metric-label">Capacity Factor (%)</div>
              <div class="metric-label">Availability (%)</div>
              <div class="metric-label">Status</div>
            </div>
            <div 
              v-for="plant in selectedForComparison" 
              :key="plant.code"
              class="comparison-column data-column"
            >
              <div class="plant-name">{{ plant.name }}</div>
              <div class="plant-code-badge">{{ plant.code }}</div>
              <div class="metric-value">{{ getPlantCapacity(plant.code) }}</div>
              <div class="metric-value highlight">{{ formatNumber(plant.generation) }}</div>
              <div class="metric-value">
                <div class="metric-with-bar">
                  <span>{{ formatNumber(plant.capacityFactor) }}</span>
                  <div class="mini-progress">
                    <div 
                      class="mini-progress-fill" 
                      :style="{ 
                        width: plant.capacityFactor + '%',
                        background: getProgressColor(plant.capacityFactor)
                      }"
                    ></div>
                  </div>
                </div>
              </div>
              <div class="metric-value">
                <div class="metric-with-bar">
                  <span>{{ formatNumber(plant.availability) }}</span>
                  <div class="mini-progress">
                    <div 
                      class="mini-progress-fill" 
                      :style="{ 
                        width: plant.availability + '%',
                        background: getProgressColor(plant.availability)
                      }"
                    ></div>
                  </div>
                </div>
              </div>
              <div class="metric-value">
                <span class="status-badge active">
                  <i class="pi pi-circle-fill"></i> Active
                </span>
              </div>
            </div>
          </div>

          <!-- Comparison Charts -->
          <div class="comparison-charts">
            <div class="chart-card">
              <h3>Generation Comparison</h3>
              <div class="bar-chart">
                <div 
                  v-for="plant in selectedForComparison" 
                  :key="'gen-' + plant.code"
                  class="bar-item"
                >
                  <div class="bar-label">{{ plant.code }}</div>
                  <div class="bar-container">
                    <div 
                      class="bar-fill"
                      :style="{ 
                        width: getBarWidth(plant.generation, 'generation') + '%',
                        background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                      }"
                    >
                      <span class="bar-value">{{ formatNumber(plant.generation) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="chart-card">
              <h3>Capacity Factor Comparison</h3>
              <div class="bar-chart">
                <div 
                  v-for="plant in selectedForComparison" 
                  :key="'cf-' + plant.code"
                  class="bar-item"
                >
                  <div class="bar-label">{{ plant.code }}</div>
                  <div class="bar-container">
                    <div 
                      class="bar-fill"
                      :style="{ 
                        width: plant.capacityFactor + '%',
                        background: getProgressColor(plant.capacityFactor)
                      }"
                    >
                      <span class="bar-value">{{ formatNumber(plant.capacityFactor) }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="exportComparison" class="btn-export-comparison glass-button">
            <i class="pi pi-download"></i>
            Export Comparison
          </button>
          <button @click="closeComparison" class="btn-close glass-button">
            Close
          </button>
        </div>
      </div>
    </div>
    </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import PlantDetailModal from './PlantDetailModal.vue';
import AppLayout from './AppLayout.vue';
import { 
  exportPlantToCSV, 
  exportComparisonToCSV, 
  exportDashboardToCSV,
  downloadCSV,
  downloadBlob,
  formatDate 
} from '../utils/exportUtils';
import pdfExporter from '../utils/pdfExport';
import favoritesManager from '../utils/favorites';
import keyboardShortcuts from '../utils/keyboardShortcuts';

export default {
  name: 'DashboardView',
  components: {
    PlantDetailModal,
    AppLayout,
  },
  data() {
    return {
      loading: true,
      stats: {
        totalGeneration: 0,
        avgCapacityFactor: 0,
        avgAvailability: 0,
        totalOperatingHours: 0,
      },
      plantsData: [],
      filteredPlants: [],
      recentUploads: [],
      showModal: false,
      selectedPlant: null,
      searchQuery: '',
      sortBy: 'name',
      sortOrder: 'asc',
      viewMode: 'grid',
      activeFilters: [],
      autoRefresh: false,
      refreshInterval: null,
      lastUpdated: null,
      comparisonMode: false,
      selectedForComparison: [],
      showComparisonModal: false,
      exportingPlant: null,
    };
  },
  mounted() {
    this.loadDashboardData();
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  methods: {
    async loadDashboardData() {
      this.loading = true;
      try {
        // Load overall statistics
        await this.loadOverallStats();
        
        // Load per-plant statistics
        await this.loadPlantsStats();
        
        // Load recent uploads
        await this.loadRecentUploads();
        
        this.lastUpdated = new Date();
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        this.loading = false;
      }
    },
    
    refreshData() {
      this.loadDashboardData();
    },
    
    toggleAutoRefresh() {
      this.autoRefresh = !this.autoRefresh;
      
      if (this.autoRefresh) {
        this.$toast.success('Auto-refresh enabled (30s interval)');
        // Refresh every 30 seconds
        this.refreshInterval = setInterval(() => {
          this.loadDashboardData();
          this.$toast.info('Dashboard refreshed', 2000);
        }, 30000);
      } else {
        this.$toast.info('Auto-refresh disabled');
        if (this.refreshInterval) {
          clearInterval(this.refreshInterval);
          this.refreshInterval = null;
        }
      }
    },
    
    // PDF Export
    async exportDashboardToPDF() {
      try {
        this.$toast.info('Generating PDF...');
        const doc = await pdfExporter.exportDashboard(this.plantsData, {
          title: 'NPC Dashboard Report',
          date: new Date().toLocaleDateString()
        });
        await pdfExporter.downloadPDF(doc, `npc-dashboard-${Date.now()}.pdf`);
        this.$toast.success('PDF downloaded successfully!');
      } catch (error) {
        console.error('PDF export error:', error);
        this.$toast.error('Failed to generate PDF. Install jspdf: npm install jspdf jspdf-autotable');
      }
    },
    
    // Favorites Management
    toggleFavorite(plant) {
      const item = {
        id: plant.code,
        type: 'plant',
        name: plant.name,
        code: plant.code,
        data: plant
      };
      
      const added = favoritesManager.toggle(item);
      
      if (added) {
        this.$toast.success(`${plant.name} added to favorites`);
      } else {
        this.$toast.info(`${plant.name} removed from favorites`);
      }
      
      // Force re-render
      this.$forceUpdate();
    },
    
    isFavorite(plantCode) {
      return favoritesManager.isFavorite(plantCode, 'plant');
    },
    
    getFavorites() {
      return favoritesManager.getByType('plant');
    },
    
    async loadOverallStats() {
      try {
        const response = await api.getReportSummary();
        this.stats = {
          totalGeneration: response.data.total_generation || 0,
          avgCapacityFactor: response.data.avg_capacity_factor || 0,
          avgAvailability: response.data.avg_availability_factor || 0,
          totalOperatingHours: response.data.total_operating_hours || 0,
        };
      } catch (error) {
        console.error('Error loading overall stats:', error);
      }
    },
    
    async loadPlantsStats() {
      try {
        const plants = await api.getPlants();
        const plantsList = plants.data.results || plants.data;
        
        console.log('=== LOADING PLANT STATS ===');
        console.log('Plants to check:', plantsList.map(p => `${p.code} (${p.name})`));
        
        // Load stats for each plant
        const plantsWithStats = await Promise.all(
          plantsList.map(async (plant) => {
            try {
              console.log(`\n--- Checking ${plant.code} ---`);
              
              // Get reports count for this plant first
              const reportsResponse = await api.getGenerationReports({ plant_code: [plant.code] });
              const reports = reportsResponse.data.results || reportsResponse.data;
              
              console.log(`${plant.code}: Found ${reports.length} reports`);
              
              // Only fetch stats if plant has data
              if (reports && reports.length > 0) {
                const stats = await api.getReportSummary({ plant_code: [plant.code] });
                console.log(`${plant.code} Summary:`, {
                  generation: stats.data.total_generation,
                  capacityFactor: stats.data.avg_capacity_factor,
                  availability: stats.data.avg_availability_factor
                });
                
                return {
                  code: plant.code,
                  name: plant.name,
                  generation: stats.data.total_generation || 0,
                  capacityFactor: stats.data.avg_capacity_factor || 0,
                  availability: stats.data.avg_availability_factor || 0,
                  hasData: true,
                };
              } else {
                // No data for this plant
                console.log(`${plant.code}: NO DATA - returning zeros`);
                return {
                  code: plant.code,
                  name: plant.name,
                  generation: 0,
                  capacityFactor: 0,
                  availability: 0,
                  hasData: false,
                };
              }
            } catch (error) {
              console.error(`${plant.code}: ERROR -`, error.message);
              return {
                code: plant.code,
                name: plant.name,
                generation: 0,
                capacityFactor: 0,
                availability: 0,
                hasData: false,
              };
            }
          })
        );
        
        console.log('\n=== FINAL RESULTS ===');
        plantsWithStats.forEach(p => {
          console.log(`${p.code}: Gen=${p.generation}, CF=${p.capacityFactor}%, Avail=${p.availability}%, HasData=${p.hasData}`);
        });
        
        this.plantsData = plantsWithStats;
        this.filteredPlants = [...plantsWithStats];
        this.sortPlants();
      } catch (error) {
        console.error('Error loading plants stats:', error);
      }
    },
    
    async loadRecentUploads() {
      try {
        const response = await api.getUploadedFiles();
        const uploads = response.data.results || response.data;
        this.recentUploads = uploads.slice(0, 5); // Get last 5 uploads
      } catch (error) {
        console.error('Error loading recent uploads:', error);
      }
    },
    
    formatNumber(value) {
      if (!value) return '0.00';
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;
      const minutes = Math.floor(diff / 60000);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      
      if (minutes < 60) return `${minutes}m ago`;
      if (hours < 24) return `${hours}h ago`;
      if (days < 7) return `${days}d ago`;
      return date.toLocaleDateString();
    },
    
    getStatusIcon(status) {
      const icons = {
        COMPLETED: 'pi pi-check-circle',
        FAILED: 'pi pi-times-circle',
        PROCESSING: 'pi pi-spin pi-spinner',
        PENDING: 'pi pi-clock',
      };
      return icons[status] || 'pi pi-circle';
    },
    
    openPlantDetails(plant) {
      // Get full plant info including capacity
      const fullPlant = {
        code: plant.code,
        name: plant.name,
        location: 'Lanao del Sur',
        capacity_mw: this.getPlantCapacity(plant.code),
      };
      this.selectedPlant = fullPlant;
      this.showModal = true;
    },
    
    getPlantCapacity(code) {
      const capacities = {
        'AGUS1': 50,
        'AGUS2': 180,
        'AGUS4': 158,
        'AGUS5': 52,
        'AGUS6': 200,
        'AGUS7': 200,
        'PULANGI4': 255,
      };
      return capacities[code] || 0;
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedPlant = null;
    },
    
    filterPlants() {
      let filtered = [...this.plantsData];
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(plant => 
          plant.name.toLowerCase().includes(query) || 
          plant.code.toLowerCase().includes(query)
        );
      }
      
      this.filteredPlants = filtered;
      this.sortPlants();
    },
    
    sortPlants() {
      this.filteredPlants.sort((a, b) => {
        let aVal = a[this.sortBy];
        let bVal = b[this.sortBy];
        
        if (this.sortBy === 'name') {
          aVal = aVal.toLowerCase();
          bVal = bVal.toLowerCase();
        }
        
        if (this.sortOrder === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
    },
    
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      this.sortPlants();
    },
    
    clearFilters() {
      this.searchQuery = '';
      this.activeFilters = [];
      this.filterPlants();
    },
    
    removeFilter(filter) {
      this.activeFilters = this.activeFilters.filter(f => f !== filter);
      this.filterPlants();
    },
    
    getProgressColor(value) {
      if (value >= 80) return 'linear-gradient(90deg, #10b981, #34d399)';
      if (value >= 60) return 'linear-gradient(90deg, #3b82f6, #60a5fa)';
      if (value >= 40) return 'linear-gradient(90deg, #f59e0b, #fbbf24)';
      return 'linear-gradient(90deg, #ef4444, #f87171)';
    },
    
    highlightStat(event) {
      event.currentTarget.style.transform = 'scale(1.05)';
      event.currentTarget.style.background = '#e0f2fe';
    },
    
    unhighlightStat(event) {
      event.currentTarget.style.transform = 'scale(1)';
      event.currentTarget.style.background = 'transparent';
    },
    
    toggleComparisonMode() {
      this.comparisonMode = !this.comparisonMode;
      if (!this.comparisonMode) {
        this.selectedForComparison = [];
      }
    },
    
    comparePlant(plant) {
      if (!this.comparisonMode) {
        // Start comparison mode with this plant
        this.comparisonMode = true;
        this.selectedForComparison = [plant];
      } else {
        // Toggle selection
        const index = this.selectedForComparison.findIndex(p => p.code === plant.code);
        if (index > -1) {
          this.selectedForComparison.splice(index, 1);
        } else {
          if (this.selectedForComparison.length < 4) {
            this.selectedForComparison.push(plant);
          } else {
            alert('You can compare up to 4 plants at a time');
          }
        }
      }
    },
    
    isSelectedForComparison(plant) {
      return this.selectedForComparison.some(p => p.code === plant.code);
    },
    
    openComparison() {
      if (this.selectedForComparison.length < 2) {
        alert('Please select at least 2 plants to compare');
        return;
      }
      this.showComparisonModal = true;
    },
    
    closeComparison() {
      this.showComparisonModal = false;
    },
    
    cancelComparison() {
      this.comparisonMode = false;
      this.selectedForComparison = [];
    },
    
    async exportPlantDataAsExcel(plant) {
      this.exportingPlant = plant.code;
      
      try {
        // Get the plant's data
        const reportsResponse = await api.getGenerationReports({ plant_code: [plant.code] });
        const reports = reportsResponse.data.results || reportsResponse.data;
        
        if (reports.length === 0) {
          alert(`No data available to export for ${plant.name}`);
          this.exportingPlant = null;
          return;
        }
        
        // Try Excel export first
        try {
          // Get date range
          const dates = reports.map(r => new Date(r.date));
          const startDate = new Date(Math.min(...dates));
          const endDate = new Date(Math.max(...dates));
          
          // Use the generate report API
          const exportData = {
            plant_codes: [plant.code],
            start_date: formatDate(startDate),
            end_date: formatDate(endDate),
            report_type: 'daily'
          };
          
          const response = await api.generateReport(exportData);
          
          // Download Excel file
          downloadBlob(
            new Blob([response.data]), 
            `${plant.code}_export_${formatDate(new Date())}.xlsx`
          );
        } catch (excelError) {
          console.log('Excel export failed, falling back to CSV:', excelError);
          
          // Fallback to CSV export
          const csvContent = exportPlantToCSV(plant, reports, this.getPlantCapacity(plant.code));
          downloadCSV(csvContent, `${plant.code}_export_${formatDate(new Date())}.csv`);
        }
        
        this.exportingPlant = null;
      } catch (error) {
        console.error('Error exporting plant data:', error);
        alert(`Failed to export data for ${plant.name}. Please try again.`);
        this.exportingPlant = null;
      }
    },
    
    exportAllDashboardData() {
      const csvContent = exportDashboardToCSV(
        this.stats, 
        this.plantsData, 
        this.getPlantCapacity.bind(this)
      );
      downloadCSV(csvContent, `dashboard_export_${formatDate(new Date())}.csv`);
    },
    
    getBarWidth(value, metric) {
      const maxValue = Math.max(...this.selectedForComparison.map(p => p[metric]));
      return maxValue > 0 ? (value / maxValue) * 100 : 0;
    },
    
    exportComparison() {
      const csvContent = exportComparisonToCSV(
        this.selectedForComparison, 
        this.getPlantCapacity.bind(this)
      );
      downloadCSV(csvContent, `plant-comparison-${formatDate(new Date())}.csv`);
    },
    
    formatLastUpdated(date) {
      const now = new Date();
      const diff = now - date;
      const seconds = Math.floor(diff / 1000);
      
      if (seconds < 60) return `${seconds}s ago`;
      const minutes = Math.floor(seconds / 60);
      if (minutes < 60) return `${minutes}m ago`;
      const hours = Math.floor(minutes / 60);
      return `${hours}h ago`;
    },
  },
};
</script>

<style scoped>
.dashboard-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 1.5rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.header-actions {
  display: flex;
  gap: 0.875rem;
  flex-wrap: wrap;
  align-items: center;
}

.btn-refresh,
.btn-auto-refresh {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 10px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

.btn-refresh::before,
.btn-auto-refresh::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transition: left 0.5s ease;
}

.btn-refresh:hover:not(:disabled)::before,
.btn-auto-refresh:hover::before {
  left: 100%;
}

.btn-refresh:hover:not(:disabled),
.btn-auto-refresh:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.2);
}

.btn-refresh:active:not(:disabled),
.btn-auto-refresh:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px -1px rgba(59, 130, 246, 0.15);
}

.btn-refresh i,
.btn-auto-refresh i {
  font-size: 1rem;
  transition: transform 0.3s ease;
}

.btn-refresh:hover:not(:disabled) i,
.btn-auto-refresh:hover i {
  transform: scale(1.1);
}

.btn-export-pdf,
.btn-export-csv {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
}

.btn-export-pdf::before,
.btn-export-csv::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-export-pdf:hover::before,
.btn-export-csv:hover::before {
  left: 100%;
}

.btn-export-pdf {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.btn-export-pdf:hover {
  background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.4), 0 4px 6px -2px rgba(220, 38, 38, 0.2);
}

.btn-export-pdf:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.3);
}

.btn-export-csv {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
}

.btn-export-csv:hover {
  background: linear-gradient(135deg, #15803d 0%, #166534 100%);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(22, 163, 74, 0.4), 0 4px 6px -2px rgba(22, 163, 74, 0.2);
}

.btn-export-csv:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.3);
}

.btn-export-pdf i,
.btn-export-csv i {
  font-size: 1.125rem;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.btn-auto-refresh.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3), 0 2px 4px -1px rgba(59, 130, 246, 0.2);
}

.btn-auto-refresh.active::before {
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
}

.btn-auto-refresh.active:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  border-color: #2563eb;
  color: white;
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4), 0 4px 6px -2px rgba(59, 130, 246, 0.2);
}

.btn-auto-refresh.active i {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.last-updated {
  font-size: 0.8125rem;
  color: #94a3b8;
  font-style: italic;
}

.page-title {
  font-size: 1.75rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
}

.page-title i {
  color: #3b82f6;
}

.page-description {
  color: #64748b;
  font-size: 0.9375rem;
  margin: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  gap: 1rem;
}

.loading-state i {
  font-size: 3rem;
  color: #3b82f6;
}

.loading-state p {
  color: #64748b;
  font-size: 1.125rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card:hover {
  box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.75rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-content label {
  display: block;
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stat-value {
  display: block;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.stat-unit {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-left: 0.25rem;
}

/* Card */
.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.card-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 0.75rem;
  color: #94a3b8;
  font-size: 0.875rem;
}

.search-box input {
  padding: 0.5rem 0.75rem 0.5rem 2.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  width: 200px;
  transition: all 0.2s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.sort-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  background: white;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-select:focus {
  outline: none;
  border-color: #3b82f6;
}

.btn-sort-order {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #475569;
}

.btn-sort-order:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  color: #3b82f6;
}

.view-toggle {
  display: flex;
  gap: 0.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.btn-view {
  padding: 0.5rem 0.75rem;
  border: none;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #475569;
}

.btn-view:hover {
  background: #f8fafc;
}

.btn-view.active {
  background: #3b82f6;
  color: white;
}

.filter-chips {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
}

.filter-chip i {
  cursor: pointer;
  font-size: 0.75rem;
}

.filter-chip i:hover {
  color: #1e3a8a;
}

.card-title {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
}

.card-title i {
  color: #3b82f6;
}

.card-body {
  padding: 1.5rem;
}

/* Plants Grid */
.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

.plants-grid.list-view {
  grid-template-columns: 1fr;
}

.plants-grid.list-view .plant-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1.5rem;
}

.plants-grid.list-view .plant-header {
  flex: 0 0 200px;
}

.plants-grid.list-view .plant-stats {
  flex: 1;
  flex-direction: row;
  gap: 2rem;
}

.plant-fade-enter-active,
.plant-fade-leave-active {
  transition: all 0.3s ease;
}

.plant-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.plant-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.plant-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: visible;
  display: flex;
  flex-direction: column;
}

.plant-card.clickable {
  cursor: pointer;
}

.plant-card.clickable:hover {
  border-color: #3b82f6;
  box-shadow: 0 8px 16px -4px rgba(59, 130, 246, 0.2);
  transform: translateY(-4px);
}

.plant-card:not(.clickable):hover {
  border-color: #cbd5e0;
}

.plant-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
  gap: 0.75rem;
}

.plant-header h4 {
  font-size: 1.125rem;
  color: #1e293b;
  margin: 0;
  font-weight: 600;
  flex: 1;
  min-width: 0;
  word-wrap: break-word;
}

.plant-badges {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-end;
  flex-shrink: 0;
}

.badge-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.plant-code {
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.status-badge.active {
  background: #dcfce7;
  color: #16a34a;
}

.status-badge.inactive {
  background: #f1f5f9;
  color: #64748b;
}

.status-badge i {
  font-size: 0.5rem;
}

.plant-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.plant-stat {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.plant-stat i {
  color: #3b82f6;
  font-size: 1.25rem;
}

.plant-stat div {
  flex: 1;
}

.plant-stat label {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.plant-stat span {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.animated-value {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.plant-card.no-data {
  opacity: 0.6;
}

.no-data-message {
  text-align: center;
  padding: 2rem 1rem;
  color: #94a3b8;
}

.no-data-message i {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  display: block;
}

.no-data-message p {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 500;
}

.plant-progress {
  margin-top: 1rem;
  position: relative;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.6s ease;
  border-radius: 4px;
}

.progress-label {
  position: absolute;
  right: 0;
  top: -1.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
}

.plant-footer {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.btn-compare,
.btn-export {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  min-width: 0;
}

.btn-compare i,
.btn-export i {
  flex-shrink: 0;
}

.btn-compare:hover {
  background: #dbeafe;
  border-color: #3b82f6;
  color: #1e40af;
}

.btn-export:hover {
  background: #dcfce7;
  border-color: #16a34a;
  color: #15803d;
}

.btn-export:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-export:disabled:hover {
  background: white;
  border-color: #e2e8f0;
  color: #475569;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #94a3b8;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-state p {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 500;
}

.btn-clear-filters {
  padding: 0.625rem 1.25rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-clear-filters:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

/* Comparison Mode */
.btn-compare-mode {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-compare-mode:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-compare-mode.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.comparison-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #dbeafe;
  border: 1px solid #93c5fd;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.comparison-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #1e40af;
  font-weight: 500;
}

.comparison-info i {
  font-size: 1.25rem;
}

.comparison-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-view-comparison,
.btn-cancel-comparison {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-view-comparison {
  background: #3b82f6;
  color: white;
}

.btn-view-comparison:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

.btn-view-comparison:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel-comparison {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.btn-cancel-comparison:hover {
  background: #f8fafc;
  border-color: #cbd5e0;
}

.plant-card.comparison-mode {
  cursor: pointer;
}

.plant-card.selected-for-comparison {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.comparison-checkbox {
  font-size: 1.25rem;
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.comparison-checkbox i {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.selected-for-comparison .comparison-checkbox {
  color: #16a34a;
}

/* Favorite Button */
.btn-favorite {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #94a3b8;
  transition: all 0.2s ease;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.btn-favorite:hover {
  color: #fbbf24;
  transform: scale(1.15);
  background: rgba(251, 191, 36, 0.1);
}

.btn-favorite.is-favorite {
  color: #fbbf24;
  animation: starPulse 0.3s ease;
}

.btn-favorite.is-favorite:hover {
  color: #f59e0b;
}

@keyframes starPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

/* Comparison Modal */
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
  padding: 2rem;
  animation: fadeIn 0.2s ease;
}

.comparison-modal {
  background: white;
  border-radius: 16px;
  max-width: 1200px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-header h2 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0;
  font-size: 1.5rem;
  color: #1e293b;
}

.modal-header h2 i {
  color: #3b82f6;
}

.btn-close-modal {
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s ease;
}

.btn-close-modal:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 200px repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
  overflow-x: auto;
  padding-bottom: 1rem;
}

.comparison-column {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.header-column {
  font-weight: 700;
  color: #1e293b;
}

.metric-label {
  padding: 1.25rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 10px;
  font-size: 0.9375rem;
  min-height: 70px;
  display: flex;
  align-items: center;
  font-weight: 600;
  border: 1px solid #e2e8f0;
}

.data-column {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 14px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.data-column:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  transform: translateY(-2px);
}

.plant-name {
  padding: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 10px;
  font-size: 1rem;
  min-height: 70px;
  display: flex;
  align-items: center;
  border: 1px solid #93c5fd;
}

.plant-code-badge {
  padding: 1.25rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 10px;
  font-weight: 700;
  text-align: center;
  font-size: 0.9375rem;
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 0.05em;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
}

.metric-value {
  padding: 1.25rem;
  background: #f8fafc;
  border-radius: 10px;
  font-size: 1rem;
  color: #1e293b;
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  border: 1px solid #e2e8f0;
}

.metric-value.highlight {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  font-weight: 700;
  border-color: #fbbf24;
  color: #92400e;
}

.metric-with-bar {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.mini-progress {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.mini-progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.comparison-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.chart-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.chart-card h3 {
  margin: 0 0 2rem 0;
  font-size: 1.25rem;
  color: #1e293b;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}

.chart-card h3::before {
  content: '';
  width: 4px;
  height: 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 2px;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideInLeft 0.5s ease;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.bar-label {
  width: 100px;
  font-weight: 700;
  color: #1e293b;
  font-size: 0.9375rem;
  text-align: right;
  flex-shrink: 0;
}

.bar-container {
  flex: 1;
  height: 50px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-radius: 10px;
  overflow: visible;
  position: relative;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
}

.bar-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 1rem;
  border-radius: 10px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 100px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.bar-fill::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.bar-value {
  color: white;
  font-weight: 700;
  font-size: 0.9375rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 1;
  white-space: nowrap;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.btn-export-comparison,
.btn-close {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-export-comparison {
  background: #16a34a;
  color: white;
}

.btn-export-comparison:hover {
  background: #15803d;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.3);
}

.btn-close {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.btn-close:hover {
  background: #f8fafc;
  border-color: #cbd5e0;
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.activity-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e0;
}

.activity-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.activity-icon i {
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-icon.completed {
  background: #dcfce7;
  color: #16a34a;
}

.activity-icon.failed {
  background: #fee2e2;
  color: #dc2626;
}

.activity-icon.processing {
  background: #dbeafe;
  color: #2563eb;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-content h4 {
  font-size: 0.9375rem;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.activity-content p {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

.activity-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.activity-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.activity-status {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.activity-status.completed {
  background: #dcfce7;
  color: #16a34a;
}

.activity-status.failed {
  background: #fee2e2;
  color: #dc2626;
}

.activity-status.processing {
  background: #dbeafe;
  color: #2563eb;
}

/* Quick Actions */
.quick-actions {
  margin-top: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.section-title i {
  color: #3b82f6;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
  transform: translateY(-4px);
}

.action-card i {
  font-size: 2.5rem;
  color: #3b82f6;
  margin-bottom: 1rem;
}

.action-card h4 {
  font-size: 1.125rem;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.action-card p {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

.empty-state-small {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
}

.empty-state-small i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.empty-state-small p {
  margin: 0;
  font-size: 0.9375rem;
}
</style>
