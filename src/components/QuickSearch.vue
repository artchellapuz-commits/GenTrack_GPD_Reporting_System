<template>
  <div class="quick-search">
    <button @click="toggleSearch" class="search-trigger" title="Search (Ctrl+K)">
      <i class="pi pi-search"></i>
    </button>

    <transition name="modal">
      <div v-if="isOpen" class="search-modal-overlay" @click="closeSearch">
        <div class="search-modal" @click.stop>
          <div class="search-header">
            <i class="pi pi-search search-icon"></i>
            <input
              ref="searchInput"
              v-model="query"
              type="text"
              placeholder="Search plants, reports, data..."
              class="search-input"
              @input="handleSearch"
              @keydown.esc="closeSearch"
              @keydown.down.prevent="navigateDown"
              @keydown.up.prevent="navigateUp"
              @keydown.enter="selectResult"
            />
            <button @click="closeSearch" class="search-close">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <div v-if="query" class="search-results">
            <div v-if="loading" class="search-loading">
              <i class="pi pi-spin pi-spinner"></i>
              <p>Searching...</p>
            </div>

            <div v-else-if="results.length === 0" class="search-empty">
              <i class="pi pi-search"></i>
              <p>No results found for "{{ query }}"</p>
            </div>

            <div v-else class="search-results-list">
              <div
                v-for="(result, index) in results"
                :key="result.id"
                :class="['search-result-item', { active: index === selectedIndex }]"
                @click="goToResult(result)"
                @mouseenter="selectedIndex = index"
              >
                <div class="result-icon">
                  <i :class="getResultIcon(result.type)"></i>
                </div>
                <div class="result-content">
                  <div class="result-title">{{ result.title }}</div>
                  <div class="result-subtitle">{{ result.subtitle }}</div>
                </div>
                <div class="result-type">{{ result.type }}</div>
              </div>
            </div>
          </div>

          <div v-else class="search-suggestions">
            <div class="suggestion-section">
              <h4>Quick Actions</h4>
              <div class="suggestion-item" @click="goTo('/dashboard')">
                <i class="pi pi-home"></i>
                <span>Go to Dashboard</span>
              </div>
              <div class="suggestion-item" @click="goTo('/upload')">
                <i class="pi pi-upload"></i>
                <span>Upload Report</span>
              </div>
              <div class="suggestion-item" @click="goTo('/reports')">
                <i class="pi pi-file"></i>
                <span>View Reports</span>
              </div>
              <div class="suggestion-item" @click="goTo('/generate')">
                <i class="pi pi-chart-bar"></i>
                <span>Generate Report</span>
              </div>
            </div>
          </div>

          <div class="search-footer">
            <div class="search-hint">
              <kbd>↑</kbd><kbd>↓</kbd> Navigate
              <kbd>↵</kbd> Select
              <kbd>ESC</kbd> Close
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'QuickSearch',
  data() {
    return {
      isOpen: false,
      query: '',
      results: [],
      selectedIndex: 0,
      loading: false,
      searchTimeout: null
    };
  },
  mounted() {
    // Keyboard shortcut: Ctrl+K or Cmd+K
    document.addEventListener('keydown', this.handleKeyboard);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleKeyboard);
  },
  methods: {
    handleKeyboard(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.toggleSearch();
      }
    },
    
    toggleSearch() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        this.$nextTick(() => {
          this.$refs.searchInput?.focus();
        });
      } else {
        this.query = '';
        this.results = [];
        this.selectedIndex = 0;
      }
    },
    
    closeSearch() {
      this.isOpen = false;
      this.query = '';
      this.results = [];
      this.selectedIndex = 0;
    },
    
    handleSearch() {
      clearTimeout(this.searchTimeout);
      
      if (!this.query.trim()) {
        this.results = [];
        return;
      }
      
      this.loading = true;
      
      this.searchTimeout = setTimeout(() => {
        this.performSearch();
      }, 300);
    },
    
    performSearch() {
      // Mock search - replace with actual API call
      const mockData = [
        { id: 1, type: 'Plant', title: 'Agus 1 Hydroelectric Power Plant', subtitle: 'Lanao del Sur • 50 MW' },
        { id: 2, type: 'Plant', title: 'Agus 2 Hydroelectric Power Plant', subtitle: 'Lanao del Sur • 180 MW' },
        { id: 3, type: 'Plant', title: 'Pulangi 4 Hydroelectric Power Plant', subtitle: 'Bukidnon • 255 MW' },
        { id: 4, type: 'Report', title: 'Daily Report - January 2026', subtitle: 'All Plants • 31 days' },
        { id: 5, type: 'Report', title: 'Monthly Summary - December 2025', subtitle: 'All Plants' },
        { id: 6, type: 'Page', title: 'Dashboard', subtitle: 'View system overview' },
        { id: 7, type: 'Page', title: 'Upload Excel', subtitle: 'Import new data' },
      ];
      
      const query = this.query.toLowerCase();
      this.results = mockData.filter(item =>
        item.title.toLowerCase().includes(query) ||
        item.subtitle.toLowerCase().includes(query)
      );
      
      this.loading = false;
      this.selectedIndex = 0;
    },
    
    navigateDown() {
      if (this.selectedIndex < this.results.length - 1) {
        this.selectedIndex++;
      }
    },
    
    navigateUp() {
      if (this.selectedIndex > 0) {
        this.selectedIndex--;
      }
    },
    
    selectResult() {
      if (this.results[this.selectedIndex]) {
        this.goToResult(this.results[this.selectedIndex]);
      }
    },
    
    goToResult(result) {
      console.log('Navigate to:', result);
      // Implement navigation based on result type
      if (result.type === 'Page') {
        this.goTo(result.subtitle.includes('Dashboard') ? '/dashboard' : '/upload');
      }
      this.closeSearch();
    },
    
    goTo(path) {
      this.$router.push(path);
      this.closeSearch();
    },
    
    getResultIcon(type) {
      const icons = {
        Plant: 'pi pi-bolt',
        Report: 'pi pi-file',
        Page: 'pi pi-window-maximize'
      };
      return icons[type] || 'pi pi-search';
    }
  }
};
</script>

<style scoped>
.quick-search {
  position: relative;
}

.search-trigger {
  width: 44px;
  height: 44px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  color: #64748b;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 1.125rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.search-trigger:hover {
  background: white;
  color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.search-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 100px;
}

.search-modal {
  width: 90%;
  max-width: 600px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.search-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.search-icon {
  color: #64748b;
  font-size: 1.25rem;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.125rem;
  color: #1e293b;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-close {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.search-close:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.search-results {
  max-height: 400px;
  overflow-y: auto;
}

.search-loading,
.search-empty {
  padding: 60px 20px;
  text-align: center;
  color: #64748b;
}

.search-loading i,
.search-empty i {
  font-size: 3rem;
  margin-bottom: 16px;
  display: block;
}

.search-results-list {
  padding: 8px;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.search-result-item:hover,
.search-result-item.active {
  background: #f8fafc;
}

.result-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #eff6ff;
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.result-subtitle {
  font-size: 0.8125rem;
  color: #64748b;
}

.result-type {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.search-suggestions {
  padding: 20px;
}

.suggestion-section h4 {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #64748b;
  font-weight: 600;
  margin: 0 0 12px 0;
  letter-spacing: 0.5px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #475569;
}

.suggestion-item:hover {
  background: #f8fafc;
  color: #3b82f6;
}

.suggestion-item i {
  font-size: 1rem;
}

.search-footer {
  padding: 12px 20px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.search-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.75rem;
  color: #64748b;
}

kbd {
  padding: 2px 6px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  font-size: 0.6875rem;
  font-family: monospace;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Dark Mode */
.dark-mode .search-modal {
  background: #1e293b;
}

.dark-mode .search-header {
  border-bottom-color: #334155;
}

.dark-mode .search-input {
  color: #e2e8f0;
}

.dark-mode .search-result-item:hover,
.dark-mode .search-result-item.active {
  background: #334155;
}

.dark-mode .result-title {
  color: #e2e8f0;
}

.dark-mode .search-footer {
  background: #0f172a;
  border-top-color: #334155;
}

/* Mobile */
@media (max-width: 768px) {
  .search-modal-overlay {
    padding-top: 60px;
  }

  .search-modal {
    width: 95%;
  }

  .search-header {
    padding: 16px;
  }

  .search-input {
    font-size: 1rem;
  }
}
</style>
