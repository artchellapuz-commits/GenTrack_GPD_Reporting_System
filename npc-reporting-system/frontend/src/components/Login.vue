<template>
  <div class="login-page">
    <!-- Modern Background -->
    <div class="login-background">
      <div class="mesh-gradient-bg"></div>
      <div class="energy-particles">
        <div v-for="n in 10" :key="n" class="energy-particle" :style="generateParticleStyle(n)"></div>
      </div>
      <div class="grain-overlay"></div>
    </div>
    <div class="background-overlay"></div>

    <!-- Theme Controls -->
    <ThemeControls />

    <!-- Back Button -->
    <router-link to="/" class="back-button">
      <i class="pi pi-arrow-left"></i>
      Back to Home
    </router-link>
    
    <div class="login-container">
      <div class="login-card">
        <!-- Logo and Title -->
        <div class="login-header">
          <div class="logo-icon gentrack-logo-container">
            <!-- Animated SVG Logo for GenTrack -->
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="gentrack-svg">
              <!-- Background Hexagon -->
              <polygon points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5" fill="none" stroke="#3b82f6" stroke-width="6" class="logo-hex"/>
              <!-- Power Lightning Bolt -->
              <path d="M55,20 L35,55 L50,55 L45,80 L65,45 L50,45 Z" fill="#60a5fa" class="logo-bolt"/>
              <!-- Data Connection Nodes -->
              <circle cx="35" cy="55" r="4" fill="#fb923c" class="logo-node"/>
              <circle cx="50" cy="55" r="4" fill="#fb923c" class="logo-node"/>
              <circle cx="65" cy="45" r="4" fill="#fb923c" class="logo-node"/>
              <circle cx="50" cy="45" r="4" fill="#fb923c" class="logo-node"/>
            </svg>
          </div>
          <h2>Welcome to GenTrack!</h2>
          <p>Plant Status Report Generator</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="credentials.username"
              type="text"
              placeholder="Username"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-input">
              <input
                id="password"
                v-model="credentials.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Password"
                required
                :disabled="loading"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
                :disabled="loading"
              >
                <i :class="[showPassword ? 'pi pi-eye-slash' : 'pi pi-eye', 'w-fit']"></i>
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe" />
              <span>Remember me</span>
            </label>
            <a href="#" class="forgot-password" @click.prevent="showForgotPasswordModal = true">Forgot password?</a>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="error-message">
            <i class="pi pi-exclamation-circle"></i>
            {{ error }}
          </div>

          <!-- Login Button -->
          <button type="submit" class="login-button" :disabled="loading">
            <span v-if="!loading">Sign In</span>
            <span v-else>
              <i class="pi pi-spin pi-spinner"></i>
              Signing in...
            </span>
          </button>
        </form>
      </div>
    </div>

    <!-- Forgot Password Modal -->
    <div v-if="showForgotPasswordModal" class="modal-overlay" @click.self="showForgotPasswordModal = false">
      <div class="forgot-password-modal">
        <div class="modal-header">
          <i class="pi pi-lock"></i>
          <h3>Forgot Your Password?</h3>
          <button @click="showForgotPasswordModal = false" class="modal-close">
            <i class="pi pi-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <p class="modal-message">
            For security reasons, password resets must be handled by your system administrator.
          </p>

          <!-- Password Reset Request Form -->
          <div class="reset-request-form">
            <div class="form-group">
              <label for="reset-username" style="color: #ffffff !important;">Your Username</label>
              <input
                id="reset-username"
                v-model="resetRequest.username"
                type="text"
                placeholder="Enter your username"
                :disabled="resetRequestSent"
              />
            </div>
            
            <div class="form-group">
              <label for="reset-reason" style="color: #ffffff !important;">Reason (Optional)</label>
              <textarea
                id="reset-reason"
                v-model="resetRequest.reason"
                placeholder="Brief reason for password reset..."
                rows="2"
                :disabled="resetRequestSent"
              ></textarea>
            </div>

            <button 
              @click="submitResetRequest" 
              class="btn-submit-request"
              :disabled="!resetRequest.username || resetRequestSent || resetRequestLoading"
            >
              <span v-if="!resetRequestLoading && !resetRequestSent">
                <i class="pi pi-send"></i>
                Submit Reset Request
              </span>
              <span v-else-if="resetRequestLoading">
                <i class="pi pi-spin pi-spinner"></i>
                Sending...
              </span>
              <span v-else>
                <i class="pi pi-check"></i>
                Request Sent
              </span>
            </button>

            <div v-if="resetRequestSent" class="success-message">
              <i class="pi pi-check-circle"></i>
              Your password reset request has been sent to the administrator. You will be contacted shortly.
            </div>

            <div v-if="resetRequestError" class="error-message-modal">
              <i class="pi pi-exclamation-circle"></i>
              {{ resetRequestError }}
            </div>
          </div>

          <div class="divider">
            <span>OR CONTACT DIRECTLY</span>
          </div>
          
          <div class="contact-info">
            <div class="contact-item">
              <i class="pi pi-users"></i>
              <div>
                <strong>Contact IT Support</strong>
                <p>GPD IT Department</p>
              </div>
            </div>
            
            <div class="contact-item">
              <i class="pi pi-envelope"></i>
              <div>
                <strong>Email</strong>
                <p>gpd.support@npc.gov.ph</p>
              </div>
            </div>
            
            <div class="contact-item">
              <i class="pi pi-phone"></i>
              <div>
                <strong>Phone</strong>
                <p>+63 (XX) XXXX-XXXX</p>
              </div>
            </div>
          </div>
          
          <div class="info-box">
            <i class="pi pi-info-circle"></i>
            <p>Your administrator will verify your identity and reset your password securely.</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showForgotPasswordModal = false" class="btn-close-modal">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ThemeControls from './ThemeControls.vue';

export default {
  name: 'LoginPage',
  components: {
    ThemeControls
  },
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      rememberMe: false,
      showPassword: false,
      showForgotPasswordModal: false,
      resetRequest: {
        username: '',
        reason: ''
      },
      resetRequestSent: false,
      resetRequestLoading: false,
      resetRequestError: null,
      loading: false,
      error: null
    };
  },
  mounted() {
    // Check if user just logged out
    const justLoggedOut = sessionStorage.getItem('justLoggedOut');
    
    if (justLoggedOut) {
      // Clear the logout flag
      sessionStorage.removeItem('justLoggedOut');
      
      // Load only username if Remember Me was checked, but NOT password
      const savedUsername = localStorage.getItem('rememberedUsername');
      const wasRemembered = localStorage.getItem('rememberMe') === 'true';
      
      if (wasRemembered && savedUsername) {
        this.credentials.username = savedUsername;
        this.rememberMe = true;
      }
      // Password field stays empty after logout
    } else {
      // Normal page load - load saved credentials if Remember Me was checked
      const savedUsername = localStorage.getItem('rememberedUsername');
      const savedPassword = localStorage.getItem('rememberedPassword');
      const wasRemembered = localStorage.getItem('rememberMe') === 'true';
      
      if (wasRemembered && savedUsername) {
        this.credentials.username = savedUsername;
        if (savedPassword) {
          this.credentials.password = atob(savedPassword); // Decode from base64
        }
        this.rememberMe = true;
      }
    }
  },
  beforeUnmount() {
  },
  methods: {
    generateParticleStyle(index) {
      const size = Math.random() * 4 + 2;
      const left = Math.random() * 100;
      const top = Math.random() * 100;
      const duration = Math.random() * 15 + 10;
      const delay = Math.random() * -15;
      
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${left}%`,
        top: `${top}%`,
        animationDuration: `${duration}s`,
        animationDelay: `${delay}s`,
        opacity: Math.random() * 0.4 + 0.1
      };
    },
    async submitResetRequest() {
      this.resetRequestLoading = true;
      this.resetRequestError = null;

      try {
        await axios.post(
          `${import.meta.env.VITE_APP_API_URL || 'http://localhost:8000/api'}/auth/password_reset_request/`,
          {
            username: this.resetRequest.username,
            reason: this.resetRequest.reason || 'User requested password reset'
          }
        );

        this.resetRequestSent = true;
        
        // Reset form after 5 seconds
        setTimeout(() => {
          this.showForgotPasswordModal = false;
          this.resetRequest = { username: '', reason: '' };
          this.resetRequestSent = false;
        }, 5000);

      } catch (error) {
        console.error('Password reset request error:', error);
        
        if (error.response && error.response.data) {
          this.resetRequestError = error.response.data.detail || error.response.data.error || 'Failed to submit request';
        } else {
          this.resetRequestError = 'Network error. Please contact IT support directly.';
        }
      } finally {
        this.resetRequestLoading = false;
      }
    },
    startBackgroundSlideshow() {
      this.backgroundInterval = setInterval(() => {
        this.currentRiverIndex = (this.currentRiverIndex + 1) % this.riverImages.length;
      }, 5000);
    },
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_APP_API_URL || 'http://localhost:8000/api'}/auth/login/`,
          this.credentials
        );

        // Handle Remember Me
        if (this.rememberMe) {
          localStorage.setItem('rememberedUsername', this.credentials.username);
          localStorage.setItem('rememberedPassword', btoa(this.credentials.password)); // Encode to base64
          localStorage.setItem('rememberMe', 'true');
        } else {
          localStorage.removeItem('rememberedUsername');
          localStorage.removeItem('rememberedPassword');
          localStorage.removeItem('rememberMe');
        }

        // Store user data (session-based auth)
        localStorage.setItem('user', JSON.stringify(response.data.user));
        localStorage.setItem('session_id', response.data.session_id);

        // Redirect to dashboard
        this.$router.push('/');
      } catch (error) {
        console.error('Login error:', error);
        
        if (error.response) {
          if (error.response.status === 401) {
            this.error = 'Invalid username or password';
          } else if (error.response.data && error.response.data.detail) {
            this.error = error.response.data.detail;
          } else {
            this.error = 'Login failed. Please try again.';
          }
        } else {
          this.error = 'Network error. Please check your connection.';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000000;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* Modern Background Styles */
.login-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.mesh-gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(at 0% 0%, #1e3a8a 0%, transparent 50%),
    radial-gradient(at 100% 0%, #1e40af 0%, transparent 50%),
    radial-gradient(at 100% 100%, #1e3a8a 0%, transparent 50%),
    radial-gradient(at 0% 100%, #1e40af 0%, transparent 50%),
    radial-gradient(at 50% 50%, #111827 0%, transparent 50%),
    #0f172a;
  filter: blur(20px);
  animation: meshMove 30s ease-in-out infinite alternate;
}

@keyframes meshMove {
  0% { transform: scale(1) rotate(0deg); }
  100% { transform: scale(1.2) rotate(5deg); }
}

.energy-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.energy-particle {
  position: absolute;
  background: #60a5fa;
  border-radius: 50%;
  filter: blur(1px);
  box-shadow: 0 0 10px #3b82f6;
  animation: floatParticle linear infinite;
}

@keyframes floatParticle {
  0% { transform: translate(0, 0) scale(1); opacity: 0; }
  20% { opacity: 0.6; }
  80% { opacity: 0.6; }
  100% { transform: translate(50px, -150px) scale(0); opacity: 0; }
}

.grain-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3Base-filter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.04;
  pointer-events: none;
  z-index: 2;
}

.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(15, 23, 42, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%);
  z-index: 0;
}

.login-container {
  width: 100%;
  max-width: 620px;
  position: relative;
  z-index: 10;
}

/* Dark card with teal border - matching Sakai exactly */
.login-card {
  background: #1a1a1a;
  border: 2px solid var(--primary-color, #10b981);
  border-radius: 32px;
  padding: 60px 50px;
  box-shadow: 0 0 60px rgba(var(--primary-color-rgb, 16, 185, 129), 0.2);
  position: relative;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  width: 90px;
  height: 90px;
  margin: 0 auto 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border-radius: 50%;
  padding: 0;
}

.logo-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* GenTrack SVG Logo Animations */
.gentrack-logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  background: transparent;
  box-shadow: none;
}

.gentrack-svg {
  width: 100px;
  height: 100px;
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.4));
}

.logo-hex {
  stroke-dasharray: 260;
  stroke-dashoffset: 0;
  animation: drawHex 4s ease-in-out infinite alternate;
}

.logo-bolt {
  transform-origin: center;
  animation: pulseBolt 2s infinite alternate;
}

.logo-node {
  animation: blinkNode 2s infinite;
}

.logo-node:nth-child(3) { animation-delay: 0s; }
.logo-node:nth-child(4) { animation-delay: 0.5s; }
.logo-node:nth-child(5) { animation-delay: 1s; }
.logo-node:nth-child(6) { animation-delay: 1.5s; }

@keyframes drawHex {
  0% { stroke-dashoffset: 260; }
  50% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: 0; }
}

@keyframes pulseBolt {
  0% { transform: scale(0.95); fill: #3b82f6; }
  100% { transform: scale(1.05); fill: #93c5fd; }
}

@keyframes blinkNode {
  0%, 100% { opacity: 0.3; r: 3; fill: #fb923c; }
  50% { opacity: 1; r: 5; fill: #fde047; }
}

.login-header h2 {
  margin: 0 0 12px 0;
  color: #ffffff;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.login-header p {
  margin: 0;
  color: #9ca3af;
  font-size: 15px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-group label {
  font-weight: 400;
  color: #e5e7eb;
  font-size: 15px;
}

.form-group input {
  padding: 14px 18px;
  border: 1px solid #374151;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s;
  background: #0a0a0a;
  color: #ffffff;
}

.form-group input::placeholder {
  color: #6b7280;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color, #10b981);
  background: #0f0f0f;
}

.form-group input:disabled {
  background: #1a1a1a;
  cursor: not-allowed;
  color: #6b7280;
}

.password-input {
  position: relative;
}

.password-input input {
  width: 100%;
  padding-right: 50px;
}

.toggle-password {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
  width: auto; /* Ensure it only takes needed space */
  height: auto;
  min-width: unset;
}

.toggle-password:hover {
  color: var(--primary-color, #10b981);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -8px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #d1d5db;
  font-size: 14px;
  cursor: pointer;
  user-select: none;
}

.remember-me input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary-color, #10b981);
  border-radius: 4px;
}

.forgot-password {
  color: var(--primary-color, #10b981);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.forgot-password:hover {
  color: var(--primary-hover, #059669);
}

.error-message {
  padding: 14px 18px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.login-button {
  padding: 14px 24px;
  background: var(--primary-color, #10b981);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
}

.login-button:hover:not(:disabled) {
  background: var(--primary-hover, #059669);
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(var(--primary-color-rgb, 16, 185, 129), 0.3);
}

.login-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .login-card {
    padding: 40px 30px;
    border-radius: 24px;
  }

  .login-header h2 {
    font-size: 24px;
  }

  .logo-icon {
    width: 60px;
    height: 60px;
  }

  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}

/* Back Button */
.back-button {
  position: fixed;
  top: 24px;
  left: 24px;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #1a1a1a;
  border: 1px solid #374151;
  border-radius: 8px;
  color: #e5e7eb;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: #262626;
  border-color: var(--primary-color, #10b981);
  color: var(--primary-color, #10b981);
  transform: translateX(-2px);
}

.back-button i {
  font-size: 14px;
}

/* Forgot Password Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.forgot-password-modal {
  background: rgba(26, 26, 26, 0.98);
  border: 2px solid var(--primary-color, #10b981);
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(var(--primary-color-rgb, 16, 185, 129), 0.2);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 24px 24px 20px;
  border-bottom: 1px solid #374151;
  position: relative;
  text-align: center;
}

.modal-header i.pi-lock {
  font-size: 48px;
  color: #ffffff !important;
  margin-bottom: 12px;
}

.modal-header h3 {
  margin: 0;
  color: #ffffff !important;
  font-size: 22px;
  font-weight: 600;
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  color: #ffffff !important;
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #ef4444 !important;
}

.modal-body {
  padding: 24px;
}

.modal-message {
  color: #ffffff !important;
  font-size: 15px;
  line-height: 1.6;
  margin: 0 0 24px 0;
  text-align: center;
}

.reset-request-form {
  margin-bottom: 24px;
}

.reset-request-form .form-group {
  margin-bottom: 16px;
}

.reset-request-form label {
  display: block;
  color: #ffffff !important;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
}

.reset-request-form input,
.reset-request-form textarea {
  width: 100%;
  padding: 12px 14px;
  background: #0a0a0a;
  border: 1px solid #374151;
  border-radius: 8px;
  color: #ffffff !important;
  font-size: 14px;
  transition: all 0.2s;
  font-family: inherit;
  resize: vertical;
}

.reset-request-form input::placeholder,
.reset-request-form textarea::placeholder {
  color: #6b7280 !important;
}

.reset-request-form input:focus,
.reset-request-form textarea:focus {
  outline: none;
  border-color: var(--primary-color, #10b981);
  background: #0f0f0f;
}

.reset-request-form input:disabled,
.reset-request-form textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit-request {
  width: 100%;
  padding: 12px 24px;
  background: var(--primary-color, #10b981);
  color: #ffffff !important;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

.btn-submit-request:hover:not(:disabled) {
  background: var(--primary-hover, #059669);
  transform: translateY(-1px);
}

.btn-submit-request:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.success-message {
  margin-top: 16px;
  padding: 12px;
  background: rgba(var(--primary-color-rgb, 16, 185, 129), 0.15);
  border: 1px solid rgba(var(--primary-color-rgb, 16, 185, 129), 0.4);
  border-radius: 8px;
  color: var(--primary-color, #10b981) !important;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-message-modal {
  margin-top: 16px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 8px;
  color: #fca5a5 !important;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.divider {
  position: relative;
  text-align: center;
  margin: 24px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #374151;
}

.divider span {
  position: relative;
  background: #1a1a1a;
  padding: 0 12px;
  color: #ffffff !important;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px;
  background: #0a0a0a;
  border: 1px solid #374151;
  border-radius: 8px;
  transition: all 0.2s;
}

.contact-item:hover {
  border-color: var(--primary-color, #10b981);
  background: #0f0f0f;
}

.contact-item i {
  font-size: 20px;
  color: #ffffff !important;
  margin-top: 2px;
}

.contact-item strong {
  display: block;
  color: #ffffff !important;
  font-size: 14px;
  margin-bottom: 4px;
  font-weight: 600;
}

.contact-item p {
  margin: 0;
  color: #ffffff !important;
  font-size: 14px;
  line-height: 1.4;
}

.info-box {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px;
  background: rgba(var(--primary-color-rgb, 16, 185, 129), 0.1);
  border: 1px solid rgba(var(--primary-color-rgb, 16, 185, 129), 0.3);
  border-radius: 8px;
}

.info-box i {
  font-size: 18px;
  color: #ffffff !important;
  margin-top: 2px;
  flex-shrink: 0;
}

.info-box p {
  margin: 0;
  color: #ffffff !important;
  font-size: 13px;
  line-height: 1.5;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #374151;
  display: flex;
  justify-content: center;
}

.btn-close-modal {
  padding: 10px 32px;
  background: #374151;
  color: #ffffff !important;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-close-modal:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

@media (max-width: 480px) {
  .forgot-password-modal {
    margin: 10px;
    max-width: calc(100vw - 20px);
    border-radius: 12px;
  }
  
  .modal-header {
    padding: 16px 16px 12px;
  }
  
  .modal-header i.pi-lock {
    font-size: 36px;
    margin-bottom: 8px;
  }
  
  .modal-header h3 {
    font-size: 18px;
  }
  
  .modal-close {
    top: 12px;
    right: 12px;
    font-size: 18px;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .modal-message {
    font-size: 13px;
    margin-bottom: 16px;
  }
  
  .reset-request-form .form-group {
    margin-bottom: 12px;
  }
  
  .reset-request-form label {
    font-size: 13px;
    margin-bottom: 6px;
  }
  
  .reset-request-form input,
  .reset-request-form textarea {
    padding: 10px 12px;
    font-size: 13px;
  }
  
  .btn-submit-request {
    padding: 10px 20px;
    font-size: 13px;
    margin-top: 12px;
  }
  
  .divider {
    margin: 16px 0;
  }
  
  .divider span {
    font-size: 11px;
  }
  
  .contact-info {
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .contact-item {
    padding: 10px;
    gap: 10px;
  }
  
  .contact-item i {
    font-size: 16px;
  }
  
  .contact-item strong {
    font-size: 13px;
    margin-bottom: 2px;
  }
  
  .contact-item p {
    font-size: 12px;
  }
  
  .info-box {
    padding: 10px;
    gap: 10px;
  }
  
  .info-box i {
    font-size: 16px;
  }
  
  .info-box p {
    font-size: 12px;
  }
  
  .modal-footer {
    padding: 12px 16px;
  }
  
  .btn-close-modal {
    padding: 8px 24px;
    font-size: 13px;
  }
  
  .success-message,
  .error-message-modal {
    padding: 10px;
    font-size: 12px;
    margin-top: 12px;
  }
}
</style>
