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
          <!-- <button @click="exportDashboardToPDF" class="btn-export-pdf glass-button">
            <i class="pi pi-file-pdf"></i>
            Export PDF
          </button>
          <button @click="exportAllDashboardData" class="btn-export-csv glass-button">
            <i class="pi pi-file-excel"></i>
            Export CSV
          </button> -->
          <button @click="refreshData" class="btn-refresh glass-button" :disabled="loading">
            <i class="pi" :class="loading ? 'pi-spin pi-spinner' : 'pi-refresh'"></i>
            Refresh
          </button>
          <button @click="toggleAutoRefresh" class="btn-auto-refresh glass-button" :class="{ active: autoRefresh }">
            <i class="pi pi-clock"></i>
            Auto-refresh {{ autoRefresh ? 'ON' : 'OFF' }}
          </button>
          <!-- <button @click="debugTargetStatus" class="btn-debug glass-button" style="background: #ef4444;">
            <i class="pi pi-bug"></i>
            Debug Targets
          </button> -->
        </div>
      </div>
      <div class="last-updated" v-if="lastUpdated">
        Last updated: {{ formatLastUpdated(lastUpdated) }}
      </div>
    </div>

    <!-- Loading State with Skeleton -->
    <div v-if="loading" class="loading-state fade-in">
      <!-- Skeleton for Stats Cards -->
      <SkeletonLoader type="stats" />
      
      <!-- Skeleton for Charts -->
      <div class="skeleton-charts-layout">
        <div class="skeleton-charts-column">
          <SkeletonLoader type="chart" />
          <SkeletonLoader type="chart" />
        </div>
        <div class="skeleton-plants-column">
          <SkeletonLoader type="plants" />
        </div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="z-dashboard-layout">
      <!-- Top Row: Summary Cards (KPIs) -->
      <div class="stats-grid z-top-row">
        <div class="stat-card glass-stat-card glass-float interactive-card animate-slide-up" style="animation-delay: 0.1s" @mouseenter="highlightStat" @mouseleave="unhighlightStat">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <i class="pi pi-bolt"></i>
          </div>
          <div class="stat-content">
            <label>Total Generation</label>
            <span class="stat-value">{{ formatNumber(stats.totalGeneration) }}</span>
            <span class="stat-unit">kWh</span>
          </div>
        </div>

        <div class="stat-card glass-stat-card glass-float interactive-card animate-slide-up" style="animation-delay: 0.2s" @mouseenter="highlightStat" @mouseleave="unhighlightStat">
          <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <i class="pi pi-percentage"></i>
          </div>
          <div class="stat-content">
            <label>Avg Capacity Factor</label>
            <span class="stat-value">{{ formatNumber(stats.avgCapacityFactor) }}</span>
            <span class="stat-unit">%</span>
          </div>
        </div>

        <div class="stat-card glass-stat-card glass-float interactive-card animate-slide-up" style="animation-delay: 0.3s" @mouseenter="highlightStat" @mouseleave="unhighlightStat">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="stat-content">
            <label>Avg Availability</label>
            <span class="stat-value">{{ formatNumber(stats.avgAvailability) }}</span>
            <span class="stat-unit">%</span>
          </div>
        </div>

        <div class="stat-card glass-stat-card glass-float interactive-card animate-slide-up" style="animation-delay: 0.4s" @mouseenter="highlightStat" @mouseleave="unhighlightStat">
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

      <div class="z-main-content">
        <!-- Left Column: Charts -->
        <div class="z-charts-column">
          <!-- Trends Row 1: Monthly Generation Trend -->
          <div class="z-trend-row">
            <div class="card glass-card full-width animate-slide-up" style="animation-delay: 0.5s">
              <div class="card-header flex justify-between items-center">
                <h3 class="card-title"><i class="pi pi-chart-line"></i> Generation Performance Trend</h3>
                <div class="flex gap-2">
                  <div v-if="isTargetSet" class="legend-indicator flex items-center gap-2 mr-4">
                    <span class="flex items-center gap-1"><span class="dot-bar"></span> Actual</span>
                    <span class="flex items-center gap-1"><span class="dot-line"></span> Target</span>
                  </div>
                  <div class="view-mode-toggle mr-2">
                    <button 
                      @click="openTargetModal" 
                      class="set-target-btn"
                      :title="currentTargetText ? `Current target: ${currentTargetText}` : 'Set Target Capacity Factor'"
                    >
                      <i class="pi pi-cog"></i>
                      <span>{{ currentTargetText || 'Set Target' }}</span>
                    </button>
                  </div>
                  <select v-model="trendSelectedMonth" @change="handleTrendSelectionChange" class="trend-select">
                    <option v-for="(month, index) in monthNames" :key="index + 1" :value="index + 1">{{ month }}</option>
                  </select>
                  <select v-model="trendSelectedPlant" @change="handleTrendSelectionChange" class="trend-select">
                    <option value="" disabled>Select Plant</option>
                    <option v-for="plant in plantsData" :key="plant.code" :value="plant.code">{{ simplifyPlantName(plant.name) }}</option>
                  </select>
                  <select v-model="trendSelectedYear" @change="handleTrendSelectionChange" class="trend-select">
                    <option value="" disabled>Select Year</option>
                    <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
                  </select>
                </div>
              </div>
              <div class="card-body chart-container">
                <div v-if="loadingTrendData" class="loading-chart">
                  <i class="pi pi-spin pi-spinner"></i>
                  <span>Updating chart data...</span>
                </div>
                <BarChart v-else-if="plantsData.length" :key="chartKey" :data="generationTrendData" :options="barChartOptions" />
                <div v-else class="empty-chart">No data available</div>
              </div>
            </div>
          </div>

          <!-- Trends Row 1.5: Actual vs Target Comparison -->
          <div v-if="isTargetSet" class="z-trend-row mt-4">
            <div class="card glass-card full-width animate-slide-up" style="animation-delay: 0.6s">
              <div class="card-header flex justify-between items-center">
                <h3 class="card-title"><i class="pi pi-chart-bar"></i> Total Actual vs Target</h3>
              </div>
              <div class="card-body">
                <div v-if="plantsData.length" class="professional-bar-chart">
                  <!-- SELECTED MONTH SECTION -->
                  <div class="chart-section-label">
                    SELECTED MONTH ({{ monthNames[selectedMonthIndex] }} {{ trendSelectedYear }})
                  </div>
                  
                  <div class="chart-row">
                    <div class="row-header">
                      <div class="indicator-dot target-dot"></div>
                      <span class="row-label">TARGET</span>
                    </div>
                    <div class="chart-area">
                      <div class="bar-background">
                        <div 
                          :class="['bar-fill', 'target-fill', { 'bar-fill-hidden': selectedMonthTarget <= 0 }]"
                          :style="{ width: selectedMonthTarget > 0 ? selectedMonthTargetWidth + '%' : '0%' }"
                        ></div>
                      </div>
                      <div class="value-display target-value">
                        <div class="main-value">{{ formatNumber(selectedMonthTarget) }}</div>
                        <div class="percent-value">{{ formatPercent(selectedMonthTargetPercent) }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="chart-row">
                    <div class="row-header">
                      <div class="indicator-dot actual-dot"></div>
                      <span class="row-label">ACTUAL</span>
                    </div>
                    <div class="chart-area">
                      <div class="bar-background">
                        <div 
                          :class="['bar-fill', 'actual-fill', { 'bar-fill-hidden': selectedMonthActual <= 0 }]"
                          :style="{ width: selectedMonthActual > 0 ? selectedMonthActualWidth + '%' : '0%' }"
                        ></div>
                      </div>
                      <div class="value-display actual-value">
                        <div class="main-value">{{ formatNumber(selectedMonthActual) }}</div>
                        <div class="percent-value">{{ formatPercent(selectedMonthActualPercent) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-chart">No data available</div>
              </div>
            </div>
          </div>

          <!-- Trends Row 2: Monthly Availability Trend -->
          <div class="z-trend-row mt-4">
            <div class="card glass-card full-width animate-slide-up" style="animation-delay: 0.7s">
              <div class="card-header flex justify-between items-center">
                <h3 class="card-title">
                  <i class="pi pi-chart-bar"></i> 
                  {{ availabilityViewMode === 'monthly' ? 'Monthly' : 'Daily' }} Availability Trend
                </h3>
                <div class="flex gap-2">
                  <div class="view-mode-toggle mr-2">
                    <button 
                      @click="availabilityViewMode = 'monthly'" 
                      :class="['toggle-btn', { active: availabilityViewMode === 'monthly' }]"
                    >
                      Monthly
                    </button>
                    <button 
                      @click="availabilityViewMode = 'daily'" 
                      :class="['toggle-btn', { active: availabilityViewMode === 'daily' }]"
                    >
                      Daily
                    </button>
                  </div>
                  <select v-model="trendSelectedMonth" @change="handleTrendSelectionChange" class="trend-select">
                    <option v-for="(month, index) in monthNames" :key="index + 1" :value="index + 1">{{ month }}</option>
                  </select>
                  <select v-model="trendSelectedPlant" @change="handleTrendSelectionChange" class="trend-select">
                    <option value="" disabled>Select Plant</option>
                    <option v-for="plant in plantsData" :key="plant.code" :value="plant.code">{{ simplifyPlantName(plant.name) }}</option>
                  </select>
                  <select v-model="trendSelectedYear" @change="handleTrendSelectionChange" class="trend-select">
                    <option value="" disabled>Select Year</option>
                    <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
                  </select>
                </div>
              </div>
              <div class="card-body chart-container">
                <BarChart v-if="plantsData.length" :data="availabilityTrendData" :options="barChartOptionsPercent" />
                <div v-else class="empty-chart">No data available</div>
              </div>
            </div>
          </div>

          <!-- Pie Charts Row -->
          <div class="z-pie-row mt-4">
            <div class="card glass-card z-pie-chart animate-slide-up" style="animation-delay: 0.6s">
              <div class="card-header">
                <h3 class="card-title"><i class="pi pi-chart-pie"></i> Plant Capacity</h3>
              </div>
              <div class="card-body chart-container">
                <PieChart v-if="plantsData.length" :data="plantCapacityData" :options="pieChartOptions" />
                <div v-else class="empty-chart">No data available</div>
              </div>
            </div>
            
            <div class="card glass-card z-pie-chart animate-slide-up" style="animation-delay: 0.8s">
              <div class="card-header">
                <h3 class="card-title"><i class="pi pi-chart-pie"></i> Generation Distribution</h3>
              </div>
              <div class="card-body chart-container">
                <PieChart v-if="plantsData.length" :data="generationDistributionData" :options="pieChartOptions" />
                <div v-else class="empty-chart">No data available</div>
              </div>
            </div>
          </div>

          <!-- Plant Performance Summary Table -->
          <div class="z-table-row mt-4 animate-slide-up" style="animation-delay: 0.9s">
            <!-- Comparison Bar -->
            <div v-if="comparisonMode" class="comparison-bar mb-4 glass-card">
              <div class="comparison-info">
                <i class="pi pi-info-circle"></i>
                <span>{{ selectedForComparison.length }} plants selected for comparison (Select up to 4)</span>
              </div>
              <div class="comparison-actions">
                <button @click="openComparison" class="btn-view-comparison" :disabled="selectedForComparison.length < 2">
                  <i class="pi pi-chart-bar"></i> Compare Now
                </button>
                <button @click="cancelComparison" class="btn-cancel-comparison">
                  Cancel
                </button>
              </div>
            </div>

            <div class="card glass-card full-width">
              <div class="card-header flex justify-between items-center">
                <h3 class="card-title"><i class="pi pi-table"></i> Plant Performance Summary</h3>
                <button @click="toggleComparisonMode" class="btn-compare-mode glass-button" :class="{ active: comparisonMode }">
                  <i class="pi pi-clone"></i> {{ comparisonMode ? 'Exit Compare' : 'Compare Plants' }}
                </button>
              </div>
              <div class="card-body table-responsive">
                <table v-if="filteredPlants.length" class="summary-table">
                  <thead>
                    <tr>
                      <th @click="setSort('name')" class="cursor-pointer hover-header">
                        Plant <i class="pi" :class="getSortIcon('name')"></i>
                      </th>
                      <th @click="setSort('generation')" class="cursor-pointer hover-header">
                        Generation (kWh) <i class="pi" :class="getSortIcon('generation')"></i>
                      </th>
                      <th @click="setSort('capacityFactor')" class="cursor-pointer hover-header">
                        Capacity Factor (%) <i class="pi" :class="getSortIcon('capacityFactor')"></i>
                      </th>
                      <th @click="setSort('availability')" class="cursor-pointer hover-header">
                        Availability (%) <i class="pi" :class="getSortIcon('availability')"></i>
                      </th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="plant in filteredPlants" :key="plant.code" :class="{ 'selected-row': isSelectedForComparison(plant) }">
                      <td class="font-medium">
                        <div class="flex items-center gap-2">
                          <i v-if="isFavorite(plant.code)" class="pi pi-star-fill text-yellow-400 text-sm"></i>
                          {{ simplifyPlantName(plant.name) }} ({{ plant.code }})
                        </div>
                      </td>
                      <td>{{ formatNumber(plant.generation) }}</td>
                      <td>
                        <div class="metric-with-bar">
                          <span>{{ formatNumber(plant.capacityFactor) }}</span>
                          <div class="mini-progress">
                            <div class="mini-progress-fill" :style="{ width: plant.capacityFactor + '%', background: getProgressColor(plant.capacityFactor) }"></div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="metric-with-bar">
                          <span>{{ formatNumber(plant.availability) }}</span>
                          <div class="mini-progress">
                            <div class="mini-progress-fill" :style="{ width: plant.availability + '%', background: getProgressColor(plant.availability) }"></div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="action-buttons flex gap-2">
                          <button @click="toggleFavorite(plant)" class="btn-icon" :title="isFavorite(plant.code) ? 'Remove from Favorites' : 'Add to Favorites'">
                            <i class="pi" :class="isFavorite(plant.code) ? 'pi-star-fill text-yellow-400' : 'pi-star text-gray-400 hover:text-yellow-400'"></i>
                          </button>
                          <button v-if="comparisonMode" @click="comparePlant(plant)" class="btn-icon" :title="isSelectedForComparison(plant) ? 'Remove from Comparison' : 'Add to Comparison'">
                            <i class="pi" :class="isSelectedForComparison(plant) ? 'pi-check-square text-blue-500' : 'pi-stop text-gray-400 hover:text-blue-500'"></i>
                          </button>
                          <button @click="openPlantDetails(plant)" class="btn-details ml-2">
                            <i class="pi pi-external-link"></i> Details
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-else class="empty-chart">No data available</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Filters and Slicers -->
        <div class="z-filters-column card glass-card animate-slide-left" style="animation-delay: 0.3s">
          <div class="card-header">
            <h3 class="card-title"><i class="pi pi-filter"></i> Filters & Slicers</h3>
          </div>
          <div class="card-body filter-body">
            <div class="filter-section">
              <h4>Plant Selection</h4>
              <div class="plant-list">
                <label v-for="plant in plantsData" :key="plant.code" class="checkbox-label">
                  <input type="checkbox" :value="plant.code" v-model="selectedPlantsFilter" @change="applyFilters" />
                  {{ simplifyPlantName(plant.name) }}
                </label>
              </div>
            </div>

            <div class="filter-section">
              <h4>Date Range</h4>
              <div class="date-filters">
                <input type="date" v-model="startDate" class="date-input" @change="applyFilters" />
                <span>to</span>
                <input type="date" v-model="endDate" class="date-input" @change="applyFilters" />
              </div>
            </div>

            <div class="filter-section">
              <h4>Sort By</h4>
              <select v-model="sortBy" @change="sortPlants" class="sort-select glass-select full-width">
                <option value="name">Plant Name</option>
                <option value="generation">Generation Output</option>
                <option value="capacityFactor">Capacity Factor</option>
                <option value="availability">Availability</option>
              </select>
            </div>
            
            <div class="filter-actions">
              <button @click="clearFilters" class="btn-clear-filters glass-button full-width">
                Clear All Filters
              </button>
            </div>

            <div class="quick-actions-section">
              <h4>Quick Actions</h4>
              <div class="vertical-actions">
                <router-link to="/upload" class="action-btn">
                  <i class="pi pi-upload"></i> Upload Data
                </router-link>
                <router-link to="/generate" class="action-btn">
                  <i class="pi pi-download"></i> Generate Report
                </router-link>
              </div>
            </div>

            <div class="recent-uploads-section">
              <h4>Recent Activities</h4>
              <div v-if="recentUploads.length" class="recent-uploads-list">
                <div v-for="upload in recentUploads" :key="upload.id" class="upload-item" @click="$router.push('/upload')">
                  <div class="upload-item-content">
                    <div class="icon-circle">
                      <i class="pi pi-file-excel"></i>
                    </div>
                    <div class="upload-info">
                      <p class="upload-filename">{{ upload.filename || upload.name || 'Data Upload' }}</p>
                      <p class="upload-date">{{ formatDate(upload.uploaded_at || upload.date) }}</p>
                    </div>
                    <div class="status-indicator">
                      <i :class="getStatusIcon(upload.status)" :title="upload.status"></i>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-activities">
                No recent activities
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</AppLayout>

  <!-- Set Target Modal - Moved outside AppLayout to prevent clipping -->
  <div v-if="showTargetModal" class="modal-overlay target-modal-overlay" @click="showTargetModal = false">
      <div class="enhanced-target-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <div class="title-icon">
              <i class="pi pi-chart-line"></i>
            </div>
            <div class="title-text">
              <h3>Set Monthly Performance Target</h3>
              <p>Configure capacity factor targets for optimal performance tracking</p>
            </div>
          </div>
          <button @click="showTargetModal = false" class="btn-close-modal">
            <i class="pi pi-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <!-- Target Type Selection -->
          <div class="target-type-section">
            <label class="section-label">
              <i class="pi pi-sitemap"></i>
              Target Scope
            </label>
            <div class="target-type-options">
              <div class="target-type-option" :class="{ active: targetType === 'individual' }" @click="targetType = 'individual'">
                <div class="option-icon">
                  <i class="pi pi-building"></i>
                </div>
                <div class="option-content">
                  <h4>Individual Plant</h4>
                  <p>Set target for a specific plant</p>
                </div>
                <div class="option-radio">
                  <i class="pi pi-circle" v-if="targetType !== 'individual'"></i>
                  <i class="pi pi-check-circle" v-else></i>
                </div>
              </div>
              
              <div class="target-type-option" :class="{ active: targetType === 'all' }" @click="targetType = 'all'">
                <div class="option-icon">
                  <i class="pi pi-globe"></i>
                </div>
                <div class="option-content">
                  <h4>All Plants</h4>
                  <p>Set same target for all plants</p>
                </div>
                <div class="option-radio">
                  <i class="pi pi-circle" v-if="targetType !== 'all'"></i>
                  <i class="pi pi-check-circle" v-else></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Plant Selection (only for individual) -->
          <div class="target-form-group" v-if="targetType === 'individual'">
            <label class="section-label">
              <i class="pi pi-building"></i>
              Select Plant
            </label>
            <div class="custom-select-wrapper">
              <select 
                id="targetPlant"
                v-model="tempTargetPlant" 
                @change="loadCurrentTarget"
                class="enhanced-select"
              >
                <option value="" disabled>Choose a plant...</option>
                <option v-for="plant in plantsData" :key="plant.code" :value="plant.code">
                  {{ simplifyPlantName(plant.name) }} ({{ plant.code }})
                </option>
              </select>
              <i class="pi pi-chevron-down select-arrow"></i>
            </div>
          </div>

          <!-- Selected Plant Data Display (only for individual) -->
          <div class="selected-plant-data-card animate-fade-in" v-if="targetType === 'individual' && selectedPlantStats">
            <div class="data-header">
              <i class="pi pi-chart-bar"></i>
              <span>Current Performance Data</span>
            </div>
            <div class="data-grid">
              <div class="data-item">
                <span class="label">Total Generation:</span>
                <span class="value">{{ formatNumber(selectedPlantStats.generation) }} kWh</span>
              </div>
              <div class="data-item">
                <span class="label">Avg Capacity Factor:</span>
                <span class="value">{{ formatNumber(selectedPlantStats.capacityFactor) }}%</span>
              </div>
              <div class="data-item">
                <span class="label">Avg Availability:</span>
                <span class="value">{{ formatNumber(selectedPlantStats.availability) }}%</span>
              </div>
            </div>
          </div>

          <!-- Time Period Selection -->
          <div class="time-period-section">
            <label class="section-label">
              <i class="pi pi-calendar"></i>
              Time Period
            </label>
            <div class="time-period-grid">
              <div class="time-field">
                <label>Month</label>
                <div class="custom-select-wrapper">
                  <select 
                    id="targetMonth"
                    v-model.number="tempTargetMonth" 
                    @change="loadCurrentTarget"
                    class="enhanced-select"
                  >
                    <option v-for="(month, index) in monthNames" :key="index + 1" :value="index + 1">
                      {{ month }}
                    </option>
                  </select>
                  <i class="pi pi-chevron-down select-arrow"></i>
                </div>
              </div>
              
              <div class="time-field">
                <label>Year</label>
                <div class="custom-select-wrapper">
                  <select 
                    id="targetYear"
                    v-model.number="tempTargetYear" 
                    @change="loadCurrentTarget"
                    class="enhanced-select"
                  >
                    <option v-for="year in availableYears" :key="year" :value="year">
                      {{ year }}
                    </option>
                  </select>
                  <i class="pi pi-chevron-down select-arrow"></i>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Target Value -->
          <div class="target-value-section">
            <label class="section-label">
              <i class="pi pi-percentage"></i>
              Target Capacity Factor
            </label>
            <div class="target-input-wrapper">
              <div class="input-with-unit">
                <input 
                  id="targetCF"
                  type="number" 
                  v-model.number="tempTargetCapacityFactor" 
                  class="enhanced-target-input" 
                  min="0" 
                  max="100" 
                  step="0.1"
                  placeholder="85.0"
                />
                <span class="input-unit">%</span>
              </div>
              <div class="target-range-indicator">
                <div class="range-bar">
                  <div class="range-fill" :style="{ width: Math.min(tempTargetCapacityFactor || 0, 100) + '%' }"></div>
                </div>
                <div class="range-labels">
                  <span>0%</span>
                  <span>50%</span>
                  <span>100%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Summary Card -->
          <div class="target-summary-card" v-if="tempTargetCapacityFactor && tempTargetMonth && tempTargetYear">
            <div class="summary-header">
              <i class="pi pi-info-circle"></i>
              <span>Target Summary</span>
            </div>
            <div class="summary-content">
              <div class="summary-item">
                <span class="label">Scope:</span>
                <span class="value">
                  {{ targetType === 'all' ? 'All Plants' : (tempTargetPlant ? simplifyPlantName(plantsData.find(p => p.code === tempTargetPlant)?.name || '') : 'No plant selected') }}
                </span>
              </div>
              <div class="summary-item">
                <span class="label">Period:</span>
                <span class="value">{{ monthNames[tempTargetMonth - 1] }} {{ tempTargetYear }}</span>
              </div>
              <div class="summary-item">
                <span class="label">Target:</span>
                <span class="value highlight">{{ tempTargetCapacityFactor }}% Capacity Factor</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showTargetModal = false" class="btn-cancel">
            <i class="pi pi-times"></i>
            Cancel
          </button>
          <button 
            @click="saveTarget" 
            class="btn-save-target" 
            :disabled="isSaveDisabled"
            :class="{ 'locked': isCurrentMonthLocked && !overrideMode }"
          >
            <i class="pi" :class="overrideMode ? 'pi-unlock' : 'pi-check'"></i>
            {{ overrideMode ? 'Override & Save' : (targetType === 'all' ? 'Set for All Plants' : 'Save Target') }}
          </button>
          
          <!-- Secret Override Button (appears when current month is locked) -->
          <button 
            v-if="isCurrentMonthLocked && !overrideMode"
            @click="enableOverride"
            @keydown.ctrl.shift="enableOverride"
            class="btn-override-secret"
            title="Click while holding Ctrl+Shift to override locked target"
          >
            <i class="pi pi-lock"></i>
            <span class="override-hint">Locked</span>
          </button>
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
              <div class="plant-name">{{ simplifyPlantName(plant.name) }}</div>
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
</template>

<script>
import api from '../services/api';
import PlantDetailModal from './PlantDetailModal.vue';
import AppLayout from './AppLayout.vue';
import SkeletonLoader from './SkeletonLoader.vue';
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

import { isAdmin, isManagerOrAbove } from '../utils/auth';

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  ArcElement,
  Filler
} from 'chart.js';
import { Pie, Bar } from 'vue-chartjs';

import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ChartDataLabels
);

export default {
  name: 'DashboardView',
  components: {
    PlantDetailModal,
    AppLayout,
    SkeletonLoader,
    PieChart: Pie,
    BarChart: Bar
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
      sortBy: 'name',
      sortOrder: 'asc',
      viewMode: 'grid',
      activeFilters: [],
      selectedPlantsFilter: [],
      startDate: '',
      endDate: '',
      autoRefresh: false,
      refreshInterval: null,
      lastUpdated: null,
      comparisonMode: false,
      isAdminUser: false,
      isManagerOrAboveUser: false,
      showTargetModal: false,
      tempTargetCapacityFactor: 85,
      tempTargetPlant: '',
      tempTargetMonth: null,
      tempTargetYear: null,
      targetType: 'individual', // 'individual' or 'all'
      targetCapacityFactor: 85, // Default 85% Target CF (legacy)
      currentMonthlyTarget: null, // Current month's target for selected plant
      monthlyTargets: {}, // Cache for monthly targets
      buttonTargetText: null, // Dedicated reactive property for button text
      overrideMode: false, // Allow overriding locked targets
      selectedForComparison: [],
      showComparisonModal: false,
      exportingPlant: null,

      // Monthly Trend State
      trendSelectedPlant: 'AGUS1',  // Default to Agus 1
      trendSelectedMonth: new Date().getMonth() + 1, // Default to current month
      trendSelectedYear: '',   // Empty string to show placeholder
      trendMonthlyData: Array(12).fill(0),
      trendMonthlyAvailabilityData: Array(12).fill(0),
      trendMonthlyTargetData: Array(12).fill(0),
      loadingTrendData: false,
      chartKey: 0,
      availabilityViewMode: 'monthly',
      trendDailyLabels: [],
      trendDailyAvailabilityData: [],
      
      // Chart Options
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        },
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          datalabels: {
            display: false
          },
          legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
              usePointStyle: true,
              font: {
                size: 12,
                weight: '500'
              },
              color: '#374151',
              padding: 15,
              generateLabels: function(chart) {
                const datasets = chart.data.datasets;
                return datasets.map((dataset, index) => ({
                  text: dataset.label,
                  fillStyle: dataset.type === 'line' ? dataset.borderColor : dataset.backgroundColor,
                  strokeStyle: dataset.type === 'line' ? dataset.borderColor : dataset.borderColor,
                  lineWidth: dataset.type === 'line' ? 3 : 1,
                  pointStyle: dataset.type === 'line' ? 'line' : 'rect',
                  hidden: !chart.isDatasetVisible(index),
                  datasetIndex: index
                }));
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            titleColor: '#1e293b',
            bodyColor: '#475569',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            padding: 12,
            boxPadding: 6,
            usePointStyle: true,
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                
                // Add custom target CF if this is the target dataset
                if (context.dataset.customTargetCFs && context.dataIndex !== undefined) {
                  const cf = context.dataset.customTargetCFs[context.dataIndex];
                  label += ` (${cf.toFixed(1)}% CF)`;
                }
                
                if (label) {
                  label += ': ';
                }
                
                if (context.parsed.y !== null) {
                  if (label.toLowerCase().includes('generation')) {
                    label += new Intl.NumberFormat('en-US').format(context.parsed.y) + ' kWh';
                  } else {
                    label += new Intl.NumberFormat('en-US').format(context.parsed.y);
                  }
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            border: { display: false },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 },
              callback: function(value) {
                return new Intl.NumberFormat('en-US', { notation: 'compact', compactDisplay: 'short' }).format(value);
              }
            },
            grid: {
              color: 'rgba(226, 232, 240, 0.6)',
              drawTicks: false
            }
          },
          x: {
            border: { display: false },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 }
            },
            grid: {
              display: false
            }
          }
        }
      },
      barChartOptionsPercent: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1500, // Increase duration for a slower animation
          easing: 'easeOutQuart', // Smooth easing out
          delay: (context) => {
            let delay = 0;
            if (context.type === 'data' && context.mode === 'default') {
              delay = context.dataIndex * 50; // Stagger animation for each bar
            }
            return delay;
          }
        },
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          datalabels: {
            display: false
          },
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            titleColor: '#1e293b',
            bodyColor: '#475569',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            padding: 12,
            boxPadding: 6,
            usePointStyle: true,
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += context.parsed.y.toFixed(2) + '%';
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            border: { display: false },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 },
              callback: function(value) {
                return value + '%';
              }
            },
            grid: {
              color: 'rgba(226, 232, 240, 0.6)',
              drawTicks: false
            }
          },
          x: {
            border: { display: false },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 }
            },
            grid: {
              display: false
            }
          }
        }
      },
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          datalabels: {
            display: false
          },
          legend: {
            position: 'bottom',
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += new Intl.NumberFormat('en-US').format(context.parsed.y) + ' kWh';
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return new Intl.NumberFormat('en-US', { notation: 'compact', compactDisplay: 'short' }).format(value);
              }
            }
          }
        }
      },
      lineChartOptionsPercent: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          datalabels: {
            display: false
          },
          legend: {
            position: 'bottom',
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += context.parsed.y.toFixed(2) + '%';
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: function(value) {
                return value + '%';
              }
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.05)',
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      },
      pieChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          datalabels: {
            color: '#fff',
            font: {
              weight: 'bold',
              size: 11
            },
            formatter: (value, ctx) => {
              let sum = 0;
              let dataArr = ctx.chart.data.datasets[0].data;
              dataArr.map(data => {
                sum += data;
              });
              let percentage = (value * 100 / sum).toFixed(1) + "%";
              return percentage;
            }
          },
          legend: {
            position: 'right',
          }
        }
      }
    };
  },
  computed: {
    monthNames() {
      return [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];
    },
    
    currentTargetText() {
      // PRIORITY 1: Use the dedicated button text if it was just set
      if (this.buttonTargetText) {
        console.log('🔘 Button text from dedicated property:', this.buttonTargetText);
        return this.buttonTargetText;
      }
      
      // PRIORITY 2: Check if there's a target for the currently selected plant
      if (this.currentMonthlyTarget) {
        const plantName = this.plantsData.find(p => p.code === this.currentMonthlyTarget.plant_code)?.name || this.currentMonthlyTarget.plant_code;
        const simplifiedName = this.simplifyPlantName(plantName);
        const text = `${this.currentMonthlyTarget.target_percentage}% (${simplifiedName})`;
        console.log('🔘 Button text from currentMonthlyTarget:', text);
        return text;
      }
      
      // PRIORITY 3: If no target for selected plant, check if there are any targets set for the selected month/year
      const currentMonth = this.trendSelectedMonth;
      const currentYear = this.trendSelectedYear || new Date().getFullYear();
      
      // Look for any plant with a target for the current month, prioritize by highest target percentage
      const currentMonthTargets = Object.values(this.monthlyTargets).filter(target => {
        return parseInt(target.month) === currentMonth && 
               parseInt(target.year || this.trendSelectedYear) === currentYear &&
               target.target_percentage > 0;
      });
      
      if (currentMonthTargets.length > 0) {
        // Sort by target percentage (highest first) to show the most significant target
        const sortedTargets = currentMonthTargets.sort((a, b) => parseFloat(b.target_percentage) - parseFloat(a.target_percentage));
        const topTarget = sortedTargets[0];
        
        const plantName = this.plantsData.find(p => p.code === topTarget.plant_code)?.name || topTarget.plant_code;
        const simplifiedName = this.simplifyPlantName(plantName);
        
        // If there are multiple targets, show count
        if (currentMonthTargets.length > 1) {
          const text = `${topTarget.target_percentage}% (${simplifiedName} +${currentMonthTargets.length - 1} more)`;
          console.log('🔘 Button text from multiple targets:', text);
          return text;
        } else {
          const text = `${topTarget.target_percentage}% (${simplifiedName})`;
          console.log('🔘 Button text from single target:', text);
          return text;
        }
      }
      
      console.log('🔘 No button text found, returning null');
      return null;
    },
    
    isFormValid() {
      const hasRequiredFields = this.tempTargetMonth && this.tempTargetYear && this.tempTargetCapacityFactor !== null;
      
      if (this.targetType === 'individual') {
        return hasRequiredFields && this.tempTargetPlant;
      } else {
        return hasRequiredFields;
      }
    },
    
    isCurrentMonthLocked() {
      // Check if we're trying to modify the current month's target
      const now = new Date();
      const currentMonth = now.getMonth() + 1;
      const currentYear = now.getFullYear();
      
      // Only lock if it's the current month AND a target already exists
      if (this.tempTargetMonth === currentMonth && this.tempTargetYear === currentYear) {
        if (this.targetType === 'individual' && this.tempTargetPlant) {
          const cacheKey = `${this.tempTargetPlant}-${currentYear}-${currentMonth}`;
          const existingTarget = this.monthlyTargets[cacheKey];
          return existingTarget && existingTarget.target_percentage > 0;
        } else if (this.targetType === 'all') {
          // Check if any plant has a target for current month
          return Object.keys(this.monthlyTargets).some(key => {
            const target = this.monthlyTargets[key];
            return target.month === currentMonth && target.year === currentYear && target.target_percentage > 0;
          });
        }
      }
      return false;
    },
    
    isSaveDisabled() {
      // Disable if form is invalid OR if current month is locked (unless override mode is active)
      if (!this.isFormValid) return true;
      if (this.isCurrentMonthLocked && !this.overrideMode) return true;
      return false;
    },
    
    availableYears() {
      const currentYear = new Date().getFullYear();
      return [currentYear - 2, currentYear - 1, currentYear, currentYear + 1];
    },
    
    selectedPlantStats() {
      if (!this.tempTargetPlant || this.targetType !== 'individual') return null;
      return this.plantsData.find(p => p.code === this.tempTargetPlant);
    },
    
    isTargetSet() {
      // Check if there are any targets for the currently selected plant and year
      if (!this.trendSelectedPlant || !this.trendSelectedYear) return false;
      
      // Check if any month has a target > 0 for the selected plant and year
      for (let month = 1; month <= 12; month++) {
        const cacheKey = `${this.trendSelectedPlant}-${this.trendSelectedYear}-${month}`;
        const target = this.monthlyTargets[cacheKey];
        if (target && target.target_percentage > 0) {
          return true;
        }
      }
      
      return false;
    },
    
    generationTrendData() {
      const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      
      const datasets = [
        {
          type: 'bar',
          label: 'Actual Generation (kWh)',
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderColor: '#3b82f6',
          borderWidth: 1,
          borderRadius: 4,
          data: this.trendMonthlyData,
          order: 2
        }
      ];

      if (this.isTargetSet) {
        // Calculate the equivalent capacity factor percentage
        const plantCapacity = this.getPlantCapacity(this.trendSelectedPlant);
        
        // Find the actual target percentage from the monthly targets cache per month
        const monthlyTargetCFs = [];
        let firstValidTarget = 0;
        for (let month = 1; month <= 12; month++) {
          const cacheKey = `${this.trendSelectedPlant}-${this.trendSelectedYear}-${month}`;
          const target = this.monthlyTargets[cacheKey];
          const cf = target && target.target_percentage > 0 ? parseFloat(target.target_percentage) : 0;
          monthlyTargetCFs.push(cf);
          if (cf > 0 && firstValidTarget === 0) {
            firstValidTarget = cf;
          }
        }
        
        datasets.push({
          type: 'line',
          label: 'Target Generation',
          customTargetCFs: monthlyTargetCFs,
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          borderWidth: 3,
          borderDash: [5, 5],
          pointRadius: 4,
          pointBackgroundColor: '#f59e0b',
          tension: 0.4,
          data: this.trendMonthlyTargetData,
          order: 1
        });
      }

      return {
        labels,
        datasets
      };
    },
    totalTarget() {
      return this.trendMonthlyTargetData.reduce((sum, val) => sum + val, 0);
    },
    totalActual() {
      return this.trendMonthlyData.reduce((sum, val) => sum + val, 0);
    },
    currentMonthIndex() {
      return new Date().getMonth();
    },
    currentMonthActual() {
      // Only show current month data if the selected year is the current year
      const currentYear = new Date().getFullYear();
      if (this.trendSelectedYear !== currentYear) return 0;
      return this.trendMonthlyData[this.currentMonthIndex] || 0;
    },
    currentMonthTarget() {
      const currentYear = new Date().getFullYear();
      if (this.trendSelectedYear !== currentYear) return 0;
      return this.trendMonthlyTargetData[this.currentMonthIndex] || 0;
    },
    selectedMonthIndex() {
      return (this.trendSelectedMonth || 1) - 1;
    },
    selectedMonthActual() {
      return this.trendMonthlyData[this.selectedMonthIndex] || 0;
    },
    selectedMonthTarget() {
      return this.trendMonthlyTargetData[this.selectedMonthIndex] || 0;
    },
    yearlyActualPercent() {
      return this.calculateGenerationPercentage(this.totalActual, this.trendSelectedYear);
    },
    selectedMonthTargetPercent() {
      return this.getMonthlyTargetPercentage(this.selectedMonthIndex + 1, this.trendSelectedYear);
    },
    selectedMonthActualPercent() {
      return this.calculateGenerationPercentage(this.selectedMonthActual, this.trendSelectedYear, this.selectedMonthIndex + 1);
    },
    currentMonthTargetPercent() {
      const currentYear = new Date().getFullYear();
      if (this.trendSelectedYear !== currentYear) return 0;
      return this.getMonthlyTargetPercentage(this.currentMonthIndex + 1, this.trendSelectedYear);
    },
    currentMonthActualPercent() {
      const currentYear = new Date().getFullYear();
      if (this.trendSelectedYear !== currentYear) return 0;
      return this.calculateGenerationPercentage(this.currentMonthActual, this.trendSelectedYear, this.currentMonthIndex + 1);
    },
    currentMonthTargetWidth() {
      return (this.currentMonthTarget / this.maxChartValue) * 100;
    },
    currentMonthActualWidth() {
      return (this.currentMonthActual / this.maxChartValue) * 100;
    },
    selectedMonthTargetWidth() {
      return (this.selectedMonthTarget / this.maxChartValue) * 100;
    },
    selectedMonthActualWidth() {
      return (this.selectedMonthActual / this.maxChartValue) * 100;
    },
    maxChartValue() {
      let max = 0;
      
      // Check selected month values
      if (this.selectedMonthTarget > 0 || this.selectedMonthActual > 0) {
        max = Math.max(max, this.selectedMonthTarget || 0, this.selectedMonthActual || 0);
      }
      
      // Return max without padding so the highest bar is always 100% full
      return max > 0 ? max : 1;
    },
  plantCapacityData() {
      const labels = this.filteredPlants.map(p => p.name.replace(/ Hydroelectric Power Plant/gi, ''));
      const data = this.filteredPlants.map(p => this.getPlantCapacity(p.code));
      const backgroundColors = [
        '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#14b8a6', '#f97316'
      ];
      
      return {
        labels,
        datasets: [
          {
            label: 'Capacity (MW)',
            backgroundColor: backgroundColors.slice(0, labels.length),
            borderColor: '#ffffff',
            borderWidth: 2,
            hoverOffset: 4,
            data
          }
        ]
      };
    },
    availabilityTrendData() {
      const isMonthly = this.availabilityViewMode === 'monthly';
      const labels = isMonthly ? ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] : this.trendDailyLabels;
      const data = isMonthly ? this.trendMonthlyAvailabilityData : this.trendDailyAvailabilityData;
      
      return {
        labels,
        datasets: [
          {
            label: 'Availability (%)',
            backgroundColor: 'rgba(16, 185, 129, 0.8)',
            borderColor: '#10b981',
            borderWidth: 1,
            borderRadius: 4,
            data: data
          }
        ]
      };
    },
    generationDistributionData() {
      const labels = this.filteredPlants.map(p => p.name.replace(/ Hydroelectric Power Plant/gi, ''));
      const data = this.filteredPlants.map(p => p.generation);
      const backgroundColors = [
        '#6366f1', '#ec4899', '#eab308', '#06b6d4', '#f43f5e', '#84cc16', '#a855f7'
      ];
      
      return {
        labels,
        datasets: [
          {
            label: 'Generation Output',
            backgroundColor: backgroundColors.slice(0, labels.length),
            data
          }
        ]
      };
    }
  },
  created() {
    this.isAdminUser = isAdmin();
    this.isManagerOrAboveUser = isManagerOrAbove();
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
      console.log('🔄 Loading dashboard data...');
      
      try {
        // Step 1: Load plants first as they are required for trend and target data
        await this.loadPlantsStatsOptimized();
        
        // Step 2: Now that trendSelectedPlant is set, load other data concurrently
        await Promise.all([
          this.loadOverallStats(),
          this.loadRecentUploads(),
          this.fetchMonthlyTrendData()
        ]);
        
        this.lastUpdated = new Date();
        console.log('✅ Dashboard data loaded successfully');
      } catch (error) {
        console.error('❌ Error loading dashboard:', error);
      } finally {
        this.loading = false;
      }
    },

    async loadPlantsStatsOptimized() {
      try {
        console.log('🔄 Loading plants stats from analytics endpoint...');
        
        // Use the plant comparison endpoint which is already optimized to return all plant data in one call
        const response = await api.getPlantComparison();
        console.log('📊 Analytics response:', response.data);
        
        const comparisonData = response.data.plants || [];
        console.log('📈 Plants data from analytics:', comparisonData);
        
        const plantsWithStats = comparisonData.map(p => ({
          code: p.plant_code,
          name: p.plant_name,
          generation: p.total_generation_mwh * 1000, // Convert back to kWh for consistency
          capacityFactor: p.avg_capacity_factor,
          availability: p.avg_availability,
          hasData: p.days_reported > 0
        }));

        console.log('✅ Processed plants data:', plantsWithStats);
        
        this.plantsData = plantsWithStats;
        this.filteredPlants = [...plantsWithStats];
        this.sortPlants();
        
        // Ensure default plant is set to AGUS1 if available
        this.ensureDefaultPlant();
      } catch (error) {
        console.error('❌ Error loading optimized plant stats:', error);
        console.error('❌ Error response:', error.response);
        // Fallback to old method if optimized one fails
        await this.loadPlantsStats();
      }
    },
    
    async fetchMonthlyTrendData() {
      this.loadingTrendData = true;
      
      // Don't fetch data if no plant or year is selected (empty string means placeholder is showing)
      if (!this.trendSelectedPlant || this.trendSelectedPlant === '') {
        if (this.plantsData.length > 0) {
          // Default to AGUS1 if available, otherwise use first plant
          const agus1Plant = this.plantsData.find(plant => plant.code === 'AGUS1');
          this.trendSelectedPlant = agus1Plant ? 'AGUS1' : this.plantsData[0].code;
        } else {
          return;
        }
      }
      
      // Don't fetch data if no year is selected
      if (!this.trendSelectedYear || this.trendSelectedYear === '') {
        // Auto-select current year if not selected
        this.trendSelectedYear = new Date().getFullYear();
      }
      
      try {
        const year = this.trendSelectedYear;
        const startDate = `${year}-01-01`;
        const endDate = `${year}-12-31`;
        
        // Fetch targets for ALL plants to ensure the modal cache is complete
        // This prevents overwriting other plants' targets with 0% when setting individual targets
        const targetsResponse = await api.getMonthlyTargets({
          year: year
        });
        
        const targetsList = targetsResponse.data.results || targetsResponse.data || [];
        const monthlyTargetMap = {};
        
        // Update local cache for the modal and chart to use
        targetsList.forEach(t => {
          const pCode = t.plant_code || (t.plant && t.plant.code);
          const cacheKey = `${pCode}-${year}-${t.month}`;
          
          console.log('Processing target:', t);
          console.log('- Plant code:', pCode);
          console.log('- Month:', t.month);
          console.log('- Target percentage:', t.target_percentage);
          console.log('- Cache key:', cacheKey);
          
          this.monthlyTargets[cacheKey] = {
            ...t,
            plant_code: pCode,
            target_percentage: parseFloat(t.target_percentage)
          };
          
          // Only add to monthlyTargetMap if it matches the currently selected plant for the chart
          if (pCode === this.trendSelectedPlant) {
            console.log('✅ Target matches selected plant, adding to chart data');
            monthlyTargetMap[t.month] = parseFloat(t.target_percentage);
          } else {
            console.log('❌ Target does not match selected plant:', pCode, 'vs', this.trendSelectedPlant);
          }
        });
        
        console.log('Fetched targets for plant:', this.trendSelectedPlant, 'year:', year);
        console.log('Targets list from API:', targetsList);
        console.log('Monthly target map:', monthlyTargetMap);
        console.log('Targets cache updated:', this.monthlyTargets);

        // Fetch reports for the selected plant and year
        const response = await api.getGenerationReports({
          plant_code: this.trendSelectedPlant,
          start_date: startDate,
          end_date: endDate,
          page_size: 1000 // Get enough records to cover the whole year
        });
        
        const reports = response.data.results || response.data;
        
        // Aggregate by month
        const monthlyGenData = Array(12).fill(0);
        const monthlyAvailSum = Array(12).fill(0);
        const monthlyAvailCount = Array(12).fill(0);
        
        // Target generation: Accurate calculation based on exact days in each month and individual monthly targets
        const plantCapacity = this.getPlantCapacity(this.trendSelectedPlant);
        const monthlyTargetData = Array(12).fill(0).map((_, monthIndex) => {
          const monthNumber = monthIndex + 1;
          const daysInMonth = new Date(year, monthNumber, 0).getDate();
          const targetPercent = monthlyTargetMap[monthNumber] !== undefined ? monthlyTargetMap[monthNumber] : 0;
          const calculatedTarget = plantCapacity * 1000 * 24 * daysInMonth * (targetPercent / 100);
          
          // Debug logging for target calculation
          if (targetPercent > 0) {
            console.log(`Month ${monthNumber}: ${targetPercent}% target`);
            console.log(`- Plant capacity: ${plantCapacity} MW`);
            console.log(`- Days in month: ${daysInMonth}`);
            console.log(`- Calculated target: ${calculatedTarget} kWh`);
          }
          
          return calculatedTarget;
        });
        this.trendMonthlyTargetData = monthlyTargetData;
        
        console.log('Calculated monthly target data:', monthlyTargetData);
        console.log('Plant capacity for', this.trendSelectedPlant, ':', plantCapacity);
        console.log('Monthly target map:', monthlyTargetMap);
        console.log('isTargetSet computed:', this.isTargetSet);

        // Update the global targetCapacityFactor for the selected month for display purposes
        const currentMonth = this.trendSelectedMonth;
        
        if (monthlyTargetMap[currentMonth] !== undefined) {
          this.targetCapacityFactor = monthlyTargetMap[currentMonth];
          
          // Update currentMonthlyTarget object for button display (ensure it's for the selected plant)
          this.currentMonthlyTarget = targetsList.find(t => {
            const pCode = t.plant_code || (t.plant && t.plant.code);
            return pCode === this.trendSelectedPlant && parseInt(t.month) === currentMonth;
          });
        } else {
          this.targetCapacityFactor = 0;
          this.currentMonthlyTarget = null;
        }

        // Daily data for availability
        const dailyAvailMap = {};
        
        reports.forEach(report => {
          const date = new Date(report.report_date);
          const month = date.getMonth(); // 0 = Jan, 11 = Dec
          
          // Sum generation
          monthlyGenData[month] += parseFloat(report.generation_kwh || 0);
          
          // Track availability factor for averaging
          if (report.availability_factor !== undefined && report.availability_factor !== null) {
            monthlyAvailSum[month] += parseFloat(report.availability_factor);
            monthlyAvailCount[month]++;
            
            // Daily tracking
            const dateStr = report.report_date;
            if (!dailyAvailMap[dateStr]) {
              dailyAvailMap[dateStr] = { sum: 0, count: 0 };
            }
            dailyAvailMap[dateStr].sum += parseFloat(report.availability_factor);
            dailyAvailMap[dateStr].count++;
          }
        });
        
        this.trendMonthlyData = monthlyGenData;
        this.trendMonthlyAvailabilityData = monthlyAvailSum.map((sum, i) => 
          monthlyAvailCount[i] > 0 ? sum / monthlyAvailCount[i] : 0
        );

        // Process daily availability
        const sortedDates = Object.keys(dailyAvailMap).sort();
        this.trendDailyLabels = sortedDates.map(d => {
          const date = new Date(d);
          return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        this.trendDailyAvailabilityData = sortedDates.map(d => dailyAvailMap[d].sum / dailyAvailMap[d].count);
      } catch (error) {
        console.error('Error fetching monthly trend data:', error);
      } finally {
        this.loadingTrendData = false;
        this.chartKey++; // Force chart refresh
      }
    },
    
    refreshData() {
      this.loadDashboardData();
    },
    
    handleTrendSelectionChange() {
      // Persist selection to localStorage to maintain context on reload
      localStorage.setItem('trendSelectedPlant', this.trendSelectedPlant);
      localStorage.setItem('trendSelectedYear', this.trendSelectedYear);
      localStorage.setItem('trendSelectedMonth', this.trendSelectedMonth);
      
      // Refresh trend data (which now also updates current target display)
      this.fetchMonthlyTrendData();
    },
    
    ensureDefaultPlant() {
      // Check localStorage first
      const savedPlant = localStorage.getItem('trendSelectedPlant');
      const savedYear = localStorage.getItem('trendSelectedYear');
      const savedMonth = localStorage.getItem('trendSelectedMonth');
      
      if (savedPlant && this.plantsData.some(p => p.code === savedPlant)) {
        this.trendSelectedPlant = savedPlant;
      }
      
      if (savedYear) {
        this.trendSelectedYear = parseInt(savedYear);
      }
      
      if (savedMonth) {
        this.trendSelectedMonth = parseInt(savedMonth);
      }

      // Ensure a plant is selected as default if none is currently selected (or not in localStorage)
      if ((!this.trendSelectedPlant || this.trendSelectedPlant === '') && this.plantsData.length > 0) {
        const agus1Plant = this.plantsData.find(plant => plant.code === 'AGUS1');
        this.trendSelectedPlant = agus1Plant ? 'AGUS1' : this.plantsData[0].code;
        console.log('🏭 Default plant set to:', this.trendSelectedPlant);
      }
    },
    
    async openTargetModal() {
      console.log('Opening target modal...'); // Debug log
      console.log('Current plant:', this.trendSelectedPlant); // Debug log
      console.log('Current year:', this.trendSelectedYear); // Debug log
      console.log('Monthly targets cache:', this.monthlyTargets); // Debug log
      
      // Clear the dedicated button text so computed property recalculates
      this.buttonTargetText = null;
      console.log('🔘 Cleared buttonTargetText for fresh calculation');
      
      // Reset override mode when opening modal
      this.overrideMode = false;
      
      // Set defaults for the modal
      const now = new Date();
      this.tempTargetMonth = this.trendSelectedMonth; // Selected month
      this.tempTargetYear = this.trendSelectedYear || now.getFullYear(); // Selected year
      this.tempTargetPlant = this.trendSelectedPlant || (this.plantsData.length > 0 ? this.plantsData[0].code : '');
      this.targetType = 'individual'; // Default to individual
      
      // DON'T set a default value - wait for loadCurrentTarget to complete
      this.tempTargetCapacityFactor = null;
      
      // Load existing target and wait for it to complete
      await this.loadCurrentTarget();
      
      // If no target was loaded, then set default
      if (this.tempTargetCapacityFactor === null) {
        this.tempTargetCapacityFactor = 0; // Default to 0 instead of 85
        console.log('No existing target found, using default 0%');
      } else {
        console.log(`Loaded existing target: ${this.tempTargetCapacityFactor}%`);
      }
      
      this.showTargetModal = true;
      console.log('Modal should be visible now, showTargetModal:', this.showTargetModal); // Debug log
      
      // Force DOM update
      this.$nextTick(() => {
        console.log('DOM updated, modal element:', document.querySelector('.enhanced-target-modal'));
      });
    },
    
    enableOverride(event) {
      // Only enable override if Ctrl+Shift are held
      if (event.ctrlKey && event.shiftKey) {
        this.overrideMode = true;
        this.$toast.info('⚠️ Override mode enabled. You can now modify the locked target.');
        console.log('🔓 Override mode enabled');
      } else {
        this.$toast.warning('Hold Ctrl+Shift while clicking to enable override mode');
      }
    },
    
    async loadCurrentTarget() {
      if (!this.tempTargetPlant || !this.tempTargetMonth || !this.tempTargetYear) {
        console.log('Missing required parameters for loadCurrentTarget');
        return;
      }
      
      console.log(`Loading target for ${this.tempTargetPlant}, ${this.tempTargetMonth}/${this.tempTargetYear}`);
      
      // First check the local cache (which was just updated by saveTarget)
      const cacheKey = `${this.tempTargetPlant}-${this.tempTargetYear}-${this.tempTargetMonth}`;
      const cachedTarget = this.monthlyTargets[cacheKey];
      
      if (cachedTarget && cachedTarget.target_percentage !== undefined) {
        const cachedValue = parseFloat(cachedTarget.target_percentage);
        this.tempTargetCapacityFactor = cachedValue;
        console.log(`✅ Loaded from local cache: ${cachedValue}%`);
        return;
      }
      
      // If not in cache, fetch from API with cache-busting
      try {
        const response = await api.getCurrentMonthlyTarget(this.tempTargetPlant, this.tempTargetMonth, this.tempTargetYear);
        // API returns the target object directly, not wrapped in 'data'
        if (response.data && response.data.target_percentage !== undefined) {
          const loadedTarget = parseFloat(response.data.target_percentage);
          this.tempTargetCapacityFactor = loadedTarget;
          
          // Update local cache with the fetched value
          this.monthlyTargets[cacheKey] = response.data;
          
          console.log(`✅ Successfully loaded from API: ${loadedTarget}%`);
        } else {
          console.log('❌ No target_percentage in response:', response.data);
          this.tempTargetCapacityFactor = null;
        }
      } catch (error) {
        // No existing target found, keep null so default can be set
        console.log('❌ No existing target found or API error:', error.message || error);
        this.tempTargetCapacityFactor = null;
      }
    },
    
    // Debug method to check plant codes and targets
    debugTargetStatus() {
      console.log('=== TARGET DEBUG INFO ===');
      console.log('Current selected plant:', this.trendSelectedPlant);
      console.log('Current selected year:', this.trendSelectedYear);
      console.log('Available plants:', this.plantsData.map(p => ({ code: p.code, name: p.name })));
      console.log('Monthly targets cache:', this.monthlyTargets);
      console.log('isTargetSet computed:', this.isTargetSet);
      console.log('trendMonthlyTargetData:', this.trendMonthlyTargetData);
      
      // Check specific targets for current plant/year
      console.log('--- Targets for current selection ---');
      for (let month = 1; month <= 12; month++) {
        const cacheKey = `${this.trendSelectedPlant}-${this.trendSelectedYear}-${month}`;
        const target = this.monthlyTargets[cacheKey];
        if (target && target.target_percentage > 0) {
          console.log(`Month ${month}: ${target.target_percentage}%`);
        }
      }
      
      // Check if there are any targets for Agus 7 specifically
      console.log('--- All Agus 7 targets ---');
      Object.keys(this.monthlyTargets).forEach(key => {
        if (key.includes('AGUS7') || key.includes('agus7')) {
          console.log(`${key}:`, this.monthlyTargets[key]);
        }
      });
      
      console.log('========================');
    },
    
    async saveTarget() {
      console.log('🚀 saveTarget() called');
      console.log('📋 Form validation check...');
      console.log('  - isFormValid:', this.isFormValid);
      console.log('  - tempTargetMonth:', this.tempTargetMonth);
      console.log('  - tempTargetYear:', this.tempTargetYear);
      console.log('  - tempTargetCapacityFactor:', this.tempTargetCapacityFactor);
      console.log('  - tempTargetPlant:', this.tempTargetPlant);
      console.log('  - targetType:', this.targetType);
      
      if (!this.isFormValid) {
        console.error('❌ Form validation FAILED');
        this.$toast.error('Please fill in all required fields');
        return;
      }
      
      console.log('✅ Form validation PASSED');
      
      // Store the value we're trying to save for verification
      const targetValueToSave = this.tempTargetCapacityFactor;
      const plantToSave = this.tempTargetPlant;
      const monthToSave = this.tempTargetMonth;
      const yearToSave = this.tempTargetYear;
      
      console.log(`💾 Attempting to save target: ${targetValueToSave}% for ${plantToSave}, ${monthToSave}/${yearToSave}`);
      
      try {
        if (this.targetType === 'all') {
          // Set target for all plants - Use bulk set to avoid multiple requests (prevents 429 error)
          const targetsToSet = this.plantsData.map(plant => ({
            plant_code: plant.code,
            month: this.tempTargetMonth,
            year: this.tempTargetYear,
            target_percentage: this.tempTargetCapacityFactor
          }));
          
          const response = await api.bulkSetTargets(targetsToSet);
          
          if (response.data.success) {
            console.log(`✅ Database save successful for all plants`);
            
            // Clear the cache first to ensure fresh data
            this.monthlyTargets = {};
            
            // Update local cache with the response data
            response.data.results.forEach(target => {
              const targetKey = `${target.plant_code}-${target.year}-${target.month}`;
              this.monthlyTargets[targetKey] = target;
              console.log(`📝 Updated cache: ${target.plant_code} = ${target.target_percentage}%`);
            });
            
            // Update current monthly target if it matches current selection
            if (this.tempTargetMonth === this.trendSelectedMonth && this.tempTargetYear === (this.trendSelectedYear || new Date().getFullYear())) {
              const currentPlantTarget = this.monthlyTargets[`${this.trendSelectedPlant}-${this.tempTargetYear}-${this.tempTargetMonth}`];
              if (currentPlantTarget) {
                this.currentMonthlyTarget = currentPlantTarget;
              }
            }
            
            this.$toast.success(`Target set for all ${response.data.updated_count} plants: ${this.tempTargetCapacityFactor}% for ${this.monthNames[this.tempTargetMonth - 1]} ${this.tempTargetYear}`);
            
            // Switch to the current year if we set targets for it
            if (this.tempTargetYear !== this.trendSelectedYear) {
              this.trendSelectedYear = this.tempTargetYear;
            }
            
            // OPTIMIZED: Single chart refresh
            this.chartKey++;
            
            // OPTIMIZED: Only fetch trend data once
            await this.fetchMonthlyTrendData();
          }
        } else {
          // Set target for individual plant - Use bulk set to handle auto-zeroing other plants
          const targetsToSet = this.plantsData.map(plant => {
            const isSelected = plant.code === this.tempTargetPlant;
            const targetKey = `${plant.code}-${this.tempTargetYear}-${this.tempTargetMonth}`;
            const existingTarget = this.monthlyTargets[targetKey];
            
            if (isSelected) {
              return {
                plant_code: plant.code,
                month: this.tempTargetMonth,
                year: this.tempTargetYear,
                target_percentage: this.tempTargetCapacityFactor
              };
            } else if (!existingTarget) {
              // Only include other plants if they don't have a target yet
              return {
                plant_code: plant.code,
                month: this.tempTargetMonth,
                year: this.tempTargetYear,
                target_percentage: 0
              };
            }
            return null;
          }).filter(t => t !== null);
          
          console.log(`📤 Sending to API:`, targetsToSet.find(t => t.plant_code === plantToSave));
          console.log(`📡 Making API call to bulkSetTargets...`);
          
          const response = await api.bulkSetTargets(targetsToSet);
          
          console.log(`📥 API call completed`);
          console.log(`📊 Response status:`, response.status);
          console.log(`📊 Response data:`, response.data);
          
          if (response.data.success) {
            console.log(`✅ Database save successful!`);
            console.log(`📊 API Response:`, response.data);
            
            // CRITICAL: Clear the entire cache to force fresh data
            const oldCache = { ...this.monthlyTargets };
            this.monthlyTargets = {};
            
            // Update local cache with the response data
            response.data.results.forEach(target => {
              const targetKey = `${target.plant_code}-${target.year}-${target.month}`;
              this.monthlyTargets[targetKey] = target;
              console.log(`📝 Updated cache: ${target.plant_code} = ${target.target_percentage}%`);
            });
            
            // Force Vue to detect the cache change by creating new object reference
            this.monthlyTargets = { ...this.monthlyTargets };
            
            console.log(`🔄 Cache cleared and rebuilt. Old entries: ${Object.keys(oldCache).length}, New entries: ${Object.keys(this.monthlyTargets).length}`);
            
            // Verify the saved value matches what we intended to save
            const savedTarget = response.data.results.find(t => t.plant_code === plantToSave);
            if (savedTarget) {
              const savedValue = parseFloat(savedTarget.target_percentage);
              if (Math.abs(savedValue - targetValueToSave) < 0.01) {
                console.log(`✅ VERIFICATION PASSED: Saved ${savedValue}% matches intended ${targetValueToSave}%`);
              } else {
                console.warn(`⚠️ VERIFICATION WARNING: Saved ${savedValue}% differs from intended ${targetValueToSave}%`);
              }
            }
            
            // Update current target display - FORCE UPDATE FOR BUTTON
            // Update for the plant we just saved, regardless of month
            const savedTargetForPlant = this.monthlyTargets[`${this.tempTargetPlant}-${this.tempTargetYear}-${this.tempTargetMonth}`];
            if (savedTargetForPlant) {
              // ALWAYS update button text for selected month saves
              if (this.tempTargetMonth === this.trendSelectedMonth && this.tempTargetYear === (this.trendSelectedYear || new Date().getFullYear())) {
                // Force update currentMonthlyTarget with new object reference
                this.currentMonthlyTarget = { ...savedTargetForPlant };
                console.log(`🔄 Updated currentMonthlyTarget for current month: ${savedTargetForPlant.target_percentage}%`);
                
                // CRITICAL: Directly set the button text to force immediate update
                const plantName = this.plantsData.find(p => p.code === this.tempTargetPlant)?.name || this.tempTargetPlant;
                const simplifiedName = this.simplifyPlantName(plantName);
                this.buttonTargetText = `${savedTargetForPlant.target_percentage}% (${simplifiedName})`;
                console.log(`🔘 FORCED button text update: ${this.buttonTargetText}`);
                
                // Force Vue reactivity by triggering a re-render
                this.$forceUpdate();
              }
              
              // If we're viewing this plant, update immediately
              if (this.tempTargetPlant === this.trendSelectedPlant) {
                this.currentMonthlyTarget = { ...savedTargetForPlant };
                console.log(`🔄 Updated currentMonthlyTarget for button display: ${savedTargetForPlant.target_percentage}%`);
              }
            }
            
            const monthName = this.monthNames[this.tempTargetMonth - 1];
            const plantName = this.simplifyPlantName(this.plantsData.find(p => p.code === this.tempTargetPlant)?.name || '');
            
            this.$toast.success(`✅ Target saved: ${targetValueToSave}% for ${plantName} in ${monthName} ${this.tempTargetYear}`);
            
            // IMPORTANT: Switch the trend view to show the plant we just set the target for
            this.trendSelectedPlant = this.tempTargetPlant;
            this.trendSelectedYear = this.tempTargetYear;
            
            // OPTIMIZED: Single chart refresh instead of multiple
            this.chartKey++;
            
            // OPTIMIZED: Only fetch trend data once, not twice
            await this.fetchMonthlyTrendData();
          } else {
            console.error('❌ API returned success=false');
            this.$toast.error('Failed to save target. API returned error.');
            return;
          }
        }
        
        // Update legacy target for chart compatibility
        this.targetCapacityFactor = this.tempTargetCapacityFactor;
        
        // Close modal immediately - don't wait for extra operations
        this.showTargetModal = false;
        
        console.log(`🎉 Save complete! Target ${targetValueToSave}% is now in database and frontend cache.`);
        
      } catch (error) {
        console.error('❌ Error saving target:', error);
        this.$toast.error(`Failed to save target: ${error.message || 'Unknown error'}`);
      }
    },
    
    async fetchMonthlyTargets() {
      // Force re-fetch all monthly targets from API to ensure button updates
      console.log('🔄 Re-fetching monthly targets from API...');
      try {
        const response = await api.getMonthlyTargets();
        if (response.data && response.data.results) {
          // Clear and rebuild cache
          this.monthlyTargets = {};
          response.data.results.forEach(target => {
            const targetKey = `${target.plant_code}-${target.year}-${target.month}`;
            this.monthlyTargets[targetKey] = target;
          });
          console.log(`✅ Refreshed ${response.data.results.length} targets from API`);
          
          // Update currentMonthlyTarget if we have one for the selected plant
          const now = new Date();
          const currentMonth = now.getMonth() + 1;
          const currentYear = now.getFullYear();
          const currentKey = `${this.trendSelectedPlant}-${currentYear}-${currentMonth}`;
          if (this.monthlyTargets[currentKey]) {
            this.currentMonthlyTarget = this.monthlyTargets[currentKey];
            
            // Update button text directly
            const plantName = this.plantsData.find(p => p.code === this.trendSelectedPlant)?.name || this.trendSelectedPlant;
            const simplifiedName = this.simplifyPlantName(plantName);
            this.buttonTargetText = `${this.currentMonthlyTarget.target_percentage}% (${simplifiedName})`;
            
            console.log(`✅ Updated button to show: ${this.buttonTargetText}`);
          }
        }
      } catch (error) {
        console.error('❌ Error fetching monthly targets:', error);
      }
    },
    
    // Force complete chart refresh
    async forceChartRefresh() {
      console.log('🔄 Forcing complete chart refresh...');
      
      // Clear cache
      this.monthlyTargets = {};
      
      // Increment chart key to force re-render
      this.chartKey++;
      
      // Fetch fresh data
      await this.fetchMonthlyTrendData();
      
      // Force Vue reactivity update
      this.$forceUpdate();
      
      // Another chart key increment after data is loaded
      this.$nextTick(() => {
        this.chartKey++;
        console.log('✅ Chart refresh complete');
      });
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
        console.log('🔄 Loading overall stats...');
        const response = await api.getReportSummary();
        console.log('📊 Report summary response:', response.data);
        
        this.stats = {
          totalGeneration: response.data.total_generation || 0,
          avgCapacityFactor: response.data.avg_capacity_factor || 0,
          avgAvailability: response.data.avg_availability_factor || 0,
          totalOperatingHours: response.data.total_operating_hours || 0,
        };
        
        console.log('✅ Processed stats:', this.stats);
      } catch (error) {
        console.error('❌ Error loading overall stats:', error);
        console.error('❌ Error response:', error.response);
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
        
        // Ensure default plant is set to AGUS1 if available
        this.ensureDefaultPlant();
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
    
    formatPercent(value) {
      if (!value) return '0.00%';
      return `${parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}%`;
    },
    
    getMonthlyTargetPercentage(month, year) {
      if (!this.trendSelectedPlant || !month || !year) return 0;
      const cacheKey = `${this.trendSelectedPlant}-${year}-${month}`;
      const target = this.monthlyTargets[cacheKey];
      return target && target.target_percentage > 0 ? parseFloat(target.target_percentage) : 0;
    },
    
    calculateGenerationPercentage(generationValue, year, month = null) {
      const plantCapacity = this.getPlantCapacity(this.trendSelectedPlant);
      if (!plantCapacity || !year || !generationValue) return 0;
      
      const periodDays = month
        ? new Date(year, month, 0).getDate()
        : new Date(year, 12, 0).getDate();
      const maxGeneration = plantCapacity * 1000 * 24 * periodDays;
      
      return maxGeneration > 0 ? (parseFloat(generationValue) / maxGeneration) * 100 : 0;
    },
    
    simplifyPlantName(name) {
      if (!name) return '';
      return name.replace(/ Hydro(-)?Electric Power Plant/gi, '').replace(/ Hydroelectric Power Plant/gi, '');
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
        'AGUS1': 80.0,
        'AGUS2': 180.0,
        'AGUS4': 158.1,
        'AGUS5': 55.0,
        'AGUS6': 200.0,
        'AGUS7': 54.0,
        'PULANGI4': 255.0,
      };
      return capacities[code] || 0;
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedPlant = null;
    },
    
    setSort(column) {
      if (this.sortBy === column) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortBy = column;
        // Default to descending for numbers, ascending for name
        this.sortOrder = column === 'name' ? 'asc' : 'desc';
      }
      this.sortPlants();
    },

    getSortIcon(column) {
      if (this.sortBy !== column) return 'pi-sort-alt text-gray-400 opacity-50';
      return this.sortOrder === 'asc' ? 'pi-sort-amount-up-alt text-blue-500' : 'pi-sort-amount-down text-blue-500';
    },
    
    sortPlants() {
      const sortFn = (a, b) => {
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
      };

      this.filteredPlants.sort(sortFn);
      this.plantsData.sort(sortFn);
    },
    
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      this.sortPlants();
    },
    
    applyFilters() {
      let result = [...this.plantsData];
      
      // Filter by selected plants
      if (this.selectedPlantsFilter.length > 0) {
        result = result.filter(plant => this.selectedPlantsFilter.includes(plant.code));
      }
      
      this.filteredPlants = result;
      this.sortPlants();
    },

    clearFilters() {
      this.selectedPlantsFilter = [];
      this.startDate = '';
      this.endDate = '';
      this.sortBy = 'name';
      this.applyFilters();
    },
    
    removeFilter(filter) {
      this.activeFilters = this.activeFilters.filter(f => f !== filter);
      this.filteredPlants = [...this.plantsData];
      this.sortPlants();
    },
    
    getProgressColor(value) {
      if (value >= 80) return 'linear-gradient(90deg, #10b981, #34d399)';
      if (value >= 60) return 'linear-gradient(90deg, #3b82f6, #60a5fa)';
      if (value >= 40) return 'linear-gradient(90deg, #f59e0b, #fbbf24)';
      return 'linear-gradient(90deg, #ef4444, #f87171)';
    },
    
    highlightStat(event) {
      event.currentTarget.style.transform = 'scale(1.05)';
      event.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
    },
    
    unhighlightStat(event) {
      event.currentTarget.style.transform = '';
      event.currentTarget.style.background = '';
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
  
  watch: {
    // Watch for changes to monthlyTargets and update button text
    monthlyTargets: {
      handler(newTargets) {
        console.log('🔍 monthlyTargets changed, updating button text...');
        const now = new Date();
        const currentMonth = now.getMonth() + 1;
        const currentYear = now.getFullYear();
        const currentKey = `${this.trendSelectedPlant}-${currentYear}-${currentMonth}`;
        
        if (newTargets[currentKey]) {
          const target = newTargets[currentKey];
          const plantName = this.plantsData.find(p => p.code === target.plant_code)?.name || target.plant_code;
          const simplifiedName = this.simplifyPlantName(plantName);
          this.buttonTargetText = `${target.target_percentage}% (${simplifiedName})`;
          console.log(`🔘 Watcher updated button text: ${this.buttonTargetText}`);
        }
      },
      deep: true
    },
    
    // Watch for changes to currentMonthlyTarget
    currentMonthlyTarget: {
      handler(newTarget) {
        if (newTarget) {
          console.log('🔍 currentMonthlyTarget changed:', newTarget);
          const plantName = this.plantsData.find(p => p.code === newTarget.plant_code)?.name || newTarget.plant_code;
          const simplifiedName = this.simplifyPlantName(plantName);
          this.buttonTargetText = `${newTarget.target_percentage}% (${simplifiedName})`;
          console.log(`🔘 Watcher updated button text from currentMonthlyTarget: ${this.buttonTargetText}`);
        }
      },
      deep: true
    }
  },
};
</script>

<style scoped>
/* Z-Pattern Dashboard Layout */
.z-dashboard-layout {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.z-top-row {
  /* Inherits from stats-grid */
  margin-bottom: 0;
}

.z-main-content {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.z-charts-column {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.z-trend-row {
  width: 100%;
}

.z-pie-row {
  display: flex;
  gap: 1.5rem;
}

.z-line-chart {
  flex: 2;
  margin-bottom: 0;
}

.z-pie-chart {
  flex: 1;
  margin-bottom: 0;
}

.chart-container {
  height: 300px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-chart {
  color: #94a3b8;
  font-style: italic;
}

.trend-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background-color: white;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
  outline: none;
  transition: all 0.2s ease;
  min-width: 120px;
}

.trend-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.z-filters-column {
  flex: 1;
  position: sticky;
  top: 1.5rem;
  margin-bottom: 0;
}

.filter-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-section h4 {
  margin: 0 0 0.75rem 0;
  color: #475569;
  font-size: 0.95rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.plant-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  color: #334155;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: #3b82f6;
  cursor: pointer;
}

.date-filters {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.date-filters span {
  text-align: center;
  color: #64748b;
  font-size: 0.85rem;
}

.date-input {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #334155;
}

.full-width {
  width: 100%;
}

.filter-actions {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.quick-actions-section {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.vertical-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  color: #3b82f6;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 1px solid #bfdbfe;
}

.action-btn:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
}

@media (max-width: 1200px) {
  .z-main-content {
    flex-direction: column;
  }
  
  .z-filters-column {
    width: 100%;
    position: static;
  }
  
  .z-middle-row, .z-bottom-row {
    flex-direction: column;
  }
  
  .z-line-chart, .z-pie-chart {
    width: 100%;
  }
}

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

/* Professional Horizontal Bar Chart Styles */
.professional-bar-chart {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.chart-section-label {
  font-size: 0.75rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;
}

.chart-section-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 0.75rem 0;
}

.chart-row {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
  padding: 0.5rem 0;
}

.chart-row:last-child {
  margin-bottom: 0;
}

.row-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 120px;
  flex-shrink: 0;
}

.indicator-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.target-dot {
  background: linear-gradient(135deg, #facc15 0%, #eab308 100%);
}

.actual-dot {
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
}

.row-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.chart-area {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.bar-background {
  flex: 1;
  height: 28px;
  background: #ffffff;
  border-radius: 14px;
  overflow: hidden;
  position: relative;
  border: 1px solid #e5e7eb;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.bar-fill {
  height: 100%;
  border-radius: 13px;
  transition: width 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  min-width: 0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
}

.bar-fill-hidden {
  opacity: 0;
  box-shadow: none;
}

.target-fill {
  background: linear-gradient(135deg, #facc15 0%, #eab308 100%);
}

.actual-fill {
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
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
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: slideShimmer 3s infinite;
}

.bar-fill-hidden::before {
  display: none;
}

@keyframes slideShimmer {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
  100% { transform: translateX(100%); }
}

.value-display {
  min-width: 140px;
  text-align: right;
  font-size: 0.95rem;
  font-weight: 700;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid transparent;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  line-height: 1.2;
}

.main-value {
  font-size: 1.05rem;
  font-weight: 800;
}

.percent-value {
  font-size: 0.8rem;
  font-weight: 600;
  opacity: 0.8;
  margin-top: 0.1rem;
}

.target-value {
  color: #a16207;
  border-color: #fde68a;
  background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
}

.actual-value {
  color: #3b82f6;
  border-color: #dbeafe;
  background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
}

.value-display:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Performance indicator */
.chart-row:nth-child(2) .value-display::after {
  content: '';
  position: absolute;
  right: -6px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid #3b82f6;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
}

/* Responsive Design */
@media (max-width: 768px) {
  .professional-bar-chart {
    padding: 1rem;
  }
  
  .chart-row {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }
  
  .row-header {
    min-width: auto;
    justify-content: center;
    padding-bottom: 0.25rem;
  }
  
  .chart-area {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .value-display {
    text-align: center;
    min-width: auto;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .professional-bar-chart {
    padding: 0.75rem;
  }
  
  .bar-background {
    height: 24px;
  }
  
  .value-display {
    font-size: 0.875rem;
    padding: 0.375rem 0.5rem;
  }
  
  .row-label {
    font-size: 0.75rem;
  }
}

/* Set Target Button Style */
.set-target-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.set-target-btn:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
  color: #1f2937;
}

.set-target-btn i {
  font-size: 0.875rem;
  color: #6b7280;
}

.glass-button-sm {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
}

.glass-button-sm:hover {
  background: white;
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

/* Target Modal Specific Styles */
.target-modal {
  max-width: 500px;
  width: 90%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

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

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.modal-title i {
  color: #6b7280;
  font-size: 1.125rem;
}

.btn-close-modal {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s ease;
}

.btn-close-modal:hover {
  background: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 2rem;
}

.target-form-group {
  margin-bottom: 1.5rem;
}

.target-form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.input-with-unit {
  position: relative;
  display: flex;
  align-items: center;
}

.target-input {
  width: 100%;
  padding: 0.875rem 3rem 0.875rem 1rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  transition: all 0.2s;
  text-align: center;
}

.target-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-unit {
  position: absolute;
  right: 1rem;
  color: #9ca3af;
  font-weight: 600;
  font-size: 1rem;
}

.input-help {
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.btn-cancel {
  padding: 0.625rem 1.25rem;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.btn-apply-target {
  padding: 0.625rem 1.25rem;
  border: none;
  background: #3b82f6;
  color: white;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-apply-target:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

.dot-bar {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  background-color: #3b82f6;
}

.dot-line {
  display: inline-block;
  width: 12px;
  height: 2px;
  background-color: #f59e0b;
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

.card-header-content h3 {
  margin: 0;
  flex-shrink: 0;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  flex: 1;
  justify-content: flex-end;
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
  flex-shrink: 0;
  min-width: 150px;
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

/* New Elements CSS */
.z-table-row {
  margin-top: 1.5rem;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.summary-table th {
  padding: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  color: #475569;
  font-weight: 600;
}

.summary-table td {
  padding: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #334155;
}

.summary-table tr:hover td {
  background: rgba(255, 255, 255, 0.05);
}

.font-medium {
  font-weight: 500;
}

.btn-details {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.btn-details:hover {
  color: #2563eb;
}

.recent-uploads-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.recent-uploads-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.upload-item {
  background: rgba(255, 255, 255, 0.5);
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: background 0.2s;
}

.upload-item:hover {
  background: rgba(255, 255, 255, 0.8);
}

.upload-item-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon-circle {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
}

.upload-info {
  flex: 1;
  min-width: 0;
}

.upload-filename {
  margin: 0;
  font-size: 0.875rem;
  color: #334155;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.upload-date {
  margin: 0;
  font-size: 0.75rem;
  color: #64748b;
}

.empty-activities {
  font-size: 0.875rem;
  color: #64748b;
  text-align: center;
  margin-top: 1rem;
}

/* Interactive Enhancements */
.interactive-card {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s ease;
  cursor: pointer;
}

.hover-header {
  user-select: pointer;
  transition: background-color 0.2s;
}

.hover-header:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.hover-header i {
  margin-left: 0.25rem;
  font-size: 0.8rem;
  transition: color 0.2s, opacity 0.2s;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 0.25rem;
  border-radius: 4px;
  transition: transform 0.2s, color 0.2s;
}

.btn-icon:hover {
  transform: scale(1.15);
}

.selected-row td {
  background-color: rgba(59, 130, 246, 0.1);
}

.action-buttons {
  display: flex;
  align-items: center;
}

/* Animations */
@keyframes slideUpFade {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideLeftFade {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-slide-up {
  opacity: 0;
  animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-slide-left {
  opacity: 0;
  animation: slideLeftFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.fade-in {
  animation: fadeIn 0.4s ease-in-out forwards;
}

/* Custom Loading Spinner */
.loader-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(59, 130, 246, 0.2);
  border-left-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background: var(--surface-card, #ffffff);
  border-radius: 16px;
  border: 1px solid var(--surface-border, #e5e7eb);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.loading-state p {
  color: var(--text-color-secondary, #64748b);
  font-weight: 500;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
}

/* Legend and Toggle Styles */
.legend-indicator {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.dot-bar {
  display: inline-block;
  width: 12px;
  height: 12px;
  background: #3b82f6;
  border-radius: 2px;
}

.dot-line {
  display: inline-block;
  width: 16px;
  height: 3px;
  background: #f59e0b;
  border-radius: 1px;
}

.view-mode-toggle {
  display: flex;
  background: rgba(226, 232, 240, 0.5); /* subtle gray background */
  border-radius: 8px;
  padding: 4px;
}

.toggle-btn {
  outline: none;
  border: none;
  cursor: pointer;
  background: transparent;
  padding: 6px 14px;
  font-size: 0.8rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  color: #64748b;
  font-weight: 600;
}

.toggle-btn:hover {
  color: #1e293b;
  background: rgba(255, 255, 255, 0.5);
}

.toggle-btn.active {
  background-color: #10b981; /* Emerald green */
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.toggle-btn.active:hover {
  color: white;
  background-color: #059669;
}

.target-input-container {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 2px 8px;
  height: 32px;
}

.target-input-container input {
  border: none;
  outline: none;
  background: transparent;
  width: 40px;
  color: #1e293b;
  font-weight: 600;
  -moz-appearance: textfield;
}

.target-input-container input::-webkit-outer-spin-button,
.target-input-container input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Skeleton Layout Styles */
.skeleton-charts-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

.skeleton-charts-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.skeleton-plants-column {
  display: flex;
  flex-direction: column;
}

@media (max-width: 1200px) {
  .skeleton-charts-layout {
    grid-template-columns: 1fr;
  }
}

/* Enhanced loading state */
.loading-state {
  padding: 20px;
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #6b7280;
  gap: 1rem;
}

.loading-chart i {
  font-size: 2rem;
  color: #3b82f6;
}

.loading-chart span {
  font-size: 0.875rem;
  font-weight: 500;
}

/* Enhanced monthly target modal styles - More specific selectors */
.target-modal-overlay.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(0, 0, 0, 0.6) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 99999 !important;
  padding: 1rem !important;
  animation: fadeIn 0.3s ease !important;
  backdrop-filter: blur(4px) !important;
  pointer-events: auto !important;
}

.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(0, 0, 0, 0.6) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 99999 !important;
  padding: 1rem !important;
  animation: fadeIn 0.3s ease !important;
  pointer-events: auto !important;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalAppear {
  from { 
    opacity: 0; 
    transform: scale(0.9) translateY(-20px); 
  }
  to { 
    opacity: 1; 
    transform: scale(1) translateY(0); 
  }
}

.enhanced-target-modal {
  max-width: 650px !important;
  width: 100% !important;
  max-height: 90vh !important;
  background: white !important;
  border-radius: 20px !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4) !important;
  overflow: hidden !important;
  animation: modalAppear 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  position: relative !important;
  margin: auto !important;
  transform: none !important;
  opacity: 1 !important;
  visibility: visible !important;
}

.modal-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: flex-start !important;
  padding: 2rem 2rem 1.5rem 2rem !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
  position: relative !important;
}

.modal-title {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.title-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
  backdrop-filter: blur(10px);
}

.title-text h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
}

.title-text p {
  margin: 0;
  font-size: 0.875rem;
  opacity: 0.9;
  line-height: 1.4;
}

.btn-close-modal {
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  backdrop-filter: blur(10px);
}

.btn-close-modal:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.modal-body {
  padding: 2rem !important;
  max-height: calc(90vh - 200px) !important;
  overflow-y: auto !important;
  background: white !important;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

.section-label i {
  color: #6b7280;
  font-size: 1rem;
}

/* Target Type Selection */
.target-type-section {
  margin-bottom: 2rem;
}

.target-type-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.target-type-option {
  padding: 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  background: white;
}

.target-type-option:hover {
  border-color: #d1d5db;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.target-type-option.active {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
}

.option-icon {
  width: 48px;
  height: 48px;
  background: #f3f4f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: #6b7280;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.target-type-option.active .option-icon {
  background: #3b82f6;
  color: white;
}

.option-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.option-content p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.4;
}

.option-radio {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.25rem;
  color: #d1d5db;
  transition: all 0.3s ease;
}

.target-type-option.active .option-radio {
  color: #3b82f6;
}

/* Form Groups */
.target-form-group {
  margin-bottom: 2rem;
}

.custom-select-wrapper {
  position: relative;
}

.enhanced-select {
  width: 100%;
  padding: 1rem 3rem 1rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  color: #1f2937;
  transition: all 0.3s ease;
  cursor: pointer;
  appearance: none;
}

.enhanced-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  font-size: 0.875rem;
  pointer-events: none;
  transition: all 0.3s ease;
}

.enhanced-select:focus + .select-arrow {
  color: #3b82f6;
  transform: translateY(-50%) rotate(180deg);
}

/* Time Period Grid */
.time-period-section {
  margin-bottom: 2rem;
}

.time-period-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.time-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

/* Target Value Section */
.target-value-section {
  margin-bottom: 2rem;
}

.target-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-with-unit {
  display: flex;
  align-items: stretch;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
  height: 54px;
}

.input-with-unit:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.enhanced-target-input {
  flex: 1;
  padding: 0 1.5rem;
  border: none !important;
  font-size: 1.25rem;
  font-weight: 600;
  background: transparent;
  color: #1f2937;
  text-align: center;
  width: 100%;
  height: 100%;
}

.enhanced-target-input:focus {
  outline: none !important;
  box-shadow: none !important;
}

/* Selected Plant Data Card in Modal */
.selected-plant-data-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 2rem;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.selected-plant-data-card .data-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #475569;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.selected-plant-data-card .data-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.selected-plant-data-card .data-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.selected-plant-data-card .data-item .label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.selected-plant-data-card .data-item .value {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1e293b;
}

@media (max-width: 640px) {
  .selected-plant-data-card .data-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

.input-unit {
  padding: 0 1.5rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-left: 2px solid #e5e7eb;
  font-size: 1.125rem;
  color: #64748b;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  height: 100%;
  margin: 0 !important;
}

.input-with-unit:focus-within .input-unit {
  border-left-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #3b82f6;
}

.target-range-indicator {
  margin-top: 1rem;
}

.range-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.range-fill {
  height: 100%;
  background: linear-gradient(90deg, #ef4444 0%, #f59e0b 50%, #10b981 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #6b7280;
}

/* Summary Card */
.target-summary-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 2px solid #bae6fd;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #0c4a6e;
}

.summary-header i {
  color: #0284c7;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.summary-item .label {
  font-weight: 500;
  color: #374151;
}

.summary-item .value {
  font-weight: 600;
  color: #1f2937;
}

.summary-item .value.highlight {
  color: #0284c7;
  font-size: 1.125rem;
}

/* Modal Footer */
.modal-footer {
  display: flex !important;
  justify-content: flex-end !important;
  gap: 1rem !important;
  padding: 1.5rem 2rem 2rem 2rem !important;
  background: #f9fafb !important;
  border-top: 1px solid #e5e7eb !important;
}

.btn-cancel {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: 2px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
  transform: translateY(-1px);
}

.btn-save-target {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-save-target:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.btn-save-target:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.6;
}

.btn-save-target.locked {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-save-target.locked:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.btn-override-secret {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: 2px dashed #f59e0b;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}

.btn-override-secret:hover {
  background: linear-gradient(135deg, #fde68a 0%, #fcd34d 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
  border-color: #d97706;
}

.override-hint {
  font-size: 0.75rem;
  opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
  .enhanced-target-modal {
    max-width: 95% !important;
    margin: 0.5rem !important;
    max-height: 95vh !important;
  }
  
  .target-type-options {
    grid-template-columns: 1fr !important;
  }
  
  .time-period-grid {
    grid-template-columns: 1fr !important;
  }
  
  .modal-header {
    padding: 1.5rem !important;
  }
  
  .modal-body {
    padding: 1.5rem !important;
    max-height: calc(95vh - 180px) !important;
  }
  
  .modal-footer {
    padding: 1.5rem !important;
    flex-direction: column !important;
  }
  
  .btn-cancel,
  .btn-save-target {
    width: 100% !important;
    justify-content: center !important;
  }
}

@media (max-width: 480px) {
  .enhanced-target-modal {
    max-width: 100% !important;
    margin: 0 !important;
    border-radius: 0 !important;
    max-height: 100vh !important;
  }
  
  .modal-header {
    padding: 1rem !important;
  }
  
  .modal-body {
    padding: 1rem !important;
    max-height: calc(100vh - 160px) !important;
  }
  
  .modal-footer {
    padding: 1rem;
  }
  
  .title-text h3 {
    font-size: 1.25rem;
  }
  
  .title-text p {
    font-size: 0.8125rem;
  }
}
</style>
