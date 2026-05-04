<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Header -->
      <div class="modal-header">
        <div class="header-content">
          <button class="back-button" @click="closeModal">
            <i class="pi pi-arrow-left"></i>
          </button>
          <div class="plant-info">
            <h2>{{ simplifyPlantName(plant.name) }}</h2>
            <p>{{ plant.location }} • {{ plant.capacity_mw }} MW</p>
          </div>
        </div>
        <button class="close-button" @click="closeModal">
          <i class="pi pi-times"></i>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <i class="pi pi-spin pi-spinner"></i>
        <p>Loading plant data...</p>
      </div>

      <!-- No Data State -->
      <div v-else-if="!hasData" class="no-data-state">
        <i class="pi pi-inbox"></i>
        <h3>No Data Available</h3>
        <p>No generation reports have been uploaded for this plant yet.</p>
        <button class="upload-button" @click="goToUpload">
          <i class="pi pi-upload"></i>
          Upload Data
        </button>
      </div>

      <!-- Content -->
      <div v-else class="modal-content">
        <!-- Summary Stats -->
        <div class="stats-row">
          <div class="stat-box">
            <i class="pi pi-bolt"></i>
            <div>
              <label>Total Generation</label>
              <span>{{ formatNumber(stats.totalGeneration) }} kWh</span>
            </div>
          </div>
          <div class="stat-box">
            <i class="pi pi-percentage"></i>
            <div>
              <label>Avg Capacity Factor</label>
              <span>{{ formatNumber(stats.avgCapacityFactor) }}%</span>
            </div>
          </div>
          <div class="stat-box">
            <i class="pi pi-check-circle"></i>
            <div>
              <label>Avg Availability</label>
              <span>{{ formatNumber(stats.avgAvailability) }}%</span>
            </div>
          </div>
          <div class="stat-box">
            <i class="pi pi-clock"></i>
            <div>
              <label>Operating Hours</label>
              <span>{{ formatNumber(stats.totalOperatingHours) }} hrs</span>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="charts-container">
          <!-- Generation Trend Chart -->
          <div class="chart-card">
            <h3><i class="pi pi-chart-line"></i> Generation Trend</h3>
            <div class="chart-wrapper">
              <canvas ref="generationChart"></canvas>
            </div>
          </div>

          <!-- Capacity Factor Chart -->
          <div class="chart-card">
            <h3><i class="pi pi-percentage"></i> Capacity Factor Trend</h3>
            <div class="chart-wrapper">
              <canvas ref="capacityChart"></canvas>
            </div>
          </div>

          <!-- Unit Performance Chart -->
          <div class="chart-card">
            <h3><i class="pi pi-chart-bar"></i> Unit Performance Comparison</h3>
            <div class="chart-wrapper">
              <canvas ref="unitChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  LineController,
  BarController,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import api from '../services/api';

Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  LineController,
  BarController,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default {
  name: 'PlantDetailModal',
  props: {
    isOpen: Boolean,
    plant: Object,
  },
  data() {
    return {
      loading: false,
      hasData: false,
      stats: {
        totalGeneration: 0,
        avgCapacityFactor: 0,
        avgAvailability: 0,
        totalOperatingHours: 0,
      },
      dailyData: [],
      unitData: [],
      charts: {
        generation: null,
        capacity: null,
        unit: null,
      },
      chartTimeout: null,
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal && this.plant) {
        this.loadPlantData();
      } else if (!newVal) {
        // Clear timeout and destroy charts when modal closes
        if (this.chartTimeout) {
          clearTimeout(this.chartTimeout);
          this.chartTimeout = null;
        }
        this.destroyCharts();
      }
    },
  },
  methods: {
    async loadPlantData() {
      this.loading = true;
      this.hasData = false;
      
      try {
        console.log('Loading data for plant:', this.plant.code);
        
        // Get reports for this plant
        const reportsResponse = await api.getGenerationReports({ 
          plant_code: [this.plant.code] 
        });
        const reports = reportsResponse.data.results || reportsResponse.data;

        console.log('Reports received:', reports.length);

        if (!reports || reports.length === 0) {
          this.hasData = false;
          this.loading = false;
          return;
        }

        this.hasData = true;

        // Get summary stats
        const statsResponse = await api.getReportSummary({ 
          plant_code: [this.plant.code] 
        });
        this.stats = {
          totalGeneration: statsResponse.data.total_generation || 0,
          avgCapacityFactor: statsResponse.data.avg_capacity_factor || 0,
          avgAvailability: statsResponse.data.avg_availability_factor || 0,
          totalOperatingHours: statsResponse.data.total_operating_hours || 0,
        };

        // Process daily data
        this.processDailyData(reports);
        
        // Process unit data
        this.processUnitData(reports);

        console.log('Daily data points:', this.dailyData.length);
        console.log('Unit data points:', this.unitData.length);

      } catch (error) {
        console.error('Error loading plant data:', error);
        this.hasData = false;
      } finally {
        this.loading = false;
        
        // Clear any existing timeout
        if (this.chartTimeout) {
          clearTimeout(this.chartTimeout);
        }
        
        // Wait longer for DOM to be fully ready
        await this.$nextTick();
        await this.$nextTick(); // Double nextTick for safety
        this.chartTimeout = setTimeout(() => {
          // Only create charts if modal is still open
          if (this.hasData && this.isOpen) {
            this.createCharts();
          }
          this.chartTimeout = null;
        }, 300); // Increased delay
      }
    },

    processDailyData(reports) {
      const dailyMap = {};
      reports.forEach(report => {
        const date = report.report_date;
        if (!dailyMap[date]) {
          dailyMap[date] = {
            generation: 0,
            capacityFactor: [],
            count: 0,
          };
        }
        dailyMap[date].generation += parseFloat(report.generation_kwh || 0);
        dailyMap[date].capacityFactor.push(parseFloat(report.capacity_factor || 0));
        dailyMap[date].count++;
      });

      this.dailyData = Object.keys(dailyMap)
        .sort()
        .map(date => ({
          date,
          generation: dailyMap[date].generation,
          capacityFactor: dailyMap[date].capacityFactor.reduce((a, b) => a + b, 0) / dailyMap[date].count,
        }));
    },

    processUnitData(reports) {
      const unitMap = {};
      reports.forEach(report => {
        const unitName = report.unit_name || `Unit ${report.unit_number}`;
        if (!unitMap[unitName]) {
          unitMap[unitName] = {
            generation: 0,
            capacityFactor: [],
          };
        }
        unitMap[unitName].generation += parseFloat(report.generation_kwh || 0);
        unitMap[unitName].capacityFactor.push(parseFloat(report.capacity_factor || 0));
      });

      this.unitData = Object.keys(unitMap).map(unit => ({
        unit,
        generation: unitMap[unit].generation,
        capacityFactor: unitMap[unit].capacityFactor.reduce((a, b) => a + b, 0) / unitMap[unit].capacityFactor.length,
      }));
    },

    createCharts() {
      console.log('=== CREATING CHARTS ===');
      console.log('Has data:', this.hasData);
      console.log('Daily data:', this.dailyData.length, 'points');
      console.log('Unit data:', this.unitData.length, 'units');
      
      this.destroyCharts();

      if (!this.hasData || this.dailyData.length === 0) {
        console.warn('No data to display charts');
        return;
      }

      // Check if refs exist
      if (!this.$refs.generationChart || !this.$refs.capacityChart || !this.$refs.unitChart) {
        console.error('Chart canvas refs not found!');
        return;
      }

      try {
        // Generation Trend Chart
        console.log('Creating generation chart...');
        const genCtx = this.$refs.generationChart.getContext('2d');
        this.charts.generation = new Chart(genCtx, {
          type: 'line',
          data: {
            labels: this.dailyData.map(d => {
              const date = new Date(d.date);
              return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }),
            datasets: [{
              label: 'Generation (kWh)',
              data: this.dailyData.map(d => d.generation),
              borderColor: '#003d82',
              backgroundColor: 'rgba(0, 61, 130, 0.1)',
              tension: 0.4,
              fill: true,
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
              legend: { display: false },
            },
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: (value) => value.toLocaleString(),
                },
              },
            },
          },
        });
        console.log('✓ Generation chart created');

        // Capacity Factor Chart
        console.log('Creating capacity chart...');
        const capCtx = this.$refs.capacityChart.getContext('2d');
        if (!capCtx) {
          console.error('Failed to get capacity chart context');
          return;
        }
        
        this.charts.capacity = new Chart(capCtx, {
          type: 'line',
          data: {
            labels: this.dailyData.map(d => {
              const date = new Date(d.date);
              return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }),
            datasets: [{
              label: 'Capacity Factor (%)',
              data: this.dailyData.map(d => d.capacityFactor),
              borderColor: '#00a651',
              backgroundColor: 'rgba(0, 166, 81, 0.1)',
              tension: 0.4,
              fill: true,
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
              legend: { display: false },
            },
            scales: {
              y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                  callback: (value) => value + '%',
                },
              },
            },
          },
        });
        console.log('✓ Capacity chart created');

        // Unit Performance Chart
        console.log('Creating unit chart...');
        const unitCtx = this.$refs.unitChart.getContext('2d');
        if (!unitCtx) {
          console.error('Failed to get unit chart context');
          return;
        }
        
        this.charts.unit = new Chart(unitCtx, {
          type: 'bar',
          data: {
            labels: this.unitData.map(u => u.unit),
            datasets: [{
              label: 'Generation (kWh)',
              data: this.unitData.map(u => u.generation),
              backgroundColor: [
                'rgba(0, 61, 130, 0.8)',
                'rgba(0, 166, 81, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(153, 102, 255, 0.8)',
              ],
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
              legend: { display: false },
            },
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: (value) => value.toLocaleString(),
                },
              },
            },
          },
        });
        console.log('✓ Unit chart created');
        console.log('=== ALL CHARTS CREATED SUCCESSFULLY ===');

      } catch (error) {
        console.error('Error creating charts:', error);
      }
    },

    destroyCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          try {
            // Stop all animations before destroying
            chart.stop();
            chart.destroy();
          } catch (e) {
            // Silently ignore errors during destruction
          }
        }
      });
      this.charts = { generation: null, capacity: null, unit: null };
    },

    closeModal() {
      // Clear any pending chart creation
      if (this.chartTimeout) {
        clearTimeout(this.chartTimeout);
        this.chartTimeout = null;
      }
      this.destroyCharts();
      this.$emit('close');
    },

    goToUpload() {
      this.closeModal();
      this.$router.push('/upload');
    },

    formatNumber(value) {
      if (!value) return '0.00';
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    },

    simplifyPlantName(name) {
      if (!name) return '';
      return name.replace(/ Hydroelectric Power Plant/gi, '');
    },
  },
  beforeUnmount() {
    // Clear timeout and destroy charts before component unmounts
    if (this.chartTimeout) {
      clearTimeout(this.chartTimeout);
      this.chartTimeout = null;
    }
    this.destroyCharts();
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
}

.modal-container {
  background: white;
  border-radius: 1rem;
  max-width: 1200px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #003d82 0%, #00a651 100%);
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button,
.close-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.back-button:hover,
.close-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.plant-info h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.plant-info p {
  margin: 0.25rem 0 0 0;
  opacity: 0.9;
  font-size: 0.9375rem;
}

.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.loading-state,
.no-data-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-state i {
  font-size: 3rem;
  color: #003d82;
  margin-bottom: 1rem;
}

.no-data-state i {
  font-size: 4rem;
  color: #cbd5e0;
  margin-bottom: 1rem;
}

.no-data-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1a202c;
}

.no-data-state p {
  margin: 0 0 1.5rem 0;
  color: #718096;
}

.upload-button {
  background: linear-gradient(135deg, #003d82 0%, #00a651 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.2s;
}

.upload-button:hover {
  transform: translateY(-2px);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 1.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 2px solid #e2e8f0;
}

.stat-box i {
  font-size: 2rem;
  color: #003d82;
}

.stat-box label {
  display: block;
  font-size: 0.875rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.stat-box span {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a202c;
}

.charts-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.chart-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.chart-card h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.125rem;
  color: #1a202c;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chart-card h3 i {
  color: #003d82;
}

.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
}

.chart-wrapper canvas {
  max-height: 300px;
}
</style>
