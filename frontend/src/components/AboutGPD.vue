<template>
  <div class="about-page">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
    </div>

    <!-- Back Button Top Left -->
    <div class="back-button-top-left">
      <router-link to="/" class="btn-back-glass-small">
        <i class="pi pi-arrow-left"></i>
        <span>Back to Home</span>
      </router-link>
    </div>

    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="logo-container">
          <img src="@/assets/NPC-logo.png" alt="GenTrack Logo" class="header-logo" />
          <div class="logo-glow"></div>
        </div>
        <h1 class="glowing-text">About GPD</h1>
        <p class="subtitle">Generation and Performance Division</p>
        <p class="tagline">Powering Excellence in Reporting</p>
      </div>
    </div>

    <!-- Mission Section -->
    <div class="mission-section">
      <div class="glass-card mission-card">
        <div class="card-icon">
          <i class="pi pi-bolt"></i>
        </div>
        <h2>Our Mission</h2>
        <p>The Generation and Performance Division (GPD) is dedicated to ensuring optimal performance and reliable power generation across all Agus-Pulangi hydroelectric power plants. We strive for excellence in monitoring, reporting, and maintaining the highest standards of operational efficiency.</p>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="stats-section">
      <div class="stat-card-glass" v-for="(stat, index) in stats" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
        <div class="stat-icon">
          <i :class="stat.icon"></i>
        </div>
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
        <div class="stat-glow"></div>
      </div>
    </div>

    <!-- Power Plants Section -->
    <div class="plants-section">
      <h2 class="section-title">Our Power Plants</h2>
      <p class="section-subtitle">7 hydroelectric facilities powering Mindanao</p>
      
      <div class="plants-grid">
        <div 
          v-for="(plant, index) in plants" 
          :key="index"
          class="plant-card-glass"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @mouseenter="activePlant = index"
          @mouseleave="activePlant = null"
        >
          <div class="plant-glow" :class="{ active: activePlant === index }"></div>
          
          <div class="plant-header">
            <div class="plant-code">{{ plant.code }}</div>
            <div class="plant-status">
              <div class="status-dot"></div>
              <span>Operational</span>
            </div>
          </div>

          <h3>{{ plant.name }}</h3>
          
          <div class="plant-details">
            <div class="detail-item">
              <i class="pi pi-map-marker"></i>
              <span>{{ plant.location }}</span>
            </div>
            <div class="detail-item">
              <i class="pi pi-bolt"></i>
              <span>{{ plant.capacity }} MW</span>
            </div>
            <div class="detail-item">
              <i class="pi pi-cog"></i>
              <span>{{ plant.units }} Units</span>
            </div>
          </div>

          <div class="plant-capacity-bar">
            <div class="capacity-fill" :style="{ width: (plant.capacity / 255 * 100) + '%' }"></div>
          </div>

          <div class="plant-corner"></div>
        </div>
      </div>
    </div>

    <!-- Total Capacity Highlight -->
    <div class="capacity-highlight">
      <div class="highlight-card-glass">
        <div class="highlight-icon">
          <i class="pi pi-chart-line"></i>
        </div>
        <div class="highlight-content">
          <div class="highlight-value">1,025 MW</div>
          <div class="highlight-label">Total System Capacity</div>
          <div class="highlight-description">Across 7 hydroelectric power plants in the Agus-Pulangi system</div>
        </div>
        <div class="highlight-particles">
          <div class="particle" v-for="n in 20" :key="n"></div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'AboutGPD',
  data() {
    return {
      activePlant: null,
      stats: [
        { icon: 'pi pi-building', value: '7', label: 'Power Plants' },
        { icon: 'pi pi-bolt', value: '1,025', label: 'Total MW' },
        { icon: 'pi pi-cog', value: '22', label: 'Total Units' },
        { icon: 'pi pi-chart-line', value: '99.9%', label: 'Uptime' }
      ],
      plants: [
        { code: 'AGUS1', name: 'Agus 1', location: 'Lanao del Sur', capacity: 50, units: 2 },
        { code: 'AGUS2', name: 'Agus 2', location: 'Lanao del Sur', capacity: 180, units: 5 },
        { code: 'AGUS4', name: 'Agus 4', location: 'Lanao del Norte', capacity: 100, units: 3 },
        { code: 'AGUS5', name: 'Agus 5', location: 'Lanao del Norte', capacity: 52, units: 2 },
        { code: 'AGUS6', name: 'Agus 6', location: 'Lanao del Norte', capacity: 200, units: 4 },
        { code: 'AGUS7', name: 'Agus 7', location: 'Lanao del Norte', capacity: 68, units: 2 },
        { code: 'PULANGI4', name: 'Pulangi 4', location: 'Bukidnon', capacity: 255, units: 4 }
      ]
    };
  }
};
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  padding: 100px 20px 80px;
  position: relative;
  overflow: hidden;
}

.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float 20s ease-in-out infinite;
}

.shape-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  top: -200px;
  left: -200px;
}

.shape-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #ec4899 0%, #f59e0b 100%);
  bottom: -150px;
  right: -150px;
  animation-delay: 5s;
}

.shape-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(100px, -100px) scale(1.1); }
  66% { transform: translate(-100px, 100px) scale(0.9); }
}

.page-header {
  text-align: center;
  margin-bottom: 80px;
  position: relative;
  z-index: 1;
}

.logo-container {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto 30px;
}

.header-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 10px 30px rgba(59, 130, 246, 0.5));
  animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.logo-glow {
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%);
  animation: glowPulse 2s ease-in-out infinite;
  z-index: 1;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

.glowing-text {
  font-size: 4rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffffff 0%, #60a5fa 50%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 16px 0;
  letter-spacing: -2px;
}

.subtitle {
  font-size: 1.75rem;
  color: #cbd5e1;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.tagline {
  font-size: 1.125rem;
  color: #94a3b8;
  margin: 0;
  font-weight: 300;
  font-style: italic;
}

.mission-section {
  max-width: 900px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.glass-card {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 50px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transition: all 0.4s ease;
}

.glass-card:hover {
  transform: translateY(-5px);
  border-color: rgba(96, 165, 250, 0.3);
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.2);
}

.card-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 30px;
  border-radius: 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
  animation: iconBounce 2s ease-in-out infinite;
}

@keyframes iconBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.mission-card h2 {
  font-size: 2.5rem;
  color: white;
  margin: 0 0 24px 0;
  font-weight: 700;
  text-align: center;
}

.mission-card p {
  font-size: 1.25rem;
  color: #cbd5e1;
  line-height: 1.8;
  margin: 0;
  text-align: center;
}

.stats-section {
  max-width: 1200px;
  margin: 0 auto 80px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  position: relative;
  z-index: 1;
}

.stat-card-glass {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 40px 30px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.stat-card-glass:hover {
  transform: translateY(-10px) scale(1.05);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.stat-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto 20px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #60a5fa;
  transition: all 0.4s ease;
}

.stat-card-glass:hover .stat-icon {
  transform: scale(1.1) rotate(5deg);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
}

.stat-value {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 12px;
}

.stat-label {
  font-size: 1rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.stat-glow {
  position: absolute;
  inset: -50%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.stat-card-glass:hover .stat-glow {
  opacity: 1;
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.plants-section {
  max-width: 1400px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.section-title {
  font-size: 3rem;
  color: white;
  text-align: center;
  margin: 0 0 16px 0;
  font-weight: 800;
}

.section-subtitle {
  font-size: 1.25rem;
  color: #94a3b8;
  text-align: center;
  margin: 0 0 60px 0;
}

.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
}

.plant-card-glass {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 30px;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out backwards;
}

.plant-card-glass:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 25px 70px rgba(59, 130, 246, 0.3);
}

.plant-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.plant-glow.active {
  opacity: 1;
  animation: rotate 10s linear infinite;
}

.plant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.plant-code {
  padding: 8px 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.875rem;
  letter-spacing: 1px;
}

.plant-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #10b981;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: statusPulse 2s ease-in-out infinite;
}

@keyframes statusPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.plant-card-glass h3 {
  font-size: 1.75rem;
  color: white;
  margin: 0 0 20px 0;
  font-weight: 700;
}

.plant-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #cbd5e1;
  font-size: 1rem;
}

.detail-item i {
  color: #60a5fa;
  font-size: 1.125rem;
}

.plant-capacity-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 20px;
}

.capacity-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
  border-radius: 4px;
  transition: width 1s ease;
}

.plant-corner {
  position: absolute;
  top: 0;
  right: 0;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, transparent 50%, rgba(96, 165, 250, 0.1) 50%);
  border-radius: 0 20px 0 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.plant-card-glass:hover .plant-corner {
  opacity: 1;
}

.capacity-highlight {
  max-width: 900px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.highlight-card-glass {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.1) 0%, 
    rgba(139, 92, 246, 0.1) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  padding: 60px;
  text-align: center;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.highlight-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 30px;
  border-radius: 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5);
  animation: iconBounce 2s ease-in-out infinite;
}

.highlight-value {
  font-size: 5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 16px;
}

.highlight-label {
  font-size: 1.5rem;
  color: white;
  font-weight: 700;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.highlight-description {
  font-size: 1.125rem;
  color: #cbd5e1;
}

.highlight-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(96, 165, 250, 0.6);
  border-radius: 50%;
  animation: particleFloat 3s ease-in-out infinite;
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(50px);
    opacity: 0;
  }
}

.particle:nth-child(1) { left: 10%; top: 20%; }
.particle:nth-child(2) { left: 20%; top: 80%; animation-delay: 0.2s; }
.particle:nth-child(3) { left: 30%; top: 40%; animation-delay: 0.4s; }
.particle:nth-child(4) { left: 40%; top: 70%; animation-delay: 0.6s; }
.particle:nth-child(5) { left: 50%; top: 30%; animation-delay: 0.8s; }
.particle:nth-child(6) { left: 60%; top: 60%; animation-delay: 1s; }
.particle:nth-child(7) { left: 70%; top: 20%; animation-delay: 1.2s; }
.particle:nth-child(8) { left: 80%; top: 50%; animation-delay: 1.4s; }
.particle:nth-child(9) { left: 90%; top: 80%; animation-delay: 1.6s; }
.particle:nth-child(10) { left: 15%; top: 60%; animation-delay: 1.8s; }

/* Back Button Top Left */
.back-button-top-left {
  position: fixed;
  top: 30px;
  left: 30px;
  z-index: 1000;
}

.btn-back-glass-small {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.3) 0%, 
    rgba(139, 92, 246, 0.3) 100%);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
}

.btn-back-glass-small:hover {
  transform: translateX(-5px);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 12px 40px rgba(59, 130, 246, 0.5);
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.4) 0%, 
    rgba(139, 92, 246, 0.4) 100%);
}

@media (max-width: 768px) {
  .glowing-text {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.25rem;
  }
  
  .plants-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .highlight-value {
    font-size: 3rem;
  }
}
</style>
