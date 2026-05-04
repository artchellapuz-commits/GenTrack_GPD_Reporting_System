<template>
  <div class="features-page">
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
        <div class="header-icon">
          <i class="pi pi-sparkles"></i>
        </div>
        <h1 class="glowing-text">Powerful Features</h1>
        <p class="subtitle">Everything you need for professional power plant reporting</p>
      </div>
    </div>

    <!-- Features Grid -->
    <div class="features-container">
      <div 
        v-for="(feature, index) in features" 
        :key="index"
        class="feature-card-glass"
        :style="{ animationDelay: `${index * 0.1}s` }"
        @mouseenter="activeFeature = index"
        @mouseleave="activeFeature = null"
      >
        <div class="feature-glow" :class="{ active: activeFeature === index }"></div>
        
        <div class="feature-icon-container">
          <div class="icon-bg"></div>
          <i :class="feature.icon" class="feature-icon"></i>
          <div class="icon-pulse"></div>
        </div>

        <div class="feature-content">
          <h2>{{ feature.title }}</h2>
          <p>{{ feature.description }}</p>
          
          <div class="feature-benefits">
            <div v-for="(benefit, idx) in feature.benefits" :key="idx" class="benefit-item">
              <i class="pi pi-check-circle"></i>
              <span>{{ benefit }}</span>
            </div>
          </div>

          <div class="feature-stats">
            <div class="stat-item">
              <span class="stat-value">{{ feature.stat }}</span>
              <span class="stat-label">{{ feature.statLabel }}</span>
            </div>
          </div>
        </div>

        <div class="feature-corner"></div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Features',
  data() {
    return {
      activeFeature: null,
      features: [
        {
          icon: 'pi pi-chart-line',
          title: 'Real-time Dashboard',
          description: 'Monitor all power plants at a glance with live data visualization and instant updates.',
          benefits: [
            'Live data streaming',
            'Instant notifications',
            'Customizable widgets'
          ],
          stat: '24/7',
          statLabel: 'Monitoring'
        },
        {
          icon: 'pi pi-upload',
          title: 'Easy Excel Upload',
          description: 'Import daily reports seamlessly with automatic validation and error checking.',
          benefits: [
            'Drag & drop interface',
            'Auto-validation',
            'Bulk import support'
          ],
          stat: '< 30s',
          statLabel: 'Upload Time'
        },
        {
          icon: 'pi pi-chart-bar',
          title: 'Advanced Analytics',
          description: 'Visualize trends, capacity factors, and performance metrics with interactive charts.',
          benefits: [
            'Interactive charts',
            'Trend analysis',
            'Predictive insights'
          ],
          stat: '15+',
          statLabel: 'Chart Types'
        },
        {
          icon: 'pi pi-download',
          title: 'Export Reports',
          description: 'Generate comprehensive reports in multiple formats with customizable options.',
          benefits: [
            'Excel & PDF export',
            'Custom templates',
            'Scheduled exports'
          ],
          stat: '5 sec',
          statLabel: 'Generation'
        },
        {
          icon: 'pi pi-calendar',
          title: 'Scheduled Reports',
          description: 'Automate report generation with flexible scheduling and email delivery.',
          benefits: [
            'Flexible scheduling',
            'Email automation',
            'Multiple recipients'
          ],
          stat: '100%',
          statLabel: 'Automated'
        },
        {
          icon: 'pi pi-users',
          title: 'User Management',
          description: 'Role-based access control with different permission levels for your team.',
          benefits: [
            'Role-based access',
            'Activity tracking',
            'Secure authentication'
          ],
          stat: '5',
          statLabel: 'User Roles'
        }
      ]
    };
  }
};
</script>

<style scoped>
.features-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  padding: 100px 20px 80px;
  position: relative;
  overflow: hidden;
}

/* Animated Background */
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
  animation-delay: 0s;
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
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(100px, -100px) scale(1.1);
  }
  66% {
    transform: translate(-100px, 100px) scale(0.9);
  }
}

/* Header */
.page-header {
  text-align: center;
  margin-bottom: 80px;
  position: relative;
  z-index: 1;
}

.header-content {
  display: inline-block;
  position: relative;
}

.header-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 30px;
  border-radius: 30px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #60a5fa;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3),
              0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 25px 70px rgba(59, 130, 246, 0.5);
  }
}

.glowing-text {
  font-size: 4rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ffffff 0%, #60a5fa 50%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 20px 0;
  letter-spacing: -2px;
  text-shadow: 0 0 80px rgba(96, 165, 250, 0.5);
  animation: textGlow 3s ease-in-out infinite;
}

@keyframes textGlow {
  0%, 100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.2);
  }
}

.subtitle {
  font-size: 1.5rem;
  color: #cbd5e1;
  margin: 0;
  font-weight: 300;
}

/* Features Container */
.features-container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 40px;
  position: relative;
  z-index: 1;
}

/* Feature Card */
.feature-card-glass {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 40px;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card-glass:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.3),
              0 0 0 1px rgba(96, 165, 250, 0.2) inset;
}

.feature-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
  pointer-events: none;
}

.feature-glow.active {
  opacity: 1;
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Feature Icon */
.feature-icon-container {
  position: relative;
  width: 100px;
  height: 100px;
  margin-bottom: 30px;
}

.icon-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  border-radius: 24px;
  opacity: 0.2;
  transition: all 0.4s ease;
}

.feature-card-glass:hover .icon-bg {
  opacity: 0.3;
  transform: scale(1.1) rotate(5deg);
}

.feature-icon {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #60a5fa;
  z-index: 2;
  transition: all 0.4s ease;
}

.feature-card-glass:hover .feature-icon {
  transform: scale(1.1);
  color: #93c5fd;
}

.icon-pulse {
  position: absolute;
  inset: -10px;
  border-radius: 24px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  opacity: 0;
  animation: pulse 2s ease-out infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 1;
  }
  100% {
    transform: scale(1.2);
    opacity: 0;
  }
}

/* Feature Content */
.feature-content h2 {
  font-size: 2rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.feature-content p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0 0 24px 0;
}

.feature-benefits {
  margin-bottom: 24px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  color: #e2e8f0 !important;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.benefit-item:hover {
  transform: translateX(10px);
  color: #60a5fa;
}

.benefit-item i {
  color: #10b981;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.feature-stats {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #94a3b8 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.feature-corner {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, transparent 50%, rgba(96, 165, 250, 0.1) 50%);
  border-radius: 0 24px 0 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card-glass:hover .feature-corner {
  opacity: 1;
}

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
  .features-container {
    grid-template-columns: 1fr;
  }
  
  .glowing-text {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.125rem;
  }
}
</style>
