<template>
  <div class="layout-wrapper" :class="{ 'layout-static-inactive': !sidebarActive }">
    <!-- Sidebar -->
    <div class="layout-sidebar">
      <div class="sidebar-header">
        <router-link to="/dashboard" class="logo">
          <img src="@/assets/NPC-logo.png" alt="NPC Logo" class="logo-image" />
          <span class="logo-text">NPC System</span>
        </router-link>
      </div>

      <div class="layout-menu-container">
        <ul class="layout-menu">
          <li class="menu-item">
            <router-link to="/dashboard" class="menu-link">
              <i class="pi pi-home"></i>
              <span>Dashboard</span>
            </router-link>
          </li>
          <li class="menu-item">
            <router-link to="/upload" class="menu-link">
              <i class="pi pi-upload"></i>
              <span>Upload Excel</span>
            </router-link>
          </li>
          <li class="menu-item">
            <router-link to="/view" class="menu-link">
              <i class="pi pi-chart-bar"></i>
              <span>View Reports</span>
            </router-link>
          </li>
          <li class="menu-item">
            <router-link to="/generate" class="menu-link">
              <i class="pi pi-download"></i>
              <span>Generate Report</span>
            </router-link>
          </li>
          <li class="menu-item">
            <router-link to="/water-nomination" class="menu-link">
              <i class="pi pi-calendar"></i>
              <span>Water Nomination</span>
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="layout-main-container">
      <!-- Top Bar -->
      <div class="layout-topbar">
        <button class="menu-button" @click="toggleSidebar">
          <i class="pi pi-bars"></i>
        </button>

        <div class="topbar-left">
          <span class="page-title">{{ pageTitle }}</span>
        </div>

        <div class="topbar-right">
          <!-- Quick Search -->
          <QuickSearch />
          
          <!-- Light/Dark Mode Toggle -->
          <button class="topbar-icon-btn" @click="toggleDarkMode" :title="isDarkMode ? 'Light Mode' : 'Dark Mode'">
            <i :class="isDarkMode ? 'pi pi-sun' : 'pi pi-moon'"></i>
          </button>
          
          <!-- Theme Customizer -->
          <button class="topbar-icon-btn theme-btn" @click="toggleThemeCustomizer" title="Theme Customizer">
            <i class="pi pi-palette"></i>
          </button>

          <!-- Admin Profile -->
          <button class="topbar-item" @click="toggleProfileMenu">
            <i class="pi pi-user"></i>
            <span class="username">{{ username }}</span>
            <i class="pi pi-angle-down"></i>
          </button>

          <div v-if="profileMenuActive" class="profile-menu">
            <ul>
              <li>
                <a href="#" @click.prevent="handleLogout" class="profile-menu-item">
                  <i class="pi pi-sign-out"></i>
                  <span>Logout</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Page Content -->
      <div class="layout-main">
        <slot></slot>
      </div>
    </div>

    <!-- Sidebar Overlay for Mobile -->
    <div v-if="sidebarActive" class="layout-mask" @click="toggleSidebar"></div>

    <!-- Theme Customizer - Always rendered to prevent ref errors -->
    <ThemeCustomizer 
      v-if="isComponentMounted"
      ref="themeCustomizer" 
      @menu-mode-changed="handleMenuModeChange"
      @dark-mode-changed="handleDarkModeChange"
    />
  </div>
</template>

<script>
import { logout, getUsername } from '../utils/auth';
import ThemeCustomizer from './ThemeCustomizer.vue';
import QuickSearch from './QuickSearch.vue';

export default {
  name: 'AppLayout',
  components: {
    ThemeCustomizer,
    QuickSearch
  },
  data() {
    return {
      sidebarActive: true,
      profileMenuActive: false,
      username: '',
      isDarkMode: false,
      isThemeCustomizerOpen: false,
      isComponentMounted: false
    };
  },
  created() {
    // Load dark mode state from localStorage
    const savedDarkMode = localStorage.getItem('dark-mode');
    if (savedDarkMode === 'true') {
      this.isDarkMode = true;
    }
  },
  computed: {
    pageTitle() {
      const route = this.$route.path;
      const titles = {
        '/dashboard': 'Dashboard',
        '/upload': 'Upload Excel',
        '/view': 'View Reports',
        '/generate': 'Generate Report',
        '/water-nomination': 'Water Nomination'
      };
      return titles[route] || 'NPC Reporting System';
    }
  },
  mounted() {
    this.username = getUsername() || 'User';
    this.checkScreenSize();
    window.addEventListener('resize', this.checkScreenSize);
    document.addEventListener('click', this.handleClickOutside);
    
    // Ensure component is fully mounted before rendering ThemeCustomizer
    this.$nextTick(() => {
      this.isComponentMounted = true;
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkScreenSize);
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    toggleSidebar() {
      this.sidebarActive = !this.sidebarActive;
    },
    toggleProfileMenu() {
      this.profileMenuActive = !this.profileMenuActive;
    },
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
      
      // Sync with ThemeCustomizer using nextTick
      this.$nextTick(() => {
        if (this.$refs.themeCustomizer) {
          this.$refs.themeCustomizer.isDarkMode = this.isDarkMode;
        }
      });
    },
    toggleThemeCustomizer() {
      this.isThemeCustomizerOpen = !this.isThemeCustomizerOpen;
      // Use nextTick to ensure ref is available
      this.$nextTick(() => {
        if (this.$refs.themeCustomizer) {
          this.$refs.themeCustomizer.toggleCustomizer();
        }
      });
    },
    handleClickOutside(event) {
      const profileButton = event.target.closest('.topbar-item');
      const profileMenu = event.target.closest('.profile-menu');
      
      if (!profileButton && !profileMenu && this.profileMenuActive) {
        this.profileMenuActive = false;
      }
    },
    checkScreenSize() {
      if (window.innerWidth < 992) {
        this.sidebarActive = false;
      } else {
        this.sidebarActive = true;
      }
    },
    handleMenuModeChange(mode) {
      console.log('Menu mode changed to:', mode);
    },
    handleDarkModeChange(isDark) {
      this.isDarkMode = isDark;
    },
    async handleLogout() {
      sessionStorage.setItem('justLoggedOut', 'true');
      await logout();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* Layout Wrapper */
.layout-wrapper {
  min-height: 100vh;
  display: flex;
}

/* Sidebar */
.layout-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 250px;
  background: #1e293b;
  z-index: 999;
  transition: transform 0.3s;
  overflow-y: auto;
}

.layout-static-inactive .layout-sidebar {
  transform: translateX(-100%);
}

.sidebar-header {
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: white;
}

.logo-image {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.layout-menu-container {
  padding: 1rem 0;
}

.layout-menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu-item {
  margin: 0;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  color: rgba(255, 255, 255, 0.87);
  text-decoration: none;
  transition: all 0.2s;
  font-size: 0.9375rem;
  border-left: 3px solid transparent;
}

.menu-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.menu-link.router-link-active {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
  border-left-color: #60a5fa;
}

.menu-link i {
  font-size: 1.125rem;
  width: 20px;
}

/* Main Container */
.layout-main-container {
  flex: 1;
  margin-left: 250px;
  transition: margin-left 0.3s;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout-static-inactive .layout-main-container {
  margin-left: 0;
}

/* Top Bar */
.layout-topbar {
  height: 70px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 998;
  gap: 1rem;
}

.menu-button {
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.menu-button:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.menu-button i {
  font-size: 1.25rem;
}

.topbar-left {
  flex: 1;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.topbar-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.topbar-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.username {
  font-weight: 500;
}

.topbar-icon-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 1.125rem;
}

.topbar-icon-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.topbar-icon-btn.theme-btn {
  background: #f59e0b;
  color: white;
}

.topbar-icon-btn.theme-btn:hover {
  background: #d97706;
}

.profile-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  min-width: 200px;
  z-index: 1000;
}

.profile-menu ul {
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
}

.profile-menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.profile-menu-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.profile-menu-item i {
  font-size: 1rem;
  width: 20px;
}

/* Main Content */
.layout-main {
  flex: 1;
  padding: 2rem;
  background: #f8fafc;
}

/* Mobile Overlay */
.layout-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 998;
  display: none;
}

/* Responsive */
@media (max-width: 991px) {
  .layout-sidebar {
    transform: translateX(-100%);
  }

  .layout-wrapper:not(.layout-static-inactive) .layout-sidebar {
    transform: translateX(0);
  }

  .layout-main-container {
    margin-left: 0;
  }

  .layout-wrapper:not(.layout-static-inactive) .layout-mask {
    display: block;
  }
}

@media (max-width: 576px) {
  .layout-topbar {
    padding: 0 1rem;
  }

  .page-title {
    font-size: 1rem;
  }

  .username {
    display: none;
  }

  .layout-main {
    padding: 1rem;
  }
}
</style>
