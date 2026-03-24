<template>
  <div class="signature-pad-container">
    <!-- Header -->
    <div class="signature-header">
      <h2>Digital Signature Required</h2>
      <p v-if="signingData">
        Please provide your digital signature for: <strong>{{ signingData.document_title }}</strong>
      </p>
      <p class="role-info">Your role: <span class="role-badge">{{ signingData?.signer_role }}</span></p>
    </div>

    <!-- Signature Type Selection -->
    <div class="signature-type-selector">
      <h3>Choose Signature Method</h3>
      <div class="type-buttons">
        <button 
          :class="['type-btn', { active: signatureType === 'DRAWN' }]"
          @click="setSignatureType('DRAWN')"
        >
          <i class="pi pi-pencil"></i>
          Draw Signature
        </button>
        <button 
          :class="['type-btn', { active: signatureType === 'UPLOADED' }]"
          @click="setSignatureType('UPLOADED')"
        >
          <i class="pi pi-upload"></i>
          Upload Image
        </button>
        <button 
          :class="['type-btn', { active: signatureType === 'TYPED' }]"
          @click="setSignatureType('TYPED')"
        >
          <i class="pi pi-font"></i>
          Type Name
        </button>
      </div>
    </div>

    <!-- Draw Signature -->
    <div v-if="signatureType === 'DRAWN'" class="signature-section">
      <h4>Draw Your Signature</h4>
      <div class="signature-pad-wrapper">
        <canvas
          ref="signatureCanvas"
          class="signature-canvas"
          :width="canvasWidth"
          :height="canvasHeight"
          @mousedown="startDrawing"
          @mousemove="draw"
          @mouseup="stopDrawing"
          @mouseleave="stopDrawing"
          @touchstart="startDrawing"
          @touchmove="draw"
          @touchend="stopDrawing"
        ></canvas>
        <div class="canvas-controls">
          <button class="btn-clear" @click="clearCanvas">
            <i class="pi pi-trash"></i>
            Clear
          </button>
          <div class="canvas-info">
            {{ canvasWidth }} × {{ canvasHeight }}
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Signature -->
    <div v-if="signatureType === 'UPLOADED'" class="signature-section">
      <h4>Upload Signature Image</h4>
      <div class="upload-area">
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="handleFileUpload"
          style="display: none"
        />
        <div 
          class="upload-dropzone"
          :class="{ 'drag-over': isDragOver }"
          @click="$refs.fileInput.click()"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="handleFileDrop"
        >
          <div v-if="!uploadedImage" class="upload-placeholder">
            <i class="pi pi-cloud-upload"></i>
            <p>Click to upload or drag and drop</p>
            <small>PNG, JPG, GIF up to 2MB</small>
          </div>
          <div v-else class="uploaded-preview">
            <img :src="uploadedImage" alt="Uploaded signature" />
            <button class="btn-remove" @click.stop="removeUploadedImage">
              <i class="pi pi-times"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Type Signature -->
    <div v-if="signatureType === 'TYPED'" class="signature-section">
      <h4>Type Your Name</h4>
      <div class="typed-signature-area">
        <input
          v-model="typedSignature"
          type="text"
          class="signature-input"
          :placeholder="signingData?.signer_name || 'Enter your full name'"
          maxlength="50"
        />
        <div class="typed-preview" v-if="typedSignature">
          <div class="signature-preview">{{ typedSignature }}</div>
        </div>
      </div>
    </div>

    <!-- Signature Preview -->
    <div v-if="hasSignature" class="signature-preview-section">
      <h4>Signature Preview</h4>
      <div class="preview-container">
        <div class="signature-preview-box">
          <img v-if="signaturePreview" :src="signaturePreview" alt="Signature preview" />
          <div v-else class="no-preview">No preview available</div>
        </div>
      </div>
    </div>

    <!-- Legal Notice -->
    <div class="legal-notice">
      <div class="notice-content">
        <i class="pi pi-info-circle"></i>
        <div>
          <p><strong>Legal Notice:</strong> By providing your digital signature, you acknowledge that:</p>
          <ul>
            <li>This signature is legally binding and equivalent to a handwritten signature</li>
            <li>You are authorized to sign this document</li>
            <li>The signature will be securely stored and may be used for verification purposes</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <button 
        class="btn-cancel" 
        @click="$emit('cancel')"
        :disabled="submitting"
      >
        Cancel
      </button>
      <button 
        class="btn-sign" 
        @click="submitSignature"
        :disabled="!hasSignature || submitting"
        :class="{ submitting: submitting }"
      >
        <i v-if="submitting" class="pi pi-spin pi-spinner"></i>
        <i v-else class="pi pi-check"></i>
        {{ submitting ? 'Signing...' : 'Sign Document' }}
      </button>
    </div>

    <!-- Success Message -->
    <div v-if="signatureComplete" class="success-message">
      <div class="success-content">
        <i class="pi pi-check-circle"></i>
        <h3>Document Signed Successfully!</h3>
        <p>Your digital signature has been recorded and the document has been signed.</p>
        <p>You will receive a confirmation email shortly.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'SignaturePad',
  props: {
    token: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      signingData: null,
      signatureType: 'DRAWN',
      
      // Canvas drawing
      isDrawing: false,
      canvasWidth: 500,
      canvasHeight: 200,
      lastX: 0,
      lastY: 0,
      
      // Upload
      uploadedImage: null,
      uploadedFile: null,
      isDragOver: false,
      
      // Typed signature
      typedSignature: '',
      
      // State
      submitting: false,
      signatureComplete: false,
      error: null
    }
  },
  computed: {
    hasSignature() {
      switch (this.signatureType) {
        case 'DRAWN':
          return this.hasDrawnSignature()
        case 'UPLOADED':
          return !!this.uploadedImage
        case 'TYPED':
          return this.typedSignature.trim().length > 0
        default:
          return false
      }
    },
    signaturePreview() {
      switch (this.signatureType) {
        case 'DRAWN':
          return this.getCanvasDataURL()
        case 'UPLOADED':
          return this.uploadedImage
        case 'TYPED':
          return this.generateTypedSignaturePreview()
        default:
          return null
      }
    }
  },
  async mounted() {
    await this.loadSigningData()
    this.initializeCanvas()
  },
  methods: {
    async loadSigningData() {
      try {
        const response = await api.verifySignatureToken(this.token)
        this.signingData = response.data
        
        // Pre-fill typed signature with signer name
        if (this.signingData.signer_name) {
          this.typedSignature = this.signingData.signer_name
        }
      } catch (error) {
        console.error('Error loading signing data:', error)
        this.error = 'Invalid or expired signature link'
        this.$emit('error', this.error)
      }
    },
    
    setSignatureType(type) {
      this.signatureType = type
      if (type === 'DRAWN') {
        this.$nextTick(() => {
          this.initializeCanvas()
        })
      }
    },
    
    // Canvas methods
    initializeCanvas() {
      const canvas = this.$refs.signatureCanvas
      if (!canvas) return
      
      const ctx = canvas.getContext('2d')
      ctx.strokeStyle = '#000000'
      ctx.lineWidth = 2
      ctx.lineCap = 'round'
      ctx.lineJoin = 'round'
      
      // Clear canvas
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight)
    },
    
    startDrawing(e) {
      this.isDrawing = true
      const rect = this.$refs.signatureCanvas.getBoundingClientRect()
      
      if (e.type === 'touchstart') {
        this.lastX = e.touches[0].clientX - rect.left
        this.lastY = e.touches[0].clientY - rect.top
      } else {
        this.lastX = e.clientX - rect.left
        this.lastY = e.clientY - rect.top
      }
    },
    
    draw(e) {
      if (!this.isDrawing) return
      
      e.preventDefault()
      const canvas = this.$refs.signatureCanvas
      const ctx = canvas.getContext('2d')
      const rect = canvas.getBoundingClientRect()
      
      let currentX, currentY
      if (e.type === 'touchmove') {
        currentX = e.touches[0].clientX - rect.left
        currentY = e.touches[0].clientY - rect.top
      } else {
        currentX = e.clientX - rect.left
        currentY = e.clientY - rect.top
      }
      
      ctx.beginPath()
      ctx.moveTo(this.lastX, this.lastY)
      ctx.lineTo(currentX, currentY)
      ctx.stroke()
      
      this.lastX = currentX
      this.lastY = currentY
    },
    
    stopDrawing() {
      this.isDrawing = false
    },
    
    clearCanvas() {
      const canvas = this.$refs.signatureCanvas
      const ctx = canvas.getContext('2d')
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight)
    },
    
    hasDrawnSignature() {
      const canvas = this.$refs.signatureCanvas
      if (!canvas) return false
      
      const ctx = canvas.getContext('2d')
      const imageData = ctx.getImageData(0, 0, this.canvasWidth, this.canvasHeight)
      
      // Check if canvas has any non-white pixels
      for (let i = 0; i < imageData.data.length; i += 4) {
        if (imageData.data[i] !== 255 || imageData.data[i + 1] !== 255 || imageData.data[i + 2] !== 255) {
          return true
        }
      }
      return false
    },
    
    getCanvasDataURL() {
      const canvas = this.$refs.signatureCanvas
      return canvas ? canvas.toDataURL('image/png') : null
    },
    
    // Upload methods
    handleFileUpload(e) {
      const file = e.target.files[0]
      if (file) {
        this.processUploadedFile(file)
      }
    },
    
    handleFileDrop(e) {
      this.isDragOver = false
      const file = e.dataTransfer.files[0]
      if (file && file.type.startsWith('image/')) {
        this.processUploadedFile(file)
      }
    },
    
    processUploadedFile(file) {
      // Validate file size (2MB limit)
      if (file.size > 2 * 1024 * 1024) {
        alert('File size must be less than 2MB')
        return
      }
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please upload an image file')
        return
      }
      
      this.uploadedFile = file
      
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        this.uploadedImage = e.target.result
      }
      reader.readAsDataURL(file)
    },
    
    removeUploadedImage() {
      this.uploadedImage = null
      this.uploadedFile = null
      this.$refs.fileInput.value = ''
    },
    
    // Typed signature methods
    generateTypedSignaturePreview() {
      if (!this.typedSignature.trim()) return null
      
      // Create a canvas to generate typed signature image
      const canvas = document.createElement('canvas')
      canvas.width = 400
      canvas.height = 100
      const ctx = canvas.getContext('2d')
      
      // Set background
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      
      // Set text style
      ctx.fillStyle = '#000000'
      ctx.font = '24px cursive'
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      
      // Draw text
      ctx.fillText(this.typedSignature, canvas.width / 2, canvas.height / 2)
      
      return canvas.toDataURL('image/png')
    },
    
    // Submission
    async submitSignature() {
      if (!this.hasSignature) return
      
      this.submitting = true
      this.error = null
      
      try {
        const formData = new FormData()
        formData.append('signature_type', this.signatureType)
        formData.append('width', this.canvasWidth.toString())
        formData.append('height', this.canvasHeight.toString())
        
        if (this.signatureType === 'DRAWN') {
          const signatureData = this.getCanvasDataURL()
          formData.append('signature_data', signatureData)
        } else if (this.signatureType === 'UPLOADED') {
          formData.append('signature_image', this.uploadedFile)
        } else if (this.signatureType === 'TYPED') {
          formData.append('signature_data', this.typedSignature)
        }
        
        await api.signDocument(this.token, formData)
        
        this.signatureComplete = true
        this.$emit('signed')
        
        // Redirect after delay
        setTimeout(() => {
          this.$emit('complete')
        }, 3000)
        
      } catch (error) {
        console.error('Error submitting signature:', error)
        this.error = error.response?.data?.error || 'Failed to submit signature'
        alert(this.error)
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.signature-pad-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.signature-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.signature-header h2 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.role-info {
  margin-top: 1rem;
}

.role-badge {
  background: #4f46e5;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.signature-type-selector {
  margin-bottom: 2rem;
}

.signature-type-selector h3 {
  margin-bottom: 1rem;
  color: #374151;
}

.type-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.type-btn:hover {
  border-color: #4f46e5;
  background: #f8fafc;
}

.type-btn.active {
  border-color: #4f46e5;
  background: #ede9fe;
  color: #4f46e5;
}

.type-btn i {
  font-size: 1.5rem;
}

.signature-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fafbfc;
}

.signature-section h4 {
  margin-bottom: 1rem;
  color: #374151;
}

/* Canvas Styles */
.signature-pad-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.signature-canvas {
  border: 2px solid #d1d5db;
  border-radius: 8px;
  background: white;
  cursor: crosshair;
  touch-action: none;
}

.canvas-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 500px;
  margin-top: 1rem;
}

.btn-clear {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-clear:hover {
  background: #dc2626;
}

.canvas-info {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Upload Styles */
.upload-area {
  width: 100%;
}

.upload-dropzone {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-dropzone:hover,
.upload-dropzone.drag-over {
  border-color: #4f46e5;
  background: #f8fafc;
}

.upload-placeholder i {
  font-size: 3rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.uploaded-preview {
  position: relative;
  max-width: 300px;
}

.uploaded-preview img {
  max-width: 100%;
  max-height: 150px;
  border-radius: 4px;
}

.btn-remove {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Typed Signature Styles */
.typed-signature-area {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.signature-input {
  padding: 1rem;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  font-size: 1.125rem;
  font-family: cursive;
}

.signature-input:focus {
  outline: none;
  border-color: #4f46e5;
}

.typed-preview {
  text-align: center;
}

.signature-preview {
  font-size: 2rem;
  font-family: cursive;
  color: #1e293b;
  padding: 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  display: inline-block;
}

/* Preview Section */
.signature-preview-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
}

.preview-container {
  text-align: center;
}

.signature-preview-box {
  display: inline-block;
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fafbfc;
  min-width: 200px;
  min-height: 100px;
}

.signature-preview-box img {
  max-width: 100%;
  height: auto;
}

.no-preview {
  color: #9ca3af;
  font-style: italic;
}

/* Legal Notice */
.legal-notice {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 8px;
}

.notice-content {
  display: flex;
  gap: 1rem;
}

.notice-content i {
  color: #d97706;
  font-size: 1.25rem;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.notice-content ul {
  margin: 0.5rem 0 0 1rem;
  padding: 0;
}

.notice-content li {
  margin-bottom: 0.25rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-cancel,
.btn-sign {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;
  justify-content: center;
}

.btn-cancel {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.btn-cancel:hover:not(:disabled) {
  background: #e2e8f0;
}

.btn-sign {
  background: #22c55e;
  color: white;
}

.btn-sign:hover:not(:disabled) {
  background: #16a34a;
  transform: translateY(-1px);
}

.btn-sign:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-sign.submitting {
  background: #6b7280;
}

/* Success Message */
.success-message {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.success-content {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  max-width: 500px;
  margin: 2rem;
}

.success-content i {
  font-size: 4rem;
  color: #22c55e;
  margin-bottom: 1rem;
}

.success-content h3 {
  color: #1e293b;
  margin-bottom: 1rem;
}

.success-content p {
  color: #64748b;
  margin-bottom: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .signature-pad-container {
    margin: 1rem;
    padding: 1rem;
  }
  
  .type-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .type-btn {
    width: 100%;
    max-width: 200px;
  }
  
  .signature-canvas {
    width: 100%;
    max-width: 400px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .btn-cancel,
  .btn-sign {
    width: 100%;
  }
}
</style>
