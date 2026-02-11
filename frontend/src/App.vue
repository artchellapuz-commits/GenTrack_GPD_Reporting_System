<template>
  <div id="app">
    <!-- Header -->
    <header class="app-header">
      <div class="container">
        <div class="header-content">
          <div class="logo-section">
            <img src="@/assets/NPC-logo.png" alt="NPC Logo" class="logo-image" />
            <div class="logo-text">
              <h1 class="logo-title">NPC Reporting System</h1>
              <p class="logo-subtitle">Agus-Pulangi Hydro-Electric Power Plants</p>
            </div>
          </div>
          <nav class="main-nav">
            <router-link to="/upload" class="nav-link">
              <i class="pi pi-upload nav-icon"></i>
              Upload
            </router-link>
            <router-link to="/reports" class="nav-link">
              <i class="pi pi-chart-line nav-icon"></i>
              Reports
            </router-link>
            <router-link to="/generate" class="nav-link">
              <i class="pi pi-download nav-icon"></i>
              Generate
            </router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <div class="container">
        <router-view />
      </div>
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <div class="container">
        <div class="footer-content">
          <p class="footer-text">
            © 2026 National Power Corporation. All rights reserved.
          </p>
          <p class="footer-links">
            <a href="#" class="footer-link">Help</a>
            <span class="footer-separator">•</span>
            <a href="#" class="footer-link">Documentation</a>
            <span class="footer-separator">•</span>
            <a href="#" class="footer-link">Contact</a>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import './assets/styles.css';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header Styles */
.app-header {
  background: linear-gradient(135deg, var(--npc-primary) 0%, var(--npc-primary-dark) 100%);
  color: white;
  box-shadow: var(--shadow-lg);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg) 0;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.logo-image {
  height: 60px;
  width: auto;
  object-fit: contain;
  display: block;
}

.logo-icon {
  font-size: 2.5rem;
  background: rgba(255, 255, 255, 0.1);
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  backdrop-filter: blur(10px);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
  letter-spacing: -0.025em;
}

.logo-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.main-nav {
  display: flex;
  gap: var(--spacing-sm);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
  background: rgba(255, 255, 255, 0.05);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.nav-icon {
  font-size: 1rem;
  color: inherit;
}

/* Main Content */
.app-main {
  flex: 1;
  padding: var(--spacing-2xl) 0;
  background: linear-gradient(180deg, var(--gray-50) 0%, white 100%);
}

/* Footer */
.app-footer {
  background-color: var(--gray-900);
  color: var(--gray-400);
  padding: var(--spacing-xl) 0;
  margin-top: auto;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.footer-text {
  margin: 0;
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin: 0;
  font-size: 0.875rem;
}

.footer-link {
  color: var(--gray-400);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: white;
}

.footer-separator {
  color: var(--gray-600);
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .main-nav {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>
