<template>
  <div class="theme-customizer">
    <!-- Customizer Panel -->
    <div class="customizer-panel" v-if="isOpen">
      <div class="customizer-header">
        <h3>Theme Customizer</h3>
        <button class="close-btn" @click="toggleCustomizer">
          <i class="pi pi-times"></i>
        </button>
      </div>

      <div class="customizer-content">
        <!-- Primary Colors -->
        <div class="customizer-section">
          <h4>Primary</h4>
          <div class="color-grid">
            <button
              v-for="color in primaryColors"
              :key="color.name"
              class="color-option"
              :style="{ backgroundColor: color.value }"
              :class="{ active: selectedPrimary === color.value }"
              @click="changePrimaryColor(color.value)"
            ></button>
          </div>
        </div>

        <!-- Surface Colors -->
        <div class="customizer-section">
          <h4>Surface</h4>
          <div class="color-grid">
            <button
              v-for="color in surfaceColors"
              :key="color.name"
              class="color-option"
              :style="{ backgroundColor: color.value }"
              :class="{ active: selectedSurface === color.value }"
              @click="changeSurfaceColor(color.value)"
            ></button>
          </div>
        </div>

        <!-- Presets -->
        <div class="customizer-section">
          <h4>Presets</h4>
          <div class="preset-buttons">
            <button
              v-for="preset in presets"
              :key="preset"
              class="preset-btn"
              :class="{ active: selectedPreset === preset }"
              @click="changePreset(preset)"
            >
              {{ preset }}
            </button>
          </div>
        </div>

        <!-- Menu Mode -->
        <div class="customizer-section">
          <h4>Menu Mode</h4>
          <div class="preset-buttons">
            <button
              v-for="mode in menuModes"
              :key="mode"
              class="preset-btn"
              :class="{ active: selectedMenuMode === mode }"
              @click="changeMenuMode(mode)"
            >
              {{ mode }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay -->
    <div class="customizer-overlay" v-if="isOpen" @click="toggleCustomizer"></div>
  </div>
</template>

<script>
export default {
  name: 'ThemeCustomizer',
  data() {
    return {
      isOpen: false,
      isDarkMode: false,
      selectedPrimary: '#3b82f6',
      selectedSurface: '#1e293b',
      selectedPreset: 'Lara',
      selectedMenuMode: 'Static',
      primaryColors: [
        { name: 'slate', value: '#334155' },
        { name: 'emerald', value: '#10b981' },
        { name: 'green', value: '#22c55e' },
        { name: 'lime', value: '#84cc16' },
        { name: 'orange', value: '#f97316' },
        { name: 'amber', value: '#f59e0b' },
        { name: 'yellow', value: '#eab308' },
        { name: 'teal', value: '#14b8a6' },
        { name: 'cyan', value: '#06b6d4' },
        { name: 'sky', value: '#0ea5e9' },
        { name: 'blue', value: '#3b82f6' },
        { name: 'indigo', value: '#6366f1' },
        { name: 'violet', value: '#8b5cf6' },
        { name: 'purple', value: '#a855f7' },
        { name: 'fuchsia', value: '#d946ef' },
        { name: 'pink', value: '#ec4899' },
        { name: 'rose', value: '#f43f5e' }
      ],
      surfaceColors: [
        { name: 'slate-900', value: '#0f172a' },
        { name: 'slate-800', value: '#1e293b' },
        { name: 'slate-700', value: '#334155' },
        { name: 'slate-600', value: '#475569' },
        { name: 'zinc-700', value: '#3f3f46' },
        { name: 'gray-700', value: '#374151' },
        { name: 'neutral-700', value: '#404040' },
        { name: 'stone-700', value: '#44403c' }
      ],
      presets: ['Aura', 'Lara', 'Nora'],
      menuModes: ['Static', 'Overlay']
    };
  },
  methods: {
    toggleCustomizer() {
      this.isOpen = !this.isOpen;
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('dark-mode', this.isDarkMode);
      
      // Apply dark mode styles
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
        document.documentElement.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
        document.documentElement.classList.remove('dark-mode');
      }
      
      // Emit event to parent
      this.$emit('dark-mode-changed', this.isDarkMode);
    },
    changePrimaryColor(color) {
      this.selectedPrimary = color;
      document.documentElement.style.setProperty('--primary-color', color);
      
      // Calculate darker shade for hover
      const hoverColor = this.darkenColor(color, 15);
      document.documentElement.style.setProperty('--primary-hover', hoverColor);
      
      // Convert hex to RGB for box-shadow
      const rgb = this.hexToRgb(color);
      document.documentElement.style.setProperty('--primary-color-rgb', `${rgb.r}, ${rgb.g}, ${rgb.b}`);
      
      // Update Sakai primary variable
      document.documentElement.style.setProperty('--sakai-primary', color);
      document.documentElement.style.setProperty('--sakai-primary-dark', hoverColor);
      
      localStorage.setItem('theme-primary', color);
      
      // Force re-render by toggling a class
      document.body.classList.add('theme-updating');
      setTimeout(() => document.body.classList.remove('theme-updating'), 10);
    },
    changeSurfaceColor(color) {
      this.selectedSurface = color;
      document.documentElement.style.setProperty('--surface-color', color);
      localStorage.setItem('theme-surface', color);
      
      // Force re-render
      document.body.classList.add('theme-updating');
      setTimeout(() => document.body.classList.remove('theme-updating'), 10);
    },
    darkenColor(color, percent) {
      // Convert hex to RGB
      const num = parseInt(color.replace('#', ''), 16);
      const r = Math.max(0, (num >> 16) - Math.round(255 * (percent / 100)));
      const g = Math.max(0, ((num >> 8) & 0x00FF) - Math.round(255 * (percent / 100)));
      const b = Math.max(0, (num & 0x0000FF) - Math.round(255 * (percent / 100)));
      return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
    },
    hexToRgb(hex) {
      const num = parseInt(hex.replace('#', ''), 16);
      return {
        r: (num >> 16) & 255,
        g: (num >> 8) & 255,
        b: num & 255
      };
    },
    changePreset(preset) {
      this.selectedPreset = preset;
      localStorage.setItem('theme-preset', preset);
      this.applyPreset(preset);
    },
    changeMenuMode(mode) {
      this.selectedMenuMode = mode;
      localStorage.setItem('menu-mode', mode);
      this.$emit('menu-mode-changed', mode);
    },
    applyPreset(preset) {
      const presetStyles = {
        'Aura': {
          borderRadius: '12px',
          fontFamily: 'Inter, system-ui, sans-serif'
        },
        'Lara': {
          borderRadius: '6px',
          fontFamily: 'system-ui, sans-serif'
        },
        'Nora': {
          borderRadius: '8px',
          fontFamily: 'Roboto, sans-serif'
        }
      };
      
      const styles = presetStyles[preset];
      if (styles) {
        document.documentElement.style.setProperty('--border-radius', styles.borderRadius);
        document.documentElement.style.setProperty('--font-family', styles.fontFamily);
      }
    },
    loadSavedTheme() {
      const savedPrimary = localStorage.getItem('theme-primary');
      const savedSurface = localStorage.getItem('theme-surface');
      const savedPreset = localStorage.getItem('theme-preset');
      const savedMenuMode = localStorage.getItem('menu-mode');
      const savedDarkMode = localStorage.getItem('dark-mode');

      if (savedPrimary) {
        this.selectedPrimary = savedPrimary;
        this.changePrimaryColor(savedPrimary);
      } else {
        // Set default primary color
        this.changePrimaryColor('#3b82f6');
      }
      
      if (savedSurface) {
        this.selectedSurface = savedSurface;
        this.changeSurfaceColor(savedSurface);
      } else {
        // Set default surface color
        this.changeSurfaceColor('#1e293b');
      }
      
      if (savedPreset) {
        this.selectedPreset = savedPreset;
        this.applyPreset(savedPreset);
      } else {
        // Set default preset
        this.applyPreset('Lara');
      }
      
      if (savedMenuMode && ['Static', 'Overlay'].includes(savedMenuMode)) {
        this.selectedMenuMode = savedMenuMode;
      }
      
      if (savedDarkMode === 'true') {
        this.isDarkMode = true;
        document.body.classList.add('dark-mode');
      }
    }
  },
  mounted() {
    this.loadSavedTheme();
  }
};
</script>

<style scoped>
.theme-customizer {
  position: fixed;
  z-index: 1000;
}

.customizer-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 320px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
  z-index: 10000;
  animation: slideIn 0.3s ease;
  overflow-y: auto;
  pointer-events: auto;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.customizer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.customizer-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  color: #64748b;
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #1e293b;
}

.customizer-content {
  padding: 20px;
}

.customizer-section {
  margin-bottom: 32px;
}

.customizer-section h4 {
  margin: 0 0 16px 0;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 8px;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  pointer-events: auto;
}

.color-option:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.color-option.active {
  border-color: #1e293b;
  box-shadow: 0 0 0 2px white, 0 0 0 4px #1e293b;
}

.preset-buttons {
  display: flex;
  gap: 12px;
}

.preset-btn {
  flex: 1;
  padding: 10px 16px;
  background: #f1f5f9;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  color: #475569;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  pointer-events: auto;
}

.preset-btn:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
}

.preset-btn.active {
  background: #fef3c7;
  border-color: #f59e0b;
  color: #92400e;
}

.customizer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  animation: fadeIn 0.3s ease;
  pointer-events: auto;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Scrollbar styling */
.customizer-panel::-webkit-scrollbar {
  width: 6px;
}

.customizer-panel::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.customizer-panel::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.customizer-panel::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
