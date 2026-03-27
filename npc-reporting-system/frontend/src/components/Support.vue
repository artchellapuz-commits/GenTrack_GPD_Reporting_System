<template>
  <div class="support-page">
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
          <i class="pi pi-question-circle"></i>
        </div>
        <h1 class="glowing-text">Support Center</h1>
        <p class="subtitle">We're here to help you succeed</p>
      </div>
    </div>

    <!-- Support Options -->
    <div class="support-container">
      <div 
        v-for="(option, index) in supportOptions" 
        :key="index"
        class="support-card-glass"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="support-icon">
          <i :class="option.icon"></i>
        </div>
        <h2>{{ option.title }}</h2>
        <p>{{ option.description }}</p>
        <div class="support-details">
          <div v-for="(detail, idx) in option.details" :key="idx" class="detail-item">
            <i class="pi pi-angle-right"></i>
            <span>{{ detail }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Info -->
    <div class="contact-info-section">
      <div class="info-card-glass">
        <h2>Need Immediate Assistance?</h2>
        <p>IT support team is available during business hours</p>
        <div class="contact-methods">
          <div class="method-item">
            <i class="pi pi-users"></i>
            <span>Contact your system administrator or IT support desk</span>
          </div>
          <div class="method-item">
            <i class="pi pi-clock"></i>
            <span>Monday - Friday, 8:00 AM - 5:00 PM</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Support',
  data() {
    return {
      supportOptions: [
        {
          icon: 'pi pi-book',
          title: 'Documentation',
          description: 'Comprehensive guides and tutorials',
          details: [
            'User manuals and guides',
            'Video tutorials',
            'API documentation',
            'Best practices'
          ]
        },
        {
          icon: 'pi pi-comments',
          title: 'Technical Support',
          description: 'Get help from our technical team',
          details: [
            'Email support',
            'Issue tracking',
            'Bug reports',
            'Feature requests'
          ]
        },
        {
          icon: 'pi pi-users',
          title: 'Training',
          description: 'Learn how to use the system effectively',
          details: [
            'Onboarding sessions',
            'Advanced training',
            'Webinars',
            'Workshops'
          ]
        },
        {
          icon: 'pi pi-wrench',
          title: 'System Status',
          description: 'Check system health and updates',
          details: [
            'Service status',
            'Scheduled maintenance',
            'System updates',
            'Performance metrics'
          ]
        }
      ]
    };
  }
};
</script>

<style scoped>
.support-page {
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
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
  animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
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
}

.subtitle {
  font-size: 1.5rem;
  color: #cbd5e1;
  margin: 0;
  font-weight: 300;
}

.support-container {
  max-width: 1200px;
  margin: 0 auto 80px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  position: relative;
  z-index: 1;
}

.support-card-glass {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 40px;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.support-card-glass:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.3);
}

.support-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #60a5fa;
  transition: all 0.4s ease;
}

.support-card-glass:hover .support-icon {
  transform: scale(1.1) rotate(5deg);
}

.support-card-glass h2 {
  font-size: 1.75rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.support-card-glass p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0 0 24px 0;
}

.support-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #e2e8f0 !important;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.detail-item:hover {
  transform: translateX(10px);
  color: #60a5fa;
}

.detail-item i {
  color: #60a5fa;
  font-size: 1rem;
}

.contact-info-section {
  max-width: 900px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.info-card-glass {
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.1) 0%, 
    rgba(139, 92, 246, 0.1) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  padding: 50px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.info-card-glass h2 {
  font-size: 2.5rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.info-card-glass p {
  font-size: 1.25rem;
  color: #cbd5e1 !important;
  margin: 0 0 40px 0;
}

.contact-methods {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.method-item {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 1.125rem;
  color: #e2e8f0 !important;
}

.method-item i {
  font-size: 1.5rem;
  color: #60a5fa;
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
  .support-container {
    grid-template-columns: 1fr;
  }
  
  .glowing-text {
    font-size: 2.5rem;
  }
}
</style>
