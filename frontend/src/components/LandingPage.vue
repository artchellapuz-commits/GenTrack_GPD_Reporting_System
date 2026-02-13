<template>
  <div class="landing-page">
    <!-- Theme Controls -->
    <ThemeControls />

    <!-- Hero Section -->
    <section id="hero" class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="logo-hero">
            <img src="@/assets/NPC-logo.png" alt="NPC Logo" class="hero-logo" />
          </div>
          <h1 class="hero-title">NPC Reporting System</h1>
          <p class="hero-subtitle">Agus-Pulangi Hydro-Electric Power Plants</p>
          <p class="hero-tagline">Streamline your power generation reporting with real-time analytics</p>
          
          <div class="cta-buttons">
            <router-link to="/register" class="btn btn-primary">
              <i class="pi pi-user-plus"></i>
              Get Started
            </router-link>
            <router-link to="/login" class="btn btn-secondary">
              <i class="pi pi-sign-in"></i>
              Sign In
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <h2 class="section-title">Powerful Features</h2>
        <p class="section-subtitle">Everything you need to manage power plant reporting</p>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-chart-line"></i>
            </div>
            <h3>Real-time Dashboard</h3>
            <p>Monitor all power plants at a glance with live data visualization and instant updates</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-upload"></i>
            </div>
            <h3>Easy Upload</h3>
            <p>Import Excel reports seamlessly with automatic data validation and error checking</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-chart-bar"></i>
            </div>
            <h3>Analytics & Charts</h3>
            <p>Visualize generation trends, capacity factors, and performance metrics</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-download"></i>
            </div>
            <h3>Export Reports</h3>
            <p>Generate comprehensive reports in multiple formats for easy sharing</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section id="stats" class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">7</div>
            <div class="stat-label">Power Plants</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">1,025</div>
            <div class="stat-label">Total Capacity (MW)</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Real-time Monitoring</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">System Uptime</div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works-section">
      <div class="container">
        <h2 class="section-title">How It Works</h2>
        <p class="section-subtitle">Get started in three simple steps</p>
        
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon">
              <i class="pi pi-file-excel"></i>
            </div>
            <h3>Upload Reports</h3>
            <p>Import your daily power generation reports in Excel format</p>
          </div>

          <div class="step-arrow">
            <i class="pi pi-arrow-right"></i>
          </div>

          <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon">
              <i class="pi pi-eye"></i>
            </div>
            <h3>View Analytics</h3>
            <p>Monitor real-time data and visualize trends across all plants</p>
          </div>

          <div class="step-arrow">
            <i class="pi pi-arrow-right"></i>
          </div>

          <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon">
              <i class="pi pi-file-pdf"></i>
            </div>
            <h3>Generate Summaries</h3>
            <p>Create comprehensive reports for stakeholders and management</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <img src="@/assets/NPC-logo.png" alt="NPC Logo" class="footer-logo" />
            <p>National Power Corporation</p>
            <p class="footer-tagline">Powering the Nation</p>
          </div>
          
          <div class="footer-links">
            <div class="footer-column">
              <h4>Product</h4>
              <a href="#">Features</a>
              <a href="#">Documentation</a>
              <a href="#">Support</a>
            </div>
            
            <div class="footer-column">
              <h4>Company</h4>
              <a href="#">About NPC</a>
              <a href="#">Contact Us</a>
              <a href="#">Careers</a>
            </div>
            
            <div class="footer-column">
              <h4>Legal</h4>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
              <a href="#">Security</a>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2026 National Power Corporation. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import ThemeControls from './ThemeControls.vue';

export default {
  name: 'LandingPage',
  components: {
    ThemeControls
  },
  mounted() {
    // Hide scrollbar but keep scrolling functionality
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.overflowX = 'hidden';
    document.body.style.msOverflowStyle = 'none';  // IE and Edge
    document.body.style.scrollbarWidth = 'none';  // Firefox
    
    // Add class to body for webkit browsers
    document.body.classList.add('hide-scrollbar');
  },
  beforeUnmount() {
    // Restore default
    document.body.style.overflowX = '';
    document.documentElement.style.overflowX = '';
    document.body.style.msOverflowStyle = '';
    document.body.style.scrollbarWidth = '';
    document.body.classList.remove('hide-scrollbar');
  }
};
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: #ffffff;
  position: relative;
  overflow-x: hidden;
  width: 100%;
  max-width: 100vw;
}

/* Hero Section */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.logo-hero {
  margin-bottom: 30px;
}

.hero-logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
  filter: drop-shadow(0 4px 20px rgba(59, 130, 246, 0.3));
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 20px 0;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 15px 0;
}

.hero-tagline {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 40px 0;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 16px 40px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

/* Features Section */
.features-section {
  padding: 100px 20px;
  background: #f8fafc;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  text-align: center;
  margin: 0 0 15px 0;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  text-align: center;
  margin: 0 0 60px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-top: 60px;
}

.feature-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
}

.feature-card h3 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.feature-card p {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

/* Stats Section */
.stats-section {
  padding: 80px 20px;
  background: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
}

.stat-card {
  text-align: center;
}

.stat-number {
  font-size: 3.5rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1.125rem;
  color: #64748b;
  font-weight: 500;
}

/* How It Works Section */
.how-it-works-section {
  padding: 100px 20px;
  background: #f8fafc;
}

.steps-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  gap: 30px;
  align-items: center;
  margin-top: 60px;
}

.step-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  position: relative;
  transition: all 0.2s ease;
}

.step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.step-number {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.step-icon {
  width: 70px;
  height: 70px;
  margin: 20px auto 20px;
  background: #eff6ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #3b82f6;
}

.step-card h3 {
  font-size: 1.375rem;
  color: #1e293b;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.step-card p {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.step-arrow {
  font-size: 2rem;
  color: #cbd5e0;
}

/* Footer */
.landing-footer {
  background: #1e293b;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 60px 20px 30px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 60px;
  margin-bottom: 40px;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
  margin-bottom: 10px;
}

.footer-brand p {
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.footer-tagline {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9375rem !important;
  font-weight: 400 !important;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.footer-column h4 {
  color: white;
  font-size: 1rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.footer-column a {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  margin-bottom: 12px;
  transition: color 0.2s ease;
  font-size: 0.9375rem;
}

.footer-column a:hover {
  color: #3b82f6;
}

.footer-bottom {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .steps-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.25rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .footer-links {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }

  .sidebar {
    width: 260px;
    left: -260px;
  }
}

@media (max-width: 480px) {
  .hero-logo {
    width: 120px;
    height: 120px;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* Hide scrollbar for Chrome, Safari and Opera */
::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
body.hide-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

body.hide-scrollbar::-webkit-scrollbar {
  display: none;  /* Chrome, Safari, Opera */
}
</style>
