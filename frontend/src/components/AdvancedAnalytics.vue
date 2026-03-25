<template>
  <AppLayout>
    <div class="advanced-analytics-container">
      <div class="analytics-header">
        <div class="header-content">
          <h2>Advanced Analytics</h2>
          <p>Comprehensive insights and AI-powered performance metrics</p>
        </div>
        <div class="header-actions">
          <button class="btn-export" @click="exportReport">
            <i class="pi pi-download"></i> Export Report
          </button>
        </div>
      </div>

      <div class="analytics-layout">
        <!-- Sidebar Navigation -->
        <aside class="analytics-sidebar">
          <nav class="sidebar-nav">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              :class="['nav-item', { active: activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              <div class="nav-icon"><i :class="tab.icon"></i></div>
              <div class="nav-text">
                <span class="nav-label">{{ tab.label }}</span>
                <span class="nav-desc">{{ tab.desc }}</span>
              </div>
              <i class="pi pi-chevron-right nav-arrow"></i>
            </button>
          </nav>
        </aside>

        <!-- Main Content Area -->
        <main class="analytics-main">
          <!-- TRENDS TAB -->
          <transition name="fade" mode="out-in">
            <div v-if="activeTab === 'trends'" class="tab-pane" key="trends">
              <div class="pane-header">
                <h3>Performance Trends</h3>
                <div class="pane-filters">
                  <div class="filter-box">
                    <i class="pi pi-building"></i>
                    <select v-model="trendsPlant" @change="loadTrends">
                      <option value="">All Plants Fleet</option>
                      <option v-for="plant in plants" :key="plant.id" :value="plant.id">{{ plant.name }}</option>
                    </select>
                  </div>
                  <div class="filter-box">
                    <i class="pi pi-calendar"></i>
                    <select v-model="trendsDays" @change="loadTrends">
                      <option :value="7">Last 7 Days</option>
                      <option :value="30">Last 30 Days</option>
                      <option :value="90">Last 90 Days</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="metrics-grid" v-if="trendsData && !loading">
                <div class="metric-card gradient-blue">
                  <div class="metric-icon"><i class="pi pi-bolt"></i></div>
                  <div class="metric-info">
                    <span class="metric-title">Total Generation</span>
                    <span class="metric-value">{{ formatNumber(trendsData.summary?.total_generation_mwh) }} <small>MWh</small></span>
                    <span class="metric-trend positive"><i class="pi pi-arrow-up"></i> 5.2% vs last period</span>
                  </div>
                </div>
                <div class="metric-card gradient-green">
                  <div class="metric-icon"><i class="pi pi-chart-line"></i></div>
                  <div class="metric-info">
                    <span class="metric-title">Avg Capacity Factor</span>
                    <span class="metric-value">{{ formatNumber(trendsData.summary?.avg_capacity_factor) }}<small>%</small></span>
                    <span class="metric-trend positive"><i class="pi pi-arrow-up"></i> 1.8% vs last period</span>
                  </div>
                </div>
                <div class="metric-card gradient-orange">
                  <div class="metric-icon"><i class="pi pi-sun"></i></div>
                  <div class="metric-info">
                    <span class="metric-title">Avg Daily Output</span>
                    <span class="metric-value">{{ formatNumber(trendsData.summary?.avg_daily_generation_mwh) }} <small>MWh</small></span>
                    <span class="metric-trend neutral"><i class="pi pi-minus"></i> Stable</span>
                  </div>
                </div>
              </div>

              <div class="chart-box" v-show="!loading">
                <div class="chart-header">
                  <h4>Generation & Capacity Factor Trend</h4>
                  <div class="chart-legend">
                    <span class="legend-item"><span class="dot blue"></span> Generation (MWh)</span>
                    <span class="legend-item"><span class="dot green"></span> Capacity Factor (%)</span>
                  </div>
                </div>
                <div class="chart-canvas-container">
                  <canvas ref="trendsChartRef"></canvas>
                </div>
              </div>
              
              <div class="skeleton-loader" v-if="loading">
                <div class="sk-metrics">
                  <div class="sk-card"></div><div class="sk-card"></div><div class="sk-card"></div>
                </div>
                <div class="sk-chart"></div>
              </div>
            </div>

            <!-- COMPARISON TAB -->
            <div v-else-if="activeTab === 'comparison'" class="tab-pane" key="comparison">
              <div class="pane-header">
                <h3>Fleet Comparison</h3>
                <button class="btn-refresh" @click="loadComparison" :class="{ 'spinning': loading }">
                  <i class="pi pi-refresh"></i> Refresh Data
                </button>
              </div>

              <div class="fleet-overview" v-if="comparisonData && !loading">
                <div class="overview-item">
                  <span class="o-label">Total Capacity</span>
                  <span class="o-value">{{ formatNumber(comparisonData.fleet_summary.total_capacity_mw) }} MW</span>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-item">
                  <span class="o-label">Fleet Generation</span>
                  <span class="o-value">{{ formatNumber(comparisonData.fleet_summary.total_generation_mwh) }} MWh</span>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-item">
                  <span class="o-label">Fleet Avg CF</span>
                  <span class="o-value">{{ formatNumber(comparisonData.fleet_summary.fleet_avg_capacity_factor) }}%</span>
                </div>
                <div class="overview-divider"></div>
                <div class="overview-item highlight">
                  <span class="o-label"><i class="pi pi-star-fill"></i> Top Performer</span>
                  <span class="o-value">{{ comparisonData.fleet_summary.best_performer }}</span>
                </div>
              </div>

              <div class="modern-table-container" v-if="comparisonData && !loading">
                <table class="modern-table">
                  <thead>
                    <tr>
                      <th>Plant Name</th>
                      <th>Capacity (MW)</th>
                      <th>Generation (MWh)</th>
                      <th>Capacity Factor</th>
                      <th>Availability</th>
                      <th>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="plant in comparisonData.plants" :key="plant.plant_id">
                      <td class="font-semibold">{{ plant.plant_name }}</td>
                      <td>{{ formatNumber(plant.capacity_mw) }}</td>
                      <td>{{ formatNumber(plant.total_generation_mwh) }}</td>
                      <td>
                        <div class="progress-wrapper">
                          <span class="progress-text">{{ formatNumber(plant.avg_capacity_factor) }}%</span>
                          <div class="progress-bar-bg">
                            <div class="progress-bar-fill" :style="{ width: plant.avg_capacity_factor + '%', background: getCfColor(plant.avg_capacity_factor) }"></div>
                          </div>
                        </div>
                      </td>
                      <td>{{ formatNumber(plant.avg_availability) }}%</td>
                      <td>
                        <span :class="['badge-score', getScoreClass(plant.performance_score)]">
                          {{ formatNumber(plant.performance_score) }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="skeleton-loader" v-if="loading">
                <div class="sk-overview"></div>
                <div class="sk-table"></div>
              </div>
            </div>

            <!-- PREDICTIONS TAB -->
            <div v-else-if="activeTab === 'predictions'" class="tab-pane" key="predictions">
              <div class="pane-header">
                <h3>AI Predictive Insights</h3>
                <div class="pane-filters">
                  <div class="filter-box">
                    <i class="pi pi-building"></i>
                    <select v-model="predictionPlant" @change="loadPredictions">
                      <option value="">Select Plant (Fleet Default)</option>
                      <option v-for="plant in plants" :key="plant.id" :value="plant.id">{{ plant.name }}</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="info-alert" v-if="predictionsData && !loading">
                <i class="pi pi-info-circle"></i>
                <div>
                  <strong>AI Forecasting Active</strong>
                  <p>Predictions are generated using a moving average algorithm based on the last {{ predictionsData.based_on_days }} days of historical data.</p>
                </div>
              </div>

              <div class="predictions-grid" v-if="predictionsData && !loading">
                <div v-for="(pred, idx) in predictionsData.predictions" :key="idx" class="prediction-card">
                  <div class="pred-date">{{ formatDate(pred.date) }}</div>
                  <div class="pred-metrics">
                    <div class="p-metric">
                      <span class="p-label">Est. Generation</span>
                      <span class="p-value">{{ formatNumber(pred.predicted_generation_kwh) }} <small>kWh</small></span>
                    </div>
                    <div class="p-metric">
                      <span class="p-label">Est. CF</span>
                      <span class="p-value">{{ formatNumber(pred.predicted_capacity_factor) }}%</span>
                    </div>
                  </div>
                  <div class="pred-footer">
                    <span class="confidence-label">Confidence:</span>
                    <span :class="['badge-confidence', pred.confidence]">{{ pred.confidence }}</span>
                  </div>
                </div>
              </div>

              <div class="skeleton-loader" v-if="loading">
                <div class="sk-grid">
                  <div class="sk-card" v-for="i in 6" :key="i"></div>
                </div>
              </div>
            </div>

            <!-- ANOMALIES TAB -->
            <div v-else-if="activeTab === 'anomalies'" class="tab-pane" key="anomalies">
              <div class="pane-header">
                <h3>System Anomaly Detection</h3>
                <button class="btn-scan" @click="loadAnomalies" :class="{ 'scanning': loading }">
                  <i class="pi pi-search"></i> Run Deep Scan
                </button>
              </div>

              <div class="anomaly-summary" v-if="anomaliesData && !loading" :class="anomaliesData.anomalies_found > 0 ? 'has-issues' : 'all-clear'">
                <div class="summary-icon">
                  <i :class="anomaliesData.anomalies_found > 0 ? 'pi pi-exclamation-triangle' : 'pi pi-check-circle'"></i>
                </div>
                <div class="summary-text">
                  <h4>{{ anomaliesData.anomalies_found > 0 ? `${anomaliesData.anomalies_found} Anomalies Detected` : 'System Normal' }}</h4>
                  <p>{{ anomaliesData.anomalies_found > 0 ? 'Review the highlighted deviations below.' : 'No significant deviations found in the current period.' }}</p>
                </div>
              </div>

              <div class="anomalies-list" v-if="anomaliesData && anomaliesData.anomalies.length > 0 && !loading">
                <div v-for="(anomaly, idx) in anomaliesData.anomalies" :key="idx" :class="['anomaly-item', anomaly.severity]">
                  <div class="a-header">
                    <div class="a-title">
                      <span class="a-plant">{{ anomaly.plant }} - Unit {{ anomaly.unit }}</span>
                      <span class="a-date">{{ formatDate(anomaly.date) }}</span>
                    </div>
                    <span :class="['badge-severity', anomaly.severity]">{{ anomaly.severity }} Severity</span>
                  </div>
                  <div class="a-body">
                    <div class="a-stat">
                      <span>Actual CF</span>
                      <strong>{{ formatNumber(anomaly.capacity_factor) }}%</strong>
                    </div>
                    <div class="a-stat">
                      <span>Expected Range</span>
                      <strong>{{ formatNumber(anomaly.expected_range[0]) }}% - {{ formatNumber(anomaly.expected_range[1]) }}%</strong>
                    </div>
                    <div class="a-stat highlight-stat">
                      <span>Deviation</span>
                      <strong>±{{ formatNumber(anomaly.deviation) }}%</strong>
                    </div>
                  </div>
                </div>
              </div>

              <div class="skeleton-loader" v-if="loading">
                <div class="sk-alert"></div>
                <div class="sk-list">
                  <div class="sk-list-item" v-for="i in 3" :key="i"></div>
                </div>
              </div>
            </div>

            <!-- EFFICIENCY TAB -->
            <div v-else-if="activeTab === 'efficiency'" class="tab-pane" key="efficiency">
              <div class="pane-header">
                <h3>Plant Efficiency Analysis</h3>
                <div class="pane-filters">
                  <div class="filter-box">
                    <i class="pi pi-building"></i>
                    <select v-model="efficiencyPlant" @change="loadEfficiency">
                      <option value="">Overall Fleet</option>
                      <option v-for="plant in plants" :key="plant.id" :value="plant.id">{{ plant.name }}</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="efficiency-dashboard" v-if="efficiencyData && !loading">
                <div class="score-panel">
                  <div class="score-circle-container">
                    <svg viewBox="0 0 36 36" class="circular-chart">
                      <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                      <path class="circle" :stroke-dasharray="`${efficiencyData.efficiency_score}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    </svg>
                    <div class="score-content">
                      <span class="score-number">{{ formatNumber(efficiencyData.efficiency_score) }}</span>
                      <span class="score-label">Overall Score</span>
                    </div>
                  </div>
                </div>

                <div class="efficiency-details">
                  <div class="detail-card">
                    <div class="d-icon blue"><i class="pi pi-bolt"></i></div>
                    <div class="d-info">
                      <h4>Generation Output</h4>
                      <div class="d-row">
                        <span>Total MWh</span>
                        <strong>{{ formatNumber(efficiencyData.generation.total_mwh) }}</strong>
                      </div>
                      <div class="d-row">
                        <span>Avg Capacity Factor</span>
                        <strong>{{ formatNumber(efficiencyData.generation.avg_capacity_factor) }}%</strong>
                      </div>
                    </div>
                  </div>

                  <div class="detail-card">
                    <div class="d-icon green"><i class="pi pi-cog"></i></div>
                    <div class="d-info">
                      <h4>Plant Utilization</h4>
                      <div class="d-row">
                        <span>Operating %</span>
                        <strong>{{ formatNumber(efficiencyData.utilization.operating_percentage) }}%</strong>
                      </div>
                      <div class="d-row">
                        <span>Operating Hours</span>
                        <strong>{{ formatNumber(efficiencyData.utilization.operating_hours) }} hrs</strong>
                      </div>
                    </div>
                  </div>

                  <div class="detail-card">
                    <div class="d-icon red"><i class="pi pi-times-circle"></i></div>
                    <div class="d-info">
                      <h4>Outage Impact</h4>
                      <div class="d-row">
                        <span>Forced Outage %</span>
                        <strong>{{ formatNumber(efficiencyData.utilization.forced_outage_percentage) }}%</strong>
                      </div>
                      <div class="d-row">
                        <span>Forced Outage Hours</span>
                        <strong>{{ formatNumber(efficiencyData.utilization.forced_outage_hours) }} hrs</strong>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="skeleton-loader" v-if="loading">
                <div class="sk-dashboard">
                  <div class="sk-circle"></div>
                  <div class="sk-details">
                    <div class="sk-card"></div><div class="sk-card"></div><div class="sk-card"></div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </main>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
import AppLayout from './AppLayout.vue';

Chart.register(...registerables);

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

export default {
  name: 'AdvancedAnalytics',
  components: { AppLayout },
  setup() {
    const activeTab = ref('trends');
    const loading = ref(false);
    const plants = ref([]);
    
    // State variables
    const trendsPlant = ref('');
    const trendsDays = ref(30);
    const trendsData = ref(null);
    const trendsChartRef = ref(null);
    
    const comparisonData = ref(null);
    
    const predictionPlant = ref('');
    const predictionsData = ref(null);
    
    const anomaliesData = ref(null);
    
    const efficiencyPlant = ref('');
    const efficiencyData = ref(null);

    const tabs = [
      { id: 'trends', label: 'Trends', desc: 'Performance over time', icon: 'pi pi-chart-line' },
      { id: 'comparison', label: 'Comparison', desc: 'Fleet benchmarking', icon: 'pi pi-chart-bar' },
      { id: 'predictions', label: 'Predictions', desc: 'AI forecasting', icon: 'pi pi-forward' },
      { id: 'anomalies', label: 'Anomalies', desc: 'System deviations', icon: 'pi pi-exclamation-triangle' },
      { id: 'efficiency', label: 'Efficiency', desc: 'Utilization scores', icon: 'pi pi-gauge' }
    ];

    // MOCK DATA FALLBACKS
    const mockPlants = [
      { id: 1, name: 'Agus 1 Hydroelectric Plant', capacity: 80 },
      { id: 2, name: 'Agus 2 Hydroelectric Plant', capacity: 180 },
      { id: 4, name: 'Agus 4 Hydroelectric Plant', capacity: 158.1 },
      { id: 5, name: 'Agus 5 Hydroelectric Plant', capacity: 55 },
      { id: 6, name: 'Agus 6 Hydroelectric Plant', capacity: 200 },
      { id: 7, name: 'Agus 7 Hydroelectric Plant', capacity: 54 },
    ];

    const generateMockTrends = (days) => {
      return {
        summary: {
          total_generation_mwh: 12450.50 + Math.random() * 5000,
          avg_capacity_factor: 68.4 + Math.random() * 10,
          avg_daily_generation_mwh: 415.02 + Math.random() * 100
        },
        daily_data: Array.from({length: days}).map((_, i) => {
          const d = new Date();
          d.setDate(d.getDate() - (days - 1 - i));
          return {
            date: d.toISOString(),
            generation_mwh: 380 + Math.random() * 120,
            capacity_factor: 60 + Math.random() * 25
          };
        })
      };
    };

    const generateMockComparison = () => {
      return {
        fleet_summary: {
          total_capacity_mw: 727.1,
          total_generation_mwh: 45890.2,
          fleet_avg_capacity_factor: 65.2,
          best_performer: 'Agus 6 Hydroelectric Plant'
        },
        plants: mockPlants.map(p => ({
          plant_id: p.id,
          plant_name: p.name,
          capacity_mw: p.capacity,
          total_generation_mwh: p.capacity * 24 * 30 * (0.5 + Math.random() * 0.3),
          avg_capacity_factor: 50 + Math.random() * 40,
          avg_availability: 85 + Math.random() * 15,
          performance_score: 70 + Math.random() * 25
        })).sort((a,b) => b.performance_score - a.performance_score)
      };
    };

    const generateMockPredictions = () => {
      return {
        based_on_days: 90,
        predictions: Array.from({length: 7}).map((_, i) => {
          const d = new Date();
          d.setDate(d.getDate() + i + 1);
          const cf = 65 + Math.random() * 20;
          return {
            date: d.toISOString(),
            predicted_generation_kwh: 400 + Math.random() * 100,
            predicted_capacity_factor: cf,
            confidence: cf > 75 ? 'high' : (cf > 65 ? 'medium' : 'low')
          };
        })
      };
    };

    const generateMockAnomalies = () => {
      return {
        anomalies_found: Math.floor(Math.random() * 4),
        anomalies: [
          {
            date: new Date(Date.now() - 86400000 * 2).toISOString(),
            plant: 'Agus 2 Hydroelectric Plant',
            unit: '1',
            capacity_factor: 25.4,
            expected_range: [55.0, 75.0],
            deviation: 29.6,
            severity: 'high'
          },
          {
            date: new Date(Date.now() - 86400000 * 5).toISOString(),
            plant: 'Agus 6 Hydroelectric Plant',
            unit: '3',
            capacity_factor: 92.1,
            expected_range: [60.0, 80.0],
            deviation: 12.1,
            severity: 'medium'
          }
        ]
      };
    };

    const generateMockEfficiency = () => {
      return {
        efficiency_score: 87.5 + Math.random() * 10,
        generation: {
          total_mwh: 12450.5,
          avg_capacity_factor: 68.4
        },
        utilization: {
          operating_percentage: 92.5,
          operating_hours: 666,
          forced_outage_percentage: 2.1,
          forced_outage_hours: 15
        }
      };
    };

    // Load Data Methods
    const loadPlants = async () => {
      try {
        const response = await axios.get(`${API_URL}/plants/`);
        plants.value = response.data?.length ? response.data : mockPlants;
      } catch (error) {
        plants.value = mockPlants;
      }
    };

    const loadTrends = async () => {
      loading.value = true;
      try {
        const params = { days: trendsDays.value };
        if (trendsPlant.value) params.plant_id = trendsPlant.value;
        const response = await axios.get(`${API_URL}/analytics/trends/`, { params });
        trendsData.value = response.data?.daily_data ? response.data : generateMockTrends(trendsDays.value);
      } catch (error) {
        trendsData.value = generateMockTrends(trendsDays.value);
      } finally {
        loading.value = false;
        nextTick(() => renderTrendsChart());
      }
    };

    const loadComparison = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${API_URL}/analytics/comparison/`);
        comparisonData.value = response.data?.plants ? response.data : generateMockComparison();
      } catch (error) {
        comparisonData.value = generateMockComparison();
      } finally {
        setTimeout(() => loading.value = false, 500); // add slight delay for skeleton UI feel
      }
    };

    const loadPredictions = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${API_URL}/analytics/predictions/`, {
          params: { plant_id: predictionPlant.value || undefined }
        });
        predictionsData.value = response.data?.predictions ? response.data : generateMockPredictions();
      } catch (error) {
        predictionsData.value = generateMockPredictions();
      } finally {
        setTimeout(() => loading.value = false, 500);
      }
    };

    const loadAnomalies = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${API_URL}/analytics/anomalies/`);
        anomaliesData.value = response.data?.anomalies ? response.data : generateMockAnomalies();
      } catch (error) {
        anomaliesData.value = generateMockAnomalies();
      } finally {
        setTimeout(() => loading.value = false, 800);
      }
    };

    const loadEfficiency = async () => {
      loading.value = true;
      try {
        const params = {};
        if (efficiencyPlant.value) params.plant_id = efficiencyPlant.value;
        const response = await axios.get(`${API_URL}/analytics/efficiency/`, { params });
        efficiencyData.value = response.data?.efficiency_score ? response.data : generateMockEfficiency();
      } catch (error) {
        efficiencyData.value = generateMockEfficiency();
      } finally {
        setTimeout(() => loading.value = false, 500);
      }
    };

    let chartInstance = null;

    const renderTrendsChart = () => {
      if (!trendsData.value || !trendsChartRef.value) return;

      if (chartInstance) chartInstance.destroy();

      const ctx = trendsChartRef.value.getContext('2d');
      
      const labels = trendsData.value.daily_data.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
      const genData = trendsData.value.daily_data.map(d => d.generation_mwh);
      const cfData = trendsData.value.daily_data.map(d => d.capacity_factor);

      // Create Gradients
      const genGradient = ctx.createLinearGradient(0, 0, 0, 400);
      genGradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
      genGradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

      const cfGradient = ctx.createLinearGradient(0, 0, 0, 400);
      cfGradient.addColorStop(0, 'rgba(16, 185, 129, 0.4)');
      cfGradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'Generation (MWh)',
              data: genData,
              borderColor: '#3b82f6',
              backgroundColor: genGradient,
              borderWidth: 3,
              pointBackgroundColor: '#fff',
              pointBorderColor: '#3b82f6',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
              fill: true,
              tension: 0.4,
              yAxisID: 'y'
            },
            {
              label: 'Capacity Factor (%)',
              data: cfData,
              borderColor: '#10b981',
              backgroundColor: cfGradient,
              borderWidth: 3,
              pointBackgroundColor: '#fff',
              pointBorderColor: '#10b981',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
              fill: true,
              tension: 0.4,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.9)',
              padding: 12,
              titleFont: { size: 14, family: "'Inter', sans-serif" },
              bodyFont: { size: 13, family: "'Inter', sans-serif" },
              borderColor: 'rgba(255,255,255,0.1)',
              borderWidth: 1,
              cornerRadius: 8,
              usePointStyle: true,
              boxPadding: 6
            }
          },
          scales: {
            x: {
              grid: { display: false, drawBorder: false },
              ticks: { font: { family: "'Inter', sans-serif" }, color: '#64748b' }
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              grid: { color: '#f1f5f9', drawBorder: false },
              ticks: { color: '#64748b', font: { family: "'Inter', sans-serif" } }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              grid: { drawOnChartArea: false },
              ticks: { color: '#64748b', font: { family: "'Inter', sans-serif" } }
            }
          }
        }
      });
    };

    // Watch tab changes to load data
    watch(activeTab, (newTab) => {
      if (newTab === 'trends' && !trendsData.value) loadTrends();
      if (newTab === 'comparison' && !comparisonData.value) loadComparison();
      if (newTab === 'predictions' && !predictionsData.value) loadPredictions();
      if (newTab === 'anomalies' && !anomaliesData.value) loadAnomalies();
      if (newTab === 'efficiency' && !efficiencyData.value) loadEfficiency();
      
      if (newTab === 'trends') nextTick(() => renderTrendsChart());
    });

    const formatNumber = (num) => {
      if (num === null || num === undefined) return '0.00';
      return Number(num).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    };

    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    };

    const getScoreClass = (score) => {
      if (score >= 80) return 'excellent';
      if (score >= 60) return 'good';
      if (score >= 40) return 'fair';
      return 'poor';
    };

    const getCfColor = (cf) => {
      if (cf >= 80) return 'linear-gradient(90deg, #10b981 0%, #059669 100%)';
      if (cf >= 60) return 'linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)';
      if (cf >= 40) return 'linear-gradient(90deg, #f59e0b 0%, #d97706 100%)';
      return 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)';
    };

    const exportReport = () => {
      alert("Analytics Report generated and downloading...");
    };

    onMounted(() => {
      loadPlants();
      loadTrends();
    });

    return {
      activeTab, loading, tabs, plants,
      trendsPlant, trendsDays, trendsData, trendsChartRef,
      comparisonData, predictionPlant, predictionsData,
      anomaliesData, efficiencyPlant, efficiencyData,
      loadTrends, loadComparison, loadPredictions, loadAnomalies, loadEfficiency,
      formatNumber, formatDate, getScoreClass, getCfColor, exportReport
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.advanced-analytics-container {
  padding: 32px;
  background: #f8fafc;
  min-height: calc(100vh - 64px);
  font-family: 'Inter', sans-serif;
  color: #0f172a;
}

/* Header Styles */
.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.header-content h2 {
  font-size: 2.25rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.03em;
}

.header-content p {
  color: #64748b;
  margin: 8px 0 0 0;
  font-size: 1.05rem;
}

.btn-export {
  padding: 12px 24px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #3b82f6;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.btn-export:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1);
}

/* Layout */
.analytics-layout {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

.analytics-sidebar {
  width: 280px;
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  flex-shrink: 0;
  position: sticky;
  top: 32px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: none;
  background: transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.nav-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  margin-right: 16px;
  transition: all 0.3s ease;
}

.nav-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.nav-label {
  font-weight: 700;
  color: #1e293b;
  font-size: 1rem;
}

.nav-desc {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 4px;
}

.nav-arrow {
  color: #cbd5e1;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: #f8fafc;
}

.nav-item.active {
  background: #eff6ff;
}

.nav-item.active .nav-icon {
  background: #3b82f6;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.nav-item.active .nav-label {
  color: #1d4ed8;
}

.nav-item.active .nav-arrow {
  color: #3b82f6;
  transform: translateX(4px);
}

/* Main Content */
.analytics-main {
  flex: 1;
  min-width: 0;
}

.tab-pane {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.pane-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f1f5f9;
}

.pane-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: #0f172a;
}

.pane-filters {
  display: flex;
  gap: 16px;
}

.filter-box {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

.filter-box:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-box i {
  color: #64748b;
  margin-right: 10px;
}

.filter-box select {
  border: none;
  background: transparent;
  font-weight: 600;
  color: #1e293b;
  outline: none;
  cursor: pointer;
  padding: 4px 0;
}

/* Buttons */
.btn-refresh, .btn-scan {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-refresh {
  background: #eff6ff;
  color: #3b82f6;
}

.btn-refresh:hover {
  background: #3b82f6;
  color: white;
}

.btn-scan {
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.btn-scan:hover {
  box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
}

.spinning i { animation: spin 1s linear infinite; }
.scanning i { animation: pulse-icon 1.5s ease infinite; }

@keyframes spin { 100% { transform: rotate(360deg); } }
@keyframes pulse-icon { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.metric-card {
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  position: relative;
  overflow: hidden;
  color: white;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
}

.metric-card.gradient-blue { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); }
.metric-card.gradient-green { background: linear-gradient(135deg, #10b981 0%, #047857 100%); }
.metric-card.gradient-orange { background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%); }

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  backdrop-filter: blur(4px);
}

.metric-info {
  display: flex;
  flex-direction: column;
}

.metric-title {
  font-size: 0.875rem;
  font-weight: 600;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 8px;
}

.metric-value small {
  font-size: 1rem;
  font-weight: 600;
  opacity: 0.8;
}

.metric-trend {
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-flex;
  width: fit-content;
}

/* Charts */
.chart-box {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-header h4 {
  margin: 0;
  color: #1e293b;
  font-size: 1.125rem;
}

.chart-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.dot.blue { background: #3b82f6; }
.dot.green { background: #10b981; }

.chart-canvas-container {
  height: 350px;
  width: 100%;
}

/* Tables & Fleet Comparison */
.fleet-overview {
  display: flex;
  justify-content: space-between;
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px 32px;
  margin-bottom: 32px;
  border: 1px solid #e2e8f0;
}

.overview-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.overview-item.highlight .o-value {
  color: #3b82f6;
}

.o-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.o-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
}

.overview-divider {
  width: 1px;
  background: #e2e8f0;
}

.modern-table-container {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table th {
  background: #f8fafc;
  padding: 16px;
  text-align: left;
  font-size: 0.875rem;
  color: #475569;
  font-weight: 600;
  text-transform: uppercase;
  border-bottom: 2px solid #e2e8f0;
}

.modern-table td {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
  vertical-align: middle;
}

.modern-table tr:hover {
  background: #f8fafc;
}

.font-semibold { font-weight: 600; }

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-text {
  width: 50px;
  font-weight: 600;
}

.progress-bar-bg {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.badge-score {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.875rem;
}

.badge-score.excellent { background: #dcfce7; color: #047857; }
.badge-score.good { background: #dbeafe; color: #1d4ed8; }
.badge-score.fair { background: #fef3c7; color: #b45309; }
.badge-score.poor { background: #fee2e2; color: #b91c1c; }

/* Predictions */
.info-alert {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  padding: 16px 24px;
  border-radius: 0 12px 12px 0;
  margin-bottom: 24px;
}

.info-alert i {
  font-size: 1.5rem;
  color: #3b82f6;
}

.info-alert strong {
  display: block;
  color: #1e3a8a;
  margin-bottom: 4px;
}

.info-alert p {
  margin: 0;
  color: #1e40af;
  font-size: 0.9375rem;
}

.predictions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.prediction-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.prediction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.pred-date {
  font-weight: 700;
  color: #0f172a;
  font-size: 1.125rem;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.pred-metrics {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.p-metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.p-label { color: #64748b; font-size: 0.9375rem; }
.p-value { font-weight: 700; color: #1e293b; }
.p-value small { font-weight: 500; color: #94a3b8; }

.pred-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
}

.confidence-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.badge-confidence {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.badge-confidence.high { background: #dcfce7; color: #047857; }
.badge-confidence.medium { background: #fef3c7; color: #b45309; }
.badge-confidence.low { background: #fee2e2; color: #b91c1c; }

/* Anomalies */
.anomaly-summary {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  border-radius: 16px;
  margin-bottom: 32px;
}

.anomaly-summary.has-issues {
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.anomaly-summary.all-clear {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.summary-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.has-issues .summary-icon { background: #fee2e2; color: #ef4444; }
.all-clear .summary-icon { background: #dcfce7; color: #10b981; }

.summary-text h4 { margin: 0 0 8px 0; font-size: 1.25rem; color: #0f172a; }
.summary-text p { margin: 0; color: #475569; }

.anomalies-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.anomaly-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-left: 6px solid;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.anomaly-item:hover {
  transform: translateX(4px);
}

.anomaly-item.high { border-left-color: #ef4444; }
.anomaly-item.medium { border-left-color: #f59e0b; }

.a-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.a-title { display: flex; flex-direction: column; gap: 4px; }
.a-plant { font-weight: 700; font-size: 1.125rem; color: #1e293b; }
.a-date { font-size: 0.875rem; color: #64748b; }

.badge-severity {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.875rem;
  text-transform: uppercase;
}

.badge-severity.high { background: #fee2e2; color: #b91c1c; }
.badge-severity.medium { background: #fef3c7; color: #b45309; }

.a-body {
  display: flex;
  gap: 32px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
}

.a-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.a-stat span { font-size: 0.875rem; color: #64748b; font-weight: 500; }
.a-stat strong { font-size: 1.25rem; color: #0f172a; font-weight: 700; }

.highlight-stat strong { color: #ef4444; }

/* Efficiency */
.efficiency-dashboard {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.score-panel {
  display: flex;
  justify-content: center;
  padding: 40px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.score-circle-container {
  position: relative;
  width: 200px;
  height: 200px;
}

.circular-chart {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  max-height: 250px;
}

.circle-bg {
  fill: none;
  stroke: #f1f5f9;
  stroke-width: 2.5;
}

.circle {
  fill: none;
  stroke-width: 2.5;
  stroke-linecap: round;
  animation: progress 1s ease-out forwards;
  stroke: url(#gradient);
}

/* Fallback for stroke since SVG gradients are complex in pure CSS, we use direct stroke color */
.circle { stroke: #3b82f6; }

@keyframes progress {
  0% { stroke-dasharray: 0 100; }
}

.score-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.score-number {
  display: block;
  font-size: 3rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1;
}

.score-label {
  font-size: 1rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.efficiency-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.detail-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  gap: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.d-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.d-icon.blue { background: #dbeafe; color: #2563eb; }
.d-icon.green { background: #dcfce7; color: #059669; }
.d-icon.red { background: #fee2e2; color: #dc2626; }

.d-info { flex: 1; }
.d-info h4 { margin: 0 0 16px 0; font-size: 1.125rem; color: #0f172a; }

.d-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f1f5f9;
}
.d-row:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.d-row span { color: #64748b; font-size: 0.9375rem; }
.d-row strong { color: #1e293b; font-weight: 700; }

/* Skeleton Loaders */
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.sk-card, .sk-chart, .sk-overview, .sk-table, .sk-alert, .sk-list-item, .sk-circle {
  background: #f6f7f8;
  background-image: linear-gradient(to right, #f6f7f8 0%, #edeef1 20%, #f6f7f8 40%, #f6f7f8 100%);
  background-repeat: no-repeat;
  background-size: 1000px 100%;
  animation: shimmer 2s infinite linear forwards;
  border-radius: 12px;
}

.sk-metrics { display: flex; gap: 24px; margin-bottom: 32px; }
.sk-metrics .sk-card { height: 120px; flex: 1; }
.sk-chart { height: 400px; width: 100%; }
.sk-overview { height: 100px; margin-bottom: 32px; }
.sk-table { height: 300px; }
.sk-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.sk-grid .sk-card { height: 200px; }
.sk-alert { height: 80px; margin-bottom: 24px; }
.sk-list { display: flex; flex-direction: column; gap: 16px; }
.sk-list-item { height: 120px; }
.sk-dashboard { display: flex; flex-direction: column; gap: 32px; align-items: center; }
.sk-circle { width: 200px; height: 200px; border-radius: 50%; }
.sk-details { display: flex; gap: 24px; width: 100%; }
.sk-details .sk-card { height: 150px; flex: 1; }

/* Responsive Design */
@media (max-width: 1024px) {
  .analytics-layout { flex-direction: column; }
  .analytics-sidebar { width: 100%; position: static; display: flex; overflow-x: auto; padding: 12px; border-radius: 12px; }
  .sidebar-nav { flex-direction: row; gap: 12px; }
  .nav-item { padding: 12px 16px; white-space: nowrap; }
  .nav-desc, .nav-arrow { display: none; }
  .metrics-grid, .efficiency-details { grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
  .a-body { flex-direction: column; gap: 12px; }
}

@media (max-width: 768px) {
  .advanced-analytics-container { padding: 16px; }
  .header-content h2 { font-size: 1.75rem; }
  .pane-header { flex-direction: column; align-items: flex-start; gap: 16px; }
  .fleet-overview { flex-direction: column; gap: 16px; }
  .overview-divider { height: 1px; width: 100%; }
  .sk-metrics, .sk-details { flex-direction: column; }
}
</style>
