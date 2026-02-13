<template>
  <div class="login-page">
    <!-- Floating gradient orbs -->
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    
    <!-- Back Button -->
    <router-link to="/" class="back-button">
      <i class="pi pi-arrow-left"></i>
      Back to Home
    </router-link>
    
    <div class="login-container">
      <div class="login-card">
        <!-- Logo and Title -->
        <div class="login-header">
          <div class="logo">
            <img src="@/assets/NPC-logo.png" alt="NPC Logo" />
          </div>
          <h2>NPC Reporting System</h2>
          <p>Agus Hydro-Electric Power Plants</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">
              <i class="pi pi-user"></i>
              Username
            </label>
            <input
              id="username"
              v-model="credentials.username"
              type="text"
              placeholder="Enter your username"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">
              <i class="pi pi-lock"></i>
              Password
            </label>
            <div class="password-input">
              <input
                id="password"
                v-model="credentials.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter your password"
                required
                :disabled="loading"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
                :disabled="loading"
              >
                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="error-message">
            <i class="pi pi-exclamation-circle"></i>
            {{ error }}
          </div>

          <!-- Login Button -->
          <button type="submit" class="login-button" :disabled="loading">
            <span v-if="!loading">
              <!-- <i class="pi pi-sign-in"></i> -->
              Login
            </span>
            <span v-else>
              <i class="pi pi-spin pi-spinner"></i>
              Logging in...
            </span>
          </button>

          <!-- Register Link -->
          <div class="register-link">
            Don't have an account?
            <router-link to="/register">Register here</router-link>
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="login-footer">
        <p>&copy; 2026 National Power Corporation. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      showPassword: false,
      loading: false,
      error: null
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/login/`,
          this.credentials
        );

        // Store tokens
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        // Set default authorization header
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;

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
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 0;
  position: relative;
  overflow: hidden;
}

/* NPC Logo watermark background */
.login-page::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 1200px;
  height: 100%;
  max-height: 1200px;
  background-image: url('@/assets/NPC-logo.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.09;
  z-index: 1;
  pointer-events: none;
}

/* Animated stars background */
.login-page::before {
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
}

.login-container {
  width: 100%;
  max-width: 450px;
  position: relative;
  z-index: 10;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}

/* Glassmorphic card */
.login-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.37),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
  position: relative;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 110px;
  height: 110px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
}

.login-header h2 {
  margin: 0 0 8px 0;
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.login-header p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group label i {
  color: rgba(102, 126, 234, 0.8);
}

.form-group input {
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: #ffffff;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-group input:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.6);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}

.form-group input:disabled {
  background: rgba(255, 255, 255, 0.05);
  cursor: not-allowed;
}

.password-input {
  position: relative;
}

.password-input input {
  width: 100%;
  padding-right: 45px;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-password:hover {
  color: rgba(102, 126, 234, 0.9);
}

.error-message {
  padding: 12px 16px;
  background: rgba(255, 100, 100, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 12px;
  color: #ffcccc;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-button {
  padding: 14px 24px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  background: linear-gradient(135deg, rgba(102, 126, 234, 1) 0%, rgba(118, 75, 162, 1) 100%);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
}

.login-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.register-link a {
  color: rgba(102, 126, 234, 0.9);
  text-decoration: none;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}

.register-link a:hover {
  color: rgba(118, 75, 162, 1);
  text-decoration: underline;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }

  .login-header h2 {
    font-size: 20px;
  }

  .logo {
    width: 100px;
    height: 100px;
  }

  .orb {
    display: none;
  }
}

/* Floating gradient orbs */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 20s infinite ease-in-out;
  z-index: 1;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255, 105, 180, 0.6) 0%, rgba(255, 105, 180, 0) 70%);
  top: -10%;
  left: -10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.6) 0%, rgba(102, 126, 234, 0) 70%);
  bottom: -15%;
  right: -15%;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(118, 75, 162, 0.6) 0%, rgba(118, 75, 162, 0) 70%);
  top: 40%;
  right: -10%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

/* Back Button */
.back-button {
  position: fixed;
  top: 30px;
  left: 30px;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(102, 126, 234, 0.5);
  transform: translateX(-5px);
}

.back-button i {
  font-size: 1rem;
}
</style>
