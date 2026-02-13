<template>
  <div class="landing-page">
    <!-- Animated background elements -->
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

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
export default {
  name: 'LandingPage',
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
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  position: relative;
  overflow: visible;
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
}

.landing-page::before,
.landing-page::after {
  max-width: 100vw;
}

/* Animated stars background */
.landing-page::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, white, transparent),
    radial-gradient(2px 2px at 60px 70px, white, transparent),
    radial-gradient(1px 1px at 50px 50px, white, transparent),
    radial-gradient(1px 1px at 130px 80px, white, transparent),
    radial-gradient(2px 2px at 90px 10px, white, transparent);
  background-size: 200px 200px;
  background-repeat: repeat;
  opacity: 0.5;
  animation: twinkle 3s infinite;
  z-index: 0;
  pointer-events: none;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}

/* Floating gradient orbs */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s infinite ease-in-out;
  z-index: 0;
  pointer-events: none;
  will-change: transform;
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.6) 0%, rgba(102, 126, 234, 0) 70%);
  top: -5%;
  left: 0;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(118, 75, 162, 0.6) 0%, rgba(118, 75, 162, 0) 70%);
  bottom: -10%;
  right: 0;
  animation-delay: -7s;
}

.orb-3 {
  width: 280px;
  height: 280px;
  background: radial-gradient(circle, rgba(255, 105, 180, 0.5) 0%, rgba(255, 105, 180, 0) 70%);
  top: 40%;
  right: 0;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(20px, -30px) scale(1.05);
  }
  66% {
    transform: translate(-15px, 15px) scale(0.95);
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
  width: 100%;
  box-sizing: border-box;
}

/* Hero Section */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 20px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.logo-hero {
  margin-bottom: 30px;
  animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.hero-logo {
  width: 180px;
  height: 180px;
  object-fit: contain;
  filter: drop-shadow(0 0 40px rgba(102, 126, 234, 0.6));
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  color: white;
  margin: 0 0 20px 0;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 15px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
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
  border-radius: 12px;
  font-size: 1.125rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
  background: linear-gradient(135deg, rgba(102, 126, 234, 1) 0%, rgba(118, 75, 162, 1) 100%);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Features Section */
.features-section {
  padding: 100px 20px;
  position: relative;
}

.section-title {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 0 0 15px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.section-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.7);
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
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: rgba(102, 126, 234, 0.9);
}

.feature-card h3 {
  font-size: 1.5rem;
  color: white;
  margin: 0 0 15px 0;
}

.feature-card p {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin: 0;
}

/* Stats Section */
.stats-section {
  padding: 80px 20px;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px);
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
  color: white;
  margin-bottom: 10px;
  text-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
}

.stat-label {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.7);
}

/* How It Works Section */
.how-it-works-section {
  padding: 100px 20px;
}

.steps-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  gap: 30px;
  align-items: center;
  margin-top: 60px;
}

.step-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
}

.step-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(102, 126, 234, 0.5);
}

.step-number {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
}

.step-icon {
  width: 70px;
  height: 70px;
  margin: 20px auto 20px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: rgba(102, 126, 234, 0.9);
}

.step-card h3 {
  font-size: 1.375rem;
  color: white;
  margin: 0 0 15px 0;
}

.step-card p {
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin: 0;
}

.step-arrow {
  font-size: 2rem;
  color: rgba(102, 126, 234, 0.5);
}

/* Footer */
.landing-footer {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 60px 20px 30px;
  margin-top: 100px;
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
  width: 80px;
  height: 80px;
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
  font-size: 1.125rem;
  margin: 0 0 20px 0;
}

.footer-column a {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  margin-bottom: 12px;
  transition: color 0.3s ease;
}

.footer-column a:hover {
  color: rgba(102, 126, 234, 0.9);
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
