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
              <h3>{{ (trendsData.summary?.total_generation_mwh || 0).toFixed(2) }} MWh</h3>
            </div>
          </div>

          <div class="summary-card">
            <div class="card-icon" style="background: #dcfce7;">
              <i class="pi pi-chart-line" style="color: #16a34a;"></i>
            </div>
            <div class="card-content">
              <p class="card-label">Avg Capacity Factor</p>
              <h3>{{ (trendsData.summary?.avg_capacity_factor || 0).toFixed(2) }}%</h3>
            </div>
          </div>

          <div class="summary-card">
            <div class="card-icon" style="background: #fef3c7;">
              <i class="pi pi-calendar" style="color: #d97706;"></i>
            </div>
            <div class="card-content">
              <p class="card-label">Avg Daily Generation</p>
              <h3>{{ (trendsData.summary?.avg_daily_generation_mwh || 0).toFixed(2) }} MWh</h3>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <div v-if="trendsData.daily_data && trendsData.daily_data.length > 0">
            <canvas ref="trendsChart"></canvas>
          </div>
          <div v-else class="chart-empty-state">
            <i class="pi pi-chart-line" style="font-size: 3rem; color: #cbd5e1; margin-bottom: 16px;"></i>
            <p style="color: #64748b; font-size: 1.125rem; font-weight: 600; margin: 0;">No trend data available</p>
            <p style="color: #94a3b8; font-size: 0.9375rem; margin: 8px 0 0 0;">Try selecting a different plant or time period</p>
          </div>
        </div>
      </div>

      <div v-else class="loading-state">
        <div class="spinner"></div>
        <p>Loading trends data...</p>
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

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

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
        const response = await axios.get(`${API_URL}/plants/`);
        plants.value = response.data;
      } catch (error) {
        console.error('Failed to load plants:', error);
      }
    };

    const loadTrends = async () => {
      try {
        const params = { days: trendsDays.value };
        if (trendsPlant.value) params.plant_id = trendsPlant.value;
        
        const response = await axios.get(`${API_URL}/analytics/trends/`, { params });
        trendsData.value = response.data;
        renderTrendsChart();
      } catch (error) {
        console.error('Failed to load trends:', error);
      }
    };

    const loadComparison = async () => {
      try {
        const response = await axios.get(`${API_URL}/analytics/comparison/`);
        comparisonData.value = response.data;
      } catch (error) {
        console.error('Failed to load comparison:', error);
      }
    };

    const loadPredictions = async () => {
      if (!predictionPlant.value) return;
      
      try {
        const response = await axios.get(`${API_URL}/analytics/predictions/`, {
          params: { plant_id: predictionPlant.value }
        });
        predictionsData.value = response.data;
      } catch (error) {
        console.error('Failed to load predictions:', error);
      }
    };

    const loadAnomalies = async () => {
      try {
        const response = await axios.get(`${API_URL}/analytics/anomalies/`);
        anomaliesData.value = response.data;
      } catch (error) {
        console.error('Failed to load anomalies:', error);
      }
    };

    const loadEfficiency = async () => {
      try {
        const params = {};
        if (efficiencyPlant.value) params.plant_id = efficiencyPlant.value;
        
        const response = await axios.get(`${API_URL}/analytics/efficiency/`, { params });
        efficiencyData.value = response.data;
      } catch (error) {
        console.error('Failed to load efficiency:', error);
      }
    };

    let chartInstance = null;

    const renderTrendsChart = () => {
      if (!trendsData.value || !trendsChart.value) return;

      // Destroy existing chart if it exists
      if (chartInstance) {
        chartInstance.destroy();
      }

      const ctx = trendsChart.value.getContext('2d');
      
      // Prepare data from API response
      const labels = trendsData.value.daily_data.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      });
      
      const generationData = trendsData.value.daily_data.map(d => d.generation_mwh);
      const capacityFactorData = trendsData.value.daily_data.map(d => d.capacity_factor);

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Generation (MWh)',
              data: generationData,
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              borderWidth: 3,
              fill: true,
              tension: 0.4,
              yAxisID: 'y'
            },
            {
              label: 'Capacity Factor (%)',
              data: capacityFactorData,
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              borderWidth: 3,
              fill: true,
              tension: 0.4,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                font: {
                  size: 14,
                  weight: '600'
                },
                padding: 20,
                usePointStyle: true
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              padding: 12,
              titleFont: {
                size: 14,
                weight: 'bold'
              },
              bodyFont: {
                size: 13
              },
              borderColor: '#e2e8f0',
              borderWidth: 1
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                font: {
                  size: 12,
                  weight: '600'
                },
                color: '#64748b'
              }
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              title: {
                display: true,
                text: 'Generation (MWh)',
                font: {
                  size: 13,
                  weight: '700'
                },
                color: '#3b82f6'
              },
              grid: {
                color: '#f1f5f9'
              },
              ticks: {
                font: {
                  size: 12,
                  weight: '600'
                },
                color: '#64748b'
              }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              title: {
                display: true,
                text: 'Capacity Factor (%)',
                font: {
                  size: 13,
                  weight: '700'
                },
                color: '#10b981'
              },
              grid: {
                drawOnChartArea: false
              },
              ticks: {
                font: {
                  size: 12,
                  weight: '600'
                },
                color: '#64748b'
              }
            }
          }
        }
      });
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
  padding: 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
}

.advanced-analytics h2 {
  font-size: 2.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 32px 0;
  letter-spacing: -0.02em;
}

.analytics-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
  background: white;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.tab-btn {
  padding: 14px 24px;
  border: none;
  background: transparent;
  color: #64748b;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 0.9375rem;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.tab-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  opacity: 0;
  transition: opacity 0.3s;
  z-index: -1;
}

.tab-btn:hover:not(.active) {
  background: #f8fafc;
  color: #3b82f6;
  transform: translateY(-2px);
}

.tab-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
}

.tab-btn.active::before {
  opacity: 1;
}

.tab-btn i {
  font-size: 1.125rem;
}

.analytics-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 20px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f1f5f9;
}

.section-header h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  color: #0f172a;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.section-header h3 i {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  color: #3b82f6;
  border-radius: 12px;
  font-size: 1.375rem;
}

.filters {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-group label i {
  font-size: 1rem;
  color: #3b82f6;
}

.filter-select {
  min-width: 200px;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.9375rem;
  color: #0f172a;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-select:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.1);
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.btn-refresh {
  padding: 12px 24px;
  border: none;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9375rem;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
}

.btn-refresh:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(59, 130, 246, 0.4);
}

.btn-refresh:active {
  transform: translateY(0);
}

.btn-refresh i {
  font-size: 1.125rem;
  animation: spin 2s linear infinite paused;
}

.btn-refresh:hover i {
  animation-play-state: running;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.summary-card {
  display: flex;
  gap: 16px;
  padding: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 16px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.summary-card:hover::before {
  opacity: 1;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  flex-shrink: 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-content {
  flex: 1;
}

.card-content h3 {
  margin: 8px 0 0 0;
  color: #0f172a;
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.025em;
}

.card-label {
  margin: 0;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.chart-container {
  background: #f8fafc;
  padding: 24px;
  border-radius: 16px;
  border: 2px solid #e2e8f0;
  height: 400px;
  position: relative;
}

.chart-container canvas {
  max-height: 100%;
}

.chart-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.loading-state p {
  color: #64748b;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 16px 0 0 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.fleet-summary {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 32px;
  border: 2px solid #e2e8f0;
}

.fleet-summary h4 {
  margin: 0 0 20px 0;
  color: #0f172a;
  font-size: 1.25rem;
  font-weight: 700;
}

.fleet-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.375rem;
  color: #0f172a;
  font-weight: 800;
  letter-spacing: -0.025em;
}

.comparison-table {
  overflow-x: auto;
  border-radius: 16px;
  border: 2px solid #e2e8f0;
}

.comparison-table table {
  width: 100%;
  border-collapse: collapse;
}

.comparison-table th,
.comparison-table td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
}

.comparison-table th {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  font-weight: 700;
  color: #475569;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  position: sticky;
  top: 0;
  z-index: 10;
}

.comparison-table tbody tr {
  transition: all 0.2s;
}

.comparison-table tbody tr:hover {
  background: #f8fafc;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 10px;
  background: #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.score-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.score-badge.excellent {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.score-badge.good {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.score-badge.fair {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.score-badge.poor {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.info-text {
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
  padding: 16px 20px;
  border-radius: 12px;
  color: #1e40af;
  font-weight: 600;
  margin-bottom: 24px;
  border-left: 4px solid #3b82f6;
}

.predictions-table,
.anomalies-list {
  margin-top: 24px;
}

.predictions-table table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid #e2e8f0;
}

.predictions-table th,
.predictions-table td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
}

.predictions-table th {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  font-weight: 700;
  color: #475569;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.predictions-table tbody tr {
  transition: all 0.2s;
}

.predictions-table tbody tr:hover {
  background: #f8fafc;
}

.confidence-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.confidence-badge.high {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.confidence-badge.medium {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.confidence-badge.low {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 16px;
  border: 2px dashed #cbd5e1;
}

.empty-state p {
  color: #64748b;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.anomalies-summary {
  margin-bottom: 24px;
}

.summary-badge {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  border-radius: 16px;
  font-size: 1.125rem;
  font-weight: 700;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.summary-badge.warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 2px solid #f59e0b;
}

.summary-badge.success {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #14532d;
  border: 2px solid #10b981;
}

.summary-badge i {
  font-size: 1.5rem;
}

.anomaly-card {
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 16px;
  border-left: 6px solid;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.anomaly-card:hover {
  transform: translateX(4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.anomaly-card.high {
  background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
  border-color: #dc2626;
}

.anomaly-card.medium {
  background: linear-gradient(135deg, #ffffff 0%, #fefce8 100%);
  border-color: #f59e0b;
}

.anomaly-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f1f5f9;
}

.anomaly-date {
  font-weight: 700;
  color: #0f172a;
  font-size: 1rem;
}

.severity-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.severity-badge.high {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.severity-badge.medium {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.anomaly-details p {
  margin: 8px 0;
  color: #475569;
  font-weight: 500;
}

.anomaly-details strong {
  color: #0f172a;
  font-weight: 700;
}

.efficiency-score {
  text-align: center;
  margin-bottom: 40px;
  padding: 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 20px;
  border: 2px solid #e2e8f0;
}

.efficiency-score h4 {
  margin: 0 0 24px 0;
  color: #0f172a;
  font-size: 1.5rem;
  font-weight: 700;
}

.score-circle {
  width: 180px;
  height: 180px;
  margin: 0 auto;
  position: relative;
}

.score-circle svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
}

.efficiency-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.metric-card {
  padding: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 16px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-card h5 {
  margin: 0 0 16px 0;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  font-size: 1.875rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0 0 8px 0;
  letter-spacing: -0.025em;
}

.metric-label {
  color: #64748b;
  font-size: 0.9375rem;
  margin: 0;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  .advanced-analytics {
    padding: 20px;
  }

  .advanced-analytics h2 {
    font-size: 1.75rem;
  }

  .analytics-tabs {
    gap: 8px;
    padding: 6px;
  }

  .tab-btn {
    padding: 10px 16px;
    font-size: 0.875rem;
  }

  .analytics-section {
    padding: 24px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-header h3 {
    font-size: 1.375rem;
  }

  .section-header h3 i {
    width: 40px;
    height: 40px;
    font-size: 1.125rem;
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
    padding: 10px 14px;
  }

  .btn-refresh {
    width: 100%;
    justify-content: center;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .summary-card {
    padding: 20px;
  }

  .card-icon {
    width: 56px;
    height: 56px;
    font-size: 1.5rem;
  }

  .card-content h3 {
    font-size: 1.5rem;
  }

  .fleet-stats {
    grid-template-columns: 1fr;
  }

  .comparison-table {
    overflow-x: auto;
  }

  .efficiency-metrics {
    grid-template-columns: 1fr;
  }

  .score-circle {
    width: 150px;
    height: 150px;
  }

  .score-text {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .advanced-analytics {
    padding: 16px;
  }

  .advanced-analytics h2 {
    font-size: 1.5rem;
  }

  .tab-btn span {
    display: none;
  }

  .tab-btn {
    padding: 12px;
  }

  .analytics-section {
    padding: 20px;
  }

  .section-header h3 {
    font-size: 1.125rem;
  }

  .filter-group label span {
    display: none;
  }

  .summary-card {
    flex-direction: column;
    text-align: center;
  }

  .card-icon {
    margin: 0 auto;
  }

  .comparison-table th,
  .comparison-table td,
  .predictions-table th,
  .predictions-table td {
    padding: 12px 8px;
    font-size: 0.875rem;
  }
}

/* Loading States */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Smooth Scrolling */
.analytics-section {
  scroll-margin-top: 20px;
}

/* Print Styles */
@media print {
  .analytics-tabs,
  .filters,
  .btn-refresh {
    display: none;
  }

  .analytics-section {
    box-shadow: none;
    border: 1px solid #e2e8f0;
    page-break-inside: avoid;
  }

  .summary-card,
  .metric-card,
  .anomaly-card {
    box-shadow: none;
    border: 1px solid #e2e8f0;
  }
}
</style>
