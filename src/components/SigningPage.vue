<template>
  <div class="signing-page">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-content">
        <i class="pi pi-spin pi-spinner"></i>
        <h3>Verifying signature request...</h3>
        <p>Please wait while we validate your signature link.</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-content">
        <i class="pi pi-exclamation-triangle"></i>
        <h3>Signature Request Error</h3>
        <p>{{ error }}</p>
        <div class="error-actions">
          <button class="btn-primary" @click="$router.push('/')">
            Return to Home
          </button>
        </div>
      </div>
    </div>

    <!-- Signature Pad -->
    <SignaturePad
      v-else-if="!signatureComplete"
      :token="token"
      @signed="handleSignatureComplete"
      @cancel="handleCancel"
      @error="handleError"
      @complete="handleComplete"
    />

    <!-- Completion State -->
    <div v-else class="completion-container">
      <div class="completion-content">
        <i class="pi pi-check-circle"></i>
        <h3>Document Signed Successfully!</h3>
        <p>Your digital signature has been recorded and the document has been signed.</p>
        <p>You will receive a confirmation email shortly.</p>
        <div class="completion-actions">
          <button class="btn-primary" @click="$router.push('/')">
            Return to Home
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SignaturePad from './SignaturePad.vue'
import api from '../services/api'

export default {
  name: 'SigningPage',
  components: {
    SignaturePad
  },
  data() {
    return {
      loading: true,
      error: null,
      signatureComplete: false,
      token: null
    }
  },
  async mounted() {
    // Get token from route params
    this.token = this.$route.params.token
    
    if (!this.token) {
      this.error = 'Invalid signature link - no token provided'
      this.loading = false
      return
    }
    
    // Verify token
    await this.verifyToken()
  },
  methods: {
    async verifyToken() {
      try {
        await api.verifySignatureToken(this.token)
        this.loading = false
      } catch (error) {
        console.error('Token verification failed:', error)
        
        if (error.response?.status === 404) {
          this.error = 'Invalid signature link - token not found'
        } else if (error.response?.status === 400) {
          this.error = error.response.data.error || 'Signature request has expired or is no longer valid'
        } else {
          this.error = 'Unable to verify signature request. Please try again later.'
        }
        
        this.loading = false
      }
    },
    
    handleSignatureComplete() {
      this.signatureComplete = true
    },
    
    handleCancel() {
      if (confirm('Are you sure you want to cancel signing this document?')) {
        this.$router.push('/')
      }
    },
    
    handleError(error) {
      this.error = error
      this.loading = false
    },
    
    handleComplete() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.signing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.loading-container,
.error-container,
.completion-container {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.loading-content i,
.error-content i,
.completion-content i {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.loading-content i {
  color: #4f46e5;
}

.error-content i {
  color: #ef4444;
}

.completion-content i {
  color: #22c55e;
}

.loading-content h3,
.error-content h3,
.completion-content h3 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.loading-content p,
.error-content p,
.completion-content p {
  color: #64748b;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.error-actions,
.completion-actions {
  margin-top: 2rem;
}

.btn-primary {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #4338ca;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .signing-page {
    padding: 1rem;
  }
  
  .loading-container,
  .error-container,
  .completion-container {
    padding: 2rem;
  }
}
</style>
