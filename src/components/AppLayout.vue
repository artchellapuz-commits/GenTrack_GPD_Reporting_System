<template>
  <div class="layout-wrapper" :class="layoutClasses">
    <!-- PWA Install Prompt -->
    <PWAInstallPrompt />
    
    <!-- Sidebar -->
    <div class="layout-sidebar" :class="sidebarClasses">
      <div class="sidebar-header">
        <router-link to="/dashboard" class="logo">
          <!-- Animated SVG Logo for GenTrack -->
          <div class="gentrack-logo">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <!-- Background Hexagon -->
              <polygon points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5" fill="none" stroke="#3b82f6" stroke-width="6" class="logo-hex"/>
              
              <!-- Power Lightning Bolt -->
              <path d="M55,20 L35,55 L50,55 L45,80 L65,45 L50,45 Z" fill="#60a5fa" class="logo-bolt"/>
              
              <!-- Data Connection Nodes -->
              <circle cx="35" cy="55" r="4" fill="#fb923c" class="logo-node"/>
              <circle cx="50" cy="55" r="4" fill="#fb923c" class="logo-node"/>
              <circle cx="65" cy="45" r="4" fill="#fb923c" class="logo-node"/>
              <circle cx="50" cy="45" r="4" fill="#fb923c" class="logo-node"/>
            </svg>
          </div>
          <span class="logo-text">GenTrack</span>
        </router-link>
        <div class="user-role-badge" v-if="userRole">
          <span class="role-badge" :class="`role-${roleBadgeColor}`">{{ roleDisplay }}</span>
        </div>
      </div>

      <div class="layout-menu-container">
        <ul class="layout-menu">
          <li class="menu-item">
            <router-link to="/dashboard" class="menu-link">
              <i class="pi pi-home"></i>
              <span>Dashboard</span>
            </router-link>
          </li>
          <li class="menu-divider"></li>
          
          <!-- Upload - Only for Operator, Manager, Admin -->
          <li class="menu-item" v-if="canUpload">
            <router-link to="/upload" class="menu-link">
              <i class="pi pi-upload"></i>
              <span>Upload Excel</span>
            </router-link>
          </li>

          
          <li class="menu-item">
            <router-link to="/generate" class="menu-link">
              <i class="pi pi-download"></i>
              <span>Generate Report</span>
            </router-link>
          </li>
          
          
          <li class="menu-item">
            <router-link to="/view" class="menu-link">
              <i class="pi pi-chart-bar"></i>
              <span>View Reports</span>
            </router-link>
          </li>
          
          <!-- Report Storage - Generated reports archive -->
          <li class="menu-item">
            <router-link to="/report-storage" class="menu-link">
              <i class="pi pi-database"></i>
              <span>Report Storage</span>
            </router-link>
          </li>
          <!-- Request Signature Access -->
          <li class="menu-item">
            <router-link to="/signatory-authorization" class="menu-link">
              <i class="pi pi-user-edit"></i>
              <span>Request Signature Access</span>
            </router-link>
          </li>
          <!-- Archive - Show for everyone who can upload -->
          <li class="menu-item" v-if="canUpload">
            <router-link to="/archive" class="menu-link">
              <i class="pi pi-inbox"></i>
              <span>Archive</span>
            </router-link>
          </li>
          <!-- <li class="menu-divider"></li> -->
          
          <!-- Water Nomination with Dropdown - Only for Operator, Manager, Admin -->
          <!-- <li class="menu-item menu-item-dropdown disabled" v-if="canUpload">
            <a href="#" @click.prevent="toggleWaterNominationDropdown" class="menu-link">
              <i class="pi pi-calendar"></i>
              <span>Water Nomination</span>
              <i class="pi pi-chevron-down dropdown-icon" :class="{ rotated: waterNominationOpen }"></i>
            </a>
            <ul class="submenu" :class="{ open: waterNominationOpen }">
              <li class="submenu-item">
                <router-link to="/water-nomination" class="submenu-link">
                  <i class="pi pi-file-edit"></i>
                  <span>Manage Nominations</span>
                </router-link>
              </li>
              <li class="submenu-item" v-if="canApprove">
                <router-link to="/approval-queue" class="submenu-link">
                  <i class="pi pi-check-circle"></i>
                  <span>Approval Queue</span>
                </router-link>
              </li>
            </ul>
          </li> -->
          
          <!-- Analytics & Reports Section -->
          <li class="menu-divider"></li>
          <li class="menu-section-title">Analytics & Automation</li>
          <li class="menu-item">
            <router-link to="/analytics" class="menu-link">
              <i class="pi pi-chart-line"></i>
              <span>Advanced Analytics</span>
            </router-link>
          </li>
          <li class="menu-item" v-if="canApprove">
            <router-link to="/scheduled-reports" class="menu-link">
              <i class="pi pi-clock"></i>
              <span>Automated Reports</span>
            </router-link>
          </li>
          
          <!-- Admin Section - Only for Admin -->
          <template v-if="isAdminUser">
            <li class="menu-divider"></li>
            <li class="menu-section-title">Administration</li>
            
            <!-- User Management with Dropdown -->
            <li class="menu-item menu-item-dropdown">
              <a href="#" @click.prevent="toggleUserManagementDropdown" class="menu-link">
                <i class="pi pi-users"></i>
                <span>User Management</span>
                <i class="pi pi-chevron-down dropdown-icon" :class="{ rotated: userManagementOpen }"></i>
              </a>
              <ul class="submenu" :class="{ open: userManagementOpen }">
                <li class="submenu-item">
                  <router-link to="/user-management" class="submenu-link">
                    <i class="pi pi-user-edit"></i>
                    <span>Manage Users</span>
                  </router-link>
                </li>
                <li class="submenu-item">
                  <router-link to="/password-reset-requests" class="submenu-link">
                    <i class="pi pi-lock"></i>
                    <span>Reset Requests</span>
                  </router-link>
                </li>
              </ul>
            </li>
            
            <li class="menu-item">
              <a href="http://localhost:8000/admin" target="_blank" class="menu-link">
                <i class="pi pi-cog"></i>
                <span>Admin Panel</span>
              </a>
            </li>
            <li class="menu-item">
              <router-link to="/audit-logs" class="menu-link">
                <i class="pi pi-history"></i>
                <span>Audit Logs</span>
              </router-link>
            </li>
          </template>
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
          <!-- Live Date/Time Display -->
          <div class="topbar-datetime">
            <span class="current-date">{{ currentDate }}</span>
            <span class="current-time">{{ currentTime }}</span>
          </div>

          <!-- Quick Search -->
          <QuickSearch />
          
          <!-- Notification Icon (Admin only) -->
          <div v-if="isAdminUser" class="notification-wrapper">
            <button 
              class="topbar-icon-btn notification-btn" 
              @click="toggleNotificationMenu"
              :title="`${pendingResetCount} pending password reset request${pendingResetCount !== 1 ? 's' : ''}`"
            >
              <i class="pi pi-bell"></i>
              <span v-if="pendingResetCount > 0" class="notification-badge">{{ pendingResetCount }}</span>
            </button>

            <!-- Notification Dropdown -->
            <div v-if="notificationMenuActive" class="notification-menu">
              <div class="notification-header">
                <h3>Notifications</h3>
                <span class="notification-count">{{ pendingResetCount }} pending</span>
              </div>
              
              <div class="notification-body">
                <div v-if="recentRequests.length === 0" class="notification-empty">
                  <i class="pi pi-check-circle"></i>
                  <p>No pending requests</p>
                </div>
                
                <div v-else class="notification-list">
                  <div 
                    v-for="request in recentRequests" 
                    :key="request.id" 
                    class="notification-item"
                    @click="viewRequest(request)"
                  >
                    <div class="notification-icon">
                      <i class="pi pi-lock"></i>
                    </div>
                    <div class="notification-content">
                      <div class="notification-title">Password Reset Request</div>
                      <div class="notification-text">
                        <strong>{{ request.username }}</strong> requested password reset
                      </div>
                      <div class="notification-time">{{ formatTimeAgo(request.created_at) }}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="notification-footer">
                <a href="#" @click.prevent="viewAllRequests" class="view-all-link">
                  View All Requests
                  <i class="pi pi-arrow-right"></i>
                </a>
              </div>
            </div>
          </div>
          
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

    <!-- Sidebar Overlay for Mobile and Overlay Mode -->
    <div v-if="shouldShowMask" class="layout-mask" @click="toggleSidebar"></div>

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
import { 
  logout, 
  getUsername, 
  getUserRole, 
  getRoleDisplayName, 
  getRoleBadgeColor,
  canUploadData,
  canApproveData,
  isAdmin
} from '../utils/auth';
import ThemeCustomizer from './ThemeCustomizer.vue';
import QuickSearch from './QuickSearch.vue';
import PWAInstallPrompt from './PWAInstallPrompt.vue';

export default {
  name: 'AppLayout',
  components: {
    ThemeCustomizer,
    QuickSearch,
    PWAInstallPrompt
  },
  data() {
    return {
      sidebarActive: true,
      profileMenuActive: false,
      username: '',
      userRole: '',
      roleDisplay: '',
      roleBadgeColor: 'secondary',
      canUpload: false,
      canApprove: false,
      isAdminUser: false,
      isDarkMode: false,
      isThemeCustomizerOpen: false,
      isComponentMounted: false,
      waterNominationOpen: false,
      userManagementOpen: false,
      pendingResetCount: 0,
      notificationInterval: null,
      notificationMenuActive: false,
      recentRequests: [],
      currentDate: '',
      currentTime: '',
      timeInterval: null,
      menuMode: 'Static', // Add menu mode state
      isMobile: false // Track mobile state
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
        '/report-storage': 'Report Storage',
        '/signatory-authorization': 'Request Signature Access',
        '/water-nomination': 'Manage Nominations',
        '/approval-queue': 'Approval Queue',
        '/audit-logs': 'Audit Logs',
        '/user-management': 'User Management',
        '/password-reset-requests': 'Password Reset Requests',
        '/analytics': 'Advanced Analytics',
        '/scheduled-reports': 'Automated Reports'
      };
      return titles[route] || 'GPD System';
    },
    layoutClasses() {
      return {
        'layout-static': this.menuMode === 'Static',
        'layout-overlay': this.menuMode === 'Overlay',
        'layout-static-inactive': this.menuMode === 'Static' && !this.sidebarActive,
        'layout-overlay-active': this.menuMode === 'Overlay' && this.sidebarActive
      };
    },
    sidebarClasses() {
      return {
        'layout-sidebar-static': this.menuMode === 'Static',
        'layout-sidebar-overlay': this.menuMode === 'Overlay'
      };
    },
    shouldShowMask() {
      // Show mask when sidebar is active and either:
      // 1. In overlay mode (desktop or mobile)
      // 2. In static mode on mobile (< 992px)
      return this.sidebarActive && (
        this.menuMode === 'Overlay' || 
        (this.menuMode === 'Static' && this.isMobile)
      );
    }
  },
  mounted() {
    this.loadUserInfo();
    this.checkScreenSize();
    this.checkCurrentRoute();
    this.updateDateTime();
    this.loadMenuMode(); // Load saved menu mode
    window.addEventListener('resize', this.checkScreenSize);
    document.addEventListener('click', this.handleClickOutside);
    
    // Update time every second
    this.timeInterval = setInterval(() => {
      this.updateDateTime();
    }, 1000);
    
    // Load pending reset count if admin
    if (this.isAdminUser) {
      this.loadPendingResetCount();
      // Poll every 30 seconds for updates
      this.notificationInterval = setInterval(() => {
        this.loadPendingResetCount();
      }, 30000);
    }
    
    // Listen for password reset processed events
    window.addEventListener('password-reset-processed', this.handlePasswordResetProcessed);
    
    // Ensure component is fully mounted before rendering ThemeCustomizer
    this.$nextTick(() => {
      this.isComponentMounted = true;
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkScreenSize);
    document.removeEventListener('click', this.handleClickOutside);
    window.removeEventListener('password-reset-processed', this.handlePasswordResetProcessed);
    
    // Clear notification polling interval
    if (this.notificationInterval) {
      clearInterval(this.notificationInterval);
    }
    
    // Clear time interval
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  },
  watch: {
    '$route'(to) {
      this.checkCurrentRoute();
    }
  },
  methods: {
    updateDateTime() {
      const now = new Date();
      const optionsDate = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
      const optionsTime = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
      
      this.currentDate = now.toLocaleDateString('en-US', optionsDate);
      this.currentTime = now.toLocaleTimeString('en-US', optionsTime);
    },
    checkCurrentRoute() {
      // Auto-open dropdown if on water nomination or approval queue pages
      const currentPath = this.$route.path;
      if (currentPath === '/water-nomination' || currentPath === '/approval-queue') {
        this.waterNominationOpen = true;
      }
      // Auto-open user management dropdown if on related pages
      if (currentPath === '/user-management' || currentPath === '/password-reset-requests') {
        this.userManagementOpen = true;
      }
    },
    loadUserInfo() {
      this.username = getUsername() || 'User';
      this.userRole = getUserRole() || 'VIEWER';
      this.roleDisplay = getRoleDisplayName(this.userRole);
      this.roleBadgeColor = getRoleBadgeColor(this.userRole);
      this.canUpload = canUploadData();
      this.canApprove = canApproveData();
      this.isAdminUser = isAdmin();
    },
    toggleSidebar() {
      this.sidebarActive = !this.sidebarActive;
    },
    toggleWaterNominationDropdown() {
      this.waterNominationOpen = !this.waterNominationOpen;
    },
    toggleUserManagementDropdown() {
      this.userManagementOpen = !this.userManagementOpen;
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
      const notificationButton = event.target.closest('.notification-btn');
      const notificationMenu = event.target.closest('.notification-menu');
      
      if (!profileButton && !profileMenu && this.profileMenuActive) {
        this.profileMenuActive = false;
      }
      
      if (!notificationButton && !notificationMenu && this.notificationMenuActive) {
        this.notificationMenuActive = false;
      }
    },
    checkScreenSize() {
      const wasMobile = this.isMobile;
      this.isMobile = window.innerWidth < 992;
      
      if (this.isMobile) {
        this.sidebarActive = false;
      } else {
        this.sidebarActive = true;
      }
      
      // If switching from mobile to desktop in overlay mode, ensure sidebar is hidden
      if (!this.isMobile && wasMobile && this.menuMode === 'Overlay') {
        this.sidebarActive = false;
      }
    },
    handleMenuModeChange(mode) {
      console.log('Menu mode changed to:', mode);
      this.menuMode = mode;
      localStorage.setItem('menu-mode', mode);
      
      // Handle sidebar state based on mode and screen size
      if (mode === 'Overlay') {
        // In overlay mode, sidebar should be hidden by default
        this.sidebarActive = false;
      } else if (mode === 'Static') {
        // In static mode, show sidebar on desktop, hide on mobile
        this.sidebarActive = !this.isMobile;
      }
    },
    loadMenuMode() {
      const savedMode = localStorage.getItem('menu-mode');
      if (savedMode && ['Static', 'Overlay'].includes(savedMode)) {
        this.menuMode = savedMode;
      }
    },
    handleDarkModeChange(isDark) {
      this.isDarkMode = isDark;
    },
    async loadPendingResetCount() {
      try {
        const response = await api.getPendingResetCount();
        this.pendingResetCount = response.data.count || 0;
      } catch (error) {
        // Silently fail - this is a non-critical feature
        this.pendingResetCount = 0;
      }
    },
    async loadRecentRequests() {
      try {
        const response = await fetch('http://localhost:8000/api/password-reset-requests/?status=PENDING', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          // Get the 5 most recent requests
          this.recentRequests = (data.results || data).slice(0, 5);
        }
      } catch (error) {
        console.error('Failed to load recent requests:', error);
      }
    },
    toggleNotificationMenu() {
      this.notificationMenuActive = !this.notificationMenuActive;
      if (this.notificationMenuActive) {
        this.loadRecentRequests();
      }
    },
    viewRequest(request) {
      this.notificationMenuActive = false;
      // Pass the request ID as a query parameter to highlight it
      this.$router.push({
        path: '/password-reset-requests',
        query: { highlight: request.id }
      });
    },
    viewAllRequests() {
      this.notificationMenuActive = false;
      this.$router.push('/password-reset-requests');
    },
    formatTimeAgo(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      const now = new Date();
      const seconds = Math.floor((now - date) / 1000);
      
      if (seconds < 60) return 'Just now';
      if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
      if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
      if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
      
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },
    handlePasswordResetProcessed() {
      // Refresh the notification count when a request is processed
      if (this.isAdminUser) {
        this.loadPendingResetCount();
      }
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

/* Static Layout (Default) */
.layout-wrapper.layout-static {
  /* Default static layout */
}

.layout-wrapper.layout-static .layout-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 250px;
  background: #1e293b;
  z-index: 999;
  transition: transform 0.3s;
  overflow-y: auto;
  overflow-x: hidden;
}

.layout-wrapper.layout-static .layout-main-container {
  flex: 1;
  margin-left: 250px;
  transition: margin-left 0.3s;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  max-width: 100%;
}

.layout-wrapper.layout-static .layout-topbar {
  left: 250px;
  transition: left 0.3s;
}

.layout-wrapper.layout-static-inactive .layout-sidebar {
  transform: translateX(-100%);
}

.layout-wrapper.layout-static-inactive .layout-main-container {
  margin-left: 0;
}

.layout-wrapper.layout-static-inactive .layout-topbar {
  left: 0;
}

/* Overlay Layout */
.layout-wrapper.layout-overlay {
  /* Overlay layout styles */
}

.layout-wrapper.layout-overlay .layout-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 250px;
  background: #1e293b;
  z-index: 1001;
  transition: transform 0.3s;
  overflow-y: auto;
  overflow-x: hidden;
  transform: translateX(-100%);
}

.layout-wrapper.layout-overlay .layout-main-container {
  flex: 1;
  margin-left: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  max-width: 100%;
}

.layout-wrapper.layout-overlay .layout-topbar {
  left: 0;
}

.layout-wrapper.layout-overlay-active .layout-sidebar {
  transform: translateX(0);
}

/* Sidebar */
.layout-sidebar {
  /* Base sidebar styles moved to layout-specific sections above */
}

.sidebar-header {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
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
  flex-shrink: 0;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  white-space: nowrap;
}

/* GenTrack SVG Logo Animations */
.gentrack-logo {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.gentrack-logo svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 4px rgba(59, 130, 246, 0.4));
}

.logo-hex {
  stroke-dasharray: 260;
  stroke-dashoffset: 0;
  animation: drawHex 4s ease-in-out infinite alternate;
}

.logo-bolt {
  transform-origin: center;
  animation: pulseBolt 2s infinite alternate;
}

.logo-node {
  animation: blinkNode 2s infinite;
}

.logo-node:nth-child(3) { animation-delay: 0s; }
.logo-node:nth-child(4) { animation-delay: 0.5s; }
.logo-node:nth-child(5) { animation-delay: 1s; }
.logo-node:nth-child(6) { animation-delay: 1.5s; }

@keyframes drawHex {
  0% { stroke-dashoffset: 260; }
  50% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: 0; }
}

@keyframes pulseBolt {
  0% { transform: scale(0.95); fill: #3b82f6; }
  100% { transform: scale(1.05); fill: #93c5fd; }
}

@keyframes blinkNode {
  0%, 100% { opacity: 0.3; r: 3; fill: #fb923c; }
  50% { opacity: 1; r: 5; fill: #fde047; }
}

.user-role-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.6rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.role-badge.role-info {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.role-badge.role-success {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.role-badge.role-warning {
  background: rgba(251, 146, 60, 0.2);
  color: #fb923c;
}

.role-badge.role-danger {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
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

/* Dropdown Styles */
.menu-item-dropdown .menu-link {
  justify-content: space-between;
  cursor: pointer;
}

.dropdown-icon {
  font-size: 0.875rem;
  transition: transform 0.3s ease;
  margin-left: auto;
}

.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.submenu {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
  background: rgba(0, 0, 0, 0.2);
  list-style: none;
  padding: 0;
  margin: 0;
}

.submenu.open {
  max-height: 200px;
}

.submenu-item {
  list-style: none;
}

.submenu-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem 0.75rem 3rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
  white-space: nowrap;
}

.submenu-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.submenu-link.router-link-active {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border-left-color: #60a5fa;
}

.submenu-link i {
  font-size: 1rem;
  width: 18px;
  flex-shrink: 0;
}

.submenu-link span {
  white-space: nowrap;
}

.menu-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0.5rem 1.5rem;
}

.menu-section-title {
  padding: 0.75rem 1.5rem 0.5rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Main Container - moved to layout-specific sections above */

/* Top Bar - moved to layout-specific sections above */

/* Top Bar */
.layout-topbar {
  height: 70px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  position: fixed;
  top: 0;
  right: 0;
  z-index: 998;
  gap: 1rem;
  /* left property is handled by layout-specific styles above */
}

/* Date/Time Display Styles */
.topbar-datetime {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-right: 1.5rem;
}

.current-date {
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
  font-weight: 500;
}

.current-time {
  font-size: 0.875rem;
  color: var(--text-color, #334155);
  font-weight: 600;
  min-width: 80px;
}

/* Dark Mode overrides for Date/Time */
.dark-mode .current-date {
  color: #94a3b8;
}

.dark-mode .current-time {
  color: #e2e8f0;
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

.notification-wrapper {
  position: relative;
}

.notification-btn {
  position: relative;
}

.notification-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #ef4444;
  color: white;
  font-size: 0.625rem;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.notification-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  width: 380px;
  max-height: 500px;
  z-index: 1000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.notification-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.notification-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.notification-count {
  font-size: 0.75rem;
  color: #64748b;
  background: #e2e8f0;
  padding: 0.25rem 0.625rem;
  border-radius: 12px;
  font-weight: 500;
}

.notification-body {
  flex: 1;
  overflow-y: auto;
  max-height: 360px;
}

.notification-empty {
  padding: 3rem 1.5rem;
  text-align: center;
  color: #94a3b8;
}

.notification-empty i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #cbd5e1;
}

.notification-empty p {
  margin: 0;
  font-size: 0.9375rem;
}

.notification-list {
  padding: 0;
}

.notification-item {
  display: flex;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.2s;
}

.notification-item:hover {
  background: #f8fafc;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon i {
  color: white;
  font-size: 1.125rem;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.notification-text {
  font-size: 0.8125rem;
  color: #64748b;
  margin-bottom: 0.375rem;
  line-height: 1.4;
}

.notification-text strong {
  color: #1e293b;
  font-weight: 600;
}

.notification-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.notification-footer {
  padding: 0.875rem 1.25rem;
  border-top: 1px solid #e5e7eb;
  background: #f8fafc;
}

.view-all-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s;
}

.view-all-link:hover {
  color: #2563eb;
  gap: 0.625rem;
}

.view-all-link i {
  font-size: 0.75rem;
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
  margin-top: 70px;
  min-width: 0;
  max-width: 100%;
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
  opacity: 1;
  transition: opacity 0.3s ease;
}

/* Responsive */
@media (max-width: 991px) {
  /* Static mode mobile */
  .layout-wrapper.layout-static .layout-sidebar {
    transform: translateX(-100%);
  }

  .layout-wrapper.layout-static:not(.layout-static-inactive) .layout-sidebar {
    transform: translateX(0);
  }

  .layout-wrapper.layout-static .layout-main-container {
    margin-left: 0;
  }
  
  .layout-wrapper.layout-static .layout-topbar {
    left: 0;
  }

  /* Overlay mode mobile - same behavior as desktop */
  .layout-wrapper.layout-overlay .layout-sidebar {
    transform: translateX(-100%);
  }

  .layout-wrapper.layout-overlay-active .layout-sidebar {
    transform: translateX(0);
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
  
  .notification-menu {
    width: calc(100vw - 2rem);
    right: -0.5rem;
  }
}
</style>
