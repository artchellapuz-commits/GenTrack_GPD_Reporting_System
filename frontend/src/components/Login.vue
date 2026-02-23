<template>
  <div class="login-page">
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
          <div class="logo-icon">
            <img src="@/assets/NPC-logo.png" alt="GPD Logo" />
          </div>
          <h2>Welcome to GPD Reporting System!</h2>
          <p>Sign in to continue</p>
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
                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="rememberMe" />
              <span>Remember me</span>
            </label>
            <a href="#" class="forgot-password">Forgot password?</a>
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

          <!-- Register Link -->
          <div class="register-link">
            Don't have an account?
            <router-link to="/register">Register here</router-link>
          </div>
        </form>
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
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/login/`,
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
  background: #000000;
  padding: 20px;
  position: relative;
  overflow: hidden;
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
  border: 2px solid #10b981;
  border-radius: 32px;
  padding: 60px 50px;
  box-shadow: 0 0 60px rgba(16, 185, 129, 0.2);
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
  border-color: #10b981;
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
}

.toggle-password:hover {
  color: #10b981;
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
  accent-color: #10b981;
  border-radius: 4px;
}

.forgot-password {
  color: #10b981;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.forgot-password:hover {
  color: #059669;
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
  background: #10b981;
  color: #000000;
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
  background: #059669;
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.login-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  font-size: 14px;
  color: #9ca3af;
  padding-top: 12px;
}

.register-link a {
  color: #10b981;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  color: #059669;
  text-decoration: underline;
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
  border-color: #10b981;
  color: #10b981;
  transform: translateX(-2px);
}

.back-button i {
  font-size: 14px;
}
</style>
