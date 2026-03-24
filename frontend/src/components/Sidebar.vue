<template>
  <div>
    <!-- Hamburger Menu Button -->
    <button class="hamburger-menu" @click="toggleSidebar" :class="{ active: isOpen }">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Sidebar -->
    <div class="sidebar" :class="{ open: isOpen }">
      <div class="sidebar-header">
        <!-- Animated SVG Logo for GenTrack -->
        <div class="gentrack-logo sidebar-logo-svg">
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
        <h3>GenTrack</h3>
        <p class="user-info">{{ username }}</p>
        <span class="role-badge" :class="`role-${roleBadgeColor}`">{{ roleDisplay }}</span>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/dashboard" @click="closeSidebar" class="nav-item">
          <i class="pi pi-chart-line"></i>
          <span class="nav-text">Dashboard</span>
        </router-link>
        
        <!-- Upload - Only for Operator, Manager, Admin -->
        <router-link v-if="canUpload" to="/upload" @click="closeSidebar" class="nav-item">
          <i class="pi pi-upload"></i>
          <span class="nav-text">Upload Excel</span>
        </router-link>
        
        <!-- Archive - Show for everyone who can upload -->
        <router-link v-if="canUpload" to="/archive" @click="closeSidebar" class="nav-item">
          <i class="pi pi-inbox"></i>
          <span class="nav-text">Archive</span>
        </router-link>
        
        <router-link to="/view" @click="closeSidebar" class="nav-item">
          <i class="pi pi-eye"></i>
          <span class="nav-text">View Reports</span>
        </router-link>
        
        <router-link to="/generate" @click="closeSidebar" class="nav-item">
          <i class="pi pi-download"></i>
          <span class="nav-text">Generate Report</span>
        </router-link>
        
        <!-- Signatory Authorization - Show for all authenticated users -->
        <router-link to="/signatory-authorization" @click="closeSidebar" class="nav-item">
          <i class="pi pi-user-edit"></i>
          <span class="nav-text">Request Signature Access</span>
        </router-link>
        
        <!-- Water Nomination with Dropdown - Only for Operator, Manager, Admin -->
        <div v-if="canUpload" class="nav-item-dropdown">
          <a href="#" @click.prevent="toggleWaterNominationDropdown" class="nav-item">
            <i class="pi pi-calendar"></i>
            <span class="nav-text">Water Nomination</span>
            <i class="pi pi-chevron-down dropdown-icon" :class="{ rotated: waterNominationOpen }"></i>
          </a>
          <div class="dropdown-menu" :class="{ open: waterNominationOpen }">
            <router-link to="/water-nomination" class="dropdown-item">
              <i class="pi pi-file-edit"></i>
              <span>Manage Nominations</span>
            </router-link>
            <router-link v-if="canApprove" to="/approval-queue" class="dropdown-item">
              <i class="pi pi-check-circle"></i>
              <span>Approval Queue</span>
            </router-link>
          </div>
        </div>
        
        <!-- Analytics & Automation Section -->
        <div class="nav-divider"></div>
        <div class="nav-section-title">Analytics & Automation</div>
        <router-link to="/analytics" @click="closeSidebar" class="nav-item">
          <i class="pi pi-chart-line"></i>
          <span class="nav-text">Advanced Analytics</span>
        </router-link>
        <router-link v-if="canApprove" to="/scheduled-reports" @click="closeSidebar" class="nav-item">
          <i class="pi pi-clock"></i>
          <span class="nav-text">Automated Reports</span>
        </router-link>
        
        <!-- Admin Section - Only for Admin -->
        <div class="nav-divider"></div>
        <div class="nav-section-title">Administration</div>
        
        <!-- User Management with Dropdown -->
        <div class="nav-item-dropdown">
          <a href="#" @click.prevent="toggleUserManagementDropdown" class="nav-item">
            <i class="pi pi-users"></i>
            <span class="nav-text">User Management</span>
            <i class="pi pi-chevron-down dropdown-icon" :class="{ rotated: userManagementOpen }"></i>
          </a>
          <div class="dropdown-menu" :class="{ open: userManagementOpen }">
            <router-link to="/user-management" class="dropdown-item">
              <i class="pi pi-user-edit"></i>
              <span>Manage Users</span>
            </router-link>
            <router-link v-if="isAdminUser" to="/password-reset-requests" class="dropdown-item">
              <i class="pi pi-lock"></i>
              <span>Reset Requests</span>
            </router-link>
          </div>
        </div>
        
        <a href="http://localhost:8000/admin" target="_blank" class="nav-item">
          <i class="pi pi-cog"></i>
          <span class="nav-text">Admin Panel</span>
        </a>
        <router-link to="/audit-logs" @click="closeSidebar" class="nav-item">
          <i class="pi pi-history"></i>
          <span class="nav-text">Audit Logs</span>
        </router-link>
        
        <div class="nav-divider"></div>
        
        <router-link to="/profile" @click="closeSidebar" class="nav-item">
          <i class="pi pi-user"></i>
          <span class="nav-text">My Profile</span>
        </router-link>
        
        <a href="#" @click.prevent="handleLogout" class="nav-item nav-item-danger">
          <i class="pi pi-sign-out"></i>
          <span class="nav-text">Logout</span>
        </a>
      </nav>
    </div>

    <!-- Sidebar Overlay -->
    <div class="sidebar-overlay" :class="{ active: isOpen }" @click="closeSidebar"></div>
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

export default {
  name: 'Sidebar',
  data() {
    return {
      isOpen: false,
      username: '',
      userRole: '',
      roleDisplay: '',
      roleBadgeColor: 'secondary',
      canUpload: false,
      canApprove: false,
      isAdminUser: false,
      waterNominationOpen: false,
      userManagementOpen: false
    };
  },
  mounted() {
    this.loadUserInfo();
    this.checkCurrentRoute();
  },
  watch: {
    '$route'(to) {
      this.checkCurrentRoute();
      // Reload user info when route changes to ensure admin status is current
      this.loadUserInfo();
    }
  },
  methods: {
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
      this.isOpen = !this.isOpen;
    },
    closeSidebar() {
      this.isOpen = false;
      // Don't close the dropdown when sidebar closes
      // this.waterNominationOpen = false;
    },
    toggleWaterNominationDropdown() {
      this.waterNominationOpen = !this.waterNominationOpen;
    },
    toggleUserManagementDropdown() {
      this.userManagementOpen = !this.userManagementOpen;
    },
    handleLogout() {
      sessionStorage.setItem('justLoggedOut', 'true');
      logout();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* Hamburger Menu Button */
.hamburger-menu {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1001;
  width: 50px;
  height: 50px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.hamburger-menu:hover {
  background: #f7fafc;
  border-color: var(--npc-primary);
  transform: scale(1.05);
}

.hamburger-menu span {
  width: 24px;
  height: 3px;
  background: var(--npc-primary);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.hamburger-menu.active span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.hamburger-menu.active span:nth-child(2) {
  opacity: 0;
}

.hamburger-menu.active span:nth-child(3) {
  transform: rotate(-45deg) translate(8px, -8px);
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: -300px;
  width: 280px;
  height: 100vh;
  background: white;
  border-right: 2px solid #e2e8f0;
  z-index: 1000;
  transition: left 0.3s ease, visibility 0s 0.3s;
  overflow: hidden;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  visibility: hidden;
}

.sidebar.open {
  left: 0;
  visibility: visible;
  transition: left 0.3s ease, visibility 0s 0s;
}

.sidebar-header {
  padding: 30px 20px;
  text-align: center;
  border-bottom: 2px solid #e2e8f0;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
}

/* GenTrack SVG Logo Animations */
.sidebar-logo-svg {
  width: 80px;
  height: 80px;
  margin: 0 auto 15px;
}

.sidebar-logo-svg svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.4));
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

.sidebar-header h3 {
  color: var(--npc-primary);
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 5px 0;
}

.user-info {
  color: #718096;
  font-size: 0.875rem;
  margin: 0 0 10px 0;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-info {
  background: #e6f7ff;
  color: #0066cc;
}

.role-success {
  background: #d4edda;
  color: #155724;
}

.role-warning {
  background: #fff3cd;
  color: #856404;
}

.role-danger {
  background: #f8d7da;
  color: #721c24;
}

.nav-section-title {
  padding: 10px 25px 5px;
  color: #a0aec0;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.sidebar-nav {
  padding: 20px 0;
  overflow-y: auto;
  max-height: calc(100vh - 200px);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 25px;
  color: #4a5568;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 1rem;
  border-left: 3px solid transparent;
  font-weight: 500;
}

.nav-item:hover {
  background: #f7fafc;
  color: var(--npc-primary);
  border-left-color: var(--npc-primary);
}

.nav-item.router-link-active {
  background: #edf2f7;
  color: var(--npc-primary);
  border-left-color: var(--npc-primary);
  font-weight: 600;
}

.nav-item i {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
}

.nav-text {
  white-space: nowrap;
}

/* Dropdown Styles */
.nav-item-dropdown {
  position: relative;
}

.nav-item-dropdown .nav-item {
  display: flex;
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

.dropdown-menu {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
  background: #f7fafc;
}

.dropdown-menu.open {
  max-height: 200px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 25px 12px 50px;
  color: #4a5568;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  border-left: 3px solid transparent;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: #edf2f7;
  color: var(--npc-primary);
  border-left-color: var(--npc-primary);
}

.dropdown-item.router-link-active {
  background: #e2e8f0;
  color: var(--npc-primary);
  border-left-color: var(--npc-primary);
  font-weight: 600;
}

.dropdown-item i {
  font-size: 1rem;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

.dropdown-item span {
  white-space: nowrap;
}

.nav-item-danger {
  color: #e53e3e;
}

.nav-item-danger:hover {
  background: #fff5f5;
  color: #c53030;
  border-left-color: #e53e3e;
}

.nav-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 15px 20px;
}

/* Sidebar Overlay */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.sidebar-overlay.active {
  opacity: 1;
  visibility: visible;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 260px;
    left: -260px;
  }
}

@media (max-width: 480px) {
  .sidebar {
    width: 240px;
    left: -240px;
  }

  .hamburger-menu {
    width: 45px;
    height: 45px;
    top: 15px;
    left: 15px;
  }
}
</style>
