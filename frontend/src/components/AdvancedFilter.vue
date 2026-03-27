<template>
  <div class="advanced-filter-panel" :class="{ 'expanded': isExpanded }">
    <div class="filter-header" @click="toggleExpand">
      <div class="header-left">
        <i class="pi pi-filter"></i>
        <h3>Advanced Filters</h3>
        <span v-if="activeFiltersCount > 0" class="filter-badge">{{ activeFiltersCount }}</span>
      </div>
      <i class="pi" :class="isExpanded ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
    </div>

    <transition name="slide-down">
      <div v-if="isExpanded" class="filter-body">
        <!-- Plant Multi-Select -->
        <div class="filter-section">
          <label class="filter-label">
            <i class="pi pi-building"></i>
            Power Plants
          </label>
          <div class="multi-select-container">
            <div class="select-all-option">
              <label class="checkbox-label">
                <input 
                  type="checkbox" 
                  :checked="allPlantsSelected"
                  @change="toggleAllPlants"
                />
                <span>Select All</span>
              </label>
            </div>
            <div class="options-grid">
              <label 
                v-for="plant in plants" 
                :key="plant.code"
                class="checkbox-label"
              >
                <input 
                  type="checkbox" 
                  :value="plant.code" 
                  v-model="localFilters.plantCodes"
                />
                <span>{{ plant.name }} ({{ plant.code }})</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Date Range -->
        <div class="filter-section">
          <label class="filter-label">
            <i class="pi pi-calendar"></i>
            Date Range
          </label>
          <div class="date-range-inputs">
            <div class="date-input-group">
              <label>From</label>
              <input 
                type="date" 
                v-model="localFilters.startDate"
                class="date-input"
              />
            </div>
            <div class="date-input-group">
              <label>To</label>
              <input 
                type="date" 
                v-model="localFilters.endDate"
                class="date-input"
              />
            </div>
          </div>
          <div class="quick-date-buttons">
            <button @click="setDateRange('today')" class="quick-btn">Today</button>
            <button @click="setDateRange('week')" class="quick-btn">This Week</button>
            <button @click="setDateRange('month')" class="quick-btn">This Month</button>
            <button @click="setDateRange('year')" class="quick-btn">This Year</button>
          </div>
        </div>

        <!-- Numeric Range Filters (for generation, capacity factor, etc.) -->
        <div v-if="showNumericFilters" class="filter-section">
          <label class="filter-label">
            <i class="pi pi-sliders-h"></i>
            Generation Range (kWh)
          </label>
          <div class="range-inputs">
            <input 
              type="number" 
              v-model.number="localFilters.minGeneration"
              placeholder="Min"
              class="range-input"
            />
            <span class="range-separator">to</span>
            <input 
              type="number" 
              v-model.number="localFilters.maxGeneration"
              placeholder="Max"
              class="range-input"
            />
          </div>
        </div>

        <div v-if="showNumericFilters" class="filter-section">
          <label class="filter-label">
            <i class="pi pi-percentage"></i>
            Capacity Factor Range (%)
          </label>
          <div class="range-inputs">
            <input 
              type="number" 
              v-model.number="localFilters.minCapacityFactor"
              placeholder="Min"
              min="0"
              max="100"
              class="range-input"
            />
            <span class="range-separator">to</span>
            <input 
              type="number" 
              v-model.number="localFilters.maxCapacityFactor"
              placeholder="Max"
              min="0"
              max="100"
              class="range-input"
            />
          </div>
        </div>

        <!-- Filter Presets -->
        <div class="filter-section">
          <label class="filter-label">
            <i class="pi pi-bookmark"></i>
            Saved Filters
          </label>
          <div class="presets-container">
            <div class="preset-buttons">
              <button 
                v-for="preset in savedPresets" 
                :key="preset.name"
                @click="loadPreset(preset)"
                class="preset-btn"
              >
                <i class="pi pi-bookmark-fill"></i>
                {{ preset.name }}
              </button>
              <button @click="showSavePresetDialog = true" class="preset-btn add-preset">
                <i class="pi pi-plus"></i>
                Save Current
              </button>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="filter-actions">
          <button @click="clearFilters" class="btn-clear">
            <i class="pi pi-times"></i>
            Clear All
          </button>
          <button @click="applyFilters" class="btn-apply">
            <i class="pi pi-check"></i>
            Apply Filters
          </button>
        </div>
      </div>
    </transition>

    <!-- Save Preset Dialog -->
    <div v-if="showSavePresetDialog" class="modal-overlay" @click="showSavePresetDialog = false">
      <div class="modal-content" @click.stop>
        <h3>Save Filter Preset</h3>
        <input 
          v-model="newPresetName" 
          type="text" 
          placeholder="Enter preset name"
          class="preset-name-input"
          @keyup.enter="savePreset"
        />
        <div class="modal-actions">
          <button @click="showSavePresetDialog = false" class="btn-cancel">Cancel</button>
          <button @click="savePreset" class="btn-save">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdvancedFilter',
  props: {
    plants: {
      type: Array,
      default: () => []
    },
    showNumericFilters: {
      type: Boolean,
      default: true
    },
    initialFilters: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      isExpanded: false,
      localFilters: {
        plantCodes: [],
        startDate: '',
        endDate: '',
        minGeneration: null,
        maxGeneration: null,
        minCapacityFactor: null,
        maxCapacityFactor: null
      },
      savedPresets: [],
      showSavePresetDialog: false,
      newPresetName: ''
    };
  },
  computed: {
    allPlantsSelected() {
      return this.plants.length > 0 && this.localFilters.plantCodes.length === this.plants.length;
    },
    activeFiltersCount() {
      let count = 0;
      if (this.localFilters.plantCodes.length > 0) count++;
      if (this.localFilters.startDate) count++;
      if (this.localFilters.endDate) count++;
      if (this.localFilters.minGeneration !== null) count++;
      if (this.localFilters.maxGeneration !== null) count++;
      if (this.localFilters.minCapacityFactor !== null) count++;
      if (this.localFilters.maxCapacityFactor !== null) count++;
      return count;
    }
  },
  mounted() {
    this.loadSavedPresets();
    if (this.initialFilters) {
      this.localFilters = { ...this.localFilters, ...this.initialFilters };
    }
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
    toggleAllPlants() {
      if (this.allPlantsSelected) {
        this.localFilters.plantCodes = [];
      } else {
        this.localFilters.plantCodes = this.plants.map(p => p.code);
      }
    },
    setDateRange(range) {
      const today = new Date();
      const year = today.getFullYear();
      const month = today.getMonth();
      const date = today.getDate();
      
      switch(range) {
        case 'today':
          this.localFilters.startDate = this.formatDate(today);
          this.localFilters.endDate = this.formatDate(today);
          break;
        case 'week':
          const weekStart = new Date(year, month, date - today.getDay());
          this.localFilters.startDate = this.formatDate(weekStart);
          this.localFilters.endDate = this.formatDate(today);
          break;
        case 'month':
          const monthStart = new Date(year, month, 1);
          this.localFilters.startDate = this.formatDate(monthStart);
          this.localFilters.endDate = this.formatDate(today);
          break;
        case 'year':
          const yearStart = new Date(year, 0, 1);
          this.localFilters.startDate = this.formatDate(yearStart);
          this.localFilters.endDate = this.formatDate(today);
          break;
      }
    },
    formatDate(date) {
      return date.toISOString().split('T')[0];
    },
    clearFilters() {
      this.localFilters = {
        plantCodes: [],
        startDate: '',
        endDate: '',
        minGeneration: null,
        maxGeneration: null,
        minCapacityFactor: null,
        maxCapacityFactor: null
      };
      this.applyFilters();
    },
    applyFilters() {
      this.$emit('filter-change', { ...this.localFilters });
    },
    loadSavedPresets() {
      const saved = localStorage.getItem('filterPresets');
      if (saved) {
        this.savedPresets = JSON.parse(saved);
      }
    },
    savePreset() {
      if (!this.newPresetName.trim()) {
        alert('Please enter a preset name');
        return;
      }
      
      const preset = {
        name: this.newPresetName,
        filters: { ...this.localFilters }
      };
      
      this.savedPresets.push(preset);
      localStorage.setItem('filterPresets', JSON.stringify(this.savedPresets));
      
      this.newPresetName = '';
      this.showSavePresetDialog = false;
      alert('Filter preset saved!');
    },
    loadPreset(preset) {
      this.localFilters = { ...preset.filters };
      this.applyFilters();
    }
  }
};
</script>

<style scoped>
.advanced-filter-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
}

.advanced-filter-panel.expanded {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
}

.filter-header:hover {
  background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-left i {
  font-size: 1.25rem;
}

.header-left h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.filter-badge {
  background: rgba(255, 255, 255, 0.3);
  padding: 0.25rem 0.625rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.filter-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #334155;
  font-size: 0.9375rem;
}

.filter-label i {
  color: #667eea;
}

.multi-select-container {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
}

.select-all-option {
  padding-bottom: 0.75rem;
  margin-bottom: 0.75rem;
  border-bottom: 2px solid #e2e8f0;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.625rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.checkbox-label:hover {
  background: #e2e8f0;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label span {
  font-size: 0.9375rem;
  color: #475569;
}

.date-range-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.date-input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.date-input-group label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.date-input {
  padding: 0.625rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.date-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.quick-date-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.quick-btn {
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.range-input {
  flex: 1;
  padding: 0.625rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9375rem;
}

.range-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.range-separator {
  color: #94a3b8;
  font-weight: 500;
}

.presets-container {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
}

.preset-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.preset-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.preset-btn.add-preset {
  background: #00a651;
  color: white;
  border-color: #00a651;
}

.preset-btn.add-preset:hover {
  background: #008a42;
}

.filter-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding-top: 0.5rem;
  border-top: 1px solid #e2e8f0;
}

.btn-clear,
.btn-apply {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-clear {
  background: #f1f5f9;
  color: #475569;
}

.btn-clear:hover {
  background: #e2e8f0;
}

.btn-apply {
  background: #667eea;
  color: white;
}

.btn-apply:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Modal Styles */
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
  z-index: 9999;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  min-width: 400px;
}

.modal-content h3 {
  margin: 0 0 1.5rem 0;
  color: #1e293b;
}

.preset-name-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.preset-name-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn-cancel,
.btn-save {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel {
  background: #f1f5f9;
  color: #475569;
}

.btn-cancel:hover {
  background: #e2e8f0;
}

.btn-save {
  background: #667eea;
  color: white;
}

.btn-save:hover {
  background: #5568d3;
}

/* Slide Down Animation */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  max-height: 0;
}

.slide-down-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
