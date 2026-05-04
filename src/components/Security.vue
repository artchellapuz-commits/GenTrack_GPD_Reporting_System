<template>
  <div class="security-page">
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
          <i class="pi pi-lock"></i>
        </div>
        <h1 class="glowing-text">Security</h1>
        <p class="subtitle">Protecting your data is our priority</p>
      </div>
    </div>

    <!-- Security Features -->
    <div class="security-container">
      <div 
        v-for="(feature, index) in securityFeatures" 
        :key="index"
        class="security-card-glass"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="security-icon">
          <i :class="feature.icon"></i>
        </div>
        <h2>{{ feature.title }}</h2>
        <p>{{ feature.description }}</p>
        <ul class="feature-list">
          <li v-for="(item, idx) in feature.items" :key="idx">
            <i class="pi pi-check-circle"></i>
            <span>{{ item }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Best Practices -->
    <div class="best-practices-section">
      <div class="practices-card-glass">
        <h2>Security Best Practices</h2>
        <p>Help us keep your account secure by following these guidelines</p>
        <div class="practices-grid">
          <div v-for="(practice, index) in bestPractices" :key="index" class="practice-item">
            <i :class="practice.icon"></i>
            <div>
              <h3>{{ practice.title }}</h3>
              <p>{{ practice.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Production Recommendations -->
    <div class="recommendations-section">
      <div class="recommendations-card-glass">
        <div class="recommendation-header">
          <i class="pi pi-info-circle"></i>
          <h2>Recommended for Production Deployment</h2>
        </div>
        <p class="recommendation-intro">For enhanced security in production environments, consider implementing:</p>
        <div class="recommendations-list">
          <div v-for="(rec, index) in productionRecommendations" :key="index" class="recommendation-item">
            <i class="pi pi-angle-right"></i>
            <span>{{ rec }}</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Security',
  data() {
    return {
      securityFeatures: [
        {
          icon: 'pi pi-lock',
          title: 'Authentication & Authorization',
          description: 'Secure user authentication with JWT tokens',
          items: [
            'JWT token-based authentication',
            'Role-based access control (RBAC)',
            'Secure password hashing (PBKDF2)',
            'Session timeout management',
            'Protected API endpoints'
          ]
        },
        {
          icon: 'pi pi-shield',
          title: 'Django Security Features',
          description: 'Built-in framework security protections',
          items: [
            'CSRF protection on all forms',
            'SQL injection prevention',
            'XSS (Cross-Site Scripting) protection',
            'Clickjacking protection',
            'Secure cookie handling'
          ]
        },
        {
          icon: 'pi pi-file-edit',
          title: 'Activity Logging',
          description: 'Comprehensive audit trail of user actions',
          items: [
            'User activity tracking',
            'Login/logout logging',
            'Data modification records',
            'File upload tracking',
            'Searchable audit logs'
          ]
        },
        {
          icon: 'pi pi-database',
          title: 'Data Protection',
          description: 'Secure data handling and storage',
          items: [
            'Input validation and sanitization',
            'File upload restrictions (25MB limit)',
            'Secure file storage',
            'Database query protection',
            'HTTPS support (when configured)'
          ]
        }
      ],
      bestPractices: [
        {
          icon: 'pi pi-key',
          title: 'Strong Passwords',
          description: 'Use complex passwords with at least 8 characters, including letters, numbers, and symbols'
        },
        {
          icon: 'pi pi-eye-slash',
          title: 'Keep Credentials Private',
          description: 'Never share your login credentials with anyone, including colleagues'
        },
        {
          icon: 'pi pi-sign-out',
          title: 'Logout When Done',
          description: 'Always log out when finished, especially on shared or public computers'
        },
        {
          icon: 'pi pi-exclamation-triangle',
          title: 'Report Suspicious Activity',
          description: 'Immediately report any unusual account activity or security concerns to IT support'
        },
        {
          icon: 'pi pi-desktop',
          title: 'Secure Your Workstation',
          description: 'Lock your computer when away and keep your operating system updated'
        },
        {
          icon: 'pi pi-shield',
          title: 'Verify File Sources',
          description: 'Only upload files from trusted sources and verify data before submission'
        }
      ],
      productionRecommendations: [
        'HTTPS/SSL certificate for encrypted data transmission',
        'Rate limiting to prevent brute force attacks',
        'Regular security audits and vulnerability assessments',
        'Backup and disaster recovery procedures',
        'Network firewall and access restrictions',
        'Security monitoring and logging tools',
        'Regular software updates and patch management',
        'Multi-factor authentication (MFA) for sensitive accounts'
      ]
    };
  }
};
</script>

<style scoped>
.security-page {
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

.security-container {
  max-width: 1400px;
  margin: 0 auto 80px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  position: relative;
  z-index: 1;
}

.security-card-glass {
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

.security-card-glass:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: rgba(96, 165, 250, 0.5);
  box-shadow: 0 30px 80px rgba(59, 130, 246, 0.3);
}

.security-icon {
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

.security-card-glass:hover .security-icon {
  transform: scale(1.1) rotate(5deg);
}

.security-card-glass h2 {
  font-size: 1.75rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.security-card-glass p {
  font-size: 1.125rem;
  color: #cbd5e1 !important;
  line-height: 1.8;
  margin: 0 0 24px 0;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  color: #e2e8f0 !important;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.feature-list li:hover {
  transform: translateX(10px);
  color: #60a5fa;
}

.feature-list li i {
  color: #10b981;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.best-practices-section {
  max-width: 1200px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.practices-card-glass {
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.1) 0%, 
    rgba(139, 92, 246, 0.1) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(96, 165, 250, 0.3);
  padding: 50px;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.practices-card-glass h2 {
  font-size: 2.5rem;
  color: white !important;
  margin: 0 0 16px 0;
  font-weight: 700;
  text-align: center;
}

.practices-card-glass > p {
  font-size: 1.25rem;
  color: #cbd5e1 !important;
  margin: 0 0 40px 0;
  text-align: center;
}

.practices-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.practice-item {
  display: flex;
  gap: 20px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.practice-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(96, 165, 250, 0.3);
  transform: translateY(-5px);
}

.practice-item i {
  font-size: 2rem;
  color: #60a5fa;
  flex-shrink: 0;
}

.practice-item h3 {
  font-size: 1.25rem;
  color: white !important;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.practice-item p {
  font-size: 1rem;
  color: #cbd5e1 !important;
  margin: 0;
  line-height: 1.6;
}

.recommendations-section {
  max-width: 1000px;
  margin: 0 auto 80px;
  position: relative;
  z-index: 1;
}

.recommendations-card-glass {
  background: linear-gradient(135deg, 
    rgba(251, 191, 36, 0.1) 0%, 
    rgba(245, 158, 11, 0.1) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(251, 191, 36, 0.3);
  padding: 50px;
  box-shadow: 0 20px 60px rgba(251, 191, 36, 0.2);
}

.recommendation-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.recommendation-header i {
  font-size: 2.5rem;
  color: #fbbf24;
}

.recommendation-header h2 {
  font-size: 2.5rem;
  color: white !important;
  margin: 0;
  font-weight: 700;
}

.recommendation-intro {
  font-size: 1.25rem;
  color: #cbd5e1 !important;
  margin: 0 0 32px 0;
  text-align: center;
}

.recommendations-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 16px;
}

.recommendation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(251, 191, 36, 0.2);
  color: #e2e8f0 !important;
  font-size: 1.125rem;
  transition: all 0.3s ease;
}

.recommendation-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(251, 191, 36, 0.4);
  transform: translateX(10px);
}

.recommendation-item i {
  color: #fbbf24;
  font-size: 1.25rem;
  flex-shrink: 0;
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
  .security-container {
    grid-template-columns: 1fr;
  }
  
  .practices-grid {
    grid-template-columns: 1fr;
  }
  
  .recommendations-list {
    grid-template-columns: 1fr;
  }
  
  .glowing-text {
    font-size: 2.5rem;
  }
  
  .recommendation-header {
    flex-direction: column;
  }
  
  .recommendation-header h2 {
    font-size: 2rem;
    text-align: center;
  }
}
</style>
