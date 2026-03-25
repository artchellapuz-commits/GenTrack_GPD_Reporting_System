<template>
  <AppLayout>
    <div class="authorization-request-page">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <div class="hero-icon">
            <i class="pi pi-shield"></i>
          </div>
          <h1 class="hero-title">Signature Authorization Center</h1>
          <p class="hero-subtitle">Secure your digital signature access with enterprise-grade authorization</p>
          
          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon success">
                <i class="pi pi-check-circle"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ userAuthorizations.length }}</div>
                <div class="stat-label">Active Authorizations</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon warning">
                <i class="pi pi-hourglass"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ pendingRequests.length }}</div>
                <div class="stat-label">Pending Requests</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon info">
                <i class="pi pi-users"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ availableSignatories.length }}</div>
                <div class="stat-label">Available Signatories</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Current Authorizations Section -->
        <div v-if="userAuthorizations.length > 0" class="section-card authorizations-section">
          <div class="section-header">
            <div class="section-title">
              <i class="pi pi-verified"></i>
              <h2>Your Active Authorizations</h2>
            </div>
            <div class="section-badge success">{{ userAuthorizations.length }} Authorizations</div>
          </div>
          
          <div class="authorizations-grid">
            <div 
              v-for="(auth, index) in userAuthorizations" 
              :key="auth.id"
              class="authorization-card"
              :class="{ 'expired': !auth.is_valid }"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="auth-card-header">
                <div class="auth-avatar">
                  <i class="pi pi-user"></i>
                  <!-- Signature Status Indicator -->
                  <div class="signature-indicator" :class="getSignatureStatusClass(auth)">
                    <i :class="getSignatureStatusIcon(auth)"></i>
                  </div>
                </div>
                <div class="auth-info">
                  <h3 class="auth-name">{{ auth.signatory_name }}</h3>
                  <p class="auth-role">{{ getSignatoryTitle(auth.signatory_name) }}</p>
                </div>
                <div class="auth-status-badge" :class="getSignatureStatusClass(auth)">
                  <i :class="getSignatureStatusIcon(auth)"></i>
                  {{ getSignatureStatusText(auth) }}
                </div>
              </div>
              
              <div class="auth-card-body">
                <div class="auth-details">
                  <div class="detail-item ">
                    <i class="pi pi-calendar"></i>
                    <span>Authorized: {{ formatDate(auth.authorization_date) }}</span>
                  </div>
                  <div v-if="auth.expiry_date" class="detail-item">
                    <i class="pi pi-clock"></i>
                    <span>Expires: {{ formatDate(auth.expiry_date) }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="pi pi-shield"></i>
                    <span>2FA: {{ auth.requires_2fa ? 'Required' : 'Not Required' }}</span>
                  </div>
                </div>
                
                <div class="auth-actions">
                  <button class="btn-action secondary" @click="viewAuthDetails(auth)">
                    <i class="pi pi-eye"></i>
                  </button>
                  <button class="btn-action danger" @click="deleteAuthorization(auth)">
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Request New Authorization Section -->
        <div class="section-card request-section">
          <div class="section-header">
            <div class="section-title">
              <i class="pi pi-plus-circle"></i>
              <h2>Request New Authorization</h2>
            </div>
            <div class="progress-indicator">
              <div class="progress-step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
                <div class="step-number">1</div>
                <span>Select Signatory</span>
              </div>
              <div class="progress-line" :class="{ active: currentStep > 1 }"></div>
              <div class="progress-step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
                <div class="step-number">2</div>
                <span>Choose Role</span>
              </div>
              <div class="progress-line" :class="{ active: currentStep > 2 }"></div>
              <div class="progress-step" :class="{ active: currentStep >= 3, completed: currentStep > 3 }">
                <div class="step-number">3</div>
                <span>Provide Justification</span>
              </div>
            </div>
          </div>

          <div class="request-form-container">
            <form @submit.prevent="submitRequest" class="request-form">
              <!-- Step 1: Signatory Selection -->
              <div class="form-step" :class="{ active: currentStep === 1 }">
                <div class="step-header">
                  <h3>Step 1: Select Signatory</h3>
                  <p>Choose the signatory name you need authorization for</p>
                </div>
                
                <div class="signatory-grid">
                  <div 
                    v-for="signatory in availableSignatories" 
                    :key="signatory.name"
                    class="signatory-card"
                    :class="{ 
                      selected: selectedSignatory === signatory.name,
                      disabled: isSignatoryDisabled(signatory.name),
                      'has-authorization': hasActiveAuthorization(signatory.name),
                      'has-pending': hasPendingRequest(signatory.name)
                    }"
                    @click="selectSignatory(signatory.name)"
                  >
                    <div class="signatory-avatar">
                      <i class="pi pi-user"></i>
                    </div>
                    <div class="signatory-info">
                      <h4>{{ signatory.name }}</h4>
                      <p>{{ signatory.title }}</p>
                      <div v-if="hasActiveAuthorization(signatory.name)" class="signatory-status active">
                        <i class="pi pi-check-circle"></i>
                        <span>Already Authorized</span>
                      </div>
                      <div v-else-if="hasPendingRequest(signatory.name)" class="signatory-status pending">
                        <i class="pi pi-clock"></i>
                        <span>Request Pending</span>
                      </div>
                    </div>
                    <div class="selection-indicator">
                      <i class="pi pi-check"></i>
                    </div>
                  </div>
                </div>
                
                <div class="step-actions">
                  <button 
                    type="button" 
                    class="btn-next" 
                    :disabled="!selectedSignatory"
                    @click="nextStep"
                  >
                    Continue
                    <i class="pi pi-arrow-right"></i>
                  </button>
                </div>
              </div>

              <!-- Step 2: Role Selection -->
              <div class="form-step" :class="{ active: currentStep === 2 }">
                <div class="step-header">
                  <h3>Step 2: Choose Your Role</h3>
                  <p>Select the role that best describes your responsibility</p>
                </div>
                
                <div class="role-grid">
                  <div 
                    v-for="role in availableRoles" 
                    :key="role.value"
                    class="role-card"
                    :class="{ selected: selectedRole === role.value }"
                    @click="selectRole(role.value)"
                  >
                    <div class="role-icon">
                      <i :class="role.icon"></i>
                    </div>
                    <div class="role-info">
                      <h4>{{ role.label }}</h4>
                      <p>{{ role.description }}</p>
                    </div>
                    <div class="selection-indicator">
                      <i class="pi pi-check"></i>
                    </div>
                  </div>
                </div>
                
                <div class="step-actions">
                  <button type="button" class="btn-back" @click="prevStep">
                    <i class="pi pi-arrow-left"></i>
                    Back
                  </button>
                  <button 
                    type="button" 
                    class="btn-next" 
                    :disabled="!selectedRole"
                    @click="nextStep"
                  >
                    Continue
                    <i class="pi pi-arrow-right"></i>
                  </button>
                </div>
              </div>

              <!-- Step 3: Justification -->
              <div class="form-step" :class="{ active: currentStep === 3 }">
                <div class="step-header">
                  <h3>Step 3: Provide Justification</h3>
                  <p>Explain why you need this authorization</p>
                </div>
                
                <div class="justification-section">
                  <div class="form-field">
                    <label class="field-label">
                      <i class="pi pi-envelope"></i>
                      Email Address
                    </label>
                    <input 
                      v-model="email"
                      type="email"
                      class="form-input"
                      placeholder="Enter your email address for notifications"
                      required
                    />
                    <div class="field-hint">
                      <i class="pi pi-info-circle"></i>
                      <span>You'll receive email notifications when your request is reviewed and processed.</span>
                    </div>
                  </div>

                  <div class="form-field">
                    <label class="field-label">
                      <i class="pi pi-comment"></i>
                      Justification Details
                    </label>
                    <div class="textarea-container">
                      <textarea 
                        v-model="justification"
                        class="form-textarea"
                        rows="6"
                        placeholder="Please provide a detailed explanation of why you need this authorization. Include your role, responsibilities, and how this authorization will be used."
                        required
                        @input="updateCharacterCount"
                      ></textarea>
                      <div class="character-count">
                        {{ justification.length }}/500 characters
                      </div>
                    </div>
                    <div class="field-hint">
                      <i class="pi pi-info-circle"></i>
                      <span>Be specific about your role and responsibilities. This helps administrators process your request faster.</span>
                    </div>
                  </div>

                  <!-- Request Summary -->
                  <div class="request-summary">
                    <h4>Request Summary</h4>
                    <div class="summary-grid">
                      <div class="summary-item">
                        <span class="summary-label">Signatory:</span>
                        <span class="summary-value">{{ selectedSignatory }}</span>
                      </div>
                      <div class="summary-item" v-if="selectedSignatory">
                        <span class="summary-label">Title:</span>
                        <span class="summary-value">{{ getSignatoryTitle(selectedSignatory) }}</span>
                      </div>
                      <div class="summary-item">
                        <span class="summary-label">Role:</span>
                        <span class="summary-value">{{ selectedRole }}</span>
                      </div>
                      <div class="summary-item">
                        <span class="summary-label">Email:</span>
                        <span class="summary-value">{{ email || '(not provided yet)' }}</span>
                      </div>
                      <div class="summary-item">
                        <span class="summary-label">Request Date:</span>
                        <span class="summary-value">{{ new Date().toLocaleDateString() }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="step-actions">
                  <button type="button" class="btn-back" @click="prevStep">
                    <i class="pi pi-arrow-left"></i>
                    Back
                  </button>
                  <button 
                    type="submit"
                    class="btn-submit"
                    :disabled="!canSubmit || submitting"
                    :class="{ submitting: submitting }"
                  >
                    <div class="btn-content">
                      <i v-if="!submitting" class="pi pi-send"></i>
                      <i v-else class="pi pi-spin pi-spinner"></i>
                      <span>{{ submitting ? 'Submitting...' : 'Submit Request' }}</span>
                    </div>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- Pending Requests Section -->
        <div v-if="pendingRequests.length > 0" class="section-card pending-section">
          <div class="section-header">
            <div class="section-title">
              <i class="pi pi-hourglass"></i>
              <h2>Pending Requests</h2>
            </div>
            <div class="section-badge warning">{{ pendingRequests.length }} Pending</div>
          </div>
          
          <div class="pending-requests-list">
            <div 
              v-for="(request, index) in pendingRequests" 
              :key="request.id"
              class="pending-request-card"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="request-header">
                <div class="request-info">
                  <h4>{{ request.signatory_name }}</h4>
                  <p>{{ request.role }}</p>
                </div>
                <div class="request-status">
                  <div class="status-indicator pending">
                    <div class="pulse-dot"></div>
                    Pending Review
                  </div>
                  <div class="request-date">{{ formatDate(request.created_at) }}</div>
                </div>
              </div>
              
              <div class="request-body">
                <div class="justification-preview">
                  <strong>Justification:</strong>
                  <p>{{ request.justification }}</p>
                </div>
                
                <div class="request-actions">
                  <button class="btn-action secondary" @click="viewRequestDetails(request)">
                    <i class="pi pi-eye"></i>
                  </button>
                  <button class="btn-action danger" @click="cancelRequest(request)">
                    <i class="pi pi-times"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Help & Information Section -->
        <div class="section-card help-section">
          <div class="section-header">
            <div class="section-title">
              <i class="pi pi-question-circle"></i>
              <h2>Help & Information</h2>
            </div>
          </div>
          
          <div class="help-content">
            <div class="help-tabs">
              <button 
                v-for="tab in helpTabs" 
                :key="tab.id"
                class="help-tab"
                :class="{ active: activeHelpTab === tab.id }"
                @click="activeHelpTab = tab.id"
              >
                <i :class="tab.icon"></i>
                {{ tab.label }}
              </button>
            </div>
            
            <div class="help-tab-content">
              <div v-if="activeHelpTab === 'overview'" class="help-panel">
                <h3>What is Signatory Authorization?</h3>
                <p>Signatory authorization is a security feature that ensures only authorized personnel can digitally sign official reports. This system provides:</p>
                <ul>
                  <li><strong>Security:</strong> Only approved users can sign documents</li>
                  <li><strong>Accountability:</strong> Full audit trail of all signatures</li>
                  <li><strong>Compliance:</strong> Meets regulatory requirements for digital signatures</li>
                  <li><strong>Flexibility:</strong> Different authorization levels for different roles</li>
                </ul>
              </div>
              
              <div v-if="activeHelpTab === 'process'" class="help-panel">
                <h3>Authorization Process</h3>
                <div class="process-steps">
                  <div class="process-step">
                    <div class="process-number">1</div>
                    <div class="process-content">
                      <h4>Submit Request</h4>
                      <p>Complete the authorization request form with your details and justification</p>
                    </div>
                  </div>
                  <div class="process-step">
                    <div class="process-number">2</div>
                    <div class="process-content">
                      <h4>Admin Review</h4>
                      <p>System administrators review your request (typically 1-2 business days)</p>
                    </div>
                  </div>
                  <div class="process-step">
                    <div class="process-number">3</div>
                    <div class="process-content">
                      <h4>Email Notification</h4>
                      <p>You'll receive an email notification when your request is approved or rejected</p>
                    </div>
                  </div>
                  <div class="process-step">
                    <div class="process-number">4</div>
                    <div class="process-content">
                      <h4>Start Signing</h4>
                      <p>Once approved, you can create your digital signature and sign reports</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="activeHelpTab === 'faq'" class="help-panel">
                <h3>Frequently Asked Questions</h3>
                <div class="faq-list">
                  <div class="faq-item">
                    <h4>How long does approval take?</h4>
                    <p>Most requests are reviewed within 1-2 business days. Complex requests may take longer.</p>
                  </div>
                  <div class="faq-item">
                    <h4>Can I request multiple authorizations?</h4>
                    <p>Yes, you can request authorization for multiple signatory names if your role requires it.</p>
                  </div>
                  <div class="faq-item">
                    <h4>What if my request is rejected?</h4>
                    <p>You'll receive an email with the reason for rejection and can resubmit with additional information.</p>
                  </div>
                  <div class="faq-item">
                    <h4>Do authorizations expire?</h4>
                    <p>Some authorizations may have expiry dates. You'll be notified before expiration to renew if needed.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Authorization Details Modal -->
    <div v-if="showAuthDetailsModal" class="modal-overlay" @click="closeAuthDetailsModal">
      <div class="modal-dialog" @click.stop>
        <div class="modal-header">
          <h3>Authorization Details</h3>
          <button class="modal-close" @click="closeAuthDetailsModal">
            <i class="pi pi-times"></i>
          </button>
        </div>
        <div class="modal-body" v-if="selectedAuthDetails">
          <div class="detail-section">
            <h4>Signatory Information</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Name:</span>
                <span class="detail-value">{{ selectedAuthDetails.signatory_name }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Title:</span>
                <span class="detail-value">{{ getSignatoryTitle(selectedAuthDetails.signatory_name) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Status:</span>
                <span class="detail-value" :class="selectedAuthDetails.is_valid ? 'status-active' : 'status-expired'">
                  {{ selectedAuthDetails.is_valid ? 'Active' : 'Expired' }}
                </span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>Authorization Details</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Authorized Date:</span>
                <span class="detail-value">{{ formatDate(selectedAuthDetails.authorization_date) }}</span>
              </div>
              <div class="detail-item" v-if="selectedAuthDetails.expiry_date">
                <span class="detail-label">Expiry Date:</span>
                <span class="detail-value">{{ formatDate(selectedAuthDetails.expiry_date) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">2FA Required:</span>
                <span class="detail-value">{{ selectedAuthDetails.requires_2fa ? 'Yes' : 'No' }}</span>
              </div>
              <div class="detail-item" v-if="selectedAuthDetails.authorized_by">
                <span class="detail-label">Authorized By:</span>
                <span class="detail-value">{{ selectedAuthDetails.authorized_by }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="selectedAuthDetails.has_signature">
            <h4>Digital Signature</h4>
            <div class="signature-display">
              <div class="signature-container">
                <img :src="selectedAuthDetails.signature_url" 
                     alt="Digital Signature" 
                     class="signature-image"
                     @load="onSignatureLoad"
                     @error="onSignatureError" />
                <div class="signature-info">
                  <div class="signature-meta">
                    <i class="pi pi-check-circle signature-verified"></i>
                    <span class="signature-status">Verified Digital Signature</span>
                  </div>
                  <div class="signature-details">
                    <small>This signature is securely stored and encrypted</small>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="!selectedAuthDetails.has_signature && selectedAuthDetails.signature_created">
            <h4>Digital Signature</h4>
            <div class="signature-display">
              <div class="signature-container no-signature">
                <div class="signature-placeholder">
                  <i class="pi pi-exclamation-triangle"></i>
                  <span>Signature file not found</span>
                  <small>The signature may have been moved or deleted</small>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="!selectedAuthDetails.signature_created">
            <h4>Digital Signature</h4>
            <div class="signature-display">
              <div class="signature-container no-signature">
                <div class="signature-placeholder">
                  <i class="pi pi-info-circle"></i>
                  <span>No signature created yet</span>
                  <small>User has not completed signature setup</small>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section" v-if="selectedAuthDetails.notes">
            <h4>Notes</h4>
            <p class="detail-notes">{{ selectedAuthDetails.notes }}</p>
          </div>

          <div class="detail-section">
            <h4>Security Information</h4>
            <div class="security-info">
              <div class="security-item">
                <i class="pi pi-shield"></i>
                <span>This authorization allows you to digitally sign reports as {{ selectedAuthDetails.signatory_name }}</span>
              </div>
              <div class="security-item">
                <i class="pi pi-lock"></i>
                <span>All signatures are logged and audited for security compliance</span>
              </div>
              <div class="security-item" v-if="selectedAuthDetails.requires_2fa">
                <i class="pi pi-mobile"></i>
                <span>Two-factor authentication is required for signing</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-modal-close" @click="closeAuthDetailsModal">Close</button>
        </div>
      </div>
    </div>

    <!-- Request Details Modal -->
    <div v-if="showRequestDetailsModal" class="modal-overlay" @click="closeRequestDetailsModal">
      <div class="modal-dialog" @click.stop>
        <div class="modal-header">
          <h3>Request Details</h3>
          <button class="modal-close" @click="closeRequestDetailsModal">
            <i class="pi pi-times"></i>
          </button>
        </div>
        <div class="modal-body" v-if="selectedRequestDetails">
          <div class="detail-section">
            <h4>Request Information</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Signatory Name:</span>
                <span class="detail-value">{{ selectedRequestDetails.signatory_name }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Role:</span>
                <span class="detail-value">{{ selectedRequestDetails.role }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Email:</span>
                <span class="detail-value">{{ selectedRequestDetails.email }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Status:</span>
                <span class="detail-value" :class="`status-${selectedRequestDetails.status.toLowerCase()}`">
                  {{ selectedRequestDetails.status }}
                </span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>Timeline</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Submitted:</span>
                <span class="detail-value">{{ formatDate(selectedRequestDetails.created_at) }}</span>
              </div>
              <div class="detail-item" v-if="selectedRequestDetails.reviewed_at">
                <span class="detail-label">Reviewed:</span>
                <span class="detail-value">{{ formatDate(selectedRequestDetails.reviewed_at) }}</span>
              </div>
              <div class="detail-item" v-if="selectedRequestDetails.reviewed_by">
                <span class="detail-label">Reviewed By:</span>
                <span class="detail-value">{{ selectedRequestDetails.reviewed_by }}</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>Justification</h4>
            <div class="justification-detail">
              <p>{{ selectedRequestDetails.justification }}</p>
            </div>
          </div>

          <div class="detail-section" v-if="selectedRequestDetails.admin_notes">
            <h4>Administrator Notes</h4>
            <div class="admin-notes">
              <p>{{ selectedRequestDetails.admin_notes }}</p>
            </div>
          </div>

          <div class="detail-section" v-if="selectedRequestDetails.status === 'PENDING'">
            <h4>Next Steps</h4>
            <div class="next-steps">
              <div class="step-item">
                <i class="pi pi-clock"></i>
                <span>Your request is being reviewed by system administrators</span>
              </div>
              <div class="step-item">
                <i class="pi pi-envelope"></i>
                <span>You will receive an email notification when a decision is made</span>
              </div>
              <div class="step-item">
                <i class="pi pi-times-circle"></i>
                <span>You can cancel this request at any time if needed</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-modal-close" @click="closeRequestDetailsModal">Close</button>
          <button 
            v-if="selectedRequestDetails.status === 'PENDING'" 
            class="btn-modal-danger" 
            @click="cancelRequest(selectedRequestDetails); closeRequestDetailsModal()"
          >
            Cancel Request
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from './AppLayout.vue';
import api from '../services/api';
import toast from '../utils/toast';

export default {
  name: 'SignatoryAuthorizationRequest',
  components: {
    AppLayout
  },
  data() {
    return {
      // Form data
      selectedSignatory: '',
      selectedRole: '',
      email: '',
      justification: '',
      submitting: false,
      
      // Step management
      currentStep: 1,
      
      // Data arrays
      userAuthorizations: [],
      pendingRequests: [],
      
      // Available options
      availableSignatories: [
        { name: 'O.M. LAVA', title: 'Prin. Engr. A, GPD' },
        { name: 'JMM MATA', title: 'Manager, GPD' },
        { name: 'EL ADIONG', title: 'Acting Manager, GPD' },
        { name: 'C.C. AMIGABLE JR.', title: 'Dept. Manager, GPD' },
        { name: 'D.R.B. CAIRO', title: 'Prin. Engr. B, GPD' },
        { name: 'DB ESMADE JR.', title: 'Acting Dept. Manager, GPD' }
      ],
      
      availableRoles: [
        {
          value: 'Prepared by:',
          label: 'Prepared by',
          description: 'Responsible for creating and preparing reports',
          icon: 'pi pi-file-edit'
        },
        {
          value: 'Checked and Reviewed by:',
          label: 'Checked and Reviewed by',
          description: 'Reviews and validates report content',
          icon: 'pi pi-search'
        },
        {
          value: 'Approved by:',
          label: 'Approved by',
          description: 'Final approval and authorization of reports',
          icon: 'pi pi-check-circle'
        }
      ],
      
      // Help system
      activeHelpTab: 'overview',
      helpTabs: [
        { id: 'overview', label: 'Overview', icon: 'pi pi-info-circle' },
        { id: 'process', label: 'Process', icon: 'pi pi-cog' },
        { id: 'faq', label: 'FAQ', icon: 'pi pi-question-circle' }
      ],
      
      // Modal states
      showAuthDetailsModal: false,
      selectedAuthDetails: null,
      showRequestDetailsModal: false,
      selectedRequestDetails: null
    };
  },
  computed: {
    canSubmit() {
      return this.selectedSignatory && 
             this.selectedRole && 
             this.email.trim().length > 0 &&
             this.isValidEmail(this.email) &&
             this.justification.trim().length >= 20 &&
             this.currentStep === 3;
    }
  },
  mounted() {
    this.loadUserAuthorizations();
    this.loadPendingRequests();
    
    // Check for query parameters to pre-fill form with animation
    if (this.$route.query.signatory && this.$route.query.role) {
      // Animate through the steps automatically
      this.$nextTick(() => {
        // Scroll to request section first
        setTimeout(() => {
          const requestSection = document.querySelector('.request-section');
          if (requestSection) {
            requestSection.scrollIntoView({ 
              behavior: 'smooth', 
              block: 'start' 
            });
          }
        }, 100);
        
        // Step 1: Show signatory selection and auto-select (2 seconds)
        setTimeout(() => {
          this.currentStep = 1;
          this.selectedSignatory = this.$route.query.signatory;
        }, 500);
        
        // Step 2: Transition to role selection (show cards first)
        setTimeout(() => {
          this.currentStep = 2;
        }, 2500);
        
        // Then auto-select the role (show checkmark animation)
        setTimeout(() => {
          this.selectedRole = this.$route.query.role;
        }, 3000);
        
        // Step 3: Transition to justification (3 seconds after step 2)
        setTimeout(() => {
          this.currentStep = 3;
        }, 5500);
      });
    } else if (this.$route.query.signatory) {
      // Only signatory provided
      this.selectedSignatory = this.$route.query.signatory;
      this.currentStep = 2;
    } else if (this.$route.query.role) {
      // Only role provided
      this.selectedRole = this.$route.query.role;
    }
  },
  methods: {
    // Data loading methods
    async loadUserAuthorizations() {
      try {
        const response = await api.getUserSignatoryAuthorizations();
        const data = Array.isArray(response.data) ? response.data : (response.data.results || []);
        if (data.length === 0) throw new Error("empty");
        this.userAuthorizations = data;
      } catch (error) {
        console.warn('Using mock authorizations');
        this.userAuthorizations = [
          {
            id: 1,
            signatory_name: 'EL ADIONG',
            authorization_date: new Date(Date.now() - 86400000 * 30).toISOString(),
            expiry_date: new Date(Date.now() + 86400000 * 335).toISOString(),
            is_valid: true,
            requires_2fa: true,
            has_signature: true,
            signature_created: true,
            signature_url: 'https://via.placeholder.com/300x100.png?text=E.+Adiong+Signature'
          },
          {
            id: 2,
            signatory_name: 'O.M. LAVA',
            authorization_date: new Date(Date.now() - 86400000 * 400).toISOString(),
            expiry_date: new Date(Date.now() - 86400000 * 35).toISOString(),
            is_valid: false,
            requires_2fa: false,
            has_signature: false,
            signature_created: true
          }
        ];
      }
    },

    async loadPendingRequests() {
      try {
        const response = await api.getUserAuthorizationRequests();
        const data = Array.isArray(response.data) ? response.data : (response.data.results || []);
        if (data.length === 0) throw new Error("empty");
        this.pendingRequests = data.filter(
          request => request.status === 'PENDING'
        );
      } catch (error) {
        console.warn('Using mock pending requests');
        this.pendingRequests = [
          {
            id: 101,
            signatory_name: 'JMM MATA',
            role: 'Approved by:',
            status: 'PENDING',
            created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
            justification: 'Need authorization to approve weekly generation reports for the Agus plant cluster as part of my new acting duties.'
          }
        ];
      }
    },

    // Step navigation
    nextStep() {
      if (this.currentStep < 3) {
        this.currentStep++;
      }
    },

    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    // Selection methods
    selectSignatory(signatoryName) {
      // Check if user already has active authorization for this signatory
      const existingAuth = this.userAuthorizations.find(
        auth => auth.signatory_name === signatoryName && auth.is_valid
      );
      
      if (existingAuth) {
        toast.warning(`⚠️ You already have active authorization for ${signatoryName}`);
        return;
      }
      
      // Check if user has pending request for this signatory
      const pendingRequest = this.pendingRequests.find(
        request => request.signatory_name === signatoryName && request.status === 'PENDING'
      );
      
      if (pendingRequest) {
        toast.warning(`⚠️ You already have a pending request for ${signatoryName}`);
        return;
      }
      
      this.selectedSignatory = signatoryName;
    },

    selectRole(roleValue) {
      this.selectedRole = roleValue;
    },

    // Form submission
    async submitRequest() {
      if (!this.canSubmit) return;

      this.submitting = true;
      try {
        console.log('Submitting authorization request:', {
          signatory_name: this.selectedSignatory,
          role: this.selectedRole,
          email: this.email,
          justification: this.justification
        });

        await api.requestSignatoryAuthorization({
          signatory_name: this.selectedSignatory,
          role: this.selectedRole,
          email: this.email,
          justification: this.justification
        });

        // Show success message
        toast.success('🎉 Authorization request submitted successfully! You will receive an email notification when it is reviewed.');

        // Reset form
        this.resetForm();

        // Reload pending requests
        await this.loadPendingRequests();

      } catch (error) {
        console.error('Error submitting request:', error);
        console.error('Error response:', error.response?.data);
        
        // Extract error message
        let errorMessage = 'Failed to submit request. Please try again.';
        
        if (error.response?.data) {
          if (error.response.data.error) {
            errorMessage = error.response.data.error;
          } else if (error.response.data.detail) {
            errorMessage = error.response.data.detail;
          } else if (typeof error.response.data === 'object') {
            // Handle field-specific errors
            const errors = Object.entries(error.response.data)
              .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
              .join('; ');
            errorMessage = errors || errorMessage;
          }
        }
        
        toast.error(`❌ ${errorMessage}`);
      } finally {
        this.submitting = false;
      }
    },

    // Utility methods
    resetForm() {
      this.selectedSignatory = '';
      this.selectedRole = '';
      this.email = '';
      this.justification = '';
      this.currentStep = 1;
    },

    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },

    updateCharacterCount() {
      // Character count is handled by the template
    },

    getSignatoryTitle(signatoryName) {
      const signatory = this.availableSignatories.find(s => s.name === signatoryName);
      return signatory ? signatory.title : 'Unknown Title';
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    // Action methods
    viewAuthDetails(auth) {
      console.log('🔍 Viewing auth details:', auth);
      console.log('🖼️ Signature URL:', auth.signature_url);
      console.log('✅ Has signature:', auth.has_signature);
      console.log('📝 Signature created:', auth.signature_created);
      
      this.selectedAuthDetails = auth;
      this.showAuthDetailsModal = true;
    },

    viewRequestDetails(request) {
      this.selectedRequestDetails = request;
      this.showRequestDetailsModal = true;
    },

    closeAuthDetailsModal() {
      this.showAuthDetailsModal = false;
      this.selectedAuthDetails = null;
    },

    onSignatureLoad() {
      console.log('✅ Signature image loaded successfully');
    },

    onSignatureError(event) {
      console.error('❌ Signature image failed to load:', event);
      console.error('❌ Image src:', event.target.src);
    },

    closeRequestDetailsModal() {
      this.showRequestDetailsModal = false;
      this.selectedRequestDetails = null;
    },

    // Helper methods for signatory status
    hasActiveAuthorization(signatoryName) {
      return this.userAuthorizations.some(
        auth => auth.signatory_name === signatoryName && auth.is_valid
      );
    },

    hasPendingRequest(signatoryName) {
      return this.pendingRequests.some(
        request => request.signatory_name === signatoryName && request.status === 'PENDING'
      );
    },

    isSignatoryDisabled(signatoryName) {
      return this.hasActiveAuthorization(signatoryName) || this.hasPendingRequest(signatoryName);
    },

    async cancelRequest(request) {
      if (confirm(`Are you sure you want to cancel the authorization request for ${request.signatory_name}?`)) {
        try {
          await api.cancelAuthorizationRequest(request.id);
          toast.success('Request cancelled successfully');
          await this.loadPendingRequests();
        } catch (error) {
          console.error('Error cancelling request:', error);
          
          // Extract error message
          let errorMessage = 'Failed to cancel request';
          if (error.response?.data?.error) {
            errorMessage = error.response.data.error;
          } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message;
          }
          
          toast.error(errorMessage);
        }
      }
    },

    async deleteAuthorization(authorization) {
      if (confirm(`Are you sure you want to delete the authorization for ${authorization.signatory_name}? This action cannot be undone.`)) {
        try {
          await api.deleteAuthorization(authorization.id);
          toast.success('Authorization deleted successfully');
          await this.loadUserAuthorizations();
        } catch (error) {
          console.error('Error deleting authorization:', error);
          
          // Extract error message
          let errorMessage = 'Failed to delete authorization';
          if (error.response?.data?.error) {
            errorMessage = error.response.data.error;
          } else if (error.response?.data?.detail) {
            errorMessage = error.response.data.detail;
          } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message;
          }
          
          toast.error(errorMessage);
        }
      }
    },

    // Signature status methods
    getSignatureStatusClass(auth) {
      if (auth.has_signature) {
        return 'signature-verified';
      } else if (auth.signature_created) {
        return 'signature-missing';
      } else {
        return 'signature-none';
      }
    },

    getSignatureStatusIcon(auth) {
      if (auth.has_signature) {
        return 'pi pi-check-circle';
      } else if (auth.signature_created) {
        return 'pi pi-exclamation-triangle';
      } else {
        return 'pi pi-times-circle';
      }
    },

    getSignatureStatusText(auth) {
      if (auth.has_signature) {
        return 'Signature Ready';
      } else if (auth.signature_created) {
        return 'Signature File Missing';
      } else {
        return 'No Signature Created';
      }
    }
  }
};
</script>

<style scoped>
/* ===== MODERN INTERACTIVE DESIGN ===== */

/* Icon Styling */
.authorization-request-page i {
  display: inline-block !important;
  font-style: normal;
  font-weight: normal;
}

/* Page Layout */
.authorization-request-page {
  background: #f8fafc;
  min-height: 100vh;
  padding: 0;
  margin: 0;
  position: relative;
}

/* Decorative Elements */
.authorization-request-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 300px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  clip-path: ellipse(100% 100% at 50% 0%);
  z-index: 0;
}

/* Hero Section */
.hero-section {
  background: transparent;
  color: white;
  padding: 4rem 2rem 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 40%),
              radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 40%);
  opacity: 0.7;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  opacity: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  color: white;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
  position: relative;
  transition: all 0.3s ease;
  animation: pulse 2s infinite;
}

.hero-icon:hover {
  transform: scale(1.1) rotate(5deg);
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.4));
}

.hero-icon i {
  display: inline-block !important;
  font-style: normal;
  font-weight: normal;
  line-height: 1;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  color: white;
  letter-spacing: -0.5px;
  position: relative;
  display: inline-block;
  background: linear-gradient(to right, white 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all 0.3s ease;
}

.hero-title:hover {
  transform: scale(1.02);
  text-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

.hero-subtitle {
  font-size: 1.4rem;
  opacity: 0.95;
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  color: white;
  text-shadow: 0 3px 8px rgba(0, 0, 0, 0.25);
  font-weight: 400;
  line-height: 1.6;
  position: relative;
  transition: all 0.3s ease;
}

.hero-subtitle:hover {
  opacity: 1;
  transform: translateY(-2px);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: fadeInUp 0.6s ease forwards;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.5);
  min-height: 160px;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed, #4f46e5);
  transform: scaleX(0);
  transition: transform 0.4s ease;
  transform-origin: left;
}

.stat-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 50px rgba(79, 70, 229, 0.2);
  border-color: rgba(79, 70, 229, 0.3);
}

.stat-card:hover::before {
  transform: scaleX(1);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon i {
  display: inline-block !important;
  font-style: normal;
  font-weight: normal;
  line-height: 1;
}

.stat-icon {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-icon::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
  transform: translateX(-100%) rotate(45deg);
  transition: transform 0.6s ease;
}

.stat-icon:hover::after {
  transform: translateX(100%) rotate(45deg);
}

.stat-icon.success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
}

.stat-icon.warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.3);
}

.stat-icon.info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

.stat-icon:hover {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 10px 30px currentColor;
}

.stat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1;
  color: #1e293b;
  letter-spacing: -1px;
  transition: all 0.3s ease;
  position: relative;
}

.stat-card:hover .stat-number {
  color: #4f46e5;
  transform: scale(1.1);
  text-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
}

.stat-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  line-height: 1.3;
  transition: all 0.3s ease;
}

.stat-card:hover .stat-label {
  color: #4f46e5;
  transform: translateY(-2px);
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  margin-top: -2rem;
  position: relative;
  z-index: 2;
}

/* Section Cards */
.section-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  margin-bottom: 2rem;
  overflow: hidden;
  border: 1px solid rgba(79, 70, 229, 0.1);
  animation: fadeInUp 0.6s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
  transition: all 0.4s ease;
  position: relative;
}

.section-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
  transform: scaleX(0);
  transition: transform 0.6s ease;
  transform-origin: left;
}

.section-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 35px 70px rgba(79, 70, 229, 0.2);
}

.section-card:hover::before {
  transform: scaleX(1);
}

.section-header {
  padding: 2rem 2rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-title i {
  font-size: 1.8rem;
  color: #4f46e5;
  display: inline-block !important;
  font-style: normal;
  font-weight: normal;
  transition: all 0.3s ease;
  position: relative;
}

.section-title:hover i {
  transform: rotate(10deg) scale(1.2);
  color: #7c3aed;
  text-shadow: 0 0 15px rgba(124, 58, 237, 0.5);
}

.section-title h2 {
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
  color: #1e293b;
}

.section-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.section-badge.success {
  background: #dcfce7;
  color: #166534;
}

.section-badge.warning {
  background: #fef3c7;
  color: #92400e;
}

/* Authorization Cards */
.authorizations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
}

.authorization-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: slideInLeft 0.6s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
  opacity: 0;
  position: relative;
  overflow: hidden;
}

.authorization-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  transform: scaleX(0);
  transition: transform 0.4s ease;
  transform-origin: left;
}

.authorization-card:hover {
  transform: translateY(-8px) scale(1.01);
  box-shadow: 0 15px 40px rgba(79, 70, 229, 0.25);
  border-color: #4f46e5;
}

.authorization-card:hover::before {
  transform: scaleX(1);
}

.authorization-card.expired {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-color: #fca5a5;
}

.auth-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.auth-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.4rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
  position: relative;
  overflow: hidden;
}

/* Signature Status Indicator on Avatar */
.signature-indicator {
  position: absolute;
  top: -3px;
  right: -3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  z-index: 2;
}

.signature-indicator.signature-verified {
  background: #22c55e;
  color: white;
}

.signature-indicator.signature-missing {
  background: #f59e0b;
  color: white;
}

.signature-indicator.signature-none {
  background: #ef4444;
  color: white;
}

.signature-indicator:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Signature Status Text */
.signature-status-text {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  margin-top: 0.3rem;
  transition: all 0.3s ease;
}

.signature-status-text.signature-verified {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.signature-status-text.signature-missing {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.signature-status-text.signature-none {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.signature-status-text i {
  font-size: 0.8rem;
  display: inline-block !important;
}

.authorization-card:hover .signature-status-text {
  transform: translateX(3px);
}

.auth-avatar::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
  transform: translateX(-100%) rotate(45deg);
  transition: transform 0.6s ease;
}

.auth-avatar:hover::after {
  transform: translateX(100%) rotate(45deg);
}

.auth-avatar:hover {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5);
}

.auth-avatar i {
  display: inline-block !important;
}

.auth-info {
  flex: 1;
}

.auth-name {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #1e293b;
  transition: all 0.3s ease;
  position: relative;
}

.authorization-card:hover .auth-name {
  color: #4f46e5;
  transform: translateX(5px);
}

.auth-role {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.auth-status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.auth-status-badge {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.auth-status-badge::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.auth-status-badge:hover::after {
  transform: translateX(100%);
}

.auth-status-badge.signature-verified {
  background: #dcfce7;
  color: #166534;
  box-shadow: 0 4px 12px rgba(22, 101, 52, 0.2);
}

.auth-status-badge.signature-missing {
  background: #fef3c7;
  color: #92400e;
  box-shadow: 0 4px 12px rgba(146, 64, 14, 0.2);
}

.auth-status-badge.signature-none {
  background: #fee2e2;
  color: #dc2626;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

.authorization-card:hover .auth-status-badge {
  transform: scale(1.05);
}

.auth-card-body {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-top: 0.5rem;
}

.auth-details {
  flex: 1;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.2;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item i {
  color: #4f46e5;
  font-size: 1.1rem;
  display: inline-block !important;
}

.btn-action {
  padding: 0.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
}

.btn-action {
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
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

.btn-action.secondary {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-action.secondary:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  color: #1e293b;
}

.btn-action.danger {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fca5a5;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
}

.btn-action.danger:hover {
  background: linear-gradient(135deg, #fca5a5 0%, #f87171 100%);
  color: white;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.3);
}

.auth-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-self: flex-start;
  margin-top: 0.25rem;
}

/* Progress Indicator */
.progress-indicator {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.progress-step.active {
  color: #4f46e5;
}

.progress-step.completed {
  color: #22c55e;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.progress-step.active .step-number {
  background: #4f46e5;
  color: white;
}

.progress-step.completed .step-number {
  background: #22c55e;
  color: white;
}

.progress-line {
  width: 60px;
  height: 2px;
  background: #e2e8f0;
  transition: all 0.3s ease;
}

.progress-line.active {
  background: #4f46e5;
}

/* Form Steps */
.request-form-container {
  padding: 2rem;
}

.form-step {
  display: none;
  animation: fadeIn 0.5s ease forwards;
}

.form-step.active {
  display: block;
}

.step-header {
  text-align: center;
  margin-bottom: 2rem;
}

.step-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.step-header p {
  color: #64748b;
  font-size: 1rem;
}

/* Interactive Grids */
.signatory-grid,
.role-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.signatory-card,
.role-card {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.signatory-card:hover,
.role-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #4f46e5;
}

.signatory-card.selected,
.role-card.selected {
  border-color: #4f46e5;
  background: linear-gradient(135deg, #ede9fe 0%, #f3f4f6 100%);
  box-shadow: 0 8px 25px rgba(79, 70, 229, 0.15);
}

.signatory-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.signatory-card.disabled:hover {
  transform: none;
  box-shadow: none;
  border-color: #cbd5e1;
}

.signatory-card.has-authorization {
  border-color: #22c55e;
  background: linear-gradient(135deg, #f0fdf4 0%, #f8fafc 100%);
}

.signatory-card.has-pending {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #f8fafc 100%);
}

.signatory-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

.signatory-status.active {
  background: #dcfce7;
  color: #166534;
}

.signatory-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.signatory-status i {
  font-size: 0.9rem;
}

.signatory-avatar,
.role-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.signatory-avatar i,
.role-icon i {
  display: inline-block !important;
}

.signatory-info h4,
.role-info h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.signatory-info p,
.role-info p {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.selection-indicator {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 24px;
  height: 24px;
  background: #22c55e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.8rem;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
}

.signatory-card.selected .selection-indicator,
.role-card.selected .selection-indicator {
  opacity: 1;
  transform: scale(1);
}

/* Step Actions */
.step-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-back,
.btn-next,
.btn-submit {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 140px;
  justify-content: center;
}

.btn-back {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.btn-back:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
}

.btn-next {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
}

.btn-next:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(79, 70, 229, 0.3);
}

.btn-next:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  min-width: 180px;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit.submitting {
  background: #94a3b8;
}

/* Form Fields */
.justification-section {
  max-width: 600px;
  margin: 0 auto;
}

.form-field {
  margin-bottom: 2rem;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.textarea-container {
  position: relative;
}

.form-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.form-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.form-textarea:focus,
.form-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
  background: white;
}

.character-count {
  position: absolute;
  bottom: 0.75rem;
  right: 1rem;
  font-size: 0.8rem;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.field-hint {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.4;
}

.field-hint i {
  color: #4f46e5;
  margin-top: 0.1rem;
  flex-shrink: 0;
}

/* Request Summary */
.request-summary {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 2rem;
}

.request-summary h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.summary-grid {
  display: grid;
  gap: 0.75rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-label {
  font-weight: 500;
  color: #64748b;
}

.summary-value {
  font-weight: 600;
  color: #1e293b;
}

/* Pending Requests */
.pending-requests-list {
  padding: 2rem;
}

.pending-request-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  animation: slideInRight 0.6s ease forwards;
  opacity: 0;
}

.pending-request-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.request-info h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.request-info p {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.request-status {
  text-align: right;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.status-indicator.pending {
  color: #92400e;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #fbbf24;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.request-date {
  font-size: 0.8rem;
  color: #94a3b8;
}

.request-body {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.justification-preview {
  margin-bottom: 1rem;
}

.justification-preview strong {
  color: #374151;
  font-size: 0.9rem;
}

.justification-preview p {
  margin: 0.5rem 0 0 0;
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.4;
}

.request-actions {
  display: flex;
  gap: 0.75rem;
}

/* Help Section */
.help-content {
  padding: 2rem;
}

.help-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.help-tab {
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.help-tab:hover {
  background: #f1f5f9;
  color: #374151;
}

.help-tab.active {
  background: #4f46e5;
  color: white;
}

.help-tab-content {
  min-height: 300px;
}

.help-panel h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.help-panel p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.help-panel ul {
  color: #64748b;
  line-height: 1.6;
  padding-left: 1.5rem;
}

.help-panel li {
  margin-bottom: 0.5rem;
}

.help-panel strong {
  color: #374151;
}

/* Process Steps */
.process-steps {
  display: grid;
  gap: 1.5rem;
}

.process-step {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.process-number {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.process-content h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.process-content p {
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

/* FAQ */
.faq-list {
  display: grid;
  gap: 1.5rem;
}

.faq-item h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.faq-item p {
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

/* Animations */
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

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
  
  .authorizations-grid {
    grid-template-columns: 1fr;
  }
  
  .signatory-grid,
  .role-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 3rem 1rem 2rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .main-content {
    padding: 1rem;
    margin-top: -1rem;
  }
  
  .section-header {
    padding: 1.5rem 1.5rem 1rem;
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .progress-indicator {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .progress-line {
    display: none;
  }
  
  .step-actions {
    flex-direction: column;
  }
  
  .btn-back,
  .btn-next,
  .btn-submit {
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 1.5rem;
  }
  
  .help-tabs {
    flex-wrap: wrap;
  }
  
  .help-tab {
    flex: 1;
    min-width: 120px;
  }
}

@media (max-width: 480px) {
  .hero-icon {
    font-size: 3rem;
  }
  
  .hero-title {
    font-size: 1.8rem;
  }
  
  .section-title h2 {
    font-size: 1.5rem;
  }
  
  .authorizations-grid,
  .pending-requests-list {
    padding: 1rem;
  }
  
  .request-form-container {
    padding: 1rem;
  }
  
  .help-content {
    padding: 1rem;
  }
}
@keyframes pulse {
  0% {
    transform: scale(1);
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
  }
  50% {
    transform: scale(1.05);
    filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.4));
  }
  100% {
    transform: scale(1);
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
  }
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-dialog {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  animation: slideInUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.modal-body {
  padding: 2rem;
  max-height: 60vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.detail-grid {
  display: grid;
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #4f46e5;
}

.detail-label {
  font-weight: 600;
  color: #374151;
}

.detail-value {
  font-weight: 500;
  color: #1e293b;
}

.detail-value.status-active {
  color: #059669;
  font-weight: 600;
}

.detail-value.status-expired {
  color: #dc2626;
  font-weight: 600;
}

.detail-value.status-pending {
  color: #d97706;
  font-weight: 600;
}

.detail-value.status-approved {
  color: #059669;
  font-weight: 600;
}

.detail-value.status-rejected {
  color: #dc2626;
  font-weight: 600;
}

.detail-value.status-cancelled {
  color: #6b7280;
  font-weight: 600;
}

.detail-notes,
.justification-detail p,
.admin-notes p {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #4f46e5;
  margin: 0;
  line-height: 1.6;
  color: #374151;
}

/* Signature Display Styles */
.signature-display {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid #e2e8f0;
}

.signature-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.signature-container.no-signature {
  padding: 2rem;
  background: #fafafa;
  border: 2px dashed #d1d5db;
  border-radius: 8px;
}

.signature-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  text-align: center;
}

.signature-placeholder i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.signature-placeholder i.pi-exclamation-triangle {
  color: #f59e0b;
}

.signature-placeholder i.pi-info-circle {
  color: #3b82f6;
}

.signature-placeholder span {
  font-weight: 600;
  font-size: 1rem;
  color: #374151;
}

.signature-placeholder small {
  font-size: 0.8rem;
  color: #6b7280;
}

.signature-image {
  max-width: 300px;
  max-height: 120px;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  background: white;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.signature-info {
  text-align: center;
}

.signature-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.signature-verified {
  color: #059669;
  font-size: 1.1rem;
}

.signature-status {
  color: #059669;
  font-weight: 600;
  font-size: 0.9rem;
}

.signature-details {
  color: #6b7280;
  font-size: 0.8rem;
}

.security-info,
.next-steps {
  display: grid;
  gap: 0.75rem;
}

.security-item,
.step-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f0f9ff;
  border-radius: 8px;
  border-left: 4px solid #0ea5e9;
}

.security-item i,
.step-item i {
  color: #0ea5e9;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.security-item span,
.step-item span {
  color: #374151;
  line-height: 1.4;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: #f8fafc;
}

.btn-modal-close,
.btn-modal-danger {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-modal-close {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.btn-modal-close:hover {
  background: #e2e8f0;
  transform: translateY(-1px);
}

.btn-modal-danger {
  background: #dc2626;
  color: white;
}

.btn-modal-danger:hover {
  background: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive Modal */
@media (max-width: 768px) {
  .modal-dialog {
    width: 95%;
    max-height: 90vh;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
  
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn-modal-close,
  .btn-modal-danger {
    width: 100%;
  }
}

/* ===== END OF STYLES ===== */
</style>
