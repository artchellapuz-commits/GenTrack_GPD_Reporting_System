<template>
  <div class="privacy-page">
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
          <i class="pi pi-shield"></i>
        </div>
        <h1 class="glowing-text">Privacy Policy</h1>
        <p class="subtitle">Your privacy is important to us</p>
        <p class="last-updated">Last Updated: February 2026</p>
      </div>
    </div>

    <!-- Content -->
    <div class="content-container">
      <div class="content-card-glass">
        <div v-for="(section, index) in sections" :key="index" class="section">
          <h2>{{ section.title }}</h2>
          <p v-for="(paragraph, idx) in section.content" :key="idx">{{ paragraph }}</p>
          <ul v-if="section.list">
            <li v-for="(item, idx) in section.list" :key="idx">{{ item }}</li>
          </ul>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'PrivacyPolicy',
  data() {
    return {
      sections: [
        {
          title: '1. Information We Collect',
          content: [
            'We collect information necessary to provide and improve our reporting services. This includes:'
          ],
          list: [
            'User account information (name, email, role)',
            'Plant operational data uploaded through the system',
            'System usage logs and analytics',
            'Technical information (IP address, browser type)'
          ]
        },
        {
          title: '2. How We Use Your Information',
          content: [
            'The information we collect is used to:'
          ],
          list: [
            'Provide and maintain the reporting system',
            'Generate performance reports and analytics',
            'Improve system functionality and user experience',
            'Ensure system security and prevent unauthorized access',
            'Communicate important system updates'
          ]
        },
        {
          title: '3. Data Security',
          content: [
            'We implement industry-standard security measures to protect your data, including encryption, secure authentication, and regular security audits. Access to sensitive data is restricted to authorized personnel only.'
          ]
        },
        {
          title: '4. Data Retention',
          content: [
            'We retain operational data as required by government regulations and organizational policies. User account information is maintained for the duration of active employment or system access.'
          ]
        },
        {
          title: '5. Data Sharing',
          content: [
            'We do not sell or share your personal information with third parties. Data may be shared internally within NPC for operational purposes and with government agencies as required by law.'
          ]
        },
        {
          title: '6. Your Rights',
          content: [
            'You have the right to access, correct, or request deletion of your personal information. Contact our support team for assistance with data-related requests.'
          ]
        },
        {
          title: '7. Changes to This Policy',
          content: [
            'We may update this privacy policy periodically. Users will be notified of significant changes through the system or email.'
          ]
        },
        {
          title: '8. Contact Us',
          content: [
            'For questions about this privacy policy, please contact your system administrator or the GPD IT support team.'
          ]
        }
      ]
    };
  }
};
</script>

<style scoped>
.privacy-page {
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
  margin: 0 0 12px 0;
  font-weight: 300;
}

.last-updated {
  font-size: 1rem;
  color: #94a3b8;
  margin: 0;
  font-style: italic;
}

.content-container {
  max-width: 1000px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.content-card-glass {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0.02) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 60px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.section {
  margin-bottom: 40px;
}

.section:last-child {
  margin-bottom: 0;
}

.section h2 {
  font-size: 1.75rem;
  color: #ffffff !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.section p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0 0 16px 0;
}

.section ul {
  list-style: none;
  padding: 0;
  margin: 16px 0 0 0;
}

.section ul li {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  padding: 8px 0 8px 32px;
  position: relative;
}

.section ul li::before {
  content: '•';
  position: absolute;
  left: 12px;
  color: #60a5fa;
  font-size: 1.5rem;
}

.back-button-container {
  text-align: center;
  margin-top: 80px;
  position: relative;
  z-index: 1;
}

.btn-back-glass {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 18px 40px;
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.2) 0%, 
    rgba(139, 92, 246, 0.2) 100%);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  color: white;
  text-decoration: none;
  font-size: 1.125rem;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
}

.btn-back-glass:hover {
  transform: translateY(-5px) scale(1.05);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.4);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent);
  transition: left 0.6s ease;
}

.btn-back-glass:hover .btn-shine {
  left: 100%;
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
  .content-card-glass {
    padding: 40px 30px;
  }
  
  .glowing-text {
    font-size: 2.5rem;
  }
}
</style>
