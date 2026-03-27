<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3><i class="pi pi-chart-line"></i> Generation Trend</h3>
      <div class="chart-controls">
        <select v-model="timeRange" @change="loadData" class="time-select">
          <option value="7">Last 7 Days</option>
          <option value="30">Last 30 Days</option>
          <option value="90">Last 90 Days</option>
          <option value="365">Last Year</option>
        </select>
      </div>
    </div>
    <div v-if="loading" class="chart-loading">
      <i class="pi pi-spin pi-spinner"></i>
      <p>Loading chart data...</p>
    </div>
    <canvas v-else ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

Chart.register(...registerables);

export default {
  name: 'GenerationTrendChart',
  props: {
    plantCode: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      chart: null,
      timeRange: 30,
      loading: false
    };
  },
  mounted() {
    this.loadData();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  },
  methods: {
    async loadData() {
      this.loading = true;
      
      try {
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - this.timeRange);

        let url = `${process.env.VUE_APP_API_URL}/generation-reports/?start_date=${startDate.toISOString().split('T')[0]}&end_date=${endDate.toISOString().split('T')[0]}`;
        
        if (this.plantCode) {
          url += `&plant_code=${this.plantCode}`;
        }

        const response = await axios.get(url);
        this.renderChart(response.data.results || []);
      } catch (error) {
        console.error('Error loading chart data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    renderChart(data) {
      // Group by date and sum generation
      const groupedData = {};
      data.forEach(item => {
        const date = item.report_date;
        if (!groupedData[date]) {
          groupedData[date] = 0;
        }
        groupedData[date] += parseFloat(item.generation_kwh);
      });

      const labels = Object.keys(groupedData).sort();
      const values = labels.map(date => groupedData[date] / 1000); // Convert to MWh

      const ctx = this.$refs.chartCanvas.getContext('2d');

      if (this.chart) {
        this.chart.destroy();
      }

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Generation (MWh)',
            data: values,
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: function(context) {
                  return `Generation: ${context.parsed.y.toFixed(2)} MWh`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Generation (MWh)'
              },
              ticks: {
                callback: function(value) {
                  return value.toLocaleString();
                }
              }
            },
            x: {
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.chart-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 400px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-controls {
  display: flex;
  gap: 10px;
}

.time-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  background: white;
}

.time-select:focus {
  outline: none;
  border-color: #667eea;
}

.chart-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 320px;
  color: #7f8c8d;
}

.chart-loading i {
  font-size: 32px;
  margin-bottom: 12px;
}

canvas {
  max-height: 320px;
}

@media (max-width: 768px) {
  .chart-container {
    height: 350px;
  }
  
  .chart-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
