<template>
  <div class="signature-setup-container">
    <div class="setup-card" v-if="!loading && !error">
      <div class="header">
        <h2>🖊️ E-Signature Setup</h2>
        <p class="subtitle">Create your digital signature for the NPC Reporting System</p>
      </div>

      <div class="user-info">
        <div class="info-row">
          <strong>User:</strong> {{ setupData.user_name }}
        </div>
        <div class="info-row">
          <strong>Signatory Name:</strong> {{ setupData.signatory_name }}
        </div>
        <div class="info-row" v-if="setupData.requires_2fa">
          <strong>Security:</strong> <span class="security-badge">2FA Required</span>
        </div>
      </div>

      <div class="signature-section">
        <h3>Draw Your Signature</h3>
        <p class="instruction" v-if="!success">Use your mouse or touch screen to draw your signature in the box below:</p>
        <p class="instruction success-instruction" v-if="success">✅ Your signature has been saved and is ready to use!</p>
        
        <div class="signature-pad-container" :class="{ 'disabled': success }">
          <canvas 
            ref="signatureCanvas"
            @mousedown="startDrawing"
            @mousemove="draw"
            @mouseup="stopDrawing"
            @touchstart="startDrawing"
            @touchmove="draw"
            @touchend="stopDrawing"
            class="signature-canvas"
            :class="{ 'disabled': success }"
          ></canvas>
          <div v-if="success" class="canvas-overlay">
            <div class="overlay-content">
              <span class="overlay-icon">✅</span>
              <span class="overlay-text">Signature Saved</span>
            </div>
          </div>
        </div>

        <div class="signature-controls">
          <button @click="clearSignature" :disabled="success" class="btn-clear">
            🗑️ Clear
          </button>
          <button @click="saveSignature" :disabled="saving || !hasSignature || success" class="btn-save">
            {{ saving ? '💾 Saving...' : success ? '✅ Signature Saved' : '✅ Save Signature' }}
          </button>
        </div>
      </div>

      <div class="security-notice">
        <p><strong>🔒 Security Notice:</strong></p>
        <ul>
          <li>This link is valid for 24 hours only</li>
          <li>Your signature will be securely stored and encrypted</li>
          <li>Once saved, you can immediately use it to sign reports</li>
        </ul>
      </div>
    </div>

    <div class="loading-card" v-if="loading">
      <div class="spinner"></div>
      <p>Loading signature setup...</p>
    </div>

    <div class="error-card" v-if="error">
      <h3>❌ Setup Error</h3>
      <p>{{ error }}</p>
      <p class="help-text">Please contact your Data Manager or System Administrator for assistance.</p>
    </div>



    <!-- Success Modal Overlay -->
    <div class="success-modal-overlay" v-if="showSuccessModal" @click="closeSuccess">
      <div class="success-modal" @click.stop>
        <div class="success-icon">
          <div class="checkmark">
            <div class="checkmark-circle">
              <div class="checkmark-stem"></div>
              <div class="checkmark-kick"></div>
            </div>
          </div>
        </div>
        <h3>Signature Saved Successfully!</h3>
        <p class="success-message">{{ successMessage }}</p>
        <div class="success-details">
          <p>✅ Your digital signature has been securely stored</p>
          <p>✅ You can now use your e-signature to sign reports</p>
          <p>✅ This window can be safely closed</p>
        </div>
        <div class="close-window-notice">
          <div class="notice-icon">🪟</div>
          <div class="notice-content">
            <p class="notice-title">You can now close this browser window/tab</p>
            <p class="notice-subtitle">Your signature setup is complete and ready to use in the NPC Reporting System</p>
          </div>
        </div>
        <div class="success-actions">
          <button @click="closeSuccess" class="btn-close-success">
            Continue to NPC Reporting System
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SignatureSetup',
  data() {
    return {
      loading: true,
      error: null,
      success: false,
      showSuccessModal: false,
      successMessage: '',
      saving: false,
      setupData: {},
      isDrawing: false,
      hasSignature: false,
      ctx: null
    }
  },
  async mounted() {
    const token = this.$route.params.token
    if (!token) {
      this.error = 'Invalid setup link. No token provided.'
      this.loading = false
      return
    }

    try {
      const response = await axios.get(`/api/signatory-authorizations/signature-setup/${token}/`)
      this.setupData = response.data
      this.loading = false
      
      // Initialize canvas
      this.$nextTick(() => {
        this.initCanvas()
      })
    } catch (err) {
      this.error = err.response?.data?.error || 'Failed to load setup data'
      this.loading = false
    }
  },
  methods: {
    initCanvas() {
      const canvas = this.$refs.signatureCanvas
      if (!canvas) return
      
      canvas.width = 600
      canvas.height = 200
      this.ctx = canvas.getContext('2d')
      this.ctx.strokeStyle = '#000'
      this.ctx.lineWidth = 2
      this.ctx.lineCap = 'round'
      
      // Add border
      this.ctx.strokeStyle = '#ddd'
      this.ctx.lineWidth = 1
      this.ctx.strokeRect(0, 0, canvas.width, canvas.height)
      
      // Reset for drawing
      this.ctx.strokeStyle = '#000'
      this.ctx.lineWidth = 2
    },
    
    getEventPos(e) {
      const canvas = this.$refs.signatureCanvas
      const rect = canvas.getBoundingClientRect()
      const clientX = e.clientX || (e.touches && e.touches[0].clientX)
      const clientY = e.clientY || (e.touches && e.touches[0].clientY)
      
      return {
        x: clientX - rect.left,
        y: clientY - rect.top
      }
    },
    
    startDrawing(e) {
      if (this.success) return // Disable drawing after success
      e.preventDefault()
      this.isDrawing = true
      const pos = this.getEventPos(e)
      this.ctx.beginPath()
      this.ctx.moveTo(pos.x, pos.y)
      this.hasSignature = true
    },
    
    draw(e) {
      if (!this.isDrawing || this.success) return // Disable drawing after success
      e.preventDefault()
      
      const pos = this.getEventPos(e)
      this.ctx.lineTo(pos.x, pos.y)
      this.ctx.stroke()
    },
    
    stopDrawing(e) {
      if (!this.isDrawing || this.success) return // Disable drawing after success
      e.preventDefault()
      this.isDrawing = false
    },
    
    clearSignature() {
      if (this.success) return // Disable clearing after success
      const canvas = this.$refs.signatureCanvas
      this.ctx.clearRect(0, 0, canvas.width, canvas.height)
      this.initCanvas()
      this.hasSignature = false
    },
    
    async saveSignature() {
      if (!this.hasSignature) return
      
      this.saving = true
      try {
        const canvas = this.$refs.signatureCanvas
        const signatureData = canvas.toDataURL('image/png')
        
        const token = this.$route.params.token
        const response = await axios.post(`/api/signatory-authorizations/save-signature/${token}/`, {
          signature: signatureData
        })
        
        this.success = true
        this.showSuccessModal = true
        this.successMessage = response.data.message || 'Signature saved successfully! You can now use your e-signature to sign reports.'
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to save signature')
      } finally {
        this.saving = false
      }
    },

    closeSuccess() {
      // Hide the success modal but keep buttons disabled
      this.showSuccessModal = false
      // Don't reset this.success = false to keep buttons disabled
    }
  }
}
</script>

<style scoped>
.signature-setup-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.setup-card, .loading-card, .error-card, .success-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  padding: 30px;
  max-width: 700px;
  width: 100%;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: 28px;
}

.subtitle {
  color: #666;
  font-size: 16px;
}

.user-info {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
}

.info-row {
  margin-bottom: 10px;
  font-size: 16px;
}

.security-badge {
  background: #28a745;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.signature-section h3 {
  color: #333;
  margin-bottom: 10px;
}

.instruction {
  color: #666;
  margin-bottom: 20px;
}

.success-instruction {
  color: #28a745;
  font-weight: 600;
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
  padding: 10px 15px;
}

.signature-pad-container {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 20px;
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
}

.signature-pad-container.disabled {
  opacity: 0.6;
  border-color: #28a745;
  background-color: #f8f9fa;
}

.signature-canvas {
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: crosshair;
  background: white;
  transition: all 0.3s ease;
}

.signature-canvas.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.canvas-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(40, 167, 69, 0.9);
  color: white;
  padding: 15px 25px;
  border-radius: 25px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
  animation: fadeInScale 0.5s ease-out;
}

.overlay-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.overlay-icon {
  font-size: 1.2rem;
}

.overlay-text {
  font-size: 1rem;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

.signature-controls {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-clear, .btn-save {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-clear {
  background: #dc3545;
  color: white;
}

.btn-clear:hover {
  background: #c82333;
}

.btn-save {
  background: #28a745;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #218838;
}

.btn-clear:disabled, .btn-save:disabled {
  background: #6c757d;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-clear:disabled:hover, .btn-save:disabled:hover {
  background: #6c757d;
  transform: none;
}

.security-notice {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 15px;
  margin-top: 30px;
  border-radius: 4px;
}

.security-notice ul {
  margin: 10px 0 0 20px;
}

.loading-card, .error-card, .success-card {
  text-align: center;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-card h3 {
  color: #dc3545;
}

.success-card h3 {
  color: #28a745;
}

.help-text, .next-steps {
  color: #666;
  font-style: italic;
  margin-top: 15px;
}

/* Success Modal Styles */
.success-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.success-modal {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 40px;
  max-width: 500px;
  width: 90%;
  text-align: center;
  animation: slideInUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}

.success-icon {
  margin-bottom: 20px;
}

.checkmark {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: block;
  stroke-width: 3;
  stroke: #28a745;
  stroke-miterlimit: 10;
  margin: 0 auto 20px;
  box-shadow: inset 0px 0px 0px #28a745;
  animation: fill 0.4s ease-in-out 0.4s forwards, scale 0.3s ease-in-out 0.9s both;
}

.checkmark-circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 3;
  stroke-miterlimit: 10;
  stroke: #28a745;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  position: relative;
  background: #f8f9fa;
  border: 3px solid #28a745;
}

.checkmark-stem {
  position: absolute;
  width: 3px;
  height: 20px;
  background: #28a745;
  left: 32px;
  top: 25px;
  transform: rotate(45deg);
  transform-origin: bottom;
  animation: checkmark-stem 0.3s ease-in-out 0.7s forwards;
  opacity: 0;
}

.checkmark-kick {
  position: absolute;
  width: 3px;
  height: 12px;
  background: #28a745;
  left: 25px;
  top: 35px;
  transform: rotate(-45deg);
  transform-origin: bottom;
  animation: checkmark-kick 0.3s ease-in-out 0.8s forwards;
  opacity: 0;
}

.success-modal h3 {
  color: #28a745;
  font-size: 28px;
  margin-bottom: 15px;
  font-weight: 700;
}

.success-message {
  color: #333;
  font-size: 16px;
  margin-bottom: 25px;
  line-height: 1.5;
}

.success-details {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  text-align: left;
}

.success-details p {
  margin: 8px 0;
  color: #28a745;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-actions {
  display: flex;
  justify-content: center;
}

.close-window-notice {
  background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
  border: 2px solid #28a745;
  border-radius: 15px;
  padding: 20px;
  margin: 25px 0;
  display: flex;
  align-items: center;
  gap: 15px;
  animation: slideInLeft 0.5s ease-out 1.2s both;
}

.notice-icon {
  font-size: 2.5rem;
  animation: bounce 1s ease-in-out 1.5s infinite;
}

.notice-content {
  flex: 1;
  text-align: left;
}

.notice-title {
  font-size: 18px;
  font-weight: 700;
  color: #155724;
  margin: 0 0 5px 0;
}

.notice-subtitle {
  font-size: 14px;
  color: #155724;
  margin: 0;
  opacity: 0.8;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.btn-close-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.btn-close-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes fill {
  100% {
    box-shadow: inset 0px 0px 0px 60px #28a745;
  }
}

@keyframes scale {
  0%, 100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes checkmark-stem {
  0% {
    opacity: 0;
    transform: rotate(45deg) scaleY(0);
  }
  100% {
    opacity: 1;
    transform: rotate(45deg) scaleY(1);
  }
}

@keyframes checkmark-kick {
  0% {
    opacity: 0;
    transform: rotate(-45deg) scaleY(0);
  }
  100% {
    opacity: 1;
    transform: rotate(-45deg) scaleY(1);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .success-modal {
    padding: 30px 20px;
    margin: 20px;
  }
  
  .checkmark {
    width: 60px;
    height: 60px;
  }
  
  .checkmark-circle {
    width: 60px;
    height: 60px;
  }
  
  .success-modal h3 {
    font-size: 24px;
  }
  
  .success-message {
    font-size: 14px;
  }
  
  .close-window-notice {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .notice-icon {
    font-size: 2rem;
  }
  
  .notice-content {
    text-align: center;
  }
}
</style>
