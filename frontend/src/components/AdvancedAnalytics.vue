<template>
  <AppLayout>
    <div class="advanced-analytics">
      <h2>Advanced Analytics</h2>

    <div class="analytics-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
      </button>
    </div>

    <!-- Performance Trends -->
    <div v-if="activeTab === 'trends'" class="analytics-section">
      <div class="section-header">
        <h3><i class="pi pi-chart-line"></i> Performance Trends</h3>
        <div class="filters">
          <div class="filter-group">
            <label><i class="pi pi-building"></i> Plant</label>
            <select v-model="trendsPlant" @change="loadTrends" class="filter-select">
              <option value="">All Plants</option>
              <option v-for="plant in plants" :key="plant.id" :value="plant.id">
                {{ plant.name }}
              </option>
            </select>
          </div>
          <div class="filter-group">
            <label><i class="pi pi-calendar"></i> Period</label>
            <select v-model="trendsDays" @change="loadTrends" class="filter-select">
              <option :value="7">Last 7 Days</option>
              <option :value="30">Last 30 Days</option>
              <option :value="90">Last 90 Days</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="trendsData" class="trends-content">
        <div class="summary-cards">
          <div class="summary-card">
            <div class="card-icon" style="background: #dbeafe;">
              <i class="pi pi-bolt" style="color: #3b82f6;"></i>
            </div>
            <div class="card-content">
              <p class="card-label">Total Generation</p>
              <h3>{{ trendsData.summary.total_generation_mwh.toFixed(2) }} MWh</h3>
            </div>
          </div>

          <div class="summary-card">
            <div class="card-icon" style="background: #dcfce7;">
              <i class="pi pi-chart-line" style="color: #16a34a;"></i>
            </div>
            <div class="card-content">
              <p class="card-label">Avg Capacity Factor</p>
              <h3>{{ trendsData.summary.avg_capacity_factor.toFixed(2) }}%</h3>
            </div>
          </div>

          <div class="summary-card">
            <div class="card-icon" style="background: #fef3c7;">
              <i class="pi pi-calendar" style="color: #d97706;"></i>
            </div>
            <div class="card-content">
              <p class="card-label">Avg Daily Generation</p>
              <h3>{{ trendsData.summary.avg_daily_generation_mwh.toFixed(2) }} MWh</h3>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <canvas ref="trendsChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Plant Comparison -->
    <div v-if="activeTab === 'comparison'" class="analytics-section">
      <div class="section-header">
        <h3><i class="pi pi-chart-bar"></i> Plant Comparison</h3>
        <button @click="loadComparison" class="btn-refresh">
          <i class="pi pi-refresh"></i> Refresh
        </button>
      </div>

      <div v-if="comparisonData" class="comparison-content">
        <div class="fleet-summary">
          <h4>Fleet Summary</h4>
          <div class="fleet-stats">
            <div class="stat-item">
              <span class="stat-label">Total Capacity</span>
              <span class="stat-value">{{ comparisonData.fleet_summary.total_capacity_mw.toFixed(2) }} MW</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Total Generation</span>
              <span class="stat-value">{{ comparisonData.fleet_summary.total_generation_mwh.toFixed(2) }} MWh</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Fleet Avg CF</span>
              <span class="stat-value">{{ comparisonData.fleet_summary.fleet_avg_capacity_factor.toFixed(2) }}%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Best Performer</span>
              <span class="stat-value">{{ comparisonData.fleet_summary.best_performer }}</span>
            </div>
          </div>
        </div>

        <div class="comparison-table">
          <table>
            <thead>
              <tr>
                <th>Plant</th>
                <th>Capacity (MW)</th>
                <th>Generation (MWh)</th>
                <th>Avg CF (%)</th>
                <th>Availability (%)</th>
                <th>Performance Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="plant in comparisonData.plants" :key="plant.plant_id">
                <td><strong>{{ plant.plant_name }}</strong></td>
                <td>{{ plant.capacity_mw.toFixed(2) }}</td>
                <td>{{ plant.total_generation_mwh.toFixed(2) }}</td>
                <td>
                  <div class="progress-cell">
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: plant.avg_capacity_factor + '%' }"></div>
                    </div>
                    <span>{{ plant.avg_capacity_factor.toFixed(2) }}%</span>
                  </div>
                </td>
                <td>{{ plant.avg_availability.toFixed(2) }}%</td>
                <td>
                  <span :class="['score-badge', getScoreClass(plant.performance_score)]">
                    {{ plant.performance_score.toFixed(2) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Predictive Insights -->
    <div v-if="activeTab === 'predictions'" class="analytics-section">
      <div class="section-header">
        <h3><i class="pi pi-forward"></i> Predictive Insights</h3>
        <div class="filter-group">
          <label><i class="pi pi-building"></i> Select Plant</label>
          <select v-model="predictionPlant" @change="loadPredictions" class="filter-select">
            <option value="">Select Plant</option>
            <option v-for="plant in plants" :key="plant.id" :value="plant.id">
              {{ plant.name }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="predictionsData && !predictionsData.error" class="predictions-content">
        <p class="info-text">
          Predictions based on {{ predictionsData.based_on_days }} days of historical data
        </p>

        <div class="predictions-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Predicted Generation (kWh)</th>
                <th>Predicted CF (%)</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pred in predictionsData.predictions" :key="pred.date">
                <td>{{ formatDate(pred.date) }}</td>
                <td>{{ pred.predicted_generation_kwh.toFixed(2) }}</td>
                <td>{{ pred.predicted_capacity_factor.toFixed(2) }}%</td>
                <td>
                  <span :class="['confidence-badge', pred.confidence]">
                    {{ pred.confidence }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-else-if="predictionsData && predictionsData.error" class="empty-state">
        <p>{{ predictionsData.error }}</p>
      </div>
    </div>

    <!-- Anomaly Detection -->
    <div v-if="activeTab === 'anomalies'" class="analytics-section">
      <div class="section-header">
        <h3><i class="pi pi-exclamation-triangle"></i> Anomaly Detection</h3>
        <button @click="loadAnomalies" class="btn-refresh">
          <i class="pi pi-refresh"></i> Scan for Anomalies
        </button>
      </div>

      <div v-if="anomaliesData" class="anomalies-content">
        <div class="anomalies-summary">
          <div class="summary-badge" :class="anomaliesData.anomalies_found > 0 ? 'warning' : 'success'">
            <i :class="anomaliesData.anomalies_found > 0 ? 'pi pi-exclamation-triangle' : 'pi pi-check-circle'"></i>
            <span>{{ anomaliesData.anomalies_found }} anomalies detected</span>
          </div>
        </div>

        <div v-if="anomaliesData.anomalies.length > 0" class="anomalies-list">
          <div v-for="(anomaly, index) in anomaliesData.anomalies" :key="index" 
               :class="['anomaly-card', anomaly.severity]">
            <div class="anomaly-header">
              <span class="anomaly-date">{{ formatDate(anomaly.date) }}</span>
              <span :class="['severity-badge', anomaly.severity]">{{ anomaly.severity }}</span>
            </div>
            <div class="anomaly-details">
              <p><strong>{{ anomaly.plant }}</strong> - Unit {{ anomaly.unit }}</p>
              <p>Capacity Factor: {{ anomaly.capacity_factor.toFixed(2) }}%</p>
              <p>Expected Range: {{ anomaly.expected_range[0].toFixed(2) }}% - {{ anomaly.expected_range[1].toFixed(2) }}%</p>
              <p>Deviation: {{ anomaly.deviation.toFixed(2) }}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Efficiency Analysis -->
    <div v-if="activeTab === 'efficiency'" class="analytics-section">
      <div class="section-header">
        <h3><i class="pi pi-gauge"></i> Efficiency Analysis</h3>
        <div class="filter-group">
          <label><i class="pi pi-building"></i> Plant</label>
          <select v-model="efficiencyPlant" @change="loadEfficiency" class="filter-select">
            <option value="">All Plants</option>
            <option v-for="plant in plants" :key="plant.id" :value="plant.id">
              {{ plant.name }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="efficiencyData" class="efficiency-content">
        <div class="efficiency-score">
          <h4>Overall Efficiency Score</h4>
          <div class="score-circle">
            <svg viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" stroke-width="10"/>
              <circle cx="50" cy="50" r="45" fill="none" stroke="#3b82f6" stroke-width="10"
                      :stroke-dasharray="`${efficiencyData.efficiency_score * 2.827} 282.7`"
                      transform="rotate(-90 50 50)"/>
            </svg>
            <div class="score-text">{{ efficiencyData.efficiency_score.toFixed(1) }}</div>
          </div>
        </div>

        <div class="efficiency-metrics">
          <div class="metric-card">
            <h5>Generation</h5>
            <p class="metric-value">{{ efficiencyData.generation.total_mwh.toFixed(2) }} MWh</p>
            <p class="metric-label">Avg CF: {{ efficiencyData.generation.avg_capacity_factor.toFixed(2) }}%</p>
          </div>

          <div class="metric-card">
            <h5>Utilization</h5>
            <p class="metric-value">{{ efficiencyData.utilization.operating_percentage.toFixed(2) }}%</p>
            <p class="metric-label">{{ efficiencyData.utilization.operating_hours.toFixed(0) }} hours</p>
          </div>

          <div class="metric-card">
            <h5>Forced Outage</h5>
            <p class="metric-value">{{ efficiencyData.utilization.forced_outage_percentage.toFixed(2) }}%</p>
            <p class="metric-label">{{ efficiencyData.utilization.forced_outage_hours.toFixed(0) }} hours</p>
          </div>
        </div>
      </div>
    </div>
    </div>
  </AppLayout>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
import AppLayout from './AppLayout.vue';

Chart.register(...registerables);

export default {
  name: 'AdvancedAnalytics',
  setup() {
    const activeTab = ref('trends');
    const plants = ref([]);
    
    // Trends
    const trendsPlant = ref('');
    const trendsDays = ref(30);
    const trendsData = ref(null);
    const trendsChart = ref(null);
    
    // Comparison
    const comparisonData = ref(null);
    
    // Predictions
    const predictionPlant = ref('');
    const predictionsData = ref(null);
    
    // Anomalies
    const anomaliesData = ref(null);
    
    // Efficiency
    const efficiencyPlant = ref('');
    const efficiencyData = ref(null);

    const tabs = [
      { id: 'trends', label: 'Trends', icon: 'pi pi-chart-line' },
      { id: 'comparison', label: 'Comparison', icon: 'pi pi-chart-bar' },
      { id: 'predictions', label: 'Predictions', icon: 'pi pi-forward' },
      { id: 'anomalies', label: 'Anomalies', icon: 'pi pi-exclamation-triangle' },
      { id: 'efficiency', label: 'Efficiency', icon: 'pi pi-gauge' }
    ];

    const loadPlants = async () => {
      try {
        const response = await axios.get('/api/plants/');
        plants.value = response.data;
      } catch (error) {
        console.error('Failed to load plants:', error);
      }
    };

    const loadTrends = async () => {
      try {
        const params = { days: trendsDays.value };
        if (trendsPlant.value) params.plant_id = trendsPlant.value;
        
        const response = await axios.get('/api/analytics/trends/', { params });
        trendsData.value = response.data;
        renderTrendsChart();
      } catch (error) {
        console.error('Failed to load trends:', error);
      }
    };

    const loadComparison = async () => {
      try {
        const response = await axios.get('/api/analytics/comparison/');
        comparisonData.value = response.data;
      } catch (error) {
        console.error('Failed to load comparison:', error);
      }
    };

    const loadPredictions = async () => {
      if (!predictionPlant.value) return;
      
      try {
        const response = await axios.get('/api/analytics/predictions/', {
          params: { plant_id: predictionPlant.value }
        });
        predictionsData.value = response.data;
      } catch (error) {
        console.error('Failed to load predictions:', error);
      }
    };

    const loadAnomalies = async () => {
      try {
        const response = await axios.get('/api/analytics/anomalies/');
        anomaliesData.value = response.data;
      } catch (error) {
        console.error('Failed to load anomalies:', error);
      }
    };

    const loadEfficiency = async () => {
      try {
        const params = {};
        if (efficiencyPlant.value) params.plant_id = efficiencyPlant.value;
        
        const response = await axios.get('/api/analytics/efficiency/', { params });
        efficiencyData.value = response.data;
      } catch (error) {
        console.error('Failed to load efficiency:', error);
      }
    };

    const renderTrendsChart = () => {
      // Chart rendering logic would go here
    };

    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString();
    };

    const getScoreClass = (score) => {
      if (score >= 80) return 'excellent';
      if (score >= 60) return 'good';
      if (score >= 40) return 'fair';
      return 'poor';
    };

    onMounted(() => {
      loadPlants();
      loadTrends();
    });

    return {
      activeTab,
      tabs,
      plants,
      trendsPlant,
      trendsDays,
      trendsData,
      trendsChart,
      comparisonData,
      predictionPlant,
      predictionsData,
      anomaliesData,
      efficiencyPlant,
      efficiencyData,
      loadTrends,
      loadComparison,
      loadPredictions,
      loadAnomalies,
      loadEfficiency,
      formatDate,
      getScoreClass
    };
  },
  components: {
    AppLayout
  }
};
</script>

<style scoped>
.advanced-analytics {
  padding: 20px;
}

.analytics-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: #f1f5f9;
  color: #64748b;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.tab-btn.active {
  background: #3b82f6;
  color: white;
}

.analytics-section {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
}

.section-header h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 600;
}

.section-header h3 i {
  color: #3b82f6;
  font-size: 1.25rem;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-group label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
}

.filter-group label i {
  font-size: 0.875rem;
  color: #3b82f6;
}

.filter-select {
  min-width: 180px;
  padding: 10px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  color: #1e293b;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.filter-select:hover {
  border-color: #3b82f6;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.btn-refresh {
  padding: 10px 20px;
  border: none;
  background: #3b82f6;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-refresh:active {
  transform: translateY(0);
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  display: flex;
  gap: 15px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 10px;
}

.card-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.card-content h3 {
  margin: 5px 0 0 0;
  color: #1e293b;
}

.card-label {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
}

.comparison-table table {
  width: 100%;
  border-collapse: collapse;
}

.comparison-table th,
.comparison-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.comparison-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #475569;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s;
}

.score-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.score-badge.excellent {
  background: #dcfce7;
  color: #16a34a;
}

.score-badge.good {
  background: #dbeafe;
  color: #3b82f6;
}

.score-badge.fair {
  background: #fef3c7;
  color: #d97706;
}

.score-badge.poor {
  background: #fee2e2;
  color: #dc2626;
}

.anomaly-card {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  border-left: 4px solid;
}

.anomaly-card.high {
  background: #fef2f2;
  border-color: #dc2626;
}

.anomaly-card.medium {
  background: #fefce8;
  border-color: #d97706;
}

.efficiency-score {
  text-align: center;
  margin-bottom: 30px;
}

.score-circle {
  width: 150px;
  height: 150px;
  margin: 20px auto;
  position: relative;
}

.score-circle svg {
  width: 100%;
  height: 100%;
}

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  font-weight: bold;
  color: #1e293b;
}

.efficiency-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.metric-card {
  padding: 20px;
  background: #f8fafc;
  border-radius: 10px;
}

.metric-card h5 {
  margin: 0 0 10px 0;
  color: #64748b;
  font-size: 0.9rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 5px 0;
}

.metric-label {
  color: #64748b;
  font-size: 0.85rem;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .advanced-analytics {
    padding: 15px;
  }

  .analytics-tabs {
    gap: 8px;
  }

  .tab-btn {
    padding: 8px 12px;
    font-size: 0.875rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-header h3 {
    font-size: 1.25rem;
  }

  .filters {
    width: 100%;
  }

  .filter-group {
    flex: 1;
    min-width: 140px;
  }

  .filter-select {
    min-width: 100%;
    font-size: 0.875rem;
    padding: 8px 12px;
  }

  .btn-refresh {
    width: 100%;
    justify-content: center;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .comparison-table {
    overflow-x: auto;
  }

  .efficiency-metrics {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .tab-btn span {
    display: none;
  }

  .tab-btn {
    padding: 10px;
  }

  .filter-group label span {
    display: none;
  }
}
</style>
