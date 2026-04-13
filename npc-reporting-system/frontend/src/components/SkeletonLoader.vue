<template>
  <div class="skeleton-loader">
    <!-- Skeleton for Stats Cards -->
    <div v-if="type === 'stats'" class="skeleton-stats-grid">
      <div v-for="n in 4" :key="n" class="skeleton-stat-card">
        <div class="skeleton-stat-icon"></div>
        <div class="skeleton-stat-content">
          <div class="skeleton-line skeleton-label"></div>
          <div class="skeleton-line skeleton-value"></div>
          <div class="skeleton-line skeleton-unit"></div>
        </div>
      </div>
    </div>

    <!-- Skeleton for Charts -->
    <div v-if="type === 'chart'" class="skeleton-chart">
      <div class="skeleton-chart-header">
        <div class="skeleton-line skeleton-chart-title"></div>
        <div class="skeleton-line skeleton-chart-subtitle"></div>
      </div>
      <div class="skeleton-chart-body">
        <div class="skeleton-chart-content"></div>
      </div>
    </div>

    <!-- Skeleton for Plant Cards -->
    <div v-if="type === 'plants'" class="skeleton-plants-grid">
      <div v-for="n in 6" :key="n" class="skeleton-plant-card">
        <div class="skeleton-plant-header">
          <div class="skeleton-line skeleton-plant-name"></div>
          <div class="skeleton-line skeleton-plant-status"></div>
        </div>
        <div class="skeleton-plant-stats">
          <div v-for="i in 3" :key="i" class="skeleton-plant-stat">
            <div class="skeleton-line skeleton-stat-small"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Skeleton for Table -->
    <div v-if="type === 'table'" class="skeleton-table">
      <div class="skeleton-table-header">
        <div v-for="n in 5" :key="n" class="skeleton-line skeleton-table-header-cell"></div>
      </div>
      <div class="skeleton-table-body">
        <div v-for="n in 5" :key="n" class="skeleton-table-row">
          <div v-for="i in 5" :key="i" class="skeleton-line skeleton-table-cell"></div>
        </div>
      </div>
    </div>

    <!-- Generic Skeleton Lines -->
    <div v-if="type === 'lines'" class="skeleton-lines">
      <div v-for="n in (lines || 3)" :key="n" class="skeleton-line" :class="`skeleton-line-${n}`"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonLoader',
  props: {
    type: {
      type: String,
      required: true,
      validator: value => ['stats', 'chart', 'plants', 'table', 'lines'].includes(value)
    },
    lines: {
      type: Number,
      default: 3
    }
  }
}
</script>

<style scoped>
.skeleton-loader {
  width: 100%;
}

/* Base skeleton animation */
@keyframes skeleton-loading {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
}

.skeleton-line {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 4px;
  height: 16px;
  margin-bottom: 8px;
}

/* Dark mode skeleton */
.dark-mode .skeleton-line {
  background: linear-gradient(90deg, #2a2a2a 25%, #3a3a3a 50%, #2a2a2a 75%);
  background-size: 200px 100%;
}

/* Stats Grid Skeleton */
.skeleton-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

@media (max-width: 1200px) {
  .skeleton-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .skeleton-stats-grid {
    grid-template-columns: 1fr;
  }
}

.skeleton-stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 120px;
}

.skeleton-stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s infinite;
  flex-shrink: 0;
}

.skeleton-stat-content {
  flex: 1;
}

.skeleton-label {
  width: 80%;
  height: 14px;
}

.skeleton-value {
  width: 60%;
  height: 24px;
  margin: 8px 0;
}

.skeleton-unit {
  width: 30%;
  height: 12px;
}

/* Chart Skeleton */
.skeleton-chart {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
}

.skeleton-chart-header {
  margin-bottom: 20px;
}

.skeleton-chart-title {
  width: 40%;
  height: 20px;
  margin-bottom: 8px;
}

.skeleton-chart-subtitle {
  width: 60%;
  height: 14px;
}

.skeleton-chart-body {
  height: 300px;
  position: relative;
}

.skeleton-chart-content {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.skeleton-chart-content::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60%;
  background: linear-gradient(
    to top,
    rgba(59, 130, 246, 0.1) 0%,
    rgba(59, 130, 246, 0.05) 50%,
    transparent 100%
  );
  border-radius: 0 0 8px 8px;
}

/* Plants Grid Skeleton */
.skeleton-plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.skeleton-plant-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 20px;
}

.skeleton-plant-header {
  margin-bottom: 16px;
}

.skeleton-plant-name {
  width: 70%;
  height: 18px;
  margin-bottom: 8px;
}

.skeleton-plant-status {
  width: 40%;
  height: 14px;
}

.skeleton-plant-stats {
  display: flex;
  gap: 12px;
}

.skeleton-plant-stat {
  flex: 1;
}

.skeleton-stat-small {
  width: 100%;
  height: 12px;
}

/* Table Skeleton */
.skeleton-table {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  overflow: hidden;
}

.skeleton-table-header {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.skeleton-table-header-cell {
  height: 16px;
  width: 80%;
}

.skeleton-table-body {
  padding: 16px;
}

.skeleton-table-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 12px;
}

.skeleton-table-cell {
  height: 14px;
  width: 90%;
}

/* Generic Lines */
.skeleton-lines {
  padding: 20px;
}

.skeleton-line-1 {
  width: 100%;
}

.skeleton-line-2 {
  width: 85%;
}

.skeleton-line-3 {
  width: 70%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .skeleton-stats-grid {
    gap: 16px;
  }
  
  .skeleton-stat-card {
    padding: 16px;
    min-height: 100px;
  }
  
  .skeleton-stat-icon {
    width: 50px;
    height: 50px;
  }
  
  .skeleton-plants-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .skeleton-chart {
    padding: 16px;
  }
  
  .skeleton-chart-body {
    height: 250px;
  }
}

/* Animation delays for staggered effect */
.skeleton-stat-card:nth-child(1) { animation-delay: 0.1s; }
.skeleton-stat-card:nth-child(2) { animation-delay: 0.2s; }
.skeleton-stat-card:nth-child(3) { animation-delay: 0.3s; }
.skeleton-stat-card:nth-child(4) { animation-delay: 0.4s; }

.skeleton-plant-card:nth-child(1) { animation-delay: 0.1s; }
.skeleton-plant-card:nth-child(2) { animation-delay: 0.2s; }
.skeleton-plant-card:nth-child(3) { animation-delay: 0.3s; }
.skeleton-plant-card:nth-child(4) { animation-delay: 0.4s; }
.skeleton-plant-card:nth-child(5) { animation-delay: 0.5s; }
.skeleton-plant-card:nth-child(6) { animation-delay: 0.6s; }

/* Pulse effect for interactive elements */
.skeleton-stat-card,
.skeleton-plant-card,
.skeleton-chart {
  animation: skeleton-pulse 2s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}
</style>