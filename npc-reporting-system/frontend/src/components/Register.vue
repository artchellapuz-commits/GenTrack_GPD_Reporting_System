<template>
  <div class="register-page">
    <!-- Background Slideshow -->
    <div class="background-slideshow">
      <img 
        v-for="(image, index) in riverImages" 
        :key="index"
        :src="image" 
        alt="" 
        class="background-image"
        :class="{ 'active': index === currentRiverIndex }"
      />
    </div>
    <div class="background-overlay"></div>

    <!-- Theme Controls -->
    <ThemeControls />

    <!-- Back Button -->
    <router-link to="/" class="back-button">
      <i class="pi pi-arrow-left"></i>
      Back to Home
    </router-link>
    
    <div class="register-container">
      <div class="register-card">
        <!-- Logo and Title -->
        <div class="register-header">
          <div class="logo-icon">
            <img src="@/assets/NPC-logo.png" alt="GenTrack Logo" />
          </div>
          <h2>Create an Account</h2>
          <p>Sign up to get started</p>
        </div>

        <!-- Register Form -->
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">First Name</label>
              <input
                id="first_name"
                v-model="formData.first_name"
                type="text"
                placeholder="First name"
                required
                :disabled="loading"
              />
            </div>
            <div class="form-group">
              <label for="last_name">Last Name</label>
              <input
                id="last_name"
                v-model="formData.last_name"
                type="text"
                placeholder="Last name"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="Username"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="Email address"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="password-input">
              <input
                id="password"
                v-model="formData.password"
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
            <small>At least 8 characters</small>
          </div>

          <div class="form-group">
            <label for="password2">Confirm Password</label>
            <div class="password-input">
              <input
                id="password2"
                v-model="formData.password2"
                :type="showPassword2 ? 'text' : 'password'"
                placeholder="Confirm password"
                required
                :disabled="loading"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword2 = !showPassword2"
                :disabled="loading"
              >
                <i :class="showPassword2 ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="error-message">
            <i class="pi pi-exclamation-circle"></i>
            {{ error }}
          </div>

          <!-- Register Button -->
          <button type="submit" class="register-button" :disabled="loading">
            <span v-if="!loading">Create Account</span>
            <span v-else>
              <i class="pi pi-spin pi-spinner"></i>
              Creating account...
            </span>
          </button>

          <!-- Login Link -->
          <div class="login-link">
            Already have an account?
            <router-link to="/login">Sign in</router-link>
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
  name: 'RegisterPage',
  components: {
    ThemeControls
  },
  data() {
    return {
      currentRiverIndex: 0,
      riverImages: [
        require('@/assets/River1.jpg'),
        require('@/assets/River2.jpg'),
        require('@/assets/River3.jpg'),
        require('@/assets/River4.jpg'),
        require('@/assets/River5.jpg'),
        require('@/assets/River6.jpg'),
        require('@/assets/River7.jpg'),
        require('@/assets/River8.jpg'),
        require('@/assets/River9.jpg'),
        require('@/assets/River10.jpg'),
        require('@/assets/River11.jpg'),
        require('@/assets/River12.jpg'),
        require('@/assets/River13.jpg'),
        require('@/assets/River14.jpg'),
        require('@/assets/River15.jpg'),
        require('@/assets/River16.jpg'),
        require('@/assets/River17.jpg')
      ],
      formData: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        password2: ''
      },
      showPassword: false,
      showPassword2: false,
      loading: false,
      error: null
    };
  },
  mounted() {
    this.startBackgroundSlideshow();
  },
  beforeUnmount() {
    if (this.backgroundInterval) {
      clearInterval(this.backgroundInterval);
    }
  },
  methods: {
    startBackgroundSlideshow() {
      this.backgroundInterval = setInterval(() => {
        this.currentRiverIndex = (this.currentRiverIndex + 1) % this.riverImages.length;
      }, 5000);
    },
    async handleRegister() {
      this.loading = true;
      this.error = null;

      if (this.formData.password !== this.formData.password2) {
        this.error = 'Passwords do not match';
        this.loading = false;
        return;
      }

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/auth/register/`,
          this.formData
        );

        localStorage.setItem('access_token', response.data.tokens.access);
        localStorage.setItem('refresh_token', response.data.tokens.refresh);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.tokens.access}`;

        this.$router.push('/');
      } catch (error) {
        console.error('Registration error:', error);
        
        if (error.response && error.response.data) {
          const errors = error.response.data;
          if (errors.username) {
            this.error = `Username: ${errors.username[0]}`;
          } else if (errors.email) {
            this.error = `Email: ${errors.email[0]}`;
          } else if (errors.password) {
            this.error = `Password: ${errors.password[0]}`;
          } else {
            this.error = 'Registration failed. Please try again.';
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
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000000;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* Background Slideshow */
.background-slideshow {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 2s ease-in-out;
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
  image-rendering: high-quality;
}

.background-image.active {
  opacity: 1;
  z-index: 1;
}

.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(51, 65, 85, 0.7) 100%);
  z-index: 1;
}

.register-container {
  width: 100%;
  max-width: 650px;
  position: relative;
  z-index: 10;
}

/* Dark card with green border - matching Sakai */
.register-card {
  background: #1a1a1a;
  border: 2px solid #10b981;
  border-radius: 32px;
  padding: 50px 50px;
  box-shadow: 0 0 60px rgba(16, 185, 129, 0.2);
  position: relative;
}

.register-header {
  text-align: center;
  margin-bottom: 36px;
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

.register-header h2 {
  margin: 0 0 12px 0;
  color: #ffffff;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.register-header p {
  margin: 0;
  color: #9ca3af;
  font-size: 15px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
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

.form-group small {
  color: #9ca3af;
  font-size: 13px;
  margin-top: -6px;
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

.register-button {
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
  margin-top: 8px;
}

.register-button:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.register-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  font-size: 14px;
  color: #9ca3af;
  padding-top: 8px;
}

.login-link a {
  color: #10b981;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  color: #059669;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .register-card {
    padding: 40px 30px;
    border-radius: 24px;
  }

  .register-header h2 {
    font-size: 24px;
  }

  .logo-icon {
    width: 60px;
    height: 60px;
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
