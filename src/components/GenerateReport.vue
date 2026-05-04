<template>
  <AppLayout>
    <div class="generate-report-page">
    <!-- Page Header -->
    <div class="page-header" v-show="!showPreview">
      <div class="header-content">
        <div class="title-section">
          <h2 class="page-title">
            <i class="pi pi-file-excel title-icon"></i>
            Generate Excel Report
          </h2>
          <p class="page-description">
            Create and download customized generation reports for all {{ plants.length }} power plants
          </p>
        </div>
        <div class="header-info">
          <div class="info-badge success">
            <i class="pi pi-check-circle"></i>
            <span>All Plants Included</span>
          </div>
          <div class="info-badge primary">
            <i class="pi pi-file-excel"></i>
            <span>PSR Format</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Form Card -->
    <div class="main-card" v-show="!showPreview">
      <div class="card-header">
        <div class="card-title">
          <i class="pi pi-calendar-plus"></i>
          <span>Report Configuration</span>
        </div>
        <div class="card-subtitle">
          Select the date for your comprehensive plant status report
        </div>
      </div>
      
      <div class="card-body">
        <form @submit.prevent="generateReport" class="report-form">
          <!-- Date Selection -->
          <div class="form-field">
            <label class="field-label">
              <i class="pi pi-calendar"></i>
              Report Date
            </label>
            <div class="date-input-wrapper">
              <input 
                type="date" 
                v-model="reportDate" 
                class="date-input"
                required
                :class="{ 'has-value': reportDate }"
                style="color: #000000 !important; background: #ffffff !important; border: 2px solid #d1d5db !important;"
              />
              <div class="input-border"></div>
            </div>
            <div class="field-hint">
              <i class="pi pi-info-circle"></i>
              <span>Generate report for the selected date across all power plants</span>
            </div>
          </div>

          <!-- Generate Button -->
          <div class="button-section">
            <button 
              type="submit"
              :disabled="!canGenerate || generating"
              class="btn-generate btn-generate-prominent"
              :class="{ 'generating': generating }"
            >
              <div class="btn-content">
                <div class="btn-icon">
                  <i v-if="!generating" class="pi pi-file-excel"></i>
                  <i v-else class="pi pi-spin pi-spinner"></i>
                </div>
                <span class="btn-text">{{ generating ? 'Generating Report...' : 'Generate Report' }}</span>
              </div>
              <div class="btn-ripple"></div>
            </button>
            
            <!-- Preview Button (shown after successful generation) -->
            <button 
              v-if="reportGenerated && !showPreview"
              @click="previewReport"
              class="btn-preview btn-preview-prominent"
              type="button"
            >
              <div class="btn-content">
                <div class="btn-icon">
                  <i class="pi pi-eye"></i>
                </div>
                <span class="btn-text">Preview Report</span>
              </div>
              <div class="btn-ripple"></div>
            </button>
            
            <div v-if="!canGenerate" class="validation-message">
              <i class="pi pi-exclamation-triangle"></i>
              <span v-if="!reportDate">Please select a report date to continue</span>
              <span v-else-if="!selectedPlants || selectedPlants.length === 0">Loading plants... Please wait</span>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Generating Loading Overlay -->
    <div v-if="generating" class="loading-modal-overlay">
      <div class="loading-modal-content">
        <div class="gears-animation">
          <i class="pi pi-cog gear-icon gear-1"></i>
          <i class="pi pi-cog gear-icon gear-2"></i>
        </div>
        <h3 class="loading-title">Generating Report</h3>
        <p class="loading-text">Please wait while we gather and process the data...</p>
        <div class="progress-bar-container">
          <div class="progress-bar-animated"></div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="success-modal-overlay" @click="closeSuccessModal">
      <div class="success-modal" @click.stop>
        <div class="success-modal-header">
          <div class="success-icon">
            <i class="pi pi-check-circle"></i>
          </div>
          <h3 class="success-title">Report Generated Successfully!</h3>
        </div>
        <div class="success-modal-body">
          <p class="success-message">
            Your Plant Status Report for <strong>{{ reportPreview?.header?.date_text }}</strong> has been generated successfully.
          </p>
          <div class="success-actions">
            <button @click="previewReport" class="btn-success-preview">
              <i class="pi pi-eye"></i>
              <span>Preview Report</span>
            </button>
            <button @click="closeSuccessModal" class="btn-success-close">
              <i class="pi pi-times"></i>
              <span>Close</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Report Preview Section -->
    <div v-if="showPreview && reportPreview" class="preview-card modern-preview">
      <div class="preview-header">
        <div class="preview-title-section">
          <div class="preview-icon">
            <i class="pi pi-file-excel"></i>
          </div>
          <div class="preview-title-content">
            <h3 class="preview-title">Excel Report Preview</h3>
            <p class="preview-subtitle">Plant Status Report - {{ reportPreview.header.date_text }}</p>
          </div>
        </div>
        
        <div class="preview-actions">
          <div class="action-group">
            <button @click="zoomOut" class="btn-zoom" :disabled="zoomLevel <= 0.5" title="Zoom Out">
              <i class="pi pi-search-minus"></i>
            </button>
            <span class="zoom-indicator">{{ Math.round(zoomLevel * 100) }}%</span>
            <button @click="zoomIn" class="btn-zoom" :disabled="zoomLevel >= 2" title="Zoom In">
              <i class="pi pi-search-plus"></i>
            </button>
          </div>
          
          <div class="action-group">
            <button @click="toggleFullscreen" class="btn-action secondary" title="Toggle Fullscreen">
              <i :class="isFullscreen ? 'pi pi-window-minimize' : 'pi pi-window-maximize'"></i>
            </button>
            <button @click="downloadExcel" class="btn-action primary" title="Download Excel">
              <i class="pi pi-download"></i>
              <span>Download Excel</span>
            </button>
            <button 
              @click="saveToReportStorage" 
              class="btn-action success" 
              title="Save to Report Storage"
              :disabled="saving"
            >
              <i v-if="!saving" class="pi pi-save"></i>
              <i v-else class="pi pi-spin pi-spinner"></i>
              <span>{{ saving ? 'Saving...' : 'Save to Storage' }}</span>
            </button>
            <button @click="closePreview" class="btn-action close" title="Close Preview">
              <i class="pi pi-times"></i>
            </button>
          </div>
        </div>
      </div>
      
      <div class="preview-body" :class="{ 'fullscreen': isFullscreen }">
        <div class="preview-toolbar">
          <div class="toolbar-left">
            <div class="page-info">
              <span class="page-indicator">Page 1 of 1</span>
            </div>
          </div>
          
          <div class="toolbar-center">
            <div class="view-options">
              <button 
                @click="viewMode = 'normal'" 
                :class="['view-btn', { active: viewMode === 'normal' }]"
                title="Normal View"
              >
                <i class="pi pi-eye"></i>
                <span>Normal</span>
              </button>
              <button 
                @click="viewMode = 'print'" 
                :class="['view-btn', { active: viewMode === 'print' }]"
                title="Print Layout"
              >
                <i class="pi pi-print"></i>
                <span>Print Layout</span>
              </button>
            </div>
          </div>
          
          <div class="toolbar-right">
            <div class="export-options">
              <button @click="exportToPDF" class="btn-export" title="Export to PDF">
                <i class="pi pi-file-pdf"></i>
                <span>PDF</span>
              </button>
            </div>
          </div>
        </div>

        <!-- User-Friendly Horizontal Scrollbar with Navigation -->
        <div v-if="showPreview" class="user-friendly-scrollbar" ref="stickyScrollContainer" style="display: none;">
          <div class="scrollbar-wrapper">
            <!-- Left Arrow Button -->
            <button 
              class="scroll-arrow scroll-left" 
              @click="scrollLeft"
              :disabled="scrollPosition <= 0"
              title="Scroll Left"
            >
              <i class="pi pi-chevron-left"></i>
            </button>
            
            <!-- Scrollbar Track with Progress Indicator -->
            <div class="scrollbar-track-container">
              <div class="scrollbar-track" ref="stickyScrollTrack">
                <div class="scrollbar-progress" :style="{ width: scrollProgress + '%' }"></div>
                <div class="scrollbar-thumb" ref="stickyScrollThumb">
                  <div class="thumb-grip"></div>
                </div>
              </div>
              
              <!-- Position Indicator -->
              <div class="position-indicator">
                <span class="current-position">{{ Math.round(scrollProgress) }}%</span>
                <span class="position-text">of document width</span>
              </div>
            </div>
            
            <!-- Right Arrow Button -->
            <button 
              class="scroll-arrow scroll-right" 
              @click="scrollRight"
              :disabled="scrollPosition >= maxScrollPosition"
              title="Scroll Right"
            >
              <i class="pi pi-chevron-right"></i>
            </button>
            
            <!-- Quick Navigation Buttons -->
            <div class="quick-nav">
              <button 
                class="quick-nav-btn" 
                @click="scrollToStart"
                title="Go to Start"
              >
                <i class="pi pi-step-backward"></i>
              </button>
              <button 
                class="quick-nav-btn" 
                @click="scrollToEnd"
                title="Go to End"
              >
                <i class="pi pi-step-forward"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="preview-content-container" 
             :style="{ transform: `scale(${zoomLevel})` }"
             @scroll="handleHorizontalScroll"
             ref="previewContainer">
          <div class="excel-document" :class="{ 'print-mode': viewMode === 'print' }">
            <div class="document-shadow"></div>
            
            <div class="preview-content-wrapper">
              <!-- Main Content (Left Side) -->
              <div class="main-content-left">
                <!-- Excel-like Header with Logo and Officials -->
            <div class="excel-header-with-logo">
              <!-- Logo and Title Row -->
              <div class="logo-title-row">
                <div class="logo-container">
                  <img src="@/assets/NPC-logo.png" alt="NPC Logo" class="npc-logo" />
                </div>
                <div class="title-container">
                  <h1 class="main-title">MINDANAO GENERATION</h1>
                  <h2 class="subtitle-title">(PSALM PORTFOLIO)</h2>
                </div>
              </div>
          
          <!-- Officials Row -->
          <div class="officials-row">
            <div class="official-box">
              <div class="official-label">FOR</div>
              <div class="official-name">MR. LARRY I. SABELLIRA</div>
              <div class="official-position">VP, Mindanao Generation</div>
            </div>
            <div class="official-box">
              <div class="official-name">MR. DENNIS EDWARD A. DELA SERNA</div>
              <div class="official-position">President and CEO, PSALM</div>
            </div>
            <div class="official-box">
              <div class="official-name">MR. ARNOLD C. FRANCISCO</div>
              <div class="official-position">VP - PAIMG, PSALM</div>
            </div>
          </div>
          
          <!-- Plant Status Report Banner -->
          <div class="psr-banner">
            <div class="psr-title">PLANT STATUS REPORT</div>
            <div class="psr-date">{{ reportPreview.header.date_text }}</div>
          </div>
        </div>

        <!-- Excel-like Table -->
        <div class="excel-table-container">
          <table class="excel-table">
            <thead>
              <tr class="excel-header-row">
                <th class="excel-th plant-col">PLANT NAME</th>
                <th class="excel-th capacity-col">Rated Capacity<br>(MW)</th>
                <th class="excel-th nominated-col">Available<br>Capacity (MW)</th>
                <th class="excel-th actual-col">Lake Lanao<br>Projected<br>Ave. Outflow</th>
                <th class="excel-th variance-col">Load at<br>0800H</th>
                <th class="excel-th remarks-col">REMARKS</th>
              </tr>
            </thead>
            <tbody>
              <!-- Dynamic Plant Rows -->
              <template v-for="(plant, index) in reportPreview.plants_data" :key="plant.code">
                <!-- If this is the first non-AGUS plant (like Pulangi IV), insert TOTAL AGUS before it. -->
                <tr v-if="plant.code === 'PULANGI4' && reportPreview.plants_data.some(p => p.code.startsWith('AGUS'))" class="total-agus-row">
                  <td class="excel-td total-label-cell">TOTAL AGUS</td>
                  <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.capacity) }}</td>
                  <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.nominated) }}</td>
                  <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.actual) }} MW</td>
                  <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.variance) }}</td>
                  <td class="excel-td total-number-cell"></td>
                </tr>

                <tr class="plant-name-row">
                  <td class="excel-td plant-name-italic">{{ plant.name }}</td>
                  <td class="excel-td number-cell">{{ formatNumber(plant.plant_totals.capacity) }}</td>
                  <td class="excel-td number-cell">{{ formatNumber(plant.plant_totals.nominated) }}</td>
                  <td class="excel-td number-cell" :rowspan="plant.units.length + 1">
                    <span v-if="plant.code === 'AGUS1'">136 CMS @<br>60 HW</span>
                    <span v-else>{{ formatNumber(plant.plant_totals.actual) }} MW</span>
                  </td>
                  <td class="excel-td number-cell">{{ formatNumber(plant.plant_totals.variance) }}</td>
                  <td class="excel-td remarks-cell">{{ getPlantLevelRemarks(plant.code) }}</td>
                </tr>
                <tr v-for="unit in plant.units" :key="`${plant.code}-${unit.number}`" class="unit-row">
                  <td class="excel-td unit-label">{{ unit.label }}</td>
                  <td class="excel-td number-cell">{{ formatNumber(unit.capacity) }}</td>
                  <td class="excel-td number-cell">{{ formatNumber(unit.nominated) }}</td>
                  <td class="excel-td number-cell" :class="{'red-text': unit.variance === 0}">{{ formatNumber(unit.variance) }}</td>
                  <td class="excel-td remarks-cell">{{ unit.remarks }}</td>
                </tr>
              </template>

              <!-- TOTAL AGUS (If no Pulangi IV is present, but Agus plants exist) -->
              <tr v-if="!reportPreview.plants_data.some(p => p.code === 'PULANGI4') && reportPreview.plants_data.some(p => p.code.startsWith('AGUS'))" class="total-agus-row">
                <td class="excel-td total-label-cell">TOTAL AGUS</td>
                <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.capacity) }}</td>
                <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.nominated) }}</td>
                <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.actual) }} MW</td>
                <td class="excel-td total-number-cell">{{ formatNumber(agusTotals.variance) }}</td>
                <td class="excel-td total-number-cell"></td>
              </tr>

              <!-- TOTAL HYDRO -->
              <tr class="grand-total-row">
                <td class="excel-td grand-total-label">TOTAL HYDRO</td>
                <td class="excel-td grand-total-number">{{ formatNumber(reportPreview.totals.total_capacity) }}</td>
                <td class="excel-td grand-total-number">{{ formatNumber(reportPreview.totals.total_nominated) }}</td>
                <td class="excel-td grand-total-number">{{ formatNumber(reportPreview.totals.total_actual) }} MW</td>
                <td class="excel-td grand-total-number">{{ formatNumber(reportPreview.totals.total_variance) }}</td>
                <td class="excel-td grand-total-number"></td>
              </tr>

              <!-- Forecasted Load Row (Yellow Background) -->
              <tr class="forecasted-load-row" v-if="reportPreview.forecasted_load">
                <td colspan="6" class="excel-td forecasted-load-cell">
                  Agus-Pulangi Forecasted Load @ 6pm, {{ reportPreview.forecasted_load.date }}: Agus = {{ formatNumber(reportPreview.forecasted_load.agus_load) }} MW & Pulangui IV = {{ formatNumber(reportPreview.forecasted_load.pulangi_load) }} MW, Total Load: {{ formatNumber(reportPreview.forecasted_load.total_load) }} MW
                </td>
              </tr>

              <!-- IPP Rows (Hidden as no real data available yet) -->
              <!-- TOTAL IPP -->
              <!-- TOTAL NPC-PSALM -->
            </tbody>
          </table>
        </div>

        <!-- Charts Section (Removed mockups) -->

        <!-- Notes Section -->
        <div class="excel-section notes-section">
          <div class="notes-header">Note:</div>
          <ol class="notes-list">
            <li v-for="(note, index) in reportPreview.notes" :key="index">{{ note }}</li>
          </ol>
        </div>

        <!-- Signature Sections -->
        <div class="excel-section signatures-section">
          <h4 class="section-title">AUTHORIZATION</h4>
          
          <!-- First Row of Signatures -->
          <div class="signature-row">
            <table class="signature-table">
              <thead>
                <tr>
                  <th v-for="sig in reportPreview.signatures.first_row" :key="sig.name" class="signature-header">
                    {{ sig.role }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <!-- Signature space -->
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`space-${sig.name}`" class="signature-cell">
                    <div v-if="signatures[sig.name]" class="signature-display">
                      <img :src="signatures[sig.name].data" :alt="`${sig.name} signature`" class="signature-image" />
                    </div>
                    <div v-else class="signature-placeholder">
                      &nbsp;
                    </div>
                  </td>
                </tr>
                <!-- Names -->
                <tr class="signature-names">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`name-${sig.name}`" class="signature-name">
                    <div class="signature-name-container">
                      <span class="name-text">{{ sig.name }}</span>
                      <div class="signature-buttons-group">
                        <!-- Show e-signature button only if authorized -->
                        <button 
                          v-if="canSignAs(sig.name)"
                          @click="openESignatureModal(sig)" 
                          class="btn-e-signature"
                          :class="{ 'has-signature': signatures[sig.name] }"
                          :title="signatures[sig.name] ? 'Edit E-Signature' : 'Add E-Signature'"
                        >
                          <i :class="signatures[sig.name] ? 'pi pi-pencil' : 'pi pi-plus'"></i>
                          <span>{{ signatures[sig.name] ? 'edit' : 'e-signature' }}</span>
                        </button>
                        <!-- Show request button if not authorized -->
                        <button 
                          v-if="!canSignAs(sig.name)"
                          @click="goToRequestSignatureAccess(sig)" 
                          class="btn-request-access-mini"
                          title="Request signature access"
                        >
                          <i class="pi pi-key"></i>
                          <span>request access</span>
                        </button>
                      </div>
                    </div>
                  </td>
                </tr>
                <!-- Titles -->
                <tr class="signature-titles">
                  <td v-for="sig in reportPreview.signatures.first_row" :key="`title-${sig.name}`" class="signature-title">
                    {{ sig.title }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Second Row of Signatures -->
          <div class="signature-row">
            <table class="signature-table">
              <thead>
                <tr>
                  <th v-for="sig in reportPreview.signatures.second_row" :key="sig.name" class="signature-header">
                    {{ sig.role }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <!-- Signature space -->
                <tr class="signature-space">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`space-${sig.name}`" class="signature-cell">
                    <div v-if="signatures[sig.name]" class="signature-display">
                      <img :src="signatures[sig.name].data" :alt="`${sig.name} signature`" class="signature-image" />
                    </div>
                    <div v-else class="signature-placeholder">
                      &nbsp;
                    </div>
                  </td>
                </tr>
                <!-- Names -->
                <tr class="signature-names">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`name-${sig.name}`" class="signature-name">
                    <div class="signature-name-container">
                      <span class="name-text">{{ sig.name }}</span>
                      <div class="signature-buttons-group">
                        <!-- Show e-signature button only if authorized -->
                        <button 
                          v-if="canSignAs(sig.name)"
                          @click="openESignatureModal(sig)" 
                          class="btn-e-signature"
                          :class="{ 'has-signature': signatures[sig.name] }"
                          :title="signatures[sig.name] ? 'Edit E-Signature' : 'Add E-Signature'"
                        >
                          <i :class="signatures[sig.name] ? 'pi pi-pencil' : 'pi pi-plus'"></i>
                          <span>{{ signatures[sig.name] ? 'edit' : 'e-signature' }}</span>
                        </button>
                        <!-- Show request button if not authorized -->
                        <button 
                          v-if="!canSignAs(sig.name)"
                          @click="goToRequestSignatureAccess(sig)" 
                          class="btn-request-access-mini"
                          title="Request signature access"
                        >
                          <i class="pi pi-key"></i>
                          <span>request access</span>
                        </button>
                      </div>
                    </div>
                  </td>
                </tr>
                <!-- Titles -->
                <tr class="signature-titles">
                  <td v-for="sig in reportPreview.signatures.second_row" :key="`title-${sig.name}`" class="signature-title">
                    {{ sig.title }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Additional Notes Section -->
        <div class="excel-section additional-notes-section">
          <div class="notes-header">Note:</div>
          <ol class="notes-list">
            <li v-for="(note, index) in reportPreview.additional_notes" :key="index">{{ note }}</li>
          </ol>
        </div>

        <!-- Footer Note -->
        <div class="excel-section footer-note-section">
          <p class="footer-note">{{ reportPreview.footer_note }}</p>
        </div>
        </div> <!-- Close main-content-left -->

        <!-- Middle Content and Right Side Content mockups removed to ensure only real data is displayed -->

        </div> <!-- Close preview-content-wrapper -->
            </div> <!-- Close excel-document -->
          </div> <!-- Close preview-content-container -->
        </div> <!-- Close preview-body -->
      </div> <!-- Close modern-preview -->
    </div> <!-- Close preview card -->

    <!-- Generation History -->
    <div v-if="generationHistory.length > 0" class="history-card">
      <div class="card-header">
        <div class="card-title" style="color: #000000 !important;">
          <i class="pi pi-history" style="color: #000000 !important;"></i>
          <span style="color: #000000 !important;">Recent Reports</span>
        </div>
        <div class="menu-wrapper">
          <button @click="toggleMenu" class="btn-menu" ref="menuButton">
            <i class="pi pi-ellipsis-v"></i>
          </button>
          <transition name="dropdown">
            <div v-if="showMenu" class="dropdown-menu" @click.stop>
              <button @click="clearHistory" class="menu-item menu-item-danger">
                <i class="pi pi-trash"></i>
                <span>Clear History</span>
              </button>
            </div>
          </transition>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="history-list">
          <div 
            v-for="(item, index) in generationHistory" 
            :key="index"
            class="history-item"
            @click="downloadHistoryReport(item)"
          >
            <div class="history-icon">
              <i class="pi pi-file-excel"></i>
            </div>
            <div class="history-details">
              <div class="history-main">
                <span class="history-filename" style="color: #000000 !important;">{{ item.filename }}</span>
                <span class="history-plant-badge" style="color: #000000 !important;">{{ item.plantName }}</span>
              </div>
              <div class="history-meta">
                <span class="history-type" style="color: #000000 !important;">
                  <i class="pi pi-tag" style="color: #000000 !important;"></i>
                  {{ item.reportTypeName }}
                </span>
                <span class="history-exact-time" style="color: #000000 !important;">
                  <i class="pi pi-clock" style="color: #000000 !important;"></i>
                  {{ formatExactTime(item.timestamp) }}
                </span>
              </div>
            </div>
            <div class="history-actions">
              <button 
                @click.stop="downloadHistoryReport(item)" 
                class="btn-download"
                title="Download this report"
              >
                <i class="pi pi-download"></i>
              </button>
              <button 
                @click.stop="regenerateReport(item)" 
                class="btn-regenerate"
                title="Load parameters to regenerate"
              >
                <i class="pi pi-refresh"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- E-Signature Modal -->
    <div v-if="showESignatureModal" class="modal-overlay" @click="closeESignatureModal">
      <div class="modal-content e-signature-modal" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            <i class="pi pi-pencil"></i>
            E-Signature for {{ selectedSignatory?.name }}
          </h3>
          <button @click="closeESignatureModal" class="btn-close-modal">
            <i class="pi pi-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="signature-options">
            <div class="option-tabs">
              <button 
                @click="signatureMode = 'draw'" 
                :class="['tab-btn', { active: signatureMode === 'draw' }]"
              >
                <i class="pi pi-pencil"></i>
                <span>Draw Signature</span>
              </button>
              <button 
                @click="signatureMode = 'upload'" 
                :class="['tab-btn', { active: signatureMode === 'upload' }]"
              >
                <i class="pi pi-upload"></i>
                <span>Upload Image</span>
              </button>
              <button 
                @click="signatureMode = 'type'" 
                :class="['tab-btn', { active: signatureMode === 'type' }]"
              >
                <i class="pi pi-font"></i>
                <span>Type Signature</span>
              </button>
            </div>

            <!-- Draw Signature -->
            <div v-if="signatureMode === 'draw'" class="signature-draw-area">
              <div class="canvas-container">
                <canvas 
                  ref="signatureCanvas" 
                  width="400" 
                  height="200"
                  class="signature-canvas"
                  @mousedown="startDrawing"
                  @mousemove="draw"
                  @mouseup="stopDrawing"
                  @mouseleave="stopDrawing"
                  @touchstart="startDrawing"
                  @touchmove="draw"
                  @touchend="stopDrawing"
                ></canvas>
              </div>
              <div class="canvas-controls">
                <button @click="clearCanvas" class="btn-clear">
                  <i class="pi pi-trash"></i>
                  Clear
                </button>
              </div>
            </div>

            <!-- Upload Image -->
            <div v-if="signatureMode === 'upload'" class="signature-upload-area">
              <!-- My Saved Signatures (for logged-in users) -->
              <div v-if="savedSignatures.length > 0" class="saved-signatures-section">
                <h4 class="section-subtitle">My Saved Signatures</h4>
                <div class="saved-signatures-grid">
                  <div 
                    v-for="(signature, index) in savedSignatures" 
                    :key="index"
                    class="saved-signature-item"
                    @click="selectSavedSignature(signature)"
                    :class="{ selected: selectedSavedSignature === signature }"
                  >
                    <img :src="signature.data" :alt="`Signature ${index + 1}`" />
                    <div class="signature-actions">
                      <button @click.stop="deleteSavedSignature(index)" class="btn-delete-signature" title="Delete">
                        <i class="pi pi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Upload New Signature -->
              <div class="upload-new-section">
                <h4 class="section-subtitle">Upload New Signature</h4>
                <div class="upload-zone" @click="$refs.fileInput.click()">
                  <i class="pi pi-cloud-upload"></i>
                  <p>Click to upload signature image</p>
                  <small>PNG, JPG, or GIF (max 2MB)</small>
                </div>
                <input 
                  ref="fileInput" 
                  type="file" 
                  accept="image/*" 
                  @change="handleFileUpload" 
                  style="display: none"
                />
                <div v-if="uploadedSignature" class="uploaded-preview">
                  <img :src="uploadedSignature" alt="Uploaded signature" />
                  <div class="upload-actions">
                    <button @click="saveSignatureToLibrary" class="btn-save-to-library">
                      <i class="pi pi-bookmark"></i>
                      Save to My Signatures
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Type Signature -->
            <div v-if="signatureMode === 'type'" class="signature-type-area">
              <div class="font-selector">
                <label>Choose Font Style:</label>
                <select v-model="selectedFont" class="font-select">
                  <option value="cursive">Cursive</option>
                  <option value="serif">Serif</option>
                  <option value="sans-serif">Sans Serif</option>
                  <option value="monospace">Monospace</option>
                </select>
              </div>
              <div class="signature-input">
                <input 
                  v-model="typedSignature" 
                  type="text" 
                  placeholder="Type your signature here"
                  class="signature-text-input"
                  :style="{ fontFamily: selectedFont, fontSize: '24px' }"
                />
              </div>
              <div class="signature-preview" :style="{ fontFamily: selectedFont }">
                {{ typedSignature || 'Preview will appear here' }}
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeESignatureModal" class="btn-cancel">
            Cancel
          </button>
          <button @click="saveSignature" class="btn-save" :disabled="!hasSignature">
            <i class="pi pi-check"></i>
            Save Signature
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import AppLayout from './AppLayout.vue';
import toast from '../utils/toast';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, LineElement, PointElement } from 'chart.js';
import { Pie, Bar } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, LineElement, PointElement);

export default {
  name: 'GenerateReport',
  components: {
    AppLayout,
    Pie,
    Bar,
  },
  data() {
    return {
      plants: [],
      selectedPlants: [],
      reportDate: '',
      reportType: 'psr',
      generating: false,
      saving: false,
      reportGenerated: false,
      showSuccessModal: false,
      generationHistory: [],
      showMenu: false,
      reportPreview: null,
      showPreview: false,
      // E-signature modal data
      showESignatureModal: false,
      selectedSignatory: null,
      signatureMode: 'draw',
      isDrawing: false,
      hasDrawnOnCanvas: false, // Track if user has drawn anything
      uploadedSignature: null,
      savedSignatures: [], // User's saved signature library
      selectedSavedSignature: null,
      typedSignature: '',
      selectedFont: 'cursive',
      signatures: {}, // Store signatures by signatory name
      
      // Security: User authorizations and current user
      userAuthorizations: [],
      currentUser: null,
      
      // Preview enhancements
      zoomLevel: 1,
      isFullscreen: false,
      viewMode: 'normal', // 'normal' or 'print'
      
      // User-friendly scrollbar data
      scrollPosition: 0,
      maxScrollPosition: 0,
      scrollProgress: 0,
      
      reportTypes: [
        {
          value: 'psr',
          label: 'Plant Status Report (PSR)',
          description: 'Official PSR format for Mindanao plants',
          icon: 'pi pi-file-excel'
        }
      ],
      // Chart data
      capacityMixData: {
        labels: ['Hydro', 'Coal Fired Thermal'],
        datasets: [{
          data: [811.31, 210.00],
          backgroundColor: ['#4472C4', '#ED7D31'],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      pieChartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.parsed || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(0);
                return `${label}: ${value.toFixed(2)} (${percentage}%)`;
              }
            }
          }
        }
      },
      loadShareData: {
        labels: ['AGUS 1', 'AGUS 2', 'AGUS 4', 'AGUS 5', 'AGUS 6', 'AGUS 7', 'PULANGI IV'],
        datasets: [{
          label: 'Load (MW)',
          data: [60.0, 120.0, 96.0, 40.0, 144.8, 40.0, 150.0],
          backgroundColor: ['#4472C4', '#A5A5A5', '#FF0000', '#ED7D31', '#FFC000', '#7030A0', '#00B050'],
          borderWidth: 1,
          borderColor: '#000'
        }]
      },
      gateChartData: {
        labels: ['AGUS 1', 'AGUS 2', 'AGUS 4', 'AGUS 5', 'AGUS 6', 'AGUS 7', 'PULANGI IV', 'AGUS 1', 'AGUS 2', 'MARCH', 'MARCH'],
        datasets: [
          {
            label: 'Actual',
            type: 'bar',
            data: [60.0, 165.0, 165.0, 60.0, 200.0, 60.0, 200.0, 165.0, 165.0, null, null],
            backgroundColor: '#5B9BD5',
            borderWidth: 0
          },
          {
            label: 'Dependable Cap.',
            type: 'bar',
            data: [80.0, 180.0, 180.0, 80.0, 180.0, 80.0, 200.0, 180.0, 180.0, null, null],
            backgroundColor: '#ED7D31',
            borderWidth: 0
          },
          {
            label: 'Yesterday\'s Peak',
            type: 'scatter',
            data: [null, null, null, null, null, null, 350, null, null, null, 270],
            backgroundColor: '#ED7D31',
            borderColor: '#ED7D31',
            pointRadius: 4,
            pointStyle: 'rect'
          },
          {
            label: 'GRID Load',
            type: 'line',
            data: [null, null, null, null, null, null, null, null, null, 180, 120],
            borderColor: '#A5A5A5',
            backgroundColor: 'transparent',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.4,
            fill: false
          }
        ]
      },
      gateChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        resizeDelay: 0,
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 10,
            bottom: 10
          }
        },
        interaction: {
          mode: 'index',
          intersect: false
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
              usePointStyle: true,
              padding: 15,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                if (context.dataset.type === 'line') {
                  return `GRID Load: ${context.parsed.y} MW`;
                } else if (context.dataset.type === 'scatter') {
                  return `Yesterday's Peak: ${context.parsed.y} MW`;
                }
                return `${context.dataset.label}: ${context.parsed.y} MW`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 400,
            ticks: {
              stepSize: 50,
              font: {
                size: 10
              }
            },
            title: {
              display: true,
              text: 'MW',
              font: {
                size: 11
              }
            },
            grid: {
              color: '#E0E0E0'
            }
          },
          x: {
            ticks: {
              font: {
                size: 9
              },
              maxRotation: 45,
              minRotation: 45
            },
            grid: {
              display: false
            },
            offset: false
          }
        },
        elements: {
          bar: {
            categoryPercentage: 1.0,
            barPercentage: 0.9
          }
        }
      },
      additionalChartData: {
        labels: ['AGUS 1', 'AGUS 2', 'AGUS 4', 'AGUS 5', 'AGUS 6', 'AGUS 7', 'PULANGI IV', 'STEAG 1', 'STEAG 2', 'MAGFP1', 'MAGFP2'],
        datasets: [
          {
            label: 'Rated',
            data: [80.0, 180.0, 158.1, 55.0, 219.0, 54.0, 255.0, 116.0, 116.0, 0.0, 0.0],
            backgroundColor: '#4472C4',
            borderWidth: 1,
            borderColor: '#000'
          },
          {
            label: 'Dependable Cap.',
            data: [70.0, 165.0, 105.4, 53.0, 144.8, 48.1, 225.0, 105.0, 105.0, 0.0, 0.0],
            backgroundColor: '#ED7D31',
            borderWidth: 1,
            borderColor: '#000'
          },
          {
            label: 'GRID Load',
            data: [60.0, 120.0, 96.0, 40.0, 144.8, 40.0, 150.0, 105.0, 105.0, 0.0, 0.0],
            backgroundColor: '#A5A5A5',
            borderWidth: 1,
            borderColor: '#000'
          }
        ]
      },
      additionalChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        resizeDelay: 0,
        layout: {
          padding: {
            left: 0,
            right: 0,
            top: 10,
            bottom: 10
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              usePointStyle: true,
              padding: 15,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.parsed.y.toFixed(1)} MW`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 300,
            ticks: {
              stepSize: 50,
              font: {
                size: 10
              }
            },
            title: {
              display: true,
              text: 'MW',
              font: {
                size: 11
              }
            },
            grid: {
              color: '#E0E0E0'
            }
          },
          x: {
            ticks: {
              font: {
                size: 9
              },
              maxRotation: 45,
              minRotation: 45
            },
            grid: {
              display: true,
              color: '#E0E0E0'
            },
            offset: false
          }
        },
        elements: {
          bar: {
            categoryPercentage: 1.0,
            barPercentage: 0.9
          }
        }
      },
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.parsed.y.toFixed(1)} MW`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 160,
            ticks: {
              stepSize: 20
            },
            title: {
              display: false
            }
          },
          x: {
            ticks: {
              font: {
                size: 11
              }
            }
          }
        }
      }
    };
  },
  watch: {
    // Watch for report date changes to load signatures for that date
    reportDate: {
      handler(newDate) {
        if (newDate) {
          this.loadReportSignatures();
        }
        // Reset report state when date changes
        this.reportGenerated = false;
        this.showPreview = false;
        this.reportPreview = null;
        this.saveStateToSession();
      },
      immediate: false
    },
    
    selectedPlants: {
      handler() {
        // Reset report state when selected plants change
        this.reportGenerated = false;
        this.showPreview = false;
        this.reportPreview = null;
        this.saveStateToSession();
      },
      deep: true
    },
    
    reportGenerated() {
      this.saveStateToSession();
    },
    
    reportPreview: {
      handler() {
        this.saveStateToSession();
      },
      deep: true
    },
    
    // Watch for preview visibility to initialize sticky scrollbar
    showPreview: {
      handler(newVal) {
        this.saveStateToSession();
        if (newVal) {
          // Wait for DOM to be fully rendered
          this.$nextTick(() => {
            setTimeout(() => {
              console.log('Initializing scrollbar from watcher');
              this.initStickyScrollbar();
              
              // Additional delay to test scrollbar
              setTimeout(() => {
                console.log('Testing scrollbar after initialization');
                this.testScrollbar();
              }, 1000);
            }, 200); // Increased delay to ensure content is rendered
          });
        } else {
          // Hide scrollbar when preview is closed
          if (this.$refs.stickyScrollContainer) {
            this.$refs.stickyScrollContainer.style.display = 'none';
          }
        }
      },
      immediate: false
    }
  },
  
  computed: {
    canGenerate() {
      // Require both report date and plants to be loaded
      return this.reportDate && this.selectedPlants && this.selectedPlants.length > 0;
    },
    agusTotals() {
      if (!this.reportPreview || !this.reportPreview.plants_data) return { capacity: 0, nominated: 0, actual: 0, variance: 0 };
      const agusPlants = this.reportPreview.plants_data.filter(p => p.code.startsWith('AGUS'));
      return agusPlants.reduce((acc, plant) => {
        acc.capacity += plant.plant_totals.capacity || 0;
        acc.nominated += plant.plant_totals.nominated || 0;
        acc.actual += plant.plant_totals.actual || 0;
        acc.variance += plant.plant_totals.variance || 0;
        return acc;
      }, { capacity: 0, nominated: 0, actual: 0, variance: 0 });
    },
    ippTotals() {
      if (!this.reportPreview || !this.reportPreview.ipp_data) return { capacity: 0, nominated: 0, actual: 0, variance: 0 };
      return this.reportPreview.ipp_data.reduce((acc, ipp) => {
        acc.capacity += ipp.capacity || 0;
        acc.nominated += ipp.nominated || 0;
        acc.actual += ipp.actual || 0;
        acc.variance += ipp.variance || 0;
        return acc;
      }, { capacity: 0, nominated: 0, actual: 0, variance: 0 });
    },
    hasSignature() {
      if (this.signatureMode === 'draw') {
        return this.hasDrawnOnCanvas && this.$refs.signatureCanvas && !this.isCanvasEmpty();
      } else if (this.signatureMode === 'upload') {
        return !!this.uploadedSignature || !!this.selectedSavedSignature;
      } else if (this.signatureMode === 'type') {
        return !!this.typedSignature.trim();
      }
      return false;
    }
  },
  mounted() {
    this.restoreStateFromSession();
    this.loadPlants();
    this.loadGenerationHistory();
    this.loadCurrentUser();
    this.loadUserAuthorizations();
    
    // Only load signatures if user is authenticated
    // Wait a bit for authentication to complete
    setTimeout(() => {
      if (localStorage.getItem('access_token')) {
        this.loadSavedSignatures(); // Load user's saved signatures
        
        // Load signatures if we already have a report date
        if (this.reportDate) {
          this.loadReportSignatures();
        }
      }
    }, 500);
    
    // Initialize sticky scrollbar
    this.initStickyScrollbar();
    
    document.addEventListener('click', this.closeMenu);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeMenu);
    
    // Cleanup sticky scrollbar event listeners
    if (this._stickyScrollbarCleanup) {
      this._stickyScrollbarCleanup();
    }
  },
  methods: {
    getPlantLevelRemarks(plantCode) {
      if (!this.reportPreview || !this.reportPreview.gate_elevation_data) return '';
      
      const gateData = this.reportPreview.gate_elevation_data;
      
      if (plantCode === 'AGUS1') {
        const data = gateData.find(g => g.plant === 'Lake Lanao');
        if (data) return `Lake Lanao Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]} m, G2- ${data.gates[1]} m)`;
      } else if (plantCode === 'AGUS2') {
        const data = gateData.find(g => g.plant === 'Agus 2');
        if (data) return `Forebay Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]}m, G2- ${data.gates[1]} m)`;
      } else if (plantCode === 'AGUS4') {
        const data = gateData.find(g => g.plant === 'Agus 4');
        if (data) return `Forebay Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]}m, G2- ${data.gates[1]} m)`;
      } else if (plantCode === 'AGUS5') {
        const data = gateData.find(g => g.plant === 'Agus 5');
        if (data) return `Forebay Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]}m, G2- ${data.gates[1]} m, G3- ${data.gates[2]} m)`;
      } else if (plantCode === 'AGUS6') {
        const data = gateData.find(g => g.plant === 'Agus 6');
        if (data) return `Forebay Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]}m, G2- ${data.gates[1]} m, G3- ${data.gates[2]} m, G4- ${data.gates[3]} m)`;
      } else if (plantCode === 'AGUS7') {
        const data = gateData.find(g => g.plant === 'Agus 7');
        if (data) return `Forebay Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]}m, G2- ${data.gates[1]} m, G3- ${data.gates[2]} m)`;
      } else if (plantCode === 'PULANGI4') {
        const data = gateData.find(g => g.plant === 'Pulangi IV');
        if (data) return `Reservoir Elevation is ${data.elevation} m.a.s.l. (G1- ${data.gates[0]}m, G2- ${data.gates[1]} m, G3- ${data.gates[2]} m, G4- ${data.gates[3]} m, G5- ${data.gates[4]} m, G6- ${data.gates[5]} m).`;
      }
      return '';
    },
    // Preview interaction methods
    zoomIn() {
      if (this.zoomLevel < 2) {
        this.zoomLevel = Math.min(2, this.zoomLevel + 0.1);
      }
    },
    
    zoomOut() {
      if (this.zoomLevel > 0.5) {
        this.zoomLevel = Math.max(0.5, this.zoomLevel - 0.1);
      }
    },
    
    toggleFullscreen() {
      this.isFullscreen = !this.isFullscreen;
      if (this.isFullscreen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = 'auto';
      }
    },
    
    exportToPDF() {
      // PDF export functionality
      toast.info('PDF export feature coming soon!');
    },

    // Sticky horizontal scrollbar methods
    saveStateToSession() {
      const state = {
        reportDate: this.reportDate,
        selectedPlants: this.selectedPlants,
      };
      sessionStorage.setItem('generateReportState', JSON.stringify(state));
    },
    
    restoreStateFromSession() {
      const savedState = sessionStorage.getItem('generateReportState');
      if (savedState) {
        try {
          const state = JSON.parse(savedState);
          if (state.reportDate) {
            // Only restore date if it's not already set
            if (!this.reportDate) this.reportDate = state.reportDate;
          }
          if (state.selectedPlants && state.selectedPlants.length) this.selectedPlants = state.selectedPlants;
          
          // Always start fresh for report generation state
          this.reportGenerated = false;
          this.showPreview = false;
          this.reportPreview = null;
        } catch (e) {
          console.error('Error restoring state from session storage', e);
        }
      }
    },

    handleHorizontalScroll(event) {
      const container = event.target;
      const scrollLeft = container.scrollLeft;
      const scrollWidth = container.scrollWidth;
      const clientWidth = container.clientWidth;
      
      // Update scroll position data
      this.scrollPosition = scrollLeft;
      this.maxScrollPosition = scrollWidth - clientWidth;
      this.scrollProgress = this.maxScrollPosition > 0 ? (scrollLeft / this.maxScrollPosition) * 100 : 0;
      
      console.log('Scroll event:', { 
        scrollLeft, 
        scrollWidth, 
        clientWidth, 
        scrollProgress: this.scrollProgress 
      });
      
      if (this.$refs.stickyScrollThumb && this.$refs.stickyScrollTrack && this.$refs.stickyScrollContainer) {
        const hasHorizontalScroll = scrollWidth > clientWidth;
        
        if (hasHorizontalScroll) {
          this.$refs.stickyScrollContainer.style.display = 'block';
          
          const thumbWidth = Math.max((clientWidth / scrollWidth) * 100, 8); // Minimum 8% width
          const maxThumbPosition = 100 - thumbWidth;
          const thumbPosition = this.maxScrollPosition > 0 ? 
            Math.min((scrollLeft / this.maxScrollPosition) * maxThumbPosition, maxThumbPosition) : 0;
          
          console.log('Updating thumb:', { thumbWidth, thumbPosition });
          
          this.$refs.stickyScrollThumb.style.width = `${thumbWidth}%`;
          this.$refs.stickyScrollThumb.style.left = `${thumbPosition}%`;
        } else {
          this.$refs.stickyScrollContainer.style.display = 'none';
        }
      } else {
        console.log('Scrollbar refs not available:', {
          thumb: !!this.$refs.stickyScrollThumb,
          track: !!this.$refs.stickyScrollTrack,
          container: !!this.$refs.stickyScrollContainer
        });
      }
    },

    // Navigation methods for user-friendly scrollbar
    scrollLeft() {
      if (this.$refs.previewContainer) {
        const container = this.$refs.previewContainer;
        const scrollAmount = container.clientWidth * 0.3; // Scroll 30% of visible width
        container.scrollLeft = Math.max(0, container.scrollLeft - scrollAmount);
      }
    },

    scrollRight() {
      if (this.$refs.previewContainer) {
        const container = this.$refs.previewContainer;
        const scrollAmount = container.clientWidth * 0.3; // Scroll 30% of visible width
        const maxScroll = container.scrollWidth - container.clientWidth;
        container.scrollLeft = Math.min(maxScroll, container.scrollLeft + scrollAmount);
      }
    },

    scrollToStart() {
      if (this.$refs.previewContainer) {
        this.$refs.previewContainer.scrollLeft = 0;
      }
    },

    scrollToEnd() {
      if (this.$refs.previewContainer) {
        const container = this.$refs.previewContainer;
        container.scrollLeft = container.scrollWidth - container.clientWidth;
      }
    },

    initStickyScrollbar() {
      this.$nextTick(() => {
        if (!this.$refs.stickyScrollTrack || !this.$refs.previewContainer || !this.$refs.stickyScrollContainer || !this.$refs.stickyScrollThumb) {
          console.log('User-friendly scrollbar refs not available');
          return;
        }

        const container = this.$refs.previewContainer;
        const stickyContainer = this.$refs.stickyScrollContainer;
        const track = this.$refs.stickyScrollTrack;
        const thumb = this.$refs.stickyScrollThumb;
        
        console.log('Initializing user-friendly scrollbar...');
        console.log('Refs:', { track, thumb, container, stickyContainer });
        
        // Check if horizontal scrolling is needed
        const checkScrollNeed = () => {
          const hasHorizontalScroll = container.scrollWidth > container.clientWidth;
          console.log('Scroll check:', { 
            scrollWidth: container.scrollWidth, 
            clientWidth: container.clientWidth, 
            hasHorizontalScroll 
          });
          
          if (hasHorizontalScroll) {
            stickyContainer.style.display = 'block';
            this.handleHorizontalScroll({ target: container });
          } else {
            stickyContainer.style.display = 'none';
          }
          
          return hasHorizontalScroll;
        };
        
        // Initial check
        if (!checkScrollNeed()) {
          console.log('No horizontal scroll needed, hiding scrollbar');
          return;
        }
        
        console.log('Setting up user-friendly scrollbar event listeners');
        
        // Handle track clicks
        track.addEventListener('click', (e) => {
          if (e.target === thumb || thumb.contains(e.target)) {
            console.log('Clicked on thumb, ignoring');
            return; // Don't handle clicks on thumb
          }
          
          const rect = track.getBoundingClientRect();
          const clickPosition = (e.clientX - rect.left) / rect.width;
          const maxScroll = container.scrollWidth - container.clientWidth;
          const scrollLeft = clickPosition * maxScroll;
          
          console.log('Track clicked:', { clickPosition, scrollLeft });
          
          // Smooth scroll to position
          container.scrollTo({
            left: scrollLeft,
            behavior: 'smooth'
          });
        });

        // Handle thumb dragging with improved UX
        let isDragging = false;
        let startX = 0;
        let startScrollLeft = 0;

        thumb.addEventListener('mousedown', (e) => {
          console.log('Thumb mousedown');
          isDragging = true;
          startX = e.clientX;
          startScrollLeft = container.scrollLeft;
          e.preventDefault();
          if (document.body) {
            document.body.style.userSelect = 'none';
          }
          if (thumb) {
            thumb.style.transform = 'scaleY(1.1)';
          }
        });

        document.addEventListener('mousemove', (e) => {
          if (!isDragging) return;
          
          const deltaX = e.clientX - startX;
          const trackWidth = track.offsetWidth;
          const scrollRatio = deltaX / trackWidth;
          const maxScroll = container.scrollWidth - container.clientWidth;
          
          const newScrollLeft = Math.max(0, Math.min(maxScroll, startScrollLeft + (scrollRatio * maxScroll)));
          console.log('Dragging:', { deltaX, scrollRatio, newScrollLeft });
          container.scrollLeft = newScrollLeft;
        });

        document.addEventListener('mouseup', () => {
          if (isDragging) {
            console.log('Thumb mouseup');
            isDragging = false;
            if (document.body) {
              document.body.style.userSelect = '';
            }
            if (thumb) {
              thumb.style.transform = '';
            }
          }
        });

        // Handle window resize
        const resizeHandler = () => {
          this.$nextTick(() => {
            checkScrollNeed();
          });
        };
        
        window.addEventListener('resize', resizeHandler);
        
        // Store cleanup function
        this._stickyScrollbarCleanup = () => {
          window.removeEventListener('resize', resizeHandler);
        };
        
        console.log('User-friendly scrollbar initialized successfully');
      });
    },

    // Method to manually update scrollbar (useful for debugging)
    updateStickyScrollbar() {
      if (this.$refs.previewContainer) {
        console.log('Manual scrollbar update triggered');
        this.handleHorizontalScroll({ target: this.$refs.previewContainer });
      }
    },

    // Debug method to test scrollbar
    testScrollbar() {
      console.log('Testing scrollbar...');
      if (this.$refs.stickyScrollThumb) {
        // Test by manually setting thumb position
        this.$refs.stickyScrollThumb.style.left = '50%';
        this.$refs.stickyScrollThumb.style.width = '20%';
        console.log('Thumb should now be at 50% position');
        
        setTimeout(() => {
          if (this.$refs.stickyScrollThumb) {
            this.$refs.stickyScrollThumb.style.left = '0%';
            console.log('Thumb reset to 0%');
          }
        }, 2000);
      } else {
        console.log('Thumb ref not available');
      }
    },

    async loadPlants() {
      try {
        const response = await api.getPlants();
        // Handle both paginated and non-paginated responses
        this.plants = response.data.results || response.data;
        console.log('Loaded plants:', this.plants);
        
        // Always select all plants automatically
        this.selectedPlants = this.plants.map(plant => plant.code);
        console.log('Selected plants:', this.selectedPlants);
        
        // Ensure we have plants selected
        if (this.selectedPlants.length === 0) {
          console.warn('No plants were selected after loading');
          toast.warning('No plants available for report generation');
        } else {
          console.log(`Successfully loaded ${this.selectedPlants.length} plants:`, this.selectedPlants);
        }
      } catch (error) {
        console.error('Error loading plants:', error);
        toast.error('Error loading plants: ' + (error.message || 'Unknown error'));
        
        // Fallback: try to use hardcoded plant codes if API fails
        console.log('Attempting fallback with hardcoded plant codes...');
        this.selectedPlants = ['AGUS1', 'AGUS2', 'AGUS4', 'AGUS5', 'AGUS6', 'AGUS7', 'PULANGI4'];
        this.plants = this.selectedPlants.map(code => ({ code, name: code }));
        toast.info('Using fallback plant codes. Some features may be limited.');
      }
    },
    
    loadGenerationHistory() {
      try {
        const history = localStorage.getItem('reportGenerationHistory');
        if (history) {
          this.generationHistory = JSON.parse(history);
          // Sort by timestamp descending (newest first)
          this.generationHistory.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        }
      } catch (error) {
        console.error('Error loading generation history:', error);
        this.generationHistory = [];
      }
    },
    
    // Security methods
    loadCurrentUser() {
      try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
          this.currentUser = JSON.parse(userStr);
        }
      } catch (error) {
        console.error('Error loading current user:', error);
      }
    },
    
    async loadUserAuthorizations() {
      try {
        const response = await api.getUserSignatoryAuthorizations();
        this.userAuthorizations = Array.isArray(response.data) ? response.data : (response.data.results || []);
        console.log('Loaded user authorizations:', this.userAuthorizations);
      } catch (error) {
        // Silently fail - user may not be logged in or have authorizations
        this.userAuthorizations = [];
      }
    },
    
    canSignAs(signatoryName) {
      // Return true by default if data isn't loaded yet (fail-open for better UX)
      if (!this.currentUser && this.userAuthorizations.length === 0) {
        return true; // Allow access until we verify authorization
      }
      
      // Solution 2: Check if user can sign as themselves
      if (this.currentUser && this.currentUser.username) {
        const username = this.currentUser.username.toUpperCase().replace(/[._]/g, ' ');
        const normalizedSignatory = signatoryName.toUpperCase().replace(/[._]/g, ' ');
        
        // Allow if username matches signatory name
        if (username === normalizedSignatory) {
          return true;
        }
      }
      
      // Solution 1: Check if user has authorization for this signatory
      const hasAuth = this.userAuthorizations.some(
        auth => auth.signatory_name === signatoryName && auth.is_valid
      );
      
      return hasAuth;
    },
    
    saveToHistory(reportData) {
      try {
        const historyItem = {
          ...reportData,
          timestamp: new Date().toISOString(),
        };
        
        this.generationHistory.unshift(historyItem);
        
        // Keep only last 50 items
        if (this.generationHistory.length > 50) {
          this.generationHistory = this.generationHistory.slice(0, 50);
        }
        
        localStorage.setItem('reportGenerationHistory', JSON.stringify(this.generationHistory));
      } catch (error) {
        console.error('Error saving to history:', error);
      }
    },
    
    clearHistory() {
      if (confirm('Are you sure you want to clear all generation history?')) {
        this.generationHistory = [];
        localStorage.removeItem('reportGenerationHistory');
        this.showMenu = false;
        toast.success('History cleared successfully');
      }
    },
    
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    
    closeMenu(e) {
      if (this.$refs.menuButton && !this.$refs.menuButton.contains(e.target)) {
        this.showMenu = false;
      }
    },
    
    async regenerateReport(historyItem) {
      this.selectedPlants = [historyItem.plantCode];
      this.reportDate = historyItem.reportDate;
      this.reportType = historyItem.reportType;
      
      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
      toast.info('Report parameters loaded. Click "Generate Report" to regenerate.');
    },
    
    async downloadHistoryReport(historyItem) {
      if (this.generating) {
        toast.warning('Please wait for the current report to finish generating');
        return;
      }
      
      this.generating = true;
      toast.info('Downloading report...');

      try {
        // Parse plant codes - they might be comma-separated
        const plantCodes = historyItem.plantCode.includes(',') 
          ? historyItem.plantCode.split(',').map(code => code.trim())
          : [historyItem.plantCode];

        console.log('Downloading history report with data:', {
          plant_codes: plantCodes,
          start_date: historyItem.reportDate,
          end_date: historyItem.reportDate,
          report_type: historyItem.reportType,
        });

        const response = await api.generateReport({
          plant_codes: plantCodes,
          start_date: historyItem.reportDate,
          end_date: historyItem.reportDate,
          report_type: historyItem.reportType,
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', historyItem.filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        toast.success('Report downloaded successfully!');
      } catch (error) {
        console.error('Download report error:', error);
        console.error('Error response:', error.response);
        console.error('Error response data:', error.response?.data);
        
        let errorMsg = 'Failed to download report';
        
        // Handle blob response errors
        if (error.response?.data instanceof Blob) {
          try {
            const text = await error.response.data.text();
            console.error('Blob error text:', text);
            const errorData = JSON.parse(text);
            errorMsg = errorData.error || errorMsg;
            
            // Show detailed validation errors if available
            if (errorData.plant_codes) {
              errorMsg = `Plant validation error: ${errorData.plant_codes.join(', ')}`;
            }
            if (errorData.start_date) {
              errorMsg = `Date validation error: ${errorData.start_date.join(', ')}`;
            }
            if (errorData.end_date) {
              errorMsg = `Date validation error: ${errorData.end_date.join(', ')}`;
            }
          } catch (e) {
            console.error('Error parsing blob:', e);
            errorMsg = error.response?.statusText || errorMsg;
          }
        } else if (error.response?.data?.error) {
          errorMsg = error.response.data.error;
        } else if (error.response?.data) {
          // Handle validation errors
          const data = error.response.data;
          console.error('Validation error data:', data);
          
          if (data.plant_codes) {
            errorMsg = `Plant validation error: ${Array.isArray(data.plant_codes) ? data.plant_codes.join(', ') : data.plant_codes}`;
          } else if (data.start_date) {
            errorMsg = `Start date validation error: ${Array.isArray(data.start_date) ? data.start_date.join(', ') : data.start_date}`;
          } else if (data.end_date) {
            errorMsg = `End date validation error: ${Array.isArray(data.end_date) ? data.end_date.join(', ') : data.end_date}`;
          } else if (data.non_field_errors) {
            errorMsg = `Validation error: ${Array.isArray(data.non_field_errors) ? data.non_field_errors.join(', ') : data.non_field_errors}`;
          } else if (data.detail) {
            errorMsg = `API error: ${data.detail}`;
          } else {
            errorMsg = `Validation error: ${JSON.stringify(data)}`;
          }
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 8000);
      } finally {
        this.generating = false;
      }
    },
    
    formatDateRange(reportDate) {
      return new Date(reportDate).toLocaleDateString();
    },
    
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
      if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
      if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
      
      return date.toLocaleDateString();
    },
    
    formatExactTime(timestamp) {
      const date = new Date(timestamp);
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      };
      return date.toLocaleString('en-US', options);
    },
    
    async generateReport() {
      if (!this.canGenerate) return;

      // Ensure we have plants selected
      if (!this.selectedPlants || this.selectedPlants.length === 0) {
        toast.error('No plants selected. Please wait for plants to load or refresh the page.');
        return;
      }

      // Validate date format (should be YYYY-MM-DD)
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateRegex.test(this.reportDate)) {
        toast.error('Invalid date format. Please select a valid date.');
        return;
      }

      console.log('Generating report with data:', {
        plant_codes: this.selectedPlants,
        start_date: this.reportDate,
        end_date: this.reportDate,
        report_type: this.reportType,
      });

      this.generating = true;
      this.reportGenerated = false;
      this.showSuccessModal = false;

      try {
        const response = await api.previewReport({
          plant_codes: this.selectedPlants,
          start_date: this.reportDate,
          end_date: this.reportDate,
          report_type: this.reportType,
        });

        this.reportPreview = response.data;
        this.reportGenerated = true;
        
        // Load signatures for this report date
        await this.loadReportSignatures();
        
        // Show success modal instead of automatically showing preview
        this.showSuccessModal = true;

        toast.success('Report generated successfully!');
      } catch (error) {
        console.error('Generate report error:', error);
        console.error('Error response:', error.response);
        console.error('Error response data:', error.response?.data);
        
        let errorMsg = 'Failed to generate report';
        
        // Handle validation errors
        if (error.response?.data) {
          const data = error.response.data;
          console.error('Validation error data:', data);
          
          if (data.plant_codes) {
            errorMsg = `Plant validation error: ${Array.isArray(data.plant_codes) ? data.plant_codes.join(', ') : data.plant_codes}`;
          } else if (data.start_date) {
            errorMsg = `Start date validation error: ${Array.isArray(data.start_date) ? data.start_date.join(', ') : data.start_date}`;
          } else if (data.end_date) {
            errorMsg = `End date validation error: ${Array.isArray(data.end_date) ? data.end_date.join(', ') : data.end_date}`;
          } else if (data.non_field_errors) {
            errorMsg = `Validation error: ${Array.isArray(data.non_field_errors) ? data.non_field_errors.join(', ') : data.non_field_errors}`;
          } else if (data.detail) {
            errorMsg = `API error: ${data.detail}`;
          } else if (data.error) {
            errorMsg = typeof data.error === 'string' ? data.error : JSON.stringify(data.error);
            if (typeof errorMsg === 'string' && errorMsg.includes('No data found')) {
              errorMsg = `No data found for the selected date (${this.reportDate}). The Excel files you uploaded might contain data for different dates. Please check the dates in your uploaded files or select a different report date.`;
            }
          } else {
            errorMsg = `Validation error: ${JSON.stringify(data)}`;
          }
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 8000);
      } finally {
        this.generating = false;
      }
    },

    previewReport() {
      if (!this.reportPreview) {
        toast.error('No report to preview. Please generate a report first.');
        return;
      }

      this.showPreview = true;
      this.showSuccessModal = false;
      
      // Scroll to preview section
      this.$nextTick(() => {
        const previewElement = document.querySelector('.preview-card');
        if (previewElement) {
          previewElement.scrollIntoView({ behavior: 'smooth' });
        }
      });
    },

    closeSuccessModal() {
      this.showSuccessModal = false;
    },

    async downloadExcel() {
      if (!this.reportPreview) return;

      this.generating = true;
      toast.info('Downloading Excel file from server...');

      try {
        const dateStr = this.reportDate.replace(/-/g, '');
        const filename = `PLANT_STATUS_${dateStr}.xlsx`;
        
        // Fetch the Excel file from backend
        const response = await api.generateReport({
          plant_codes: this.selectedPlants,
          start_date: this.reportDate,
          end_date: this.reportDate,
          report_type: this.reportType,
        });

        // Create download link from blob
        const blob = new Blob([response.data], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        // Save to history
        const selectedPlantNamesForHistory = this.plants
          .filter(p => this.selectedPlants.includes(p.code))
          .map(p => p.name)
          .join(', ');
        const reportTypeNameForHistory = this.reportTypes.find(t => t.value === this.reportType)?.label || this.reportType;
        this.saveToHistory({
          filename: filename,
          plantCode: this.selectedPlants.join(','),
          plantName: selectedPlantNamesForHistory,
          reportDate: this.reportDate,
          reportType: this.reportType,
          reportTypeName: reportTypeNameForHistory,
        });

        toast.success('Excel file downloaded successfully!');
      } catch (error) {
        console.error('Download Excel error:', error);
        toast.error('Failed to download Excel file: ' + (error.message || 'Unknown error'), 6000);
      } finally {
        this.generating = false;
      }
    },

    closePreview() {
      this.showPreview = false;
      this.reportPreview = null;
    },

    async saveToReportStorage() {
      if (!this.reportPreview) {
        toast.error('No report to save. Please generate a report first.');
        return;
      }

      this.saving = true;
      toast.info('Saving report to storage...');

      try {
        // First, generate the Excel file as a blob
        const ExcelJSModule = await import('exceljs');
        const ExcelJS = ExcelJSModule.default || ExcelJSModule;
        const wb = new ExcelJS.Workbook();
        wb.creator = 'NPC Reporting System';
        const ws = wb.addWorksheet('PSR PSALM Edit (2)');

        // Generate the Excel content (simplified version for saving)
        // You can reuse the same logic from downloadExcel method here
        // For now, let's create a basic version

        // Add header information
        ws.getCell('A1').value = 'PLANT STATUS REPORT';
        ws.getCell('A2').value = this.reportPreview.header.date_text;
        
        // Add basic table structure
        const headers = ['PLANT NAME', 'Rated Capacity (MW)', 'Available Capacity (MW)', 'Lake Lanao Projected Ave. Outflow', 'Load at 0800H', 'REMARKS'];
        headers.forEach((header, index) => {
          ws.getCell(4, index + 1).value = header;
        });

        // Generate Excel buffer
        const buffer = await wb.xlsx.writeBuffer();
        const blob = new Blob([buffer], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });

        // Create FormData to send to backend
        const formData = new FormData();
        const dateStr = this.reportDate.replace(/-/g, '');
        const filename = `PSR_${dateStr}.xlsx`;
        
        formData.append('title', `PSR Report - ${this.reportPreview.header.date_text}`);
        formData.append('document_type', 'PSR');
        formData.append('description', `Plant Status Report generated for ${this.reportPreview.header.date_text}`);
        formData.append('file_path', blob, filename); // Changed from 'file' to 'file_path'
        formData.append('status', 'DRAFT');

        // Save to backend as a document
        const response = await api.createDocument(formData);
        
        if (response.status === 201) {
          toast.success('Report saved to Report Storage successfully!');
          
          // Show success message with option to navigate
          const shouldNavigate = confirm('Report saved successfully! Would you like to view it in Report Storage?');
          if (shouldNavigate) {
            this.$router.push('/report-storage');
          }
        }

      } catch (error) {
        console.error('Error saving report to storage:', error);
        
        // Handle permission errors gracefully
        if (error.response?.status === 403) {
          toast.error('You do not have permission to save reports to storage. Please contact your administrator.', 6000);
          return;
        }
        
        let errorMsg = 'Failed to save report to storage';
        
        if (error.response?.data) {
          const data = error.response.data;
          if (data.title) {
            errorMsg = `Title error: ${Array.isArray(data.title) ? data.title.join(', ') : data.title}`;
          } else if (data.file) {
            errorMsg = `File error: ${Array.isArray(data.file) ? data.file.join(', ') : data.file}`;
          } else if (data.detail) {
            errorMsg = `API error: ${data.detail}`;
          } else if (data.error) {
            errorMsg = typeof data.error === 'string' ? data.error : JSON.stringify(data.error);
          }
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        toast.error(errorMsg, 8000);
      } finally {
        this.saving = false;
      }
    },

    formatNumber(value) {
      if (!value) return '0';
      return new Intl.NumberFormat().format(value);
    },

    formatDate(dateString) {
      if (!dateString) return '-';
      return new Date(dateString).toLocaleDateString();
    },

    // E-signature methods
    openESignatureModal(signatory) {
      this.selectedSignatory = signatory;
      this.showESignatureModal = true;
      this.signatureMode = 'draw';
      this.uploadedSignature = null;
      this.selectedSavedSignature = null;
      this.typedSignature = '';
      this.hasDrawnOnCanvas = false; // Reset drawing flag
      
      // Initialize canvas after modal is shown
      this.$nextTick(() => {
        this.initializeCanvas();
      });
    },

    closeESignatureModal() {
      this.showESignatureModal = false;
      this.selectedSignatory = null;
      this.clearCanvas();
      this.uploadedSignature = null;
      this.selectedSavedSignature = null;
      this.typedSignature = '';
      this.hasDrawnOnCanvas = false; // Reset drawing flag
    },

    goToRequestSignatureAccess(signatory) {
      // Navigate to the Request Signature Access page with pre-filled data
      if (signatory) {
        this.$router.push({
          path: '/signatory-authorization',
          query: {
            signatory: signatory.name,
            role: signatory.role
          }
        });
      } else {
        this.$router.push('/signatory-authorization');
      }
    },

    initializeCanvas() {
      const canvas = this.$refs.signatureCanvas;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      ctx.strokeStyle = '#000000';
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      // Set white background
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    },

    startDrawing(e) {
      this.isDrawing = true;
      const canvas = this.$refs.signatureCanvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      
      const x = (e.clientX || e.touches[0].clientX) - rect.left;
      const y = (e.clientY || e.touches[0].clientY) - rect.top;
      
      ctx.beginPath();
      ctx.moveTo(x, y);
      
      e.preventDefault();
    },

    draw(e) {
      if (!this.isDrawing) return;
      
      const canvas = this.$refs.signatureCanvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      
      const x = (e.clientX || e.touches[0].clientX) - rect.left;
      const y = (e.clientY || e.touches[0].clientY) - rect.top;
      
      ctx.lineTo(x, y);
      ctx.stroke();
      
      // Mark that user has drawn something
      this.hasDrawnOnCanvas = true;
      
      e.preventDefault();
    },

    stopDrawing() {
      this.isDrawing = false;
    },

    clearCanvas() {
      const canvas = this.$refs.signatureCanvas;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Reset white background
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Reset drawing flag
      this.hasDrawnOnCanvas = false;
    },

    isCanvasEmpty() {
      const canvas = this.$refs.signatureCanvas;
      if (!canvas) return true;
      
      const ctx = canvas.getContext('2d');
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;
      
      // Check if any pixel is significantly different from white
      // We allow for some tolerance due to anti-aliasing
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        const a = data[i + 3];
        
        // If any pixel is not close to white (with some tolerance for anti-aliasing)
        if (a > 0 && (r < 240 || g < 240 || b < 240)) {
          return false;
        }
      }
      return true;
    },

    // Helper method to export preview content to Excel
    _exportPreviewToExcel(ws, mainTable, rightSideContent, startRow, styles) {
      const { DARK_TEAL, YELLOW, LIGHT_BLUE, BLUE_FILL, GREY_HDR, WHITE,
              mkFill, thinBorder, safeMerge, sv } = styles;
      
      let r = startRow;
      
      // Extract header information
      const headerDate = this.reportPreview.header?.date_text || 'as of 0800H Thursday, 12 March 2026';
      
      // Header section
      ws.getRow(r).height = 20; r++;
      ws.getRow(r).height = 28;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, 'MINDANAO GENERATION', {
        font: { bold: true, size: 20 },
        alignment: { horizontal: 'center', vertical: 'middle' }
      });
      r++;
      
      ws.getRow(r).height = 18;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, '(PSALM PORTFOLIO)', {
        font: { bold: true, size: 14 },
        alignment: { horizontal: 'center', vertical: 'middle' }
      });
      r++;
      
      ws.getRow(r).height = 8; r++;
      
      // Officials section
      ws.getRow(r).height = 18;
      sv(ws, r, 1, 'FOR     :', { font: { bold: true, size: 13 }, alignment: { horizontal: 'right' } });
      sv(ws, r, 2, 'MR. LARRY I. SABELLINA', { font: { bold: true, size: 13 } });
      sv(ws, r, 10, 'MR. DENNIS EDWARD A. DELA SERNA', { font: { bold: true, size: 13 } });
      sv(ws, r, 20, 'MR. ARNOLD C. FRANCISCO', { font: { bold: true, size: 13 } });
      r++;
      
      ws.getRow(r).height = 16;
      sv(ws, r, 2, 'VP, Mindanao Generation', { font: { size: 11 } });
      sv(ws, r, 10, 'President and CEO, PSALM', { font: { size: 11 } });
      sv(ws, r, 20, 'VP - PAIMG, PSALM', { font: { size: 11 } });
      r++;
      
      ws.getRow(r).height = 6; r++;
      
      // Report title
      ws.getRow(r).height = 28;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, 'PLANT STATUS REPORT', {
        font: { bold: true, size: 18, italic: true, color: { argb: WHITE } },
        alignment: { horizontal: 'center', vertical: 'middle' },
        fill: mkFill(DARK_TEAL)
      });
      r++;
      
      ws.getRow(r).height = 22;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, headerDate, {
        font: { bold: true, size: 13, color: { argb: WHITE } },
        alignment: { horizontal: 'center', vertical: 'middle' },
        fill: mkFill(DARK_TEAL)
      });
      r++;
      
      ws.getRow(r).height = 5; r++;
      
      // Column headers
      const hdrStart = r;
      const headerRow = mainTable.querySelector('thead tr');
      if (headerRow) {
        const headers = Array.from(headerRow.querySelectorAll('th')).slice(0, 6);
        headers.forEach((th, index) => {
          const colNum = index + 1;
          const labelText = th.textContent.trim();
          safeMerge(ws, hdrStart, colNum, hdrStart + 3, colNum);
          sv(ws, hdrStart, colNum, labelText, {
            font: { bold: true, size: labelText.includes('\n') ? 11 : 13 },
            alignment: { horizontal: 'center', vertical: 'middle', wrapText: true },
            fill: mkFill(GREY_HDR),
            border: thinBorder
          });
        });
      }
      
      for (let hr = hdrStart; hr < hdrStart + 4; hr++) ws.getRow(hr).height = 16;
      r += 4;
      
      // Main table data
      const tbody = mainTable.querySelector('tbody');
      if (tbody) {
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.forEach(tableRow => {
          const cells = Array.from(tableRow.querySelectorAll('td'));
          ws.getRow(r).height = 18;
          
          cells.slice(0, 6).forEach((td, colIndex) => {
            const colNum = colIndex + 1;
            const cellValue = td.textContent.trim();
            const isBold = td.style.fontWeight === 'bold' || td.querySelector('b') || td.querySelector('strong');
            const hasRedText = td.style.color === 'red' || td.querySelector('[style*="color: red"]');
            const textAlign = td.style.textAlign || 'left';
            
            const cellStyle = {
              font: { 
                size: 11,
                bold: isBold,
                color: hasRedText ? { argb: 'FFFF0000' } : undefined
              },
              alignment: { 
                horizontal: textAlign === 'right' ? 'right' : textAlign === 'center' ? 'center' : 'left', 
                vertical: 'middle',
                wrapText: cellValue.length > 20
              },
              border: thinBorder
            };
            
            let finalValue = cellValue;
            let numFmt = null;
            
            if (/^\d+(\.\d+)?$/.test(cellValue.replace(/[^\d\.]/g, ''))) {
              const numValue = parseFloat(cellValue.replace(/[^\d\.\-]/g, ''));
              if (!isNaN(numValue)) {
                finalValue = numValue;
                if (cellValue.includes('.')) {
                  numFmt = cellValue.split('.')[1]?.length === 1 ? '0.0' : '0.00';
                } else {
                  numFmt = '0';
                }
              }
            }
            
            if (numFmt) cellStyle.numFmt = numFmt;
            sv(ws, r, colNum, finalValue, cellStyle);
          });
          
          r++;
        });
      }
      
      // Right side content
      if (rightSideContent) {
        ws.getRow(r).height = 15; r++;
        
        // Add right side tables and content
        const rightElements = rightSideContent.children;
        let rightCol = 8;
        
        Array.from(rightElements).forEach(element => {
          if (element.classList.contains('data-table-container') || element.classList.contains('data-table')) {
            const table = element.querySelector('table') || element;
            const tableRows = Array.from(table.querySelectorAll('tr'));
            
            tableRows.forEach((tr, rowIndex) => {
              const cells = Array.from(tr.querySelectorAll('td, th'));
              const currentRow = r + rowIndex;
              
              if (!ws.getRow(currentRow).height) {
                ws.getRow(currentRow).height = 16;
              }
              
              cells.forEach((cell, colIndex) => {
                const colNum = rightCol + colIndex;
                const cellValue = cell.textContent.trim();
                const isHeader = cell.tagName === 'TH';
                const isBold = isHeader || cell.style.fontWeight === 'bold';
                
                sv(ws, currentRow, colNum, cellValue, {
                  font: { size: isHeader ? 11 : 10, bold: isBold },
                  alignment: { 
                    horizontal: 'center', 
                    vertical: 'middle',
                    wrapText: cellValue.length > 15
                  },
                  border: thinBorder,
                  fill: isHeader ? mkFill(GREY_HDR) : undefined
                });
              });
            });
            
            rightCol += 10;
            if (rightCol > 40) {
              rightCol = 8;
              r += Math.max(tableRows.length, 8);
            }
          }
        });
      }
      
      // Additional sections
      if (this.reportPreview.forecasted_load) {
        const fl = this.reportPreview.forecasted_load;
        const forecastText = `Agus-Pulangi Forecasted Load @ 6pm, ${fl.date}: Agus = ${fl.agus_load} MW & Pulangui IV = ${fl.pulangi_load} MW, Total Load: ${fl.total_load} MW`;
        ws.getRow(r).height = 18;
        safeMerge(ws, r, 1, r, 30);
        sv(ws, r, 1, forecastText, {
          font: { bold: true, size: 11 },
          alignment: { horizontal: 'left', vertical: 'middle' },
          fill: mkFill(YELLOW)
        });
        r++;
      }
      
      // Notes
      ws.getRow(r).height = 16;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, 'Note:', { font: { bold: true, size: 11 }, alignment: { horizontal: 'left', vertical: 'middle' } });
      r++;
      (this.reportPreview.notes || []).forEach((note, idx) => {
        ws.getRow(r).height = 18;
        safeMerge(ws, r, 1, r, 30);
        sv(ws, r, 1, `${idx + 1}. ${note}`, {
          font: { size: 10 },
          alignment: { horizontal: 'left', vertical: 'middle', wrapText: true }
        });
        r++;
      });
      
      // Signatures
      ws.getRow(r).height = 10; r++;
      ws.getRow(r).height = 16;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, 'AUTHORIZATION', {
        font: { bold: true, size: 13 }, alignment: { horizontal: 'center', vertical: 'middle' }
      });
      r++;
      
      const writeSignatureGroup = (sigs) => {
        if (!sigs || !sigs.length) return;
        const total = sigs.length;
        ws.getRow(r).height = 14;
        sigs.forEach((sig, i) => {
          const c1 = i * Math.floor(30 / total) + 1;
          const c2 = (i + 1) * Math.floor(30 / total);
          if (c1 < c2) safeMerge(ws, r, c1, r, c2);
          sv(ws, r, c1, sig.role, { font: { size: 10, italic: true }, alignment: { horizontal: 'center', vertical: 'middle' } });
        });
        r++;
        for (let sr = 0; sr < 3; sr++) { ws.getRow(r).height = sr === 1 ? 24 : 12; r++; }
        ws.getRow(r).height = 16;
        sigs.forEach((sig, i) => {
          const c1 = i * Math.floor(30 / total) + 1;
          const c2 = (i + 1) * Math.floor(30 / total);
          if (c1 < c2) { try { ws.mergeCells(r, c1, r, c2); } catch(e) {} }
          sv(ws, r, c1, sig.name, { font: { bold: true, size: 11, underline: true }, alignment: { horizontal: 'center', vertical: 'middle' } });
        });
        r++;
        ws.getRow(r).height = 14;
        sigs.forEach((sig, i) => {
          const c1 = i * Math.floor(30 / total) + 1;
          const c2 = (i + 1) * Math.floor(30 / total);
          if (c1 < c2) { try { ws.mergeCells(r, c1, r, c2); } catch(e) {} }
          sv(ws, r, c1, sig.title, { font: { size: 10 }, alignment: { horizontal: 'center', vertical: 'middle' } });
        });
        r++;
        ws.getRow(r).height = 8; r++;
      };
      
      writeSignatureGroup(this.reportPreview.signatures?.first_row);
      writeSignatureGroup(this.reportPreview.signatures?.second_row);
      
      // Additional notes
      ws.getRow(r).height = 10; r++;
      ws.getRow(r).height = 16;
      safeMerge(ws, r, 1, r, 30);
      sv(ws, r, 1, 'Note:', { font: { bold: true, size: 11 }, alignment: { horizontal: 'left', vertical: 'middle' } });
      r++;
      (this.reportPreview.additional_notes || []).forEach((note, idx) => {
        ws.getRow(r).height = 22;
        safeMerge(ws, r, 1, r, 30);
        sv(ws, r, 1, `${idx + 1}. ${note}`, {
          font: { size: 10 },
          alignment: { horizontal: 'left', vertical: 'middle', wrapText: true }
        });
        r++;
      });
      
      // Footer note
      ws.getRow(r).height = 8; r++;
      if (this.reportPreview.footer_note) {
        ws.getRow(r).height = 40;
        safeMerge(ws, r, 1, r, 30);
        sv(ws, r, 1, this.reportPreview.footer_note, {
          font: { italic: true, size: 10 },
          alignment: { horizontal: 'left', vertical: 'middle', wrapText: true }
        });
        r++;
      }
      
      return r;
    },

    handleFileUpload(e) {
      const file = e.target.files[0];
      if (!file) return;
      
      // Validate file size (2MB max)
      if (file.size > 2 * 1024 * 1024) {
        toast.error('File size must be less than 2MB');
        return;
      }
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        toast.error('Please select an image file');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.uploadedSignature = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    async saveSignature() {
      if (!this.hasSignature) return;
      
      let signatureData = null;
      let signatureType = 'DRAW';
      
      if (this.signatureMode === 'draw') {
        const canvas = this.$refs.signatureCanvas;
        signatureData = canvas.toDataURL('image/png');
        signatureType = 'DRAW';
      } else if (this.signatureMode === 'upload') {
        signatureData = this.selectedSavedSignature?.signature_image || this.selectedSavedSignature?.data || this.uploadedSignature;
        signatureType = 'UPLOAD';
      } else if (this.signatureMode === 'type') {
        // Create a canvas with the typed signature
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 100;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#000000';
        ctx.font = `24px ${this.selectedFont}`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.typedSignature, canvas.width / 2, canvas.height / 2);
        
        signatureData = canvas.toDataURL('image/png');
        signatureType = 'TYPE';
      }
      
      try {
        // First, create or get the e-signature
        let eSignature = null;
        
        // Check if we already have a signature for this signatory
        try {
          const existingSignatures = await api.getESignaturesBySignatory(this.selectedSignatory.name);
          const existing = existingSignatures.data.find(sig => 
            sig.signatory_role === this.selectedSignatory.role && sig.is_default
          );
          
          if (existing) {
            // Update existing signature
            const updateResponse = await api.updateESignature(existing.id, {
              signature_data: signatureData,
              signature_type: signatureType
            });
            eSignature = updateResponse;
          } else {
            // Create new signature
            eSignature = await api.createESignature({
              signatory_name: this.selectedSignatory.name,
              signatory_title: this.selectedSignatory.title,
              signatory_role: this.selectedSignatory.role,
              signature_type: signatureType,
              signature_data: signatureData,
              is_default: true
            });
          }
        } catch (error) {
          console.log('Creating new signature due to error:', error);
          // Create new signature
          eSignature = await api.createESignature({
            signatory_name: this.selectedSignatory.name,
            signatory_title: this.selectedSignatory.title,
            signatory_role: this.selectedSignatory.role,
            signature_type: signatureType,
            signature_data: signatureData,
            is_default: true
          });
        }
        
        // Then, create the report signature if we have a report date
        if (this.reportDate && eSignature.data) {
          await api.signReport({
            report_date: this.reportDate,
            report_type: this.reportType,
            signature: eSignature.data.id,
            signatory_name: this.selectedSignatory.name,
            signatory_role: this.selectedSignatory.role
          });
        }
        
        // Store locally for immediate display
        this.signatures[this.selectedSignatory.name] = {
          data: signatureData,
          mode: this.signatureMode,
          timestamp: new Date().toISOString()
        };
        
        toast.success(`E-signature saved for ${this.selectedSignatory.name}`);
        this.closeESignatureModal();
        
        // Reload signatures to ensure persistence
        if (this.reportDate) {
          setTimeout(() => {
            this.loadReportSignatures();
          }, 500);
        }
        
      } catch (error) {
        console.error('Error saving signature:', error);
        toast.error('Failed to save signature: ' + (error.response?.data?.error || error.message));
        
        // Fallback to local storage
        this.signatures[this.selectedSignatory.name] = {
          data: signatureData,
          mode: this.signatureMode,
          timestamp: new Date().toISOString()
        };
        
        toast.success(`E-signature saved locally for ${this.selectedSignatory.name}`);
        this.closeESignatureModal();
      }
    },

    // Saved signatures management
    async loadSavedSignatures() {
      try {
        const response = await api.getESignatures();
        this.savedSignatures = response.data.results || response.data;
      } catch (error) {
        // Silently handle authentication/permission errors
        if (error.response?.status === 403 || error.response?.status === 401) {
          console.log('Signatures not accessible - user may not have permission');
          this.savedSignatures = [];
          return;
        }
        
        console.error('Error loading saved signatures:', error);
        // Fallback to localStorage
        try {
          const saved = localStorage.getItem('userSignatureLibrary');
          if (saved) {
            this.savedSignatures = JSON.parse(saved);
          }
        } catch (e) {
          console.error('Error loading from localStorage:', e);
          this.savedSignatures = [];
        }
      }
    },

    async loadReportSignatures() {
      if (!this.reportDate) return;
      
      try {
        console.log('Loading signatures for report date:', this.reportDate);
        const response = await api.getReportSignaturesForReport(this.reportDate, this.reportType);
        const reportSignatures = response.data;
        
        console.log('Received report signatures:', reportSignatures);
        
        // Convert to the format expected by the component
        this.signatures = {};
        if (Array.isArray(reportSignatures)) {
          reportSignatures.forEach(sig => {
            // Get signature data - prefer image URL, fallback to base64 data
            let signatureData = null;
            if (sig.signature_details?.signature_image) {
              // If it's a relative URL, make it absolute
              signatureData = sig.signature_details.signature_image;
              if (signatureData.startsWith('/media/')) {
                signatureData = `${window.location.origin}${signatureData}`;
              }
            } else if (sig.signature_details?.signature_data) {
              // Use base64 data
              signatureData = sig.signature_details.signature_data;
              if (!signatureData.startsWith('data:image/')) {
                signatureData = `data:image/png;base64,${signatureData}`;
              }
            }
            
            if (signatureData) {
              this.signatures[sig.signatory_name] = {
                data: signatureData,
                mode: sig.signature_details?.signature_type?.toLowerCase() || 'draw',
                timestamp: sig.signed_at
              };
            }
          });
        }
        
        console.log('Loaded signatures for report:', this.reportDate, this.signatures);
      } catch (error) {
        // Silently handle authentication/permission errors
        if (error.response?.status === 403 || error.response?.status === 401) {
          console.log('Report signatures not accessible - user may not have permission');
          this.signatures = {};
          return;
        }
        
        console.error('Error loading report signatures:', error);
        // Don't show error toast for missing signatures - it's normal for new reports
        if (error.response?.status !== 404) {
          console.warn('Unexpected error loading signatures:', error.message);
        }
        this.signatures = {};
      }
    },

    saveSignatureToLibrary() {
      if (!this.uploadedSignature) return;
      
      const newSignature = {
        data: this.uploadedSignature,
        name: `Signature ${this.savedSignatures.length + 1}`,
        timestamp: new Date().toISOString()
      };
      
      this.savedSignatures.push(newSignature);
      
      try {
        localStorage.setItem('userSignatureLibrary', JSON.stringify(this.savedSignatures));
        toast.success('Signature saved to your library');
      } catch (error) {
        console.error('Error saving signature to library:', error);
        toast.error('Failed to save signature to library');
      }
    },

    selectSavedSignature(signature) {
      this.selectedSavedSignature = signature;
      this.uploadedSignature = null; // Clear uploaded signature when selecting saved one
    },

    deleteSavedSignature(index) {
      if (confirm('Are you sure you want to delete this signature?')) {
        this.savedSignatures.splice(index, 1);
        
        try {
          localStorage.setItem('userSignatureLibrary', JSON.stringify(this.savedSignatures));
          toast.success('Signature deleted from library');
          
          // Clear selection if deleted signature was selected
          if (this.selectedSavedSignature && this.savedSignatures.indexOf(this.selectedSavedSignature) === -1) {
            this.selectedSavedSignature = null;
          }
        } catch (error) {
          console.error('Error deleting signature:', error);
          toast.error('Failed to delete signature');
        }
      }
    },
  },
};
</script>
<style scoped>
/* Variables */
:root {
  --primary-color: #003d82;
  --primary-light: #0056b3;
  --primary-dark: #002a5c;
  --success-color: #10b981;
  --success-light: #34d399;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --border-color: #e5e7eb;
  --border-light: #f3f4f6;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
}

/* Main Container */
.generate-report-page {
  width: 100%;
  margin: 0;
  padding: 1rem;
  box-sizing: border-box;
  overflow-x: hidden;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* Header */
.page-header {
  margin-bottom: 3rem;
  text-align: center;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.title-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.025em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title-icon {
  font-size: 2.25rem;
  color: var(--primary-color);
  filter: drop-shadow(0 2px 4px rgba(0, 61, 130, 0.2));
}

.page-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
  line-height: 1.6;
}
.header-info {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.info-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-lg);
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--shadow-md);
}

.info-badge.success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  color: var(--success-color);
  border-color: rgba(16, 185, 129, 0.2);
}

.info-badge.primary {
  background: linear-gradient(135deg, rgba(0, 61, 130, 0.1) 0%, rgba(0, 61, 130, 0.05) 100%);
  color: var(--primary-color);
  border-color: rgba(0, 61, 130, 0.2);
}

.info-badge:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.info-badge i {
  font-size: 1rem;
}

/* Main Card */
.main-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  margin-bottom: 2rem;
  border: 1px solid var(--border-light);
  backdrop-filter: blur(20px);
  width: 100%;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

/* When preview is shown, make main card smaller */
.generate-report-page:has(.preview-card) .main-card {
  max-width: 600px;
}

.card-header {
  padding: 2rem 2rem 1rem 2rem;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-bottom: 1px solid var(--border-light);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #000000 !important;
  margin: 0 0 0.5rem 0;
}

.card-title span {
  color: #000000 !important;
}

.card-title i {
  color: #000000 !important;
}

.card-title i {
  color: var(--primary-color);
  font-size: 1.375rem;
}

.card-subtitle {
  font-size: 0.9375rem;
  color: var(--text-secondary);
  margin: 0;
}

.card-body {
  padding: 2rem;
}

/* Preview card body with horizontal scroll */
.preview-card .card-body {
  padding: 2rem;
  overflow-x: scroll !important; /* Force scrollbar to always show */
  overflow-y: auto !important; /* Allow vertical scrolling inside the card */
  height: calc(100vh - 220px); /* Lock height exactly so horizontal scrollbar cannot vanish vertically */
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* Modern Preview Card */
.modern-preview {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 2rem 0;
  border: 1px solid #e5e7eb;
}

.preview-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.preview-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.preview-title-content h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.preview-subtitle {
  margin: 0.25rem 0 0 0;
  opacity: 0.9;
  font-size: 0.9rem;
}

.preview-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.action-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.5rem;
}

.btn-zoom {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-zoom:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}

.btn-zoom:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.zoom-indicator {
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  min-width: 45px;
  text-align: center;
}

.btn-action {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.btn-action.primary {
  background: #10b981;
  border-color: #10b981;
}

.btn-action.success {
  background: #22c55e;
  border-color: #22c55e;
}

.btn-action.secondary {
  background: rgba(255, 255, 255, 0.1);
}

.btn-action.close {
  background: #ef4444;
  border-color: #ef4444;
}

.btn-action:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.preview-body {
  background: #f8fafc;
  min-height: 600px;
  position: relative;
  overflow: auto;
}

.preview-body.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  background: #f8fafc;
}

.preview-toolbar {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.page-indicator {
  color: #6b7280;
  font-size: 0.9rem;
}

.view-options {
  display: flex;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 0.25rem;
}

.view-btn {
  background: transparent;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.9rem;
}

.view-btn.active {
  background: white;
  color: #374151;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-export {
  background: #f59e0b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.btn-export:hover {
  background: #d97706;
}

.preview-content-container {
  padding: 2rem;
  display: flex;
  justify-content: flex-start;
  transform-origin: top center;
  transition: transform 0.2s ease;
  overflow-x: auto;
  overflow-y: visible;
}

/* User-Friendly Horizontal Scrollbar Styles */
.user-friendly-scrollbar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: none; /* Hidden by default */
}

.scrollbar-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 12px 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(12px);
  min-width: 600px;
  max-width: 90vw;
}

/* Navigation Arrows */
.scroll-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.scroll-arrow:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.scroll-arrow:active:not(:disabled) {
  transform: translateY(0);
}

.scroll-arrow:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

/* Scrollbar Track Container */
.scrollbar-track-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.scrollbar-track {
  position: relative;
  height: 24px;
  background: #f1f5f9;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

/* Progress Indicator */
.scrollbar-progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #dbeafe, #bfdbfe);
  border-radius: 12px;
  transition: width 0.3s ease;
}

/* Enhanced Thumb */
.scrollbar-thumb {
  position: absolute;
  top: 2px;
  left: 0; /* Ensure it starts at 0 */
  height: calc(100% - 4px);
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 10px;
  cursor: grab;
  transition: all 0.2s ease;
  min-width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  z-index: 10; /* Ensure it's above other elements */
}

.scrollbar-thumb:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: scaleY(1.1);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
}

.scrollbar-thumb:active {
  cursor: grabbing;
  background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
}

/* Thumb Grip */
.thumb-grip {
  width: 16px;
  height: 4px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 2px;
  position: relative;
}

.thumb-grip::before,
.thumb-grip::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 2px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1px;
}

.thumb-grip::before {
  top: -3px;
}

.thumb-grip::after {
  bottom: -3px;
}

/* Position Indicator */
.position-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 11px;
  color: #64748b;
}

.current-position {
  font-weight: 600;
  color: #3b82f6;
  min-width: 32px;
  text-align: center;
}

.position-text {
  font-size: 10px;
}

/* Quick Navigation */
.quick-nav {
  display: flex;
  gap: 6px;
}

.quick-nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
}

.quick-nav-btn:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-1px);
}

.quick-nav-btn:active {
  transform: translateY(0);
}

/* Show scrollbar only when preview is visible */
.preview-card.modern-preview .user-friendly-scrollbar {
  display: block;
}

/* Responsive Design */
@media (max-width: 768px) {
  .scrollbar-wrapper {
    min-width: 400px;
    padding: 8px 12px;
    gap: 8px;
  }
  
  .scroll-arrow {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
  
  .quick-nav-btn {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }
  
  .position-indicator {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .scrollbar-wrapper {
    min-width: 300px;
  }
  
  .quick-nav {
    display: none; /* Hide quick nav on very small screens */
  }
}

/* Animation for smooth appearance */
.user-friendly-scrollbar {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Hide native scrollbar on the preview container */
.preview-content-container::-webkit-scrollbar {
  height: 8px;
}

.preview-content-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.preview-content-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.preview-content-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.excel-document {
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  min-width: 1200px;
  width: max-content;
  overflow: visible;
}

.excel-document.print-mode {
  box-shadow: 0 0 0 1px #e5e7eb;
  border-radius: 0;
}

.document-shadow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.02) 100%);
  pointer-events: none;
  z-index: 1;
}

/* Legacy preview card - updated for modern design */
.preview-card:not(.modern-preview) {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin: 2rem 0;
  overflow: hidden;
}

/* Enhanced content wrapper */
.preview-content-wrapper {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  background: white;
  width: max-content;
  min-width: 100%;
}

/* Main content (left side) */
.main-content-left {
  flex: 0 0 auto; 
  min-width: 1600px; /* Match the 1600px min-widths inside it */
}

/* Right side content */
.right-side-content {
  flex: 0 0 auto;
  min-width: 800px; /* Keep a decent width for the right side */
}

/* Gate Operations Table */
.gate-operations-table {
  background: white;
  border: 2px solid #000;
  margin-bottom: 1rem;
}

/* Gate Chart Section */
.gate-chart-section {
  width: 100%;
  background: white;
  border: 2px solid #000;
  padding: 0;
  margin-bottom: 2rem;
  box-sizing: border-box;
}

.gate-chart-section .chart-container {
  width: 100%;
  height: 300px;
  position: relative;
  overflow: hidden;
  padding: 10px;
  box-sizing: border-box;
}

.gate-chart-section .chart-wrapper {
  width: 100% !important;
  height: 100% !important;
  position: relative;
  display: block;
  min-width: 100%;
}

.gate-chart-section .chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  min-width: 100% !important;
}

/* Workflow Diagram Section */
.workflow-diagram-section {
  width: 100%;
  background: white;
  border: 2px solid #000;
  padding: 15px;
  margin-bottom: 2rem;
  font-family: Arial, sans-serif;
}

.workflow-header {
  margin-bottom: 15px;
}

.workflow-input-label {
  font-size: 12px;
  font-weight: bold;
  color: #000;
}

.workflow-steps {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  overflow-x: auto;
  padding: 10px 0;
}

.workflow-step {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.workflow-box {
  background: #5B9BD5;
  color: black;
  padding: 12px 15px;
  border-radius: 8px;
  width: 180px;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 10px;
  line-height: 1.3;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.workflow-arrow {
  color: #5B9BD5;
  font-size: 20px;
  font-weight: bold;
  margin: 0 10px;
  flex-shrink: 0;
}

.step-text {
  word-wrap: break-word;
  hyphens: auto;
}

.workflow-input-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.input-label {
  font-weight: bold;
  font-size: 12px;
  color: #000;
}

.input-box {
  border: 2px solid #000;
  padding: 8px 12px;
  background: white;
  font-size: 11px;
}

.input-text {
  color: #000;
}

.input-value {
  font-weight: bold;
  color: #000;
}

/* Data Tables Section */
.data-tables-section {
  width: 100%;
  background: white;
  border: 2px solid #000;
  padding: 15px;
  margin-bottom: 2rem;
  font-family: Arial, sans-serif;
}

.tables-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.data-table-container {
  flex: 1;
}

.table-header {
  font-weight: bold;
  font-size: 12px;
  margin-bottom: 5px;
  color: #000;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10px;
  border: 1px solid #000;
}

.data-table th,
.data-table td {
  border: 1px solid #000;
  padding: 3px 5px;
  text-align: left;
}

.data-table th {
  background: #FFFF00;
  font-weight: bold;
}

.data-table.small {
  font-size: 9px;
}

.left-bottom-tables {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.right-bottom-tables {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.small-table-container {
  margin-bottom: 10px;
}

.plant-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 10px 0;
}

.plant-item {
  background: #FFFF00;
  padding: 2px 5px;
  border: 1px solid #000;
  font-size: 10px;
  text-align: center;
}

.plant-number {
  background: #FFFF00;
  padding: 2px 5px;
  border: 1px solid #000;
  font-size: 10px;
  text-align: center;
  font-weight: bold;
}

.table-number {
  background: #FFFF00;
  padding: 2px 5px;
  border: 1px solid #000;
  font-size: 10px;
  text-align: center;
  font-weight: bold;
  margin-top: 5px;
}

/* Additional Chart Section */
.additional-chart-section {
  width: 100%;
  background: white;
  border: 2px solid #000;
  padding: 15px;
  margin-bottom: 2rem;
  font-family: Arial, sans-serif;
}

.chart-note {
  font-size: 11px;
  color: #000;
  margin-bottom: 15px;
  line-height: 1.4;
  text-align: justify;
}

.additional-chart-container {
  width: 100%;
  height: 300px;
  position: relative;
  border: 1px solid #ccc;
  background: white;
  padding: 0;
  box-sizing: border-box;
}

.additional-chart-container .chart-wrapper {
  width: 100% !important;
  height: 100% !important;
  position: relative;
  display: block;
  min-width: 100%;
}

.additional-chart-container .chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  min-width: 100% !important;
}

.gate-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Calibri', Arial, sans-serif;
}

.gate-th {
  background: #D9D9D9;
  border: 1px solid #000;
  padding: 8px 4px;
  text-align: center;
  font-weight: bold;
  font-size: 14px; /* Increased from 12px */
  color: #000;
}

.elevation-header {
  background: #FFFF00 !important;
  color: #000;
}

.gate-data-row {
  border-bottom: 1px solid #000;
}

.gate-cell {
  border: 1px solid #000;
  padding: 6px 4px;
  text-align: center;
  font-size: 13px; /* Increased from 11px */
  color: #000;
  background: white;
}

.elevation-value {
  background: #FFFF00 !important;
  font-weight: bold;
}

.gate-note-row {
  border-bottom: 1px solid #000;
}

.gate-note-cell {
  border: 1px solid #000;
  padding: 4px 8px;
  font-size: 12px; /* Increased from 10px */
  text-align: left;
  color: #000;
  background: white;
}

/* Bottom Forecast Section */
.forecast-bottom {
  background: #FFFF00;
  padding: 8px;
  border-top: 2px solid #000;
  text-align: center;
}

.forecast-row-bottom {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 14px; /* Increased from 12px */
  font-weight: bold;
}

.forecast-label-bottom {
  color: #000;
}

.forecast-error-bottom {
  color: #FF0000;
  font-weight: bold;
}

/* Add scrollbar styling for better UX - mimicking Excel scrollbar */
.preview-card .card-body::-webkit-scrollbar {
  height: 24px !important;
  display: block !important;
}

.preview-card .card-body::-webkit-scrollbar-track {
  background: #E8EBF0 !important;
  border-top: 1px solid #99aabf;
  border-bottom: 1px solid #99aabf;
}

.preview-card .card-body::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #9ca3af, #6b7280) !important;
  border: 2px solid #E8EBF0 !important;
  border-radius: 6px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.4);
}

.preview-card .card-body::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #6b7280, #4b5563) !important;
}

/* For Firefox */
.preview-card .card-body {
  scrollbar-width: auto;
  scrollbar-color: #6b7280 #E8EBF0;
}
/* Form */
.report-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field-label i {
  color: var(--primary-color);
  font-size: 1rem;
}

/* Date Input */
.date-input-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
}

.date-input {
  width: 100%;
  padding: 1rem 1.25rem;
  font-size: 1rem;
  color: #000000 !important;
  background: #ffffff !important;
  border: 2px solid #d1d5db !important;
  border-radius: var(--radius-lg);
  transition: all 0.3s ease;
  outline: none;
  font-family: inherit;
  font-weight: 500;
}

.date-input:hover {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.date-input:focus {
  border-color: #2563eb !important;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
  transform: translateY(-1px);
}

.date-input.has-value {
  border-color: #10b981 !important;
  background: #ffffff !important;
  color: #000000 !important;
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-light) 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}

.date-input:focus + .input-border {
  transform: scaleX(1);
}
.field-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--text-muted);
  font-style: italic;
}

.field-hint i {
  color: var(--primary-color);
  font-size: 0.875rem;
}

/* Button Section */
.button-section {
  display: flex !important;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
  visibility: visible !important;
  margin: 2rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(248, 250, 252, 0.8) 0%, rgba(241, 245, 249, 0.6) 100%);
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  backdrop-filter: blur(10px);
}

.btn-generate {
  position: relative;
  display: flex !important;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 450px;
  padding: 1.25rem 2.5rem;
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
  color: #1f2937 !important;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
  visibility: visible !important;
  opacity: 1 !important;
  text-transform: none;
  letter-spacing: 0.025em;
  backdrop-filter: blur(10px);
}

.btn-generate::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transition: left 0.5s;
}

.btn-generate:hover::before {
  left: 100%;
}

.btn-generate-prominent {
  animation: none;
  border: 2px solid #3b82f6;
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
}

.btn-generate-prominent:hover:not(:disabled) {
  border-color: #2563eb;
  box-shadow: 
    0 10px 15px -3px rgba(59, 130, 246, 0.2),
    0 4px 6px -2px rgba(59, 130, 246, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  border-color: #3b82f6;
  background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
}

.btn-generate:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
}

.btn-generate:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed;
  transform: none;
  display: flex !important;
  visibility: visible !important;
  animation: none;
  background: linear-gradient(145deg, #f3f4f6 0%, #e5e7eb 100%);
  border-color: #d1d5db;
  color: #9ca3af !important;
  box-shadow: 
    0 1px 2px 0 rgba(0, 0, 0, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
}

.btn-generate.generating {
  background: linear-gradient(135deg, var(--text-secondary) 0%, var(--text-muted) 100%);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 2;
  position: relative;
}

.btn-icon {
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  color: #3b82f6 !important;
  transition: color 0.3s ease;
}

.btn-text {
  font-weight: 600;
  letter-spacing: 0.025em;
  font-size: 1.1rem;
  color: #1f2937 !important;
  transition: color 0.3s ease;
}
.btn-ripple {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  transform: scale(0);
  transition: transform 0.6s ease;
  z-index: 1;
}

.btn-generate:active .btn-ripple {
  transform: scale(1);
}

.validation-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
  color: var(--warning-color);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
}

.validation-message i {
  font-size: 1rem;
}

/* History Card */
.history-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.history-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
}

.menu-wrapper {
  position: relative;
}

.btn-menu {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-menu:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border-color: var(--primary-color);
}
.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 180px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  z-index: 1000;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.menu-item:hover {
  background: var(--bg-secondary);
}

.menu-item-danger {
  color: var(--danger-color);
}

.menu-item-danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

/* History List */
.history-list {
  display: flex;
  flex-direction: column;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border-light);
  transition: all 0.2s ease;
  cursor: pointer;
  color: #000000 !important;
}

.history-item * {
  color: #000000 !important;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background: var(--bg-secondary);
  transform: translateX(4px);
}
.history-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--success-color) 0%, var(--success-light) 100%);
  border-radius: var(--radius-lg);
  flex-shrink: 0;
  box-shadow: var(--shadow-md);
}

.history-icon i {
  font-size: 1.5rem;
  color: white;
}

.history-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #000000 !important;
}

.history-details * {
  color: #000000 !important;
}

.history-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  color: #000000 !important;
}

.history-main * {
  color: #000000 !important;
}

.history-filename {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #000000 !important;
}

.history-plant-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: #000000 !important;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.025em;
}

.history-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.8125rem;
  color: #000000 !important;
}

.history-meta * {
  color: #000000 !important;
}

.history-meta > span {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: #000000 !important;
}

.history-type {
  font-weight: 500;
  color: #000000 !important;
}

.history-exact-time {
  color: #000000 !important;
  background: #f5f5f5 !important;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  border: 1px solid #d0d0d0 !important;
}
.history-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-download,
.btn-regenerate {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: 1px solid;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-download {
  color: var(--success-color);
  border-color: var(--success-color);
}

.btn-download:hover {
  background: var(--success-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-regenerate {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-regenerate:hover {
  background: var(--primary-color);
  color: white;
  transform: rotate(180deg);
}

/* Responsive Design */
@media (max-width: 768px) {
  .generate-report-page {
    padding: 1rem 0.5rem;
  }
  
  .page-title {
    font-size: 2rem;
    flex-direction: column;
    text-align: center;
  }
  
  .header-info {
    flex-direction: column;
    width: 100%;
  }
  
  .info-badge {
    justify-content: center;
  }
  
  .card-header,
  .card-body {
    padding: 1.5rem 1rem;
  }
  
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .history-details {
    width: 100%;
  }
  
  .history-actions {
    align-self: flex-end;
  }
  
  .btn-generate {
    font-size: 1rem;
    padding: 1rem 1.5rem;
  }
}
@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  
  .card-title {
    font-size: 1.25rem;
  }
  
  .history-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

/* Animation Classes */
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

.main-card,
.history-card,
.preview-card {
  animation: fadeInUp 0.6s ease-out;
}

.history-card {
  animation-delay: 0.2s;
}

.preview-card {
  animation-delay: 0.3s;
}

/* Preview Card Styles */
.preview-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  border: 1px solid var(--border-light);
  margin-bottom: 2rem;
  width: 100%;
}

.preview-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-download-excel {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #10b981 !important;
  color: #ffffff !important;
  border: 2px solid #10b981 !important;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 600 !important;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2) !important;
}

.btn-download-excel:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3) !important;
  background: #059669 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
}

.btn-download-excel i {
  color: #ffffff !important;
  font-size: 1rem !important;
}

.btn-download-excel span {
  color: #ffffff !important;
  font-weight: 600 !important;
}

.btn-close-preview {
  display: flex !important;
  align-items: center;
  justify-content: center;
  width: 44px !important;
  height: 44px !important;
  background: #ffffff !important;
  color: #000000 !important;
  border: 3px solid #000000 !important;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.4rem !important;
  font-weight: 900 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 1000 !important;
}

.btn-close-preview:hover {
  background: #f8f8f8 !important;
  color: #000000 !important;
  border-color: #000000 !important;
  transform: scale(1.15) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
}

.btn-close-preview:active {
  transform: scale(1.05) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
}

/* Excel-like Header with Logo and Officials */
.excel-header-with-logo {
  margin-bottom: 2rem;
  background: white;
  border: 2px solid #000;
  border-radius: 4px;
  padding: 1.5rem;
  min-width: 1600px; /* Increased minimum width for horizontal scroll */
}

.logo-title-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.logo-container {
  flex-shrink: 0;
}

.npc-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.title-container {
  text-align: center;
}

.main-title {
  font-size: 2rem;
  font-weight: bold;
  color: #000;
  margin: 0;
  line-height: 1.2;
}

.subtitle-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #000;
  margin: 0.25rem 0 0 0;
  line-height: 1.2;
}

.officials-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
}

.official-box {
  flex: 1;
  text-align: center;
  padding: 0.5rem;
}

.official-label {
  font-size: 1rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 0.5rem;
}

.official-name {
  font-size: 1rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.official-position {
  font-size: 0.9rem;
  color: #000;
  line-height: 1.3;
}

.psr-banner {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  padding: 1rem;
  text-align: center;
  border-radius: 4px;
  margin-top: 1rem;
}

.psr-title {
  font-size: 1.5rem;
  font-weight: bold;
  font-style: italic;
  letter-spacing: 1px;
  margin-bottom: 0.25rem;
}

.psr-date {
  font-size: 1.1rem;
  font-weight: normal;
}

/* Old Excel Header (keeping for backward compatibility) */
.excel-header {
  margin-bottom: 2rem;
  text-align: center;
  background: #2F4F4F;
  color: white;
  padding: 1rem;
  border-radius: var(--radius-lg);
}

.header-row {
  margin-bottom: 0.5rem;
}

.header-row:last-child {
  margin-bottom: 0;
}

.title-cell {
  font-size: 1.8rem;
  font-weight: bold;
}

.subtitle-cell {
  font-size: 1.5rem;
  font-weight: bold;
}

.portfolio-cell {
  font-size: 1.2rem;
  font-weight: bold;
}

.date-cell {
  font-size: 1.1rem;
  font-weight: normal;
}

/* Excel-like Table */
.excel-table-container {
  overflow-x: auto;
  border: 2px solid #000;
  border-radius: 4px;
  margin-bottom: 2rem;
  width: 100%;
}

.excel-table {
  width: 100%;
  min-width: 1600px; /* Increased minimum width for better horizontal scroll */
  border-collapse: collapse;
  font-family: 'Calibri', Arial, sans-serif;
  font-size: 16px;
  background: white;
}

.excel-th {
  background: #D9D9D9;
  border: 1px solid #000;
  padding: 10px 6px;
  text-align: center;
  font-weight: bold;
  font-size: 15px;
  vertical-align: middle;
  color: #000;
}

.excel-th.plant-col {
  width: 200px;
  min-width: 200px;
}

.excel-th.capacity-col,
.excel-th.nominated-col,
.excel-th.actual-col,
.excel-th.variance-col {
  width: 120px;
  min-width: 120px;
}

.excel-th.remarks-col {
  width: 400px;
  min-width: 400px;
}

.excel-td {
  border: 1px solid #000;
  padding: 6px 8px;
  font-size: 15px;
  color: #000;
  vertical-align: middle;
}

.plant-header-row {
  background: #E6E6E6;
}

.plant-name-cell {
  font-weight: bold;
  text-align: center;
  background: #E6E6E6;
}

.plant-name-italic {
  font-style: italic;
  font-weight: bold;
  text-align: left;
  vertical-align: top;
  padding: 8px 12px;
  background: white;
  border: 1px solid #000;
}

.plant-name-row {
  background: white;
}

.plant-name-row .excel-td {
  font-weight: bold;
}

.unit-cell {
  padding-left: 20px;
  text-align: left;
}

.unit-label {
  padding-left: 30px;
  text-align: left;
  font-style: normal;
  font-weight: normal;
  color: #000;
}

.red-text {
  color: #FF0000 !important;
}

.number-cell {
  text-align: center;
}

.number-cell.negative {
  color: #FF0000;
}

.total-agus-row {
  background: #F2F2F2;
  font-weight: bold;
  border-top: 1px solid #000;
}

.total-agus-row .excel-td {
  font-weight: bold;
}plant-total-row {
  background: #F2F2F2;
  font-weight: bold;
}

.total-agus-row {
  background: #F2F2F2;
  font-weight: bold;
  border-top: 1px solid #000;
}

.total-agus-row .excel-td {
  font-weight: bold;
}

.total-label-cell {
  font-weight: bold;
  text-align: left;
  padding-left: 10px;
}

.total-number-cell {
  text-align: center;
  font-weight: bold;
}

.grand-total-row {
  background: #D9D9D9;
  font-weight: bold;
  border-top: 2px solid #000;
}

.grand-total-label {
  font-weight: bold;
  text-align: left;
  padding-left: 10px;
}

.grand-total-number {
  text-align: center;
  font-weight: bold;
}

/* Forecasted Load Row (Yellow Background) */
.forecasted-load-row {
  background: #FFFF00 !important;
  font-weight: bold;
}

.forecasted-load-cell {
  text-align: center;
  font-weight: bold;
  padding: 10px !important;
  font-size: 15px;
  color: #000;
  background: #FFFF00 !important;
}

/* IPP Rows */
.ipp-row {
  background: white;
}

/* Total IPP Row */
.total-ipp-row {
  background: #E6E6E6;
  font-weight: bold;
}

/* Total NPC-PSALM Row (Blue Background) */
.total-npc-psalm-row {
  background: #B4C7E7 !important;
  font-weight: bold;
  border-top: 2px solid #000;
  border-bottom: 2px solid #000;
}

.total-npc-label {
  font-weight: bold;
  text-align: left;
  padding-left: 10px;
  background: #B4C7E7 !important;
}

.total-npc-number {
  text-align: center;
  font-weight: bold;
  background: #B4C7E7 !important;
}

.remarks-cell {
  text-align: left;
  max-width: 150px;
  word-wrap: break-word;
}

/* Excel Sections */
.excel-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  background: #FAFAFA;
  width: 100%;
  min-width: 1600px; /* Increased minimum width to ensure horizontal scroll */
}

.section-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #000;
  text-align: center;
  background: #D9D9D9;
  padding: 0.75rem;
  border: 1px solid #000;
  border-radius: 4px;
}

/* Charts Section */
.charts-section {
  background: white;
  border: 2px solid #000;
  padding: 1.5rem;
  min-width: 1600px; /* Increased minimum width for horizontal scroll */
}

.charts-container {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  align-items: flex-start;
}

.chart-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.chart-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: white;
  background: #2F4F4F;
  padding: 0.5rem 1rem;
  margin-bottom: 1rem;
  text-align: center;
  width: 100%;
  border-radius: 4px;
}

.chart-wrapper {
  width: 100%;
  max-width: 400px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-legend {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
  padding: 0.75rem;
  background: #FFF2CC;
  border: 1px solid #000;
  border-radius: 4px;
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: bold;
}

.legend-color {
  width: 20px;
  height: 20px;
  border: 1px solid #000;
  display: inline-block;
}

.small-table {
  width: 100%;
  max-width: none;
  margin: 0;
}

.label-cell {
  text-align: left;
  font-weight: normal;
  padding-left: 10px;
}

.ipp-row:nth-child(even) {
  background: #F9F9F9;
}

.notes-section {
  background: white;
  border: 2px solid #000;
  padding: 1.5rem;
}

.notes-header {
  font-size: 1.1rem;
  font-weight: bold;
  font-style: italic;
  color: #000;
  margin-bottom: 0.75rem;
}

.notes-list {
  list-style-type: decimal;
  padding-left: 2rem;
  margin: 0;
}

.notes-list li {
  margin-bottom: 0.5rem;
  color: #000;
  line-height: 1.5;
}

/* Additional Notes Section (same styling as notes) */
.additional-notes-section {
  background: white;
  border: 2px solid #000;
  padding: 1.5rem;
}

/* Signature Sections */
.signatures-section {
  background: white;
  border: 2px solid #000;
}

.signature-row {
  margin-bottom: 2rem;
}

.signature-row:last-child {
  margin-bottom: 0;
}

.signature-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Calibri', Arial, sans-serif;
}

.signature-header {
  background: #F2F2F2;
  border: 1px solid #000;
  padding: 10px;
  text-align: left;
  font-size: 14px;
  font-weight: normal;
  color: #000;
  width: 25%;
}

.signature-cell {
  border: 1px solid #000;
  padding: 8px;
  height: 20px;
  background: white;
}

.signature-space {
  height: 20px;
}

.signature-name {
  border: 1px solid #000;
  padding: 10px 12px; /* Increased padding */
  font-size: 16px; /* Increased font size */
  font-weight: bold;
  color: #000;
  text-align: left;
  min-height: 85px; /* Added minimum height for better spacing */
}

.signature-title {
  border: 1px solid #000;
  padding: 6px 10px;
  font-size: 14px;
  font-weight: normal;
  color: #000;
  text-align: left;
}

/* Footer Note */
.footer-note-section {
  background: white;
  border: 1px solid #ccc;
  margin-top: 2rem;
}

.footer-note {
  font-size: 14px;
  color: #000;
  line-height: 1.4;
  margin: 0;
  padding: 1rem;
  font-style: italic;
}

/* E-Signature Styles */
.signature-name-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.7rem; /* Increased gap for better spacing */
  padding: 4px 0; /* Added padding */
}

.signature-buttons-group {
  display: flex;
  gap: 0.5rem; /* Increased gap between buttons */
  align-items: center;
  justify-content: center; /* Center the buttons */
}

.name-text {
  font-size: 16px; /* Increased from 13px */
  font-weight: bold;
  color: #000;
  margin-bottom: 8px; /* Added margin for better spacing */
}

.btn-e-signature {
  display: flex;
  align-items: center;
  gap: 0.4rem; /* Increased gap */
  padding: 0.5rem 0.8rem; /* Increased padding */
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px; /* Slightly larger border radius */
  font-size: 12px; /* Increased font size */
  font-weight: 500; /* Added font weight */
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 32px; /* Added minimum height */
}

.btn-e-signature:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.btn-e-signature.has-signature {
  background: #10b981;
}

.btn-e-signature.has-signature:hover {
  background: #059669;
}

.btn-e-signature i {
  font-size: 12px; /* Increased from 10px */
}

.btn-request-access-mini {
  display: flex;
  align-items: center;
  gap: 0.4rem; /* Increased gap */
  padding: 0.5rem 0.7rem; /* Increased padding */
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 6px; /* Increased border radius */
  font-size: 11px; /* Increased font size */
  font-weight: 500; /* Added font weight */
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  min-height: 32px; /* Added minimum height to match e-signature button */
}

.btn-request-access-mini:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

.btn-request-access-mini i {
  font-size: 11px; /* Increased from 9px */
}

/* Request Signature Access Button - Inline Position */
.request-access-button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 0;
  margin: 0.5rem 0;
}

.btn-request-signature-access-inline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.25);
}

.btn-request-signature-access-inline:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.35);
}

.btn-request-signature-access-inline:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.25);
}

.btn-request-signature-access-inline i {
  font-size: 1.125rem;
}

/* Signature Display Styles */
.signature-display {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 2px;
}

.signature-image {
  max-width: 100%;
  max-height: 50px;
  object-fit: contain;
  border: none;
  background: transparent;
}

.signature-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Signature cell adjustments */
.signature-cell {
  border: 1px solid #000;
  padding: 6px 8px;
  font-size: 13px;
  color: #000;
  vertical-align: middle;
  position: relative;
  height: 60px;
  min-height: 60px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
}

.e-signature-modal {
  width: 600px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.btn-close-modal {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close-modal:hover {
  background: #e5e7eb;
  color: #374151;
}

.modal-body {
  padding: 2rem;
}

.option-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.tab-btn:hover {
  color: #374151;
  background: #f3f4f6;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: #eff6ff;
}

/* Canvas Styles */
.signature-draw-area {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.canvas-container {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.signature-canvas {
  display: block;
  cursor: crosshair;
  background: white;
}

.canvas-controls {
  display: flex;
  justify-content: center;
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
  transition: all 0.2s ease;
}

.btn-clear:hover {
  background: #dc2626;
}

/* NEW: Right-side sections styles */
.right-side-sections {
  background: white;
  border: 2px solid #000;
  padding: 1rem;
}

.right-side-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  width: 100%;
}

.right-section {
  background: #FAFAFA;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.right-section .section-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
  color: #000;
  text-align: center;
  background: #2F5496;
  color: white;
  padding: 0.5rem;
  border: 1px solid #000;
  border-radius: 4px;
}

.right-section .small-table {
  font-size: 11px;
  min-width: auto;
}

.right-section .excel-th {
  background: #FFFF00;
  font-size: 10px;
  padding: 6px 4px;
  font-weight: bold;
  color: #000;
}

.right-section .excel-td {
  font-size: 10px;
  padding: 4px 6px;
  text-align: center;
}

.storage-section .excel-td:first-child,
.inflow-section .excel-td:first-child,
.generation-data-section .excel-td:first-child,
.capacity-factor-section .excel-td:first-child,
.gate-elevation-section .excel-td:first-child {
  text-align: left;
  padding-left: 8px;
}

.total-row .excel-td,
.average-row .excel-td {
  background: #D9D9D9;
  font-weight: bold;
}

.gate-elevation-section .excel-table {
  font-size: 9px;
}

.gate-elevation-section .excel-th,
.gate-elevation-section .excel-td {
  font-size: 8px;
  padding: 3px 2px;
}

.sub-section {
  margin-bottom: 1rem;
}

.sub-section-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #000;
  text-align: center;
  background: #B4C7E7;
  padding: 0.4rem;
  border: 1px solid #000;
  border-radius: 4px;
}

.workflow-boxes {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.workflow-box {
  background: #FFFF00;
  border: 2px solid #000;
  padding: 0.75rem;
  text-align: center;
  font-weight: bold;
  font-size: 0.9rem;
  border-radius: 4px;
}

.workflow-notes {
  margin-top: 1rem;
}

.workflow-note {
  font-size: 0.8rem;
  color: #000;
  margin-bottom: 0.25rem;
  font-style: italic;
}

/* Responsive adjustments for right-side sections */
@media (max-width: 1200px) {
  .right-side-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

/* Upload Styles */
.signature-upload-area {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.saved-signatures-section {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.section-subtitle {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
}

.saved-signatures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
}

.saved-signature-item {
  position: relative;
  padding: 0.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.saved-signature-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

.saved-signature-item.selected {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.saved-signature-item img {
  width: 100%;
  height: 60px;
  object-fit: contain;
  border-radius: 4px;
}

.signature-actions {
  position: absolute;
  top: 4px;
  right: 4px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.saved-signature-item:hover .signature-actions {
  opacity: 1;
}

.btn-delete-signature {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 10px;
  transition: all 0.2s ease;
}

.btn-delete-signature:hover {
  background: #dc2626;
}

.upload-new-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.upload-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f9fafb;
}

.upload-zone:hover {
  border-color: #3b82f6;
  background: #eff6ff;
}

.upload-zone i {
  font-size: 3rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.upload-zone p {
  font-size: 1rem;
  font-weight: 500;
  color: #374151;
  margin: 0 0 0.5rem 0;
}

.upload-zone small {
  color: #6b7280;
}

.uploaded-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
}

.uploaded-preview img {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain;
}

.upload-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-save-to-library {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.btn-save-to-library:hover {
  background: #2563eb;
}

/* Type Signature Styles */
.signature-type-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.font-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.font-selector label {
  font-weight: 500;
  color: #374151;
}

.font-select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.signature-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.signature-text-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1.125rem;
}

.signature-preview {
  padding: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  text-align: center;
  font-size: 24px;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
}

/* Modal Footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: transparent;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #f3f4f6;
  color: #374151;
}

.btn-save {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-save:hover:not(:disabled) {
  background: #059669;
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading Animation Styles */
.loading-modal-overlay {
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
  z-index: 9999;
  animation: fadeIn 0.3s ease-out;
}

.loading-modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: var(--radius-xl);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.gears-animation {
  position: relative;
  height: 80px;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gear-icon {
  font-size: 3rem;
  color: var(--primary-color);
  position: absolute;
}

.gear-1 {
  animation: spinRight 2s linear infinite;
  transform-origin: center;
  margin-right: 35px;
  margin-bottom: 20px;
}

.gear-2 {
  font-size: 2rem;
  color: var(--secondary-color, #475569);
  animation: spinLeft 2s linear infinite;
  transform-origin: center;
  margin-left: 35px;
  margin-top: 15px;
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.loading-text {
  color: #64748b;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.progress-bar-container {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.progress-bar-animated {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 50%;
  background: linear-gradient(90deg, var(--primary-color) 0%, #3b82f6 50%, var(--primary-color) 100%);
  background-size: 200% 100%;
  border-radius: 999px;
  animation: loadingBar 1.5s ease-in-out infinite, gradientMove 2s linear infinite;
}

@keyframes spinRight {
  100% { transform: rotate(360deg); }
}

@keyframes spinLeft {
  100% { transform: rotate(-360deg); }
}

@keyframes loadingBar {
  0% { left: -50%; }
  100% { left: 100%; }
}

@keyframes gradientMove {
  0% { background-position: 100% 0; }
  100% { background-position: -100% 0; }
}

/* Preview Button Styles */
.btn-preview {
  margin-top: 1rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  min-height: 56px;
  width: 100%;
}

.btn-preview:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.btn-preview:active {
  transform: translateY(0);
}

.btn-preview .btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  position: relative;
  z-index: 2;
}

.btn-preview .btn-icon {
  font-size: 1.25rem;
}

.btn-preview .btn-ripple {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-preview:hover .btn-ripple {
  opacity: 1;
}

/* Success Modal Styles */
.success-modal-overlay {
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
  animation: fadeIn 0.3s ease;
}

.success-modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

.success-modal-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.success-icon {
  font-size: 4rem;
  color: #10b981;
  margin-bottom: 1rem;
}

.success-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.success-modal-body {
  text-align: center;
}

.success-message {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.success-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-success-preview {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-success-preview:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-success-close {
  background: #f3f4f6;
  color: #6b7280;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-success-close:hover {
  background: #e5e7eb;
  color: #374151;
}

/* Animation Keyframes */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Enhanced Generate Button Animation */
.btn-generate.generating {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  cursor: not-allowed;
}

.btn-generate.generating .btn-content {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* Loading Animation for Generate Button */
.btn-generate.generating .btn-icon i.pi-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
