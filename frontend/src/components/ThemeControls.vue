<template>
  <div class="theme-controls">
    <!-- Theme Customizer -->
    <button class="theme-control-btn theme-palette-btn" @click="toggleCustomizer" title="Theme Customizer">
      <i class="pi pi-palette"></i>
    </button>
    
    <!-- Light/Dark Mode Toggle -->
    <button class="theme-control-btn" @click="toggleDarkMode" :title="isDarkMode ? 'Light Mode' : 'Dark Mode'">
      <i :class="isDarkMode ? 'pi pi-sun' : 'pi pi-moon'"></i>
    </button>

    <!-- Theme Customizer Panel -->
    <ThemeCustomizer 
      ref="themeCustomizer" 
      @dark-mode-changed="handleDarkModeChange"
    />
  </div>
</template>

<script>
import ThemeCustomizer from './ThemeCustomizer.vue';

export default {
  name: 'ThemeControls',
  components: {
    ThemeCustomizer
  },
  data() {
    return {
      isDarkMode: false
    };
  },
  created() {
    // Load dark mode state from localStorage
    const savedDarkMode = localStorage.getItem('dark-mode');
    if (savedDarkMode === 'true') {
      this.isDarkMode = true;
      document.body.classList.add('dark-mode');
      document.documentElement.classList.add('dark-mode');
    }
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('dark-mode', this.isDarkMode);
      
      // Apply dark mode to body
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
        document.documentElement.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
        document.documentElement.classList.remove('dark-mode');
      }
      
      // Sync with ThemeCustomizer
      if (this.$refs.themeCustomizer) {
        this.$refs.themeCustomizer.isDarkMode = this.isDarkMode;
      }
    },
    toggleCustomizer() {
      this.$refs.themeCustomizer?.toggleCustomizer();
    },
    handleDarkModeChange(isDark) {
      this.isDarkMode = isDark;
    }
  }
};
</script>

<style scoped>
.theme-controls {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  z-index: 9998;
}

.theme-control-btn {
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
  backdrop-filter: blur(10px);
}

.theme-control-btn:hover {
  background: white;
  color: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.theme-palette-btn {
  background: var(--primary-color) !important;
  color: white !important;
}

.theme-palette-btn:hover {
  background: var(--primary-hover) !important;
  color: white !important;
}

/* Dark mode styles */
.dark-mode .theme-control-btn {
  background: rgba(30, 41, 59, 0.9);
  color: #e2e8f0;
}

.dark-mode .theme-control-btn:hover {
  background: #334155;
  color: #f1f5f9;
}

/* Responsive */
@media (max-width: 576px) {
  .theme-controls {
    top: 10px;
    right: 10px;
  }

  .theme-control-btn {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>
