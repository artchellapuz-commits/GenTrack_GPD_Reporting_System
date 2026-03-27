<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h2 class="page-title">
        <i class="pi pi-chart-line"></i>
        Dashboard
      </h2>
      <p class="page-description">
        Overview of Agus Hydroelectric Power Plants Generation Performance
      </p>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <div class="charts-grid">
        <GenerationTrendChart />
        <CapacityFactorChart />
      </div>
    </div>

    <!-- Stats Grid -->
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

    <!-- Plants Grid -->
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
            v-for="plant in plants" 
            :key="plant.code" 
            class="plant-card"
          >
            <div class="plant-header">
              <h4>{{ plant.name }}</h4>
              <span class="plant-code">{{ plant.code }}</span>
            </div>
            <div class="plant-info">
              <div class="info-item">
                <i class="pi pi-bolt"></i>
                <span>{{ plant.capacity_mw }} MW</span>
              </div>
              <div class="info-item">
                <i class="pi pi-map-marker"></i>
                <span>{{ plant.location }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import GenerationTrendChart from './charts/GenerationTrendChart.vue';
import CapacityFactorChart from './charts/CapacityFactorChart.vue';

export default {
  name: 'DashboardWithCharts',
  components: {
    GenerationTrendChart,
    CapacityFactorChart
  },
  data() {
    return {
      plants: [],
      stats: {
        totalGeneration: 0,
        avgCapacityFactor: 0,
        avgAvailability: 0,
        totalOperatingHours: 0
      }
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    async loadData() {
      try {
        // Load plants
        const plantsResponse = await axios.get(`${process.env.VUE_APP_API_URL}/plants/`);
        this.plants = plantsResponse.data;

        // Load summary stats
        const summaryResponse = await axios.get(`${process.env.VUE_APP_API_URL}/generation-reports/summary/`);
        this.calculateStats(summaryResponse.data);
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      }
    },
    calculateStats(summaryData) {
      let totalGen = 0;
      let totalCF = 0;
      let totalAvail = 0;
      let totalHours = 0;
      let count = 0;

      Object.values(summaryData).forEach(plant => {
        totalGen += plant.total_generation || 0;
        totalCF += plant.avg_capacity_factor || 0;
        totalAvail += plant.avg_availability || 0;
        totalHours += plant.total_operating_hours || 0;
        count++;
      });

      this.stats = {
        totalGeneration: totalGen,
        avgCapacityFactor: count > 0 ? totalCF / count : 0,
        avgAvailability: count > 0 ? totalAvail / count : 0,
        totalOperatingHours: totalHours
      };
    },
    formatNumber(value) {
      if (!value) return '0';
      return parseFloat(value).toLocaleString('en-US', {
        maximumFractionDigits: 2
      });
    }
  }
};
</script>

<style scoped>
.dashboard-page {
  padding: 0;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-description {
  color: #7f8c8d;
  margin: 0;
  font-size: 16px;
}

/* Charts Section */
.charts-section {
  margin-bottom: 32px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-content label {
  display: block;
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  display: block;
}

.stat-unit {
  font-size: 14px;
  color: #95a5a6;
}

/* Card */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #ecf0f1;
}

.card-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-body {
  padding: 24px;
}

/* Plants Grid */
.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.plant-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
}

.plant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.plant-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.plant-code {
  background: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.plant-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .plants-grid {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style>
