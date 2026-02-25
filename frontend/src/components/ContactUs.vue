<template>
  <div class="contact-page">
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
          <i class="pi pi-envelope"></i>
        </div>
        <h1 class="glowing-text">Contact Us</h1>
        <p class="subtitle">Get in touch with the GPD team</p>
      </div>
    </div>

    <!-- Contact Info -->
    <div class="contact-container">
      <div 
        v-for="(contact, index) in contactInfo" 
        :key="index"
        class="contact-card-glass"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="contact-icon">
          <i :class="contact.icon"></i>
        </div>
        <h2>{{ contact.title }}</h2>
        <p>{{ contact.description }}</p>
        <div class="contact-details">
          <div v-for="(detail, idx) in contact.details" :key="idx" class="detail-item">
            <i class="pi pi-angle-right"></i>
            <span>{{ detail }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Office Location -->
    <div class="location-section">
      <div class="location-card-glass">
        <h2>Office Location</h2>
        <div class="location-details">
          <div class="location-item">
            <i class="pi pi-map-marker"></i>
            <div>
              <h3>Generation and Performance Division</h3>
              <p>National Power Corporation</p>
              <p>Mindanao Region</p>
            </div>
          </div>
          <div class="location-item">
            <i class="pi pi-clock"></i>
            <div>
              <h3>Office Hours</h3>
              <p>Monday - Friday</p>
              <p>8:00 AM - 5:00 PM</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'ContactUs',
  data() {
    return {
      contactInfo: [
        {
          icon: 'pi pi-envelope',
          title: 'Email Support',
          description: 'Send us an email for inquiries and support',
          details: [
            'System Administrator',
            'IT Support Team',
            'GPD Technical Staff'
          ]
        },
        {
          icon: 'pi pi-phone',
          title: 'Phone',
          description: 'Contact during business hours',
          details: [
            'GPD Main Office',
            'IT Support Desk',
            'System Administrator'
          ]
        },
        {
          icon: 'pi pi-comments',
          title: 'Internal Support',
          description: 'Get help from IT support team',
          details: [
            'Available during office hours',
            'Submit support tickets',
            'Technical and system inquiries'
          ]
        }
      ]
    };
  }
};
</script>

<style scoped>
.contact-page {
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

.contact-container {
  max-width: 1200px;
  margin: 0 auto 80px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
  position: relative;
  z-index: 1;
}

.contact-card-glass {
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

.contact-card-glass:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.3);
}

.contact-icon {
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

.contact-card-glass:hover .contact-icon {
  transform: scale(1.1) rotate(5deg);
}

.contact-card-glass h2 {
  font-size: 1.75rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.contact-card-glass p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0 0 24px 0;
}

.contact-details {
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

.location-section {
  max-width: 900px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.location-card-glass {
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.1) 0%, 
    rgba(139, 92, 246, 0.1) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  padding: 50px;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.location-card-glass h2 {
  font-size: 2.5rem;
  color: white !important;
  margin: 0 0 40px 0;
  font-weight: 700;
  text-align: center;
}

.location-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.location-item {
  display: flex;
  gap: 20px;
}

.location-item i {
  font-size: 2rem;
  color: #60a5fa;
  flex-shrink: 0;
}

.location-item h3 {
  font-size: 1.5rem;
  color: white !important;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.location-item p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  margin: 4px 0;
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
  .contact-container {
    grid-template-columns: 1fr;
  }
  
  .location-details {
    grid-template-columns: 1fr;
  }
  
  .glowing-text {
    font-size: 2.5rem;
  }
}
</style>
