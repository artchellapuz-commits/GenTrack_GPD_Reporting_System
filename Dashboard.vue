<template>
  <div class="dashboard-page">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">
        <i class="pi pi-chart-line"></i>
        Dashboard
      </h2>
      <p class="page-description">
        Overview of Agus Hydroelectric Power Plants Generation Performance
      </p>
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
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <i class="pi pi-bolt"></i>
          </div>
          <div class="stat-content">
            <label>Total Generation</label>
            <span class="stat-value">{{ formatNumber(stats.totalGeneration) }}</span>
            <span class="stat-unit">kWh</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <i class="pi pi-percentage"></i>
          </div>
          <div class="stat-content">
            <label>Avg Capacity Factor</label>
            <span class="stat-value">{{ formatNumber(stats.avgCapacityFactor) }}</span>
            <span class="stat-unit">%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <label>Avg Availability</label>
            <span class="stat-value">{{ formatNumber(stats.avgAvailability) }}</span>
            <span class="stat-unit">%</span>
          </div>
        </div>

        <div class="stat-card">
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
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            <i class="pi pi-building"></i>
            Plants Overview
          </h3>
        </div>
        <div class="card-body">
          <div class="plants-grid">
            <div 
              v-for="plant in plantsData" 
              :key="plant.code" 
              class="plant-card" 
              :class="{ 'no-data': !plant.hasData, 'clickable': plant.hasData }"
              @click="plant.hasData && openPlantDetails(plant)"
            >
              <div class="plant-header">
                <h4>{{ plant.name }}</h4>
                <span class="plant-code">{{ plant.code }}</span>
              </div>
              <div v-if="plant.hasData" class="plant-stats">
                <div class="plant-stat">
                  <i class="pi pi-bolt"></i>
                  <div>
                    <label>Generation</label>
                    <span>{{ formatNumber(plant.generation) }} kWh</span>
                  </div>
                </div>
                <div class="plant-stat">
                  <i class="pi pi-percentage"></i>
                  <div>
                    <label>Capacity Factor</label>
                    <span>{{ formatNumber(plant.capacityFactor) }}%</span>
                  </div>
                </div>
                <div class="plant-stat">
                  <i class="pi pi-check-circle"></i>
                  <div>
                    <label>Availability</label>
                    <span>{{ formatNumber(plant.availability) }}%</span>
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
                    :style="{ width: plant.capacityFactor + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card">
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
  </div>
</template>

<script>
import api from '../services/api';
import PlantDetailModal from './PlantDetailModal.vue';

export default {
  name: 'DashboardView',
  components: {
    PlantDetailModal,
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
      recentUploads: [],
      showModal: false,
      selectedPlant: null,
    };
  },
  mounted() {
    this.loadDashboardData();
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
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        this.loading = false;
      }
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
        COMPLETED: 'pi-check-circle',
        FAILED: 'pi-times-circle',
        PROCESSING: 'pi-spin pi-spinner',
        PENDING: 'pi-clock',
      };
      return icons[status] || 'pi-circle';
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
      };
      return capacities[code] || 0;
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedPlant = null;
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
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  color: #1a202c;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.page-title i {
  color: var(--npc-primary);
}

.page-description {
  color: #718096;
  font-size: 1rem;
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
  color: var(--npc-primary);
}

.loading-state p {
  color: #718096;
  font-size: 1.125rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: all 0.3s ease;
}

/* .stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
} */

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 1rem;
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
  color: #718096;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stat-value {
  display: block;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1a202c;
  line-height: 1;
}

.stat-unit {
  font-size: 0.875rem;
  color: #a0aec0;
  margin-left: 0.25rem;
}

/* Plants Grid */
.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.plant-card {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.plant-card.clickable {
  cursor: pointer;
}

.plant-card.clickable:hover {
  border-color: var(--npc-primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 61, 130, 0.1);
}

.plant-card:not(.clickable):hover {
  border-color: #cbd5e0;
}

.plant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.plant-header h4 {
  font-size: 1.125rem;
  color: #1a202c;
  margin: 0;
  font-weight: 600;
}

.plant-code {
  background: var(--npc-primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
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
}

.plant-stat i {
  color: var(--npc-primary);
  font-size: 1.25rem;
}

.plant-stat div {
  flex: 1;
}

.plant-stat label {
  display: block;
  font-size: 0.75rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.plant-stat span {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
}

.plant-card.no-data {
  opacity: 0.6;
}

.no-data-message {
  text-align: center;
  padding: 2rem 1rem;
  color: #a0aec0;
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
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--npc-primary), var(--npc-secondary));
  transition: width 0.3s ease;
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
  background: #f7fafc;
  border-radius: 0.75rem;
  transition: all 0.2s ease;
}

.activity-item:hover {
  background: #edf2f7;
}

.activity-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.activity-icon.completed {
  background: #c6f6d5;
  color: #22543d;
}

.activity-icon.failed {
  background: #fed7d7;
  color: #742a2a;
}

.activity-icon.processing {
  background: #bee3f8;
  color: #2c5282;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-content h4 {
  font-size: 0.9375rem;
  color: #1a202c;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.activity-content p {
  font-size: 0.875rem;
  color: #718096;
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
  color: #a0aec0;
}

.activity-status {
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.activity-status.completed {
  background: #c6f6d5;
  color: #22543d;
}

.activity-status.failed {
  background: #fed7d7;
  color: #742a2a;
}

.activity-status.processing {
  background: #bee3f8;
  color: #2c5282;
}

/* Quick Actions */
.quick-actions {
  margin-top: 2rem;
}

.section-title {
  font-size: 1.25rem;
  color: #1a202c;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title i {
  color: var(--npc-primary);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem 1.5rem;
  text-align: center;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  border-color: var(--npc-primary);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 61, 130, 0.15);
}

.action-card i {
  font-size: 2.5rem;
  color: var(--npc-primary);
  margin-bottom: 1rem;
}

.action-card h4 {
  font-size: 1.125rem;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.action-card p {
  font-size: 0.875rem;
  color: #718096;
  margin: 0;
}

.empty-state-small {
  text-align: center;
  padding: 2rem;
  color: #a0aec0;
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
