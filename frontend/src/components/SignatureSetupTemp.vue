<template>
  <div class="signature-setup-container">
    <div class="setup-card">
      <div class="header">
        <h2>🖊️ E-Signature Setup</h2>
        <p class="subtitle">Create your digital signature for the NPC Reporting System</p>
      </div>

      <div class="user-info">
        <div class="info-row">
          <strong>Signatory Name:</strong> JMM MATA
        </div>
        <div class="info-row">
          <strong>Security:</strong> <span class="security-badge">2FA Required</span>
        </div>
      </div>

      <div class="signature-section">
        <h3>Draw Your Signature</h3>
        <p class="instruction">Use your mouse or touch screen to draw your signature in the box below:</p>
        
        <div class="signature-pad-container">
          <canvas 
            ref="signatureCanvas"
            @mousedown="startDrawing"
            @mousemove="draw"
            @mouseup="stopDrawing"
            @touchstart="startDrawing"
            @touchmove="draw"
            @touchend="stopDrawing"
            class="signature-canvas"
          ></canvas>
        </div>

        <div class="signature-controls">
          <button @click="clearSignature" class="btn-clear">
            🗑️ Clear
          </button>
          <button @click="saveSignature" :disabled="saving || !hasSignature" class="btn-save">
            {{ saving ? '💾 Saving...' : '✅ Save Signature' }}
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

    <div class="success-card" v-if="success">
      <h3>🎉 Signature Saved Successfully!</h3>
      <p>{{ successMessage }}</p>
      <p class="next-steps">You can now close this window and use your e-signature in the NPC Reporting System.</p>
    </div>

    <div class="error-card" v-if="error">
      <h3>❌ Setup Error</h3>
      <p>{{ error }}</p>
      <p class="help-text">Please contact your Data Manager or System Administrator for assistance.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SignatureSetupTemp',
  data() {
    return {
      error: null,
      success: false,
      successMessage: '',
      saving: false,
      isDrawing: false,
      hasSignature: false,
      ctx: null
    }
  },
  mounted() {
    // Initialize canvas immediately without API call
    this.$nextTick(() => {
      this.initCanvas()
    })
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
      e.preventDefault()
      this.isDrawing = true
      const pos = this.getEventPos(e)
      this.ctx.beginPath()
      this.ctx.moveTo(pos.x, pos.y)
      this.hasSignature = true
    },
    
    draw(e) {
      if (!this.isDrawing) return
      e.preventDefault()
      
      const pos = this.getEventPos(e)
      this.ctx.lineTo(pos.x, pos.y)
      this.ctx.stroke()
    },
    
    stopDrawing(e) {
      if (!this.isDrawing) return
      e.preventDefault()
      this.isDrawing = false
    },
    
    clearSignature() {
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
        
        // Try the new endpoint first (without auth)
        try {
          const response = await axios.post(`/api/save-signature/${token}/`, {
            signature: signatureData
          })
          
          this.success = true
          this.successMessage = response.data.message
        } catch (newEndpointError) {
          // If new endpoint fails, try the old one (with potential auth issues)
          try {
            const response = await axios.post(`/api/signatory-authorizations/save-signature/${token}/`, {
              signature: signatureData
            })
            
            this.success = true
            this.successMessage = response.data.message
          } catch (oldEndpointError) {
            // Both endpoints failed
            this.error = 'Unable to save signature. Please restart the Django server and try again.'
          }
        }
        
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to save signature'
      } finally {
        this.saving = false
      }
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

.setup-card, .success-card, .error-card {
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

.signature-pad-container {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 20px;
  text-align: center;
}

.signature-canvas {
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: crosshair;
  background: white;
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

.btn-save:disabled {
  background: #6c757d;
  cursor: not-allowed;
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

.success-card, .error-card {
  text-align: center;
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
</style>
