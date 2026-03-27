<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3><i class="pi pi-chart-bar"></i> Capacity Factor Comparison</h3>
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
  name: 'CapacityFactorChart',
  data() {
    return {
      chart: null,
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
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/generation-reports/summary/`);
        this.renderChart(response.data);
      } catch (error) {
        console.error('Error loading chart data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    renderChart(data) {
      const plants = Object.keys(data);
      const capacityFactors = plants.map(plant => data[plant].avg_capacity_factor || 0);

      const ctx = this.$refs.chartCanvas.getContext('2d');

      if (this.chart) {
        this.chart.destroy();
      }

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: plants,
          datasets: [{
            label: 'Capacity Factor (%)',
            data: capacityFactors,
            backgroundColor: [
              'rgba(102, 126, 234, 0.8)',
              'rgba(118, 75, 162, 0.8)',
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 206, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
              'rgb(102, 126, 234)',
              'rgb(118, 75, 162)',
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 206, 86)',
              'rgb(75, 192, 192)'
            ],
            borderWidth: 2,
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `Capacity Factor: ${context.parsed.y.toFixed(2)}%`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: 'Capacity Factor (%)'
              },
              ticks: {
                callback: function(value) {
                  return value + '%';
                }
              }
            },
            x: {
              title: {
                display: true,
                text: 'Plant'
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
}
</style>
