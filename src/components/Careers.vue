<template>
  <div class="careers-page">
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
          <i class="pi pi-briefcase"></i>
        </div>
        <h1 class="glowing-text">Careers at GPD</h1>
        <p class="subtitle">Join our team and power the future</p>
      </div>
    </div>

    <!-- Why Join Us -->
    <div class="why-join-section">
      <div class="section-card-glass">
        <h2>Why Join GPD?</h2>
        <p>Be part of a team that powers Mindanao's energy future. We offer competitive benefits, professional growth opportunities, and a collaborative work environment.</p>
      </div>
    </div>

    <!-- Benefits -->
    <div class="benefits-container">
      <div 
        v-for="(benefit, index) in benefits" 
        :key="index"
        class="benefit-card-glass"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="benefit-icon">
          <i :class="benefit.icon"></i>
        </div>
        <h3>{{ benefit.title }}</h3>
        <p>{{ benefit.description }}</p>
      </div>
    </div>

    <!-- Contact for Opportunities -->
    <div class="opportunities-section">
      <div class="opportunities-card-glass">
        <h2>Interested in Joining NPC?</h2>
        <p>For career opportunities with the National Power Corporation, please visit the official NPC website or contact the Human Resources department at your nearest NPC office</p>
        <div class="contact-info">
          <div class="info-item">
            <i class="pi pi-building"></i>
            <span>Visit NPC Official Website</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Careers',
  data() {
    return {
      benefits: [
        {
          icon: 'pi pi-dollar',
          title: 'Competitive Salary',
          description: 'Industry-standard compensation packages with performance bonuses'
        },
        {
          icon: 'pi pi-heart',
          title: 'Health Benefits',
          description: 'Comprehensive health insurance for you and your family'
        },
        {
          icon: 'pi pi-chart-line',
          title: 'Career Growth',
          description: 'Professional development programs and advancement opportunities'
        },
        {
          icon: 'pi pi-users',
          title: 'Team Culture',
          description: 'Collaborative and supportive work environment'
        },
        {
          icon: 'pi pi-calendar',
          title: 'Work-Life Balance',
          description: 'Flexible schedules and generous leave policies'
        },
        {
          icon: 'pi pi-graduation-cap',
          title: 'Training Programs',
          description: 'Continuous learning and skills development opportunities'
        }
      ]
    };
  }
};
</script>

<style scoped>
.careers-page {
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

.why-join-section {
  max-width: 900px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.section-card-glass {
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

.section-card-glass h2 {
  font-size: 2.5rem;
  color: white !important;
  margin: 0 0 24px 0;
  font-weight: 700;
}

.section-card-glass p {
  font-size: 1.25rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0;
}

.benefits-container {
  max-width: 1200px;
  margin: 0 auto 80px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  position: relative;
  z-index: 1;
}

.benefit-card-glass {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 40px;
  text-align: center;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.benefit-card-glass:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.3);
}

.benefit-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #60a5fa;
  transition: all 0.4s ease;
}

.benefit-card-glass:hover .benefit-icon {
  transform: scale(1.1) rotate(5deg);
}

.benefit-card-glass h3 {
  font-size: 1.5rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.benefit-card-glass p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0;
}

.opportunities-section {
  max-width: 900px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.opportunities-card-glass {
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

.opportunities-card-glass h2 {
  font-size: 2.5rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.opportunities-card-glass p {
  font-size: 1.25rem;
  color: #cbd5e1 !important;
  margin: 0 0 40px 0;
}

.contact-info {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 1.25rem;
  color: #e2e8f0 !important;
}

.info-item i {
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
  .benefits-container {
    grid-template-columns: 1fr;
  }
  
  .glowing-text {
    font-size: 2.5rem;
  }
  
  .contact-info {
    flex-direction: column;
    gap: 20px;
  }
}
</style>
