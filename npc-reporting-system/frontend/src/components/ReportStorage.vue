<template>
  <AppLayout>
    <div class="report-storage">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1>Report Storage</h1>
          <p>Manage and access your generated reports with digital signatures</p>
        </div>
        <div class="header-actions">
          <button class="btn-primary" @click="refreshReports">
            <i class="pi pi-refresh" :class="{ 'pi-spin': loading }"></i>
            Refresh
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="pi pi-file-check"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.totalReports }}</h3>
              <p>Total Reports</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon signed">
              <i class="pi pi-verified"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.signedReports }}</h3>
              <p>Signed Reports</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon pending">
              <i class="pi pi-clock"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.pendingSignatures }}</h3>
              <p>Pending Signatures</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon recent">
              <i class="pi pi-calendar"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.recentReports }}</h3>
              <p>This Month</p>
            </div>
          </div>
        </div>
      </div>
      <!-- Filters and Search -->
      <div class="filters-section">
        <div class="search-bar">
          <i class="pi pi-search"></i>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search reports by title, type, or plant..."
            class="search-input"
          />
        </div>
        <div class="filters">
          <select v-model="typeFilter" class="filter-select">
            <option value="">All Report Types</option>
            <option value="PSR">PSR Reports</option>
            <option value="Daily Status">Daily Status</option>
            <option value="Monthly">Monthly Reports</option>
            <option value="Custom">Custom Reports</option>
          </select>
          <select v-model="statusFilter" class="filter-select">
            <option value="">All Status</option>
            <option value="DRAFT">Draft</option>
            <option value="PENDING_SIGNATURE">Pending Signature</option>
            <option value="SIGNED">Signed & Complete</option>
          </select>
          <select v-model="plantFilter" class="filter-select">
            <option value="">All Plants</option>
            <option value="PLANT_A">Plant A</option>
            <option value="PLANT_B">Plant B</option>
            <option value="PLANT_C">Plant C</option>
          </select>
        </div>
      </div>

      <!-- Reports List -->
      <div class="reports-section">
        <div v-if="loading" class="loading-state">
          <i class="pi pi-spin pi-spinner"></i>
          <p>Loading reports...</p>
        </div>

        <div v-else-if="filteredReports.length === 0" class="empty-state">
          <i class="pi pi-file-excel"></i>
          <h3>{{ hasFilters ? 'No reports found' : 'No reports available' }}</h3>
          <p>{{ hasFilters ? 'Try adjusting your search or filter criteria.' : 'Generated reports will appear here once created.' }}</p>
          <button v-if="hasFilters" class="btn-action secondary" @click="clearFilters">
            <i class="pi pi-filter-slash"></i>
            Clear Filters
          </button>
        </div>
        <div v-else class="reports-grid">
          <div 
            v-for="report in filteredReports" 
            :key="report.id"
            class="report-card"
          >
            <div class="report-header">
              <div class="report-info">
                <h3>{{ report.title }}</h3>
                <div class="report-meta">
                  <span class="report-type">
                    <i class="pi pi-file-excel"></i>
                    {{ report.document_type || 'PSR Report' }}
                  </span>
                  <span class="report-date">
                    <i class="pi pi-calendar"></i>
                    {{ formatDate(report.created_at) }}
                  </span>
                  <span v-if="report.plant_code" class="report-plant">
                    <i class="pi pi-building"></i>
                    {{ report.plant_code }}
                  </span>
                </div>
              </div>
              <div class="report-status flex items-center gap-2">
                <span :class="['status-badge', getStatusClass(report.status)]">
                  <i :class="getStatusIcon(report.status)"></i>
                  {{ getStatusLabel(report.status) }}
                </span>
                <div class="action-menu">
                  <button class="menu-trigger" @click="toggleReportMenu(report.id, $event)" :class="{ active: activeMenu === report.id }">
                    <i class="pi pi-ellipsis-v"></i>
                  </button>
                  <div v-if="activeMenu === report.id" class="menu-dropdown" @click.stop>
                    <button class="menu-item" @click="duplicateReport(report)">
                      <i class="pi pi-copy"></i>
                      Duplicate
                    </button>
                    <button class="menu-item" @click="archiveReport(report)">
                      <i class="pi pi-box"></i>
                      Archive
                    </button>
                    <div class="menu-divider"></div>
                    <button class="menu-item danger" @click="confirmDeleteReport(report)">
                      <i class="pi pi-trash"></i>
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="report-content">
              <div class="report-description" v-if="report.description">
                <p>{{ report.description }}</p>
              </div>
              
              <!-- Signature Status -->
              <div class="signature-status">
                <div v-if="report.signature_requests && report.signature_requests.length > 0" class="signatures-info">
                  <h4>Signature Status:</h4>
                  <div class="signatures-list">
                    <div 
                      v-for="signature in report.signature_requests" 
                      :key="signature.id"
                      class="signature-item"
                    >
                      <div class="signer-info">
                        <span class="signer-name">{{ signature.signer_name }}</span>
                        <span class="signer-role">{{ signature.signer_role }}</span>
                      </div>
                      <span :class="['signature-status-badge', signature.status.toLowerCase()]">
                        <i :class="getSignatureStatusIcon(signature.status)"></i>
                        {{ signature.status }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-else class="no-signatures">
                  <i class="pi pi-info-circle"></i>
                  <span>No signatures required</span>
                </div>
              </div>
            </div>
            <div class="report-actions">
              <button 
                class="btn-action primary" 
                @click="downloadReport(report)"
                v-if="report.file_path"
                title="Download Report"
              >
                <i class="pi pi-download"></i>
                Download
              </button>
              <button 
                class="btn-action secondary" 
                @click="viewSignatures(report)"
                v-if="report.signature_requests && report.signature_requests.length > 0"
                title="View Signatures"
              >
                <i class="pi pi-eye"></i>
                View Signatures
              </button>
              <button 
                class="btn-action secondary" 
                @click="requestSignatures(report)"
                v-if="report.status === 'DRAFT'"
                title="Request Signatures"
              >
                <i class="pi pi-send"></i>
                Request Signatures
              </button>
              <button 
                class="btn-action secondary" 
                @click="viewDetails(report)"
                title="View Details"
              >
                <i class="pi pi-info-circle"></i>
                Details
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- Signatures Viewer Modal -->
      <div v-if="showSignaturesViewerModal" class="modal-overlay" @click="showSignaturesViewerModal = false">
        <div class="modal-content large" @click.stop>
          <div class="modal-header">
            <h3>Signatures for "{{ selectedReportForViewing?.title }}"</h3>
            <button class="btn-close" @click="showSignaturesViewerModal = false">
              <i class="pi pi-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="signatures-list">
              <div v-if="selectedReportSignatures.length === 0" class="empty-state">
                <i class="pi pi-file-edit"></i>
                <p>No signature requests found for this report.</p>
              </div>
              <div 
                v-for="signature in selectedReportSignatures" 
                :key="signature.id"
                class="signature-item"
              >
                <div class="signature-info">
                  <h5>{{ signature.signer_name }}</h5>
                  <p>Role: {{ signature.signer_role }}</p>
                  <p>Email: {{ signature.signer_email }}</p>
                  <p>Status: <span :class="['status-badge', signature.status.toLowerCase()]">{{ signature.status }}</span></p>
                  <p v-if="signature.signed_at">Signed: {{ formatDate(signature.signed_at) }}</p>
                </div>
                
                <!-- Digital Signature Display -->
                <div v-if="signature.digitalSignature && signature.status === 'SIGNED'" class="signature-display">
                  <h6>Digital Signature:</h6>
                  <div class="signature-image-container">
                    <img 
                      :src="getSignatureImageUrl(signature.digitalSignature)"
                      :alt="`Signature by ${signature.signer_name}`"
                      class="signature-image"
                      @error="handleSignatureImageError"
                    />
                    <div class="signature-metadata">
                      <small>Type: {{ getSignatureTypeLabel(signature.digitalSignature.signature_type) }}</small>
                      <small>Signed: {{ formatDate(signature.digitalSignature.signing_timestamp) }}</small>
                    </div>
                  </div>
                </div>
                
                <!-- Pending Signature Placeholder -->
                <div v-else-if="signature.status === 'PENDING'" class="signature-pending">
                  <div class="pending-signature-placeholder">
                    <i class="pi pi-clock"></i>
                    <span>Awaiting signature</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>
<script>
import AppLayout from './AppLayout.vue'
import api from '../services/api'

export default {
  name: 'ReportStorage',
  components: {
    AppLayout
  },
  data() {
    return {
      reports: [],
      loading: false,
      searchQuery: '',
      typeFilter: '',
      statusFilter: '',
      plantFilter: '',
      activeMenu: null,
      
      // Stats
      stats: {
        totalReports: 0,
        signedReports: 0,
        pendingSignatures: 0,
        recentReports: 0
      },
      
      // Signature viewer modal
      showSignaturesViewerModal: false,
      selectedReportForViewing: null,
      selectedReportSignatures: []
    }
  },
  computed: {
    filteredReports() {
      let filtered = this.reports
      
      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(report => 
          report.title.toLowerCase().includes(query) ||
          (report.document_type && report.document_type.toLowerCase().includes(query)) ||
          (report.plant_code && report.plant_code.toLowerCase().includes(query))
        )
      }
      
      // Type filter
      if (this.typeFilter) {
        filtered = filtered.filter(report => 
          report.document_type === this.typeFilter
        )
      }
      
      // Status filter
      if (this.statusFilter) {
        filtered = filtered.filter(report => 
          report.status === this.statusFilter
        )
      }
      
      // Plant filter
      if (this.plantFilter) {
        filtered = filtered.filter(report => 
          report.plant_code === this.plantFilter
        )
      }
      
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    },
    
    hasFilters() {
      return this.searchQuery || this.typeFilter || this.statusFilter || this.plantFilter
    }
  },
  mounted() {
    this.loadReports()
    this.calculateStats()
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    handleClickOutside(event) {
      if (this.activeMenu) {
        const isMenuClick = event.target.closest('.action-menu')
        if (!isMenuClick) {
          this.activeMenu = null
        }
      }
    },
    async loadReports() {
      this.loading = true
      try {
        // Load documents (which are now treated as reports)
        const response = await api.getDocuments()
        this.reports = response.data.results || response.data || []
        
        // Load signature requests for each report
        await this.loadSignatureRequests()
        
        this.calculateStats()
      } catch (error) {
        console.error('Error loading reports:', error)
        // Show sample data for demo
        this.loadSampleReports()
      } finally {
        this.loading = false
      }
    },
    
    async loadSignatureRequests() {
      try {
        const response = await api.getSignatureRequests()
        const signatureRequests = response.data.results || response.data || []
        
        // Group signature requests by document
        const requestsByDocument = {}
        signatureRequests.forEach(request => {
          if (!requestsByDocument[request.document]) {
            requestsByDocument[request.document] = []
          }
          requestsByDocument[request.document].push(request)
        })
        
        // Add signature requests to reports
        this.reports = this.reports.map(report => ({
          ...report,
          signature_requests: requestsByDocument[report.id] || []
        }))
      } catch (error) {
        console.warn('Could not load signature requests:', error)
      }
    },
    
    loadSampleReports() {
      // Realistic Sample Data for Demonstration
      this.reports = [
        {
          id: 'report-2026-001',
          title: 'Agus Fleet Daily Status Report',
          document_type: 'Daily Status',
          status: 'COMPLETED',
          created_at: new Date(Date.now() - 86400000 * 1).toISOString(),
          plant_code: 'AGUS_FLEET',
          description: 'Comprehensive daily generation status and availability for the entire Agus Hydroelectric complex.',
          file_path: '/reports/agus-fleet-daily-2026.xlsx',
          signature_requests: [
            {
              id: 101,
              signer_name: 'EL ADIONG',
              signer_role: 'Prepared by',
              signer_email: 'eladiong@npc.gov.ph',
              status: 'SIGNED',
              signed_at: new Date(Date.now() - 86400000 * 1 + 3600000).toISOString(),
              digitalSignature: { signature_type: 'UPLOADED', signing_timestamp: new Date(Date.now() - 86400000 * 1 + 3600000).toISOString() }
            },
            {
              id: 102,
              signer_name: 'O.M. LAVA',
              signer_role: 'Noted by',
              signer_email: 'omlava@npc.gov.ph',
              status: 'SIGNED',
              signed_at: new Date(Date.now() - 86400000 * 1 + 7200000).toISOString(),
              digitalSignature: { signature_type: 'DRAWN', signing_timestamp: new Date(Date.now() - 86400000 * 1 + 7200000).toISOString() }
            }
          ]
        },
        {
          id: 'report-2026-002',
          title: 'Plant Status Report - Agus 6',
          document_type: 'PSR',
          status: 'PENDING_SIGNATURE',
          created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
          plant_code: 'AGUS_6',
          description: 'Detailed weekly capacity factor analysis and maintenance logs for Agus 6 Units 1-5.',
          file_path: '/reports/psr-agus6-wk12.xlsx',
          signature_requests: [
            {
              id: 201,
              signer_name: 'JMM MATA',
              signer_role: 'Prepared by',
              signer_email: 'jmmmata@npc.gov.ph',
              status: 'SIGNED',
              signed_at: new Date(Date.now() - 86400000 * 1.5).toISOString(),
              digitalSignature: { signature_type: 'TYPED', signing_timestamp: new Date(Date.now() - 86400000 * 1.5).toISOString() }
            },
            {
              id: 202,
              signer_name: 'EL ADIONG',
              signer_role: 'Approved by',
              signer_email: 'eladiong@npc.gov.ph',
              status: 'PENDING',
              signed_at: null
            }
          ]
        },
        {
          id: 'report-2026-003',
          title: 'Monthly Efficiency Summary',
          document_type: 'Monthly',
          status: 'DRAFT',
          created_at: new Date().toISOString(),
          plant_code: 'ALL_PLANTS',
          description: 'Aggregated monthly efficiency metrics, identifying top performers and deviation anomalies.',
          file_path: '/reports/monthly-efficiency-mar.pdf',
          signature_requests: []
        }
      ]
    },
    calculateStats() {
      this.stats.totalReports = this.reports.length
      this.stats.signedReports = this.reports.filter(r => r.status === 'SIGNED').length
      this.stats.pendingSignatures = this.reports.filter(r => r.status === 'PENDING_SIGNATURE').length
      
      // Reports created this month
      const thisMonth = new Date()
      thisMonth.setDate(1)
      this.stats.recentReports = this.reports.filter(r => 
        new Date(r.created_at) >= thisMonth
      ).length
    },
    
    async refreshReports() {
      await this.loadReports()
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.typeFilter = ''
      this.statusFilter = ''
      this.plantFilter = ''
    },
    
    toggleReportMenu(reportId, event) {
      if (event) {
        event.stopPropagation()
      }
      this.activeMenu = this.activeMenu === reportId ? null : reportId
    },
    
    // Report actions
    async downloadReport(report) {
      if (report.file_path) {
        // Create download link
        const link = document.createElement('a')
        link.href = `http://localhost:8000${report.file_path}`
        link.download = `${report.title}.xlsx`
        link.click()
      }
    },
    
    async viewSignatures(report) {
      try {
        // Get signature requests for this report
        const response = await api.getSignatureRequests()
        
        let allSignatures = []
        if (response.data) {
          if (Array.isArray(response.data)) {
            allSignatures = response.data
          } else if (response.data.results && Array.isArray(response.data.results)) {
            allSignatures = response.data.results
          }
        }
        
        // Filter signatures for this report
        const signatures = allSignatures.filter(sig => sig.document === report.id)
        
        // Get digital signatures
        let digitalSignatures = []
        try {
          const digitalSigResponse = await api.getDigitalSignatures()
          if (digitalSigResponse.data) {
            if (Array.isArray(digitalSigResponse.data)) {
              digitalSignatures = digitalSigResponse.data
            } else if (digitalSigResponse.data.results && Array.isArray(digitalSigResponse.data.results)) {
              digitalSignatures = digitalSigResponse.data.results
            }
          }
        } catch (error) {
          console.warn('Could not fetch digital signatures:', error)
        }
        
        // Merge signature requests with their digital signatures
        const signaturesWithImages = signatures.map(sig => {
          const digitalSig = digitalSignatures.find(ds => ds.signature_request === sig.id)
          return {
            ...sig,
            digitalSignature: digitalSig || null
          }
        })
        
        // Sort signatures by signed_at date (newest first)
        signaturesWithImages.sort((a, b) => {
          const dateA = a.signed_at ? new Date(a.signed_at) : new Date(0)
          const dateB = b.signed_at ? new Date(b.signed_at) : new Date(0)
          return dateB - dateA
        })
        
        // Show signatures in modal
        this.selectedReportSignatures = signaturesWithImages
        this.selectedReportForViewing = report
        this.showSignaturesViewerModal = true
      } catch (error) {
        console.error('Error loading signatures:', error)
        alert('Could not load signatures. Please try again.')
      }
    },
    async requestSignatures(report) {
      // Navigate to Request Signature Access page
      this.$router.push('/signatory-authorization')
    },
    
    viewDetails(report) {
      // Show detailed report information
      alert(`Report Details:\n\nTitle: ${report.title}\nType: ${report.document_type}\nStatus: ${report.status}\nCreated: ${this.formatDate(report.created_at)}`)
    },
    
    duplicateReport(report) {
      // Duplicate report functionality
      alert(`Duplicate report: ${report.title}`)
    },
    
    archiveReport(report) {
      // Archive report functionality
      alert(`Archive report: ${report.title}`)
    },
    
    confirmDeleteReport(report) {
      if (confirm(`Are you sure you want to delete "${report.title}"?`)) {
        this.deleteReport(report)
      }
    },
    
    async deleteReport(report) {
      try {
        await api.deleteDocument(report.id)
        this.reports = this.reports.filter(r => r.id !== report.id)
        this.calculateStats()
      } catch (error) {
        console.error('Error deleting report:', error)
        alert('Could not delete report. Please try again.')
      }
    },
    
    // Status and formatting helpers
    getStatusClass(status) {
      const statusMap = {
        'DRAFT': 'draft',
        'PENDING_SIGNATURE': 'pending',
        'SIGNED': 'signed',
        'COMPLETED': 'completed'
      }
      return statusMap[status] || 'draft'
    },
    
    getStatusIcon(status) {
      const iconMap = {
        'DRAFT': 'pi-file-edit',
        'PENDING_SIGNATURE': 'pi-clock',
        'SIGNED': 'pi-check-circle',
        'COMPLETED': 'pi-verified'
      }
      return iconMap[status] || 'pi-file'
    },
    
    getStatusLabel(status) {
      const labelMap = {
        'DRAFT': 'Draft',
        'PENDING_SIGNATURE': 'Pending Signature',
        'SIGNED': 'Signed & Complete',
        'COMPLETED': 'Completed'
      }
      return labelMap[status] || status
    },
    
    getSignatureStatusIcon(status) {
      const iconMap = {
        'PENDING': 'pi-clock',
        'SIGNED': 'pi-check',
        'EXPIRED': 'pi-times-circle'
      }
      return iconMap[status] || 'pi-question'
    },
    // Signature display helpers
    getSignatureImageUrl(digitalSignature) {
      if (digitalSignature && digitalSignature.signature_image) {
        if (digitalSignature.signature_image.startsWith('http')) {
          return digitalSignature.signature_image
        }
        return `http://localhost:8000/media/${digitalSignature.signature_image}`
      }
      return null
    },
    
    getSignatureTypeLabel(signatureType) {
      const typeLabels = {
        'DRAWN': 'Hand Drawn',
        'UPLOADED': 'Uploaded Image',
        'TYPED': 'Typed Text'
      }
      return typeLabels[signatureType] || signatureType
    },
    
    handleSignatureImageError(event) {
      console.warn('Failed to load signature image:', event.target.src)
      event.target.style.display = 'none'
      const container = event.target.closest('.signature-image-container')
      if (container && !container.querySelector('.image-error')) {
        const errorMsg = document.createElement('div')
        errorMsg.className = 'image-error'
        errorMsg.innerHTML = '<i class="pi pi-exclamation-triangle"></i> Signature image not available'
        container.appendChild(errorMsg)
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>
<style scoped>
/* ===== REPORT STORAGE DESIGN ===== */

.report-storage {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: #f8fafc;
  min-height: 100vh;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-content h1 {
  color: #0f172a;
  margin-bottom: 0.5rem;
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.025em;
}

.header-content p {
  color: #64748b;
  margin: 0;
  font-size: 1.1rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}

/* Stats Section */
.stats-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff !important;
  font-size: 2rem;
  transition: transform 0.3s ease;
  z-index: 2;
  box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.4);
}

.stat-card:hover .stat-icon {
  transform: scale(1.05) rotate(5deg);
}

.stat-icon i {
  color: inherit !important;
  opacity: 1 !important;
  display: inline-block !important;
  visibility: visible !important;
  font-size: 2rem !important;
}

.stat-icon.signed {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 6px 12px -2px rgba(16, 185, 129, 0.4);
}

.stat-icon.pending {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 6px 12px -2px rgba(245, 158, 11, 0.4);
}

.stat-icon.recent {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  box-shadow: 0 6px 12px -2px rgba(139, 92, 246, 0.4);
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 0.25rem 0;
  line-height: 1;
}

.stat-content p {
  color: #64748b;
  margin: 0;
  font-size: 0.95rem;
  font-weight: 500;
}

/* Filters Section */
.filters-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.search-bar {
  position: relative;
  margin-bottom: 1.25rem;
}

.search-bar i {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 1.1rem;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: white;
  color: #334155;
  min-width: 180px;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.2em;
  transition: all 0.2s ease;
}

.filter-select:hover {
  border-color: #cbd5e1;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Reports Grid */
.reports-section {
  background: transparent;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}

.loading-state i, .empty-state i {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: #94a3b8;
}

.empty-state h3 {
  color: #0f172a;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.reports-grid {
  display: grid;
  gap: 1.5rem;
}

.report-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: visible; /* Ensure dropdown can overflow */
  display: flex;
  flex-direction: column;
}

/* Updated before pseudo-element to use absolute positioning but not require overflow: hidden */
.report-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 6px;
  height: 100%;
  background: #cbd5e1;
  transition: background 0.3s ease;
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.report-card:hover::before {
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.report-info h3 {
  color: #0f172a;
  margin: 0 0 0.75rem 0;
  font-size: 1.35rem;
  font-weight: 700;
  line-height: 1.4;
}

.report-meta {
  display: flex;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.report-meta span {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.9rem;
  color: #64748b;
  background: #f8fafc;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.report-meta i {
  color: #94a3b8;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 1rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.status-badge.draft {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
}

.status-badge.pending {
  background: #fffbeb;
  color: #d97706;
  border: 1px solid #fde68a;
}

.status-badge.signed {
  background: #f0fdf4;
  color: #059669;
  border: 1px solid #bbf7d0;
}

/* Signature Status */
.signature-status {
  margin: 1.25rem 0;
  padding: 1.25rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.signatures-info h4 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #334155;
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.signatures-info h4::before {
  content: '\e910';
  font-family: 'primeicons';
  color: #94a3b8;
}

.signatures-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.signature-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.signer-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.signer-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: #1e293b;
}

.signer-role {
  font-size: 0.8rem;
  color: #64748b;
}

.signature-status-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.signature-status-badge.pending {
  background: #fef3c7;
  color: #d97706;
}

.signature-status-badge.signed {
  background: #d1fae5;
  color: #059669;
}

.no-signatures {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.95rem;
  padding: 0.5rem 0;
}

/* Report Actions */
.report-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid #e2e8f0;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: white;
  color: #475569;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #94a3b8;
  transform: translateY(-1px);
}

.btn-action.primary {
  background: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}

.btn-action.primary:hover {
  background: #dbeafe;
  border-color: #93c5fd;
}

.btn-action.secondary {
  background: white;
}

.action-menu {
  position: relative;
  /* Removed margin-left: auto so it sits right next to the badge */
}

.menu-trigger {
  padding: 0.625rem;
  border: 1px solid transparent;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.menu-trigger:hover, .menu-trigger.active {
  background: #f1f5f9;
  color: #0f172a;
  border-color: #e2e8f0;
}

.menu-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  z-index: 50; /* Increased z-index */
  min-width: 160px;
  padding: 0.5rem;
}

.report-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: visible; /* Ensure dropdown can overflow */
  display: flex;
  flex-direction: column;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.625rem 1rem;
  border: none;
  border-radius: 6px;
  background: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: #475569;
  transition: all 0.2s;
}

.menu-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.menu-item.danger {
  color: #ef4444;
}

.menu-item.danger:hover {
  background: #fef2f2;
  color: #dc2626;
}

.menu-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 0.5rem 0;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-content.large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 1.25rem;
  font-weight: 700;
}

.btn-close {
  padding: 0.5rem;
  border: none;
  background: white;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
}

.signature-image-container {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  background: #f8fafc;
  text-align: center;
  margin-top: 1rem;
}

.signature-image {
  max-width: 100%;
  max-height: 150px;
  object-fit: contain;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  background: white;
  padding: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.signature-metadata {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.signature-pending {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

.pending-signature-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
}

.pending-signature-placeholder i {
  font-size: 2rem;
  color: #94a3b8;
}

.pending-signature-placeholder span {
  font-weight: 500;
  color: #475569;
}

/* Responsive */
@media (max-width: 768px) {
  .report-storage {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .btn-primary {
    width: 100%;
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .report-header {
    flex-direction: column;
    gap: 1.25rem;
  }
  
  .report-meta {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .report-actions {
    flex-wrap: wrap;
  }
  
  .btn-action {
    flex: 1;
    justify-content: center;
  }
  
  .action-menu {
    width: 100%;
  }
  
  .menu-trigger {
    width: 100%;
  }
  
  .menu-dropdown {
    width: 100%;
    top: auto;
    bottom: 100%;
    margin-bottom: 0.5rem;
  }
}
</style>
