<template>
  <AppLayout>
    <div class="document-manager">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1>Document Manager</h1>
          <p>Create documents and request digital signatures</p>
        </div>
        <div class="header-actions">
          <button class="btn-primary" @click="showCreateModal = true">
            <i class="pi pi-plus"></i>
            Create Document
          </button>
        </div>
      </div>

      <!-- Documents List -->
      <div class="documents-section">
        <div class="section-header">
          <h2>Your Documents</h2>
          <div class="filters">
            <select v-model="statusFilter" class="filter-select">
              <option value="">All Status</option>
              <option value="DRAFT">Draft</option>
              <option value="PENDING_SIGNATURE">Pending Signature</option>
              <option value="SIGNED">Signed</option>
              <option value="COMPLETED">Completed</option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <i class="pi pi-spin pi-spinner"></i>
          <p>Loading documents...</p>
        </div>

        <div v-else-if="filteredDocuments.length === 0" class="empty-state">
          <i class="pi pi-file"></i>
          <h3>No documents found</h3>
          <p>Create your first document to get started with digital signatures.</p>
          <button class="btn-primary" @click="showCreateModal = true">
            Create Document
          </button>
        </div>

        <div v-else class="documents-grid">
          <div 
            v-for="document in filteredDocuments" 
            :key="document.id"
            class="document-card"
          >
            <div class="document-header">
              <div class="document-info">
                <h3>{{ document.title }}</h3>
                <p class="document-type">{{ document.document_type }}</p>
              </div>
              <div class="document-status">
                <span :class="['status-badge', document.status.toLowerCase().replace(' ', '_')]">
                  {{ document.status.replace('_', ' ') }}
                </span>
              </div>
            </div>

            <div class="document-body">
              <div class="document-stats">
                <div class="stat">
                  <i class="pi pi-users"></i>
                  <span>{{ document.signature_requests_count || 0 }} signers</span>
                </div>
                <div class="stat">
                  <i class="pi pi-check-circle"></i>
                  <span>{{ document.signed_count || 0 }} signed</span>
                </div>
                <div class="stat">
                  <i class="pi pi-calendar"></i>
                  <span>{{ formatDate(document.created_at) }}</span>
                </div>
              </div>

              <div class="document-actions">
                <button 
                  class="btn-action secondary"
                  @click="viewDocument(document)"
                >
                  <i class="pi pi-eye"></i>
                  View
                </button>
                <button 
                  v-if="document.status === 'DRAFT'"
                  class="btn-action primary"
                  @click="requestSignatures(document)"
                >
                  <i class="pi pi-send"></i>
                  Request Signatures
                </button>
                <button 
                  v-else
                  class="btn-action info"
                  @click="viewSignatures(document)"
                >
                  <i class="pi pi-list"></i>
                  View Signatures
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Document Modal -->
      <div v-if="showCreateModal" class="modal-overlay" @click="closeCreateModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Create New Document</h3>
            <button class="btn-close" @click="closeCreateModal">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <form @submit.prevent="createDocument" class="modal-body">
            <div class="form-field">
              <label>Document Title</label>
              <input 
                v-model="newDocument.title"
                type="text"
                class="form-input"
                placeholder="Enter document title"
                required
              />
            </div>

            <div class="form-field">
              <label>Document Type</label>
              <select v-model="newDocument.document_type" class="form-select" required>
                <option value="">Select type</option>
                <option value="PSR">Plant Status Report</option>
                <option value="DAILY">Daily Report</option>
                <option value="MONTHLY">Monthly Report</option>
                <option value="CUSTOM">Custom Document</option>
              </select>
            </div>

            <div class="form-field">
              <label>Content</label>
              <textarea 
                v-model="newDocument.content"
                class="form-textarea"
                rows="6"
                placeholder="Enter document content or description"
                required
              ></textarea>
            </div>

            <div class="form-field">
              <label>Document File (Optional)</label>
              <input 
                ref="fileInput"
                type="file"
                class="form-input"
                accept=".pdf,.doc,.docx"
                @change="handleFileUpload"
              />
              <small>Upload a PDF or Word document if available</small>
            </div>

            <div class="modal-actions">
              <button type="button" class="btn-secondary" @click="closeCreateModal">
                Cancel
              </button>
              <button type="submit" class="btn-primary" :disabled="creating">
                <i v-if="creating" class="pi pi-spin pi-spinner"></i>
                <i v-else class="pi pi-plus"></i>
                {{ creating ? 'Creating...' : 'Create Document' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Request Signatures Modal -->
      <div v-if="showSignatureModal" class="modal-overlay" @click="closeSignatureModal">
        <div class="modal-content large" @click.stop>
          <div class="modal-header">
            <h3>Request Signatures</h3>
            <button class="btn-close" @click="closeSignatureModal">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <form @submit.prevent="submitSignatureRequests" class="modal-body">
            <div class="document-info-section">
              <h4>Document: {{ selectedDocument?.title }}</h4>
              <p>{{ selectedDocument?.document_type }}</p>
            </div>

            <div class="signers-section">
              <div class="section-header">
                <h4>Signers</h4>
                <button type="button" class="btn-add" @click="addSigner">
                  <i class="pi pi-plus"></i>
                  Add Signer
                </button>
              </div>

              <div class="signers-list">
                <div 
                  v-for="(signer, index) in signatureRequest.signers" 
                  :key="index"
                  class="signer-card"
                >
                  <div class="signer-fields">
                    <div class="form-field">
                      <label>Name</label>
                      <input 
                        v-model="signer.name"
                        type="text"
                        class="form-input"
                        placeholder="Signer name"
                        required
                      />
                    </div>
                    <div class="form-field">
                      <label>Email</label>
                      <input 
                        v-model="signer.email"
                        type="email"
                        class="form-input"
                        placeholder="signer@example.com"
                        required
                      />
                    </div>
                    <div class="form-field">
                      <label>Role</label>
                      <select v-model="signer.role" class="form-select" required>
                        <option value="">Select role</option>
                        <option value="Prepared by">Prepared by</option>
                        <option value="Checked and Reviewed by">Checked and Reviewed by</option>
                        <option value="Approved by">Approved by</option>
                        <option value="Authorized by">Authorized by</option>
                      </select>
                    </div>
                  </div>
                  <button 
                    type="button" 
                    class="btn-remove"
                    @click="removeSigner(index)"
                    :disabled="signatureRequest.signers.length === 1"
                  >
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="form-field">
              <label>Expiration</label>
              <select v-model="signatureRequest.expires_in_hours" class="form-select">
                <option value="24">24 hours</option>
                <option value="72">3 days</option>
                <option value="168">1 week</option>
              </select>
            </div>

            <div class="modal-actions">
              <button type="button" class="btn-secondary" @click="closeSignatureModal">
                Cancel
              </button>
              <button type="submit" class="btn-primary" :disabled="submittingSignatures">
                <i v-if="submittingSignatures" class="pi pi-spin pi-spinner"></i>
                <i v-else class="pi pi-send"></i>
                {{ submittingSignatures ? 'Sending...' : 'Send Signature Requests' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from './AppLayout.vue'
import api from '../services/api'

export default {
  name: 'DocumentManager',
  components: {
    AppLayout
  },
  data() {
    return {
      documents: [],
      loading: true,
      statusFilter: '',
      
      // Create document modal
      showCreateModal: false,
      creating: false,
      newDocument: {
        title: '',
        document_type: '',
        content: '',
        file: null
      },
      
      // Signature request modal
      showSignatureModal: false,
      selectedDocument: null,
      submittingSignatures: false,
      signatureRequest: {
        signers: [
          { name: '', email: '', role: '' }
        ],
        expires_in_hours: 72
      }
    }
  },
  computed: {
    filteredDocuments() {
      if (!this.statusFilter) {
        return this.documents
      }
      return this.documents.filter(doc => doc.status === this.statusFilter)
    }
  },
  async mounted() {
    await this.loadDocuments()
  },
  methods: {
    async loadDocuments() {
      try {
        this.loading = true
        const response = await api.getDocuments()
        this.documents = response.data.results || response.data
      } catch (error) {
        console.error('Error loading documents:', error)
        this.$toast.error('Failed to load documents')
      } finally {
        this.loading = false
      }
    },
    
    // Create document methods
    closeCreateModal() {
      this.showCreateModal = false
      this.newDocument = {
        title: '',
        document_type: '',
        content: '',
        file: null
      }
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },
    
    handleFileUpload(event) {
      const file = event.target.files[0]
      this.newDocument.file = file
    },
    
    async createDocument() {
      try {
        this.creating = true
        
        const formData = new FormData()
        formData.append('title', this.newDocument.title)
        formData.append('document_type', this.newDocument.document_type)
        formData.append('content', this.newDocument.content)
        
        if (this.newDocument.file) {
          formData.append('file_path', this.newDocument.file)
        }
        
        await api.createDocument(formData)
        
        this.$toast.success('Document created successfully')
        this.closeCreateModal()
        await this.loadDocuments()
        
      } catch (error) {
        console.error('Error creating document:', error)
        this.$toast.error('Failed to create document')
      } finally {
        this.creating = false
      }
    },
    
    // Signature request methods
    requestSignatures(document) {
      this.selectedDocument = document
      this.showSignatureModal = true
    },
    
    closeSignatureModal() {
      this.showSignatureModal = false
      this.selectedDocument = null
      this.signatureRequest = {
        signers: [
          { name: '', email: '', role: '' }
        ],
        expires_in_hours: 72
      }
    },
    
    addSigner() {
      this.signatureRequest.signers.push({
        name: '',
        email: '',
        role: ''
      })
    },
    
    removeSigner(index) {
      if (this.signatureRequest.signers.length > 1) {
        this.signatureRequest.signers.splice(index, 1)
      }
    },
    
    async submitSignatureRequests() {
      try {
        this.submittingSignatures = true
        
        await api.requestSignatures(this.selectedDocument.id, {
          signers: this.signatureRequest.signers,
          expires_in_hours: this.signatureRequest.expires_in_hours
        })
        
        this.$toast.success('Signature requests sent successfully')
        this.closeSignatureModal()
        await this.loadDocuments()
        
      } catch (error) {
        console.error('Error sending signature requests:', error)
        this.$toast.error('Failed to send signature requests')
      } finally {
        this.submittingSignatures = false
      }
    },
    
    // Document actions
    viewDocument(document) {
      // TODO: Implement document viewer
      this.$toast.info(`Viewing document: ${document.title}`)
    },
    
    viewSignatures(document) {
      // TODO: Implement signature viewer
      this.$toast.info(`Viewing signatures for: ${document.title}`)
    },
    
    // Utility methods
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
/* ===== MODERN DOCUMENT MANAGER DESIGN ===== */

.document-manager {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
  position: relative;
}

/* Decorative background elements */
.document-manager::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  clip-path: ellipse(80% 100% at 50% 0%);
  z-index: 0;
}

/* Page Header with Enhanced Styling */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 1;
  animation: slideDown 0.6s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-content h1 {
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e293b 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  display: inline-block;
}

.header-content h1::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  border-radius: 2px;
}

.header-content p {
  color: #64748b;
  margin: 0;
  font-size: 1.1rem;
  font-weight: 400;
}

/* Enhanced Primary Button */
.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.6s;
}

.btn-primary:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 12px 35px rgba(79, 70, 229, 0.4);
}

.btn-primary:hover::before {
  left: 100%;
}

.btn-primary:active {
  transform: translateY(-1px) scale(0.98);
}

/* Documents Section with Glass Effect */
.documents-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(79, 70, 229, 0.1);
}

.section-header h2 {
  color: #1e293b;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  position: relative;
  display: inline-block;
}

.section-header h2::after {
  content: '';
  position: absolute;
  bottom: -1.5rem;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  border-radius: 2px;
}

/* Enhanced Filter Select */
.filter-select {
  padding: 0.75rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  font-weight: 500;
  color: #374151;
  transition: all 0.3s ease;
  cursor: pointer;
  min-width: 180px;
}

.filter-select:hover {
  border-color: #4f46e5;
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.1);
}

.filter-select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}

/* Loading and Empty States */
.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
  animation: fadeIn 0.6s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.loading-state i,
.empty-state i {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  color: #9ca3af;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #374151;
  margin-bottom: 0.75rem;
}

.empty-state p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* Enhanced Documents Grid */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 2rem;
}

/* Document Card with Advanced Effects */
.document-card {
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.75rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

.document-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
  transform: scaleX(0);
  transition: transform 0.4s ease;
  transform-origin: left;
}

.document-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 50px rgba(79, 70, 229, 0.2);
  border-color: rgba(79, 70, 229, 0.3);
}

.document-card:hover::before {
  transform: scaleX(1);
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.document-info h3 {
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  transition: all 0.3s ease;
}

.document-card:hover .document-info h3 {
  color: #4f46e5;
  transform: translateX(5px);
}

.document-type {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.document-type::before {
  content: '📄';
  font-size: 1.1rem;
}

/* Enhanced Status Badges */
.status-badge {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.status-badge::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.document-card:hover .status-badge::after {
  transform: translateX(100%);
}

.status-badge.draft {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #374151;
  box-shadow: 0 4px 12px rgba(55, 65, 81, 0.1);
}

.status-badge.pending_signature {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  box-shadow: 0 4px 12px rgba(146, 64, 14, 0.2);
}

.status-badge.signed {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #166534;
  box-shadow: 0 4px 12px rgba(22, 101, 52, 0.2);
}

.status-badge.completed {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
}

/* Enhanced Document Stats */
.document-stats {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  border-radius: 12px;
  background: rgba(248, 250, 252, 0.7);
  border: 1px solid rgba(226, 232, 240, 0.5);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.9rem;
  color: #4b5563;
  font-weight: 500;
  transition: all 0.3s ease;
}

.stat i {
  color: #4f46e5;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.document-card:hover .stat i {
  transform: scale(1.2) rotate(5deg);
  color: #7c3aed;
}

/* Enhanced Document Actions */
.document-actions {
  display: flex;
  gap: 0.8rem;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 1.25rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  flex: 1;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.btn-action::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn-action:hover::after {
  width: 300px;
  height: 300px;
}

.btn-action:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.btn-action.secondary {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.btn-action.secondary:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  color: #1e293b;
}

.btn-action.primary {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
}

.btn-action.primary:hover {
  box-shadow: 0 10px 30px rgba(79, 70, 229, 0.4);
}

.btn-action.info {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
}

.btn-action.info:hover {
  box-shadow: 0 10px 30px rgba(14, 165, 233, 0.4);
}

/* ===== ENHANCED MODAL STYLES ===== */

/* Modal Overlay with Blur Effect */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  animation: fadeIn 0.3s ease forwards;
}

/* Enhanced Modal Content */
.modal-content {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  max-width: 550px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.3);
  animation: modalSlideIn 0.4s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-content.large {
  max-width: 750px;
}

/* Enhanced Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.75rem 2rem;
  border-bottom: 2px solid rgba(79, 70, 229, 0.1);
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 20px 20px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 700;
  position: relative;
  display: inline-block;
}

.modal-header h3::after {
  content: '';
  position: absolute;
  bottom: -0.75rem;
  left: 0;
  width: 30px;
  height: 3px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  border-radius: 2px;
}

/* Enhanced Close Button */
.btn-close {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border: 2px solid #e2e8f0;
  font-size: 1.25rem;
  cursor: pointer;
  color: #64748b;
  padding: 0.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-color: #ef4444;
  transform: rotate(90deg) scale(1.1);
}

/* Enhanced Modal Body */
.modal-body {
  padding: 2rem;
}

/* Enhanced Form Fields */
.form-field {
  margin-bottom: 1.75rem;
  position: relative;
}

.form-field label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
  position: relative;
}

.form-field label::after {
  content: '*';
  color: #ef4444;
  margin-left: 0.25rem;
  font-weight: 700;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #ffffff;
  position: relative;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.15);
  transform: translateY(-2px);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

/* Enhanced Modal Actions */
.modal-actions {
  display: flex;
  gap: 1.25rem;
  justify-content: flex-end;
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid rgba(226, 232, 240, 0.5);
}

/* Enhanced Secondary Button */
.btn-secondary {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 2px solid #e2e8f0;
  padding: 0.85rem 1.75rem;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-secondary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.6s;
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  color: #1e293b;
  border-color: #cbd5e1;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover::before {
  left: 100%;
}

/* Enhanced File Input Styling */
.form-input[type="file"] {
  padding: 1rem;
}

.form-input[type="file"]::-webkit-file-upload-button {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  margin-right: 1rem;
  transition: all 0.3s ease;
}

.form-input[type="file"]::-webkit-file-upload-button:hover {
  background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
  transform: translateY(-1px);
}

/* Small text styling */
.form-field small {
  display: block;
  margin-top: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
  font-style: italic;
}

/* ===== SIGNATURE MODAL ENHANCEMENTS ===== */

/* Enhanced Document Info Section */
.document-info-section {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 1.5rem;
  border-radius: 16px;
  margin-bottom: 2.5rem;
  border: 2px solid rgba(14, 165, 233, 0.1);
  box-shadow: 0 4px 20px rgba(14, 165, 233, 0.1);
  position: relative;
  overflow: hidden;
}

.document-info-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0ea5e9, #0284c7, #0ea5e9);
}

.document-info-section h4 {
  margin: 0 0 0.5rem 0;
  color: #0c4a6e;
  font-size: 1.25rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.document-info-section h4::before {
  content: '📝';
  font-size: 1.4rem;
}

.document-info-section p {
  color: #0369a1;
  font-weight: 500;
  margin: 0;
  font-size: 1.05rem;
}

/* Enhanced Signers Section */
.signers-section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(34, 197, 94, 0.2);
}

.signers-section .section-header h4 {
  margin: 0;
  color: #1e293b;
  font-size: 1.3rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.signers-section .section-header h4::before {
  content: '👥';
  font-size: 1.3rem;
}

/* Enhanced Add Signer Button */
.btn-add {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
  position: relative;
  overflow: hidden;
}

.btn-add::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.6s;
}

.btn-add:hover {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
}

.btn-add:hover::before {
  left: 100%;
}

/* Enhanced Signer Card */
.signer-card {
  display: flex;
  gap: 1.25rem;
  align-items: flex-end;
  padding: 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  margin-bottom: 1.25rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.signer-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: left;
}

.signer-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 8px 25px rgba(79, 70, 229, 0.15);
  transform: translateY(-3px);
}

.signer-card:hover::before {
  transform: scaleX(1);
}

/* Enhanced Signer Fields Grid */
.signer-fields {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.25rem;
  flex: 1;
}

/* Enhanced Remove Button */
.btn-remove {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 12px;
  cursor: pointer;
  height: fit-content;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
}

.btn-remove:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: scale(1.1) rotate(10deg);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.btn-remove:disabled {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-remove:disabled:hover {
  transform: none;
  box-shadow: none;
}

/* ===== RESPONSIVE DESIGN ===== */

@media (max-width: 1200px) {
  .documents-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }
}

@media (max-width: 992px) {
  .document-manager {
    padding: 1.5rem;
  }
  
  .documents-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
  
  .documents-section {
    padding: 2rem;
  }
}

@media (max-width: 768px) {
  .document-manager {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
    padding: 1.5rem;
  }
  
  .header-content h1 {
    font-size: 1.8rem;
  }
  
  .documents-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
  
  .document-card {
    padding: 1.5rem;
  }
  
  .document-stats {
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .document-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .signer-fields {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .signer-card {
    flex-direction: column;
    align-items: stretch;
    gap: 1.25rem;
    padding: 1.25rem;
  }
  
  .modal-content {
    margin: 1rem;
    max-height: 95vh;
  }
  
  .modal-header,
  .modal-body {
    padding: 1.5rem;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary,
  .btn-add {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .document-manager {
    padding: 0.75rem;
  }
  
  .page-header {
    padding: 1.25rem;
  }
  
  .header-content h1 {
    font-size: 1.5rem;
  }
  
  .documents-section {
    padding: 1.5rem;
  }
  
  .document-card {
    padding: 1.25rem;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .modal-content {
    margin: 0.5rem;
    border-radius: 16px;
  }
  
  .modal-header,
  .modal-body {
    padding: 1.25rem;
  }
}

/* ===== END OF STYLES ===== */
</style>