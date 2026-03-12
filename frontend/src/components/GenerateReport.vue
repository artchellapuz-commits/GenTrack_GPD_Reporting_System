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
                  <i v-if="!generating" class="pi pi-eye"></i>
                  <i v-else class="pi pi-spin pi-spinner"></i>
                </div>
                <span class="btn-text">{{ generating ? 'Loading Preview...' : 'Preview Report' }}</span>
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

    <!-- Report Preview Section -->
    <div v-if="showPreview && reportPreview" class="preview-card">
      <div class="card-header">
        <div class="card-title">
          <i class="pi pi-file-excel"></i>
          <span>Excel Report Preview</span>
        </div>
        <div class="preview-actions">
          <button @click="downloadExcel" class="btn-download-excel" style="color: #ffffff !important; background: #10b981 !important; border: 2px solid #10b981 !important;">
            <i class="pi pi-download" style="color: #ffffff !important;"></i>
            <span style="color: #ffffff !important; font-weight: 600 !important;">Download Excel</span>
          </button>
          <button @click="closePreview" class="btn-close-preview" style="background: #ffffff !important; color: #000000 !important; border: 3px solid #000000 !important; display: flex !important; visibility: visible !important; opacity: 1 !important;">
            <i class="pi pi-times" style="color: #000000 !important; font-size: 1.4rem !important; font-weight: 900 !important;"></i>
          </button>
        </div>
      </div>
      
      <div class="card-body">
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
              <!-- AGUS 1 -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">AGUS 1</td>
                <td class="excel-td number-cell">80.0</td>
                <td class="excel-td number-cell">70.0</td>
                <td class="excel-td number-cell" rowspan="3">136 CMS @<br>60 HW</td>
                <td class="excel-td number-cell">60.00</td>
                <td class="excel-td remarks-cell">Lake Lanao Elevation is 701.19 m.a.s.l. (G1- 0.10 m, G2- 0.10 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">40.0</td>
                <td class="excel-td number-cell">35.0</td>
                <td class="excel-td number-cell">30.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">40.0</td>
                <td class="excel-td number-cell">35.0</td>
                <td class="excel-td number-cell">30.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- AGUS 2 -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">AGUS 2</td>
                <td class="excel-td number-cell">180.0</td>
                <td class="excel-td number-cell">165.0</td>
                <td class="excel-td number-cell" rowspan="4">123 MW</td>
                <td class="excel-td number-cell">120.00</td>
                <td class="excel-td remarks-cell">Forebay Elevation is 637.8 m.a.s.l. (G1- 0.00m, G2- 0.00 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">60.0</td>
                <td class="excel-td number-cell">55.0</td>
                <td class="excel-td number-cell">40.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">60.0</td>
                <td class="excel-td number-cell">55.0</td>
                <td class="excel-td number-cell">40.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 3</td>
                <td class="excel-td number-cell">60.0</td>
                <td class="excel-td number-cell">55.0</td>
                <td class="excel-td number-cell">40.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- AGUS 4 -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">AGUS 4</td>
                <td class="excel-td number-cell">158.1</td>
                <td class="excel-td number-cell">105.4</td>
                <td class="excel-td number-cell" rowspan="4">105 MW</td>
                <td class="excel-td number-cell">96.00</td>
                <td class="excel-td remarks-cell">Forebay Elevation is 358.8 m.a.s.l. (G1- 0.50m, G2- 0.00 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">52.7</td>
                <td class="excel-td number-cell">0.0</td>
                <td class="excel-td number-cell red-text">0.00</td>
                <td class="excel-td remarks-cell">Extended GOMP (28 Dec. 2025 - 21 Feb. 2026).</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">52.7</td>
                <td class="excel-td number-cell">52.7</td>
                <td class="excel-td number-cell">48.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 3</td>
                <td class="excel-td number-cell">52.7</td>
                <td class="excel-td number-cell">52.7</td>
                <td class="excel-td number-cell">48.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- AGUS 5 -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">AGUS 5</td>
                <td class="excel-td number-cell">55.0</td>
                <td class="excel-td number-cell">53.0</td>
                <td class="excel-td number-cell" rowspan="3">40 MW</td>
                <td class="excel-td number-cell">39.08</td>
                <td class="excel-td remarks-cell">Forebay Elevation is 243.3 m.a.s.l. (G1- 0.55m, G2- 0.00 m, G3- 0.10 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">27.5</td>
                <td class="excel-td number-cell">25.50</td>
                <td class="excel-td number-cell">19.50</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">27.5</td>
                <td class="excel-td number-cell">27.50</td>
                <td class="excel-td number-cell">19.58</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- AGUS 6 -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">AGUS 6</td>
                <td class="excel-td number-cell">219.0</td>
                <td class="excel-td number-cell">144.8</td>
                <td class="excel-td number-cell" rowspan="6">184 MW</td>
                <td class="excel-td number-cell">144.80</td>
                <td class="excel-td remarks-cell">Forebay Elevation is 199.8 m.a.s.l. (G1- 0.20m, G2- 0.20 m, G3- 0.20 m, G4- 0.00 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">34.5</td>
                <td class="excel-td number-cell">34.5</td>
                <td class="excel-td number-cell">34.50</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">34.5</td>
                <td class="excel-td number-cell">34.5</td>
                <td class="excel-td number-cell">34.50</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 3</td>
                <td class="excel-td number-cell">50.0</td>
                <td class="excel-td number-cell">0.0</td>
                <td class="excel-td number-cell red-text">0.00</td>
                <td class="excel-td remarks-cell">Extended GOMP (31 Dec. 2025- 13 Feb. 2026).</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 4</td>
                <td class="excel-td number-cell">50.0</td>
                <td class="excel-td number-cell">32.0</td>
                <td class="excel-td number-cell">32.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Limited to 32 MW due to gen. rotor pole & stator core temp./cooling issues.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 5</td>
                <td class="excel-td number-cell">50.0</td>
                <td class="excel-td number-cell">43.8</td>
                <td class="excel-td number-cell">43.80</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- AGUS 7 -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">AGUS 7</td>
                <td class="excel-td number-cell">54.0</td>
                <td class="excel-td number-cell">48.1</td>
                <td class="excel-td number-cell" rowspan="3">35 MW</td>
                <td class="excel-td number-cell">40.00</td>
                <td class="excel-td remarks-cell">Forebay Elevation is 34.1 m.a.s.l. (G1- 0.00m, G2- 0.00 m, G3- 0.00 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">27.0</td>
                <td class="excel-td number-cell">26.14</td>
                <td class="excel-td number-cell">20.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">27.0</td>
                <td class="excel-td number-cell">22.00</td>
                <td class="excel-td number-cell">20.00</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- TOTAL AGUS -->
              <tr class="total-agus-row">
                <td class="excel-td total-label-cell">TOTAL AGUS</td>
                <td class="excel-td total-number-cell">746.1</td>
                <td class="excel-td total-number-cell">586.3</td>
                <td class="excel-td total-number-cell">547 MW</td>
                <td class="excel-td total-number-cell">499.88</td>
                <td class="excel-td total-number-cell"></td>
              </tr>

              <!-- PULANGI IV -->
              <tr class="plant-name-row">
                <td class="excel-td plant-name-italic">PULANGI IV</td>
                <td class="excel-td number-cell">255.0</td>
                <td class="excel-td number-cell">225.0</td>
                <td class="excel-td number-cell" rowspan="4">100 MW</td>
                <td class="excel-td number-cell">135.61</td>
                <td class="excel-td remarks-cell">Reservoir Elevation is 285.45 m.a.s.l. (G1- 0.00m, G2- 0.00 m, G3- 0.00 m, G4- 0.00 m, G5- 0.00 m, G6- 0.00 m). Bottom Sluice Gate: (G1- 0.10m, G2- 0.00 m)</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 1</td>
                <td class="excel-td number-cell">85.0</td>
                <td class="excel-td number-cell">75.0</td>
                <td class="excel-td number-cell">57.75</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 2</td>
                <td class="excel-td number-cell">85.0</td>
                <td class="excel-td number-cell">75.0</td>
                <td class="excel-td number-cell">57.26</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>
              <tr class="unit-row">
                <td class="excel-td unit-label">unit 3</td>
                <td class="excel-td number-cell">85.0</td>
                <td class="excel-td number-cell">75.0</td>
                <td class="excel-td number-cell">20.60</td>
                <td class="excel-td remarks-cell">OPERATIONAL. Maximized with respect to ave. outflow.</td>
              </tr>

              <!-- TOTAL HYDRO -->
              <tr class="grand-total-row">
                <td class="excel-td grand-total-label">TOTAL HYDRO</td>
                <td class="excel-td grand-total-number">1,001.1</td>
                <td class="excel-td grand-total-number">811.3</td>
                <td class="excel-td grand-total-number">647 MW</td>
                <td class="excel-td grand-total-number">635.49</td>
                <td class="excel-td grand-total-number"></td>
              </tr>

              <!-- Forecasted Load Row (Yellow Background) -->
              <tr class="forecasted-load-row">
                <td colspan="6" class="excel-td forecasted-load-cell">
                  Agus-Pulangi Forecasted Load @ 6pm, {{ reportPreview.forecasted_load.date }}: Agus = {{ reportPreview.forecasted_load.agus_load }} MW & Pulangui IV = {{ reportPreview.forecasted_load.pulangi_load }} MW, Total Load: {{ reportPreview.forecasted_load.total_load }} MW
                </td>
              </tr>

              <!-- IPP Rows -->
              <tr class="ipp-row">
                <td class="excel-td">MCFPP (STEAG), unit 1</td>
                <td class="excel-td number-cell">116.0</td>
                <td class="excel-td number-cell">105.0</td>
                <td class="excel-td number-cell">105.00</td>
                <td class="excel-td number-cell">61.50</td>
                <td class="excel-td remarks-cell">Normal Operation</td>
              </tr>
              <tr class="ipp-row">
                <td class="excel-td">MCFPP (STEAG), unit 2</td>
                <td class="excel-td number-cell">116.0</td>
                <td class="excel-td number-cell">105.0</td>
                <td class="excel-td number-cell">105.00</td>
                <td class="excel-td number-cell">62.60</td>
                <td class="excel-td remarks-cell">Normal Operation</td>
              </tr>

              <!-- TOTAL IPP -->
              <tr class="total-ipp-row">
                <td class="excel-td total-label-cell">TOTAL IPP</td>
                <td class="excel-td total-number-cell">232.00</td>
                <td class="excel-td total-number-cell">210.00</td>
                <td class="excel-td total-number-cell">210.00</td>
                <td class="excel-td total-number-cell">124.10</td>
                <td class="excel-td total-number-cell"></td>
              </tr>

              <!-- TOTAL NPC-PSALM -->
              <tr class="total-npc-psalm-row">
                <td class="excel-td total-npc-label">TOTAL NPC-PSALM</td>
                <td class="excel-td total-npc-number">1,233.10</td>
                <td class="excel-td total-npc-number">1,021.3</td>
                <td class="excel-td total-npc-number">857.00</td>
                <td class="excel-td total-npc-number">759.59</td>
                <td class="excel-td total-npc-number"></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Charts Section -->
        <div class="excel-section charts-section">
          <div class="charts-container">
            <!-- NPC-PSALM Capacity Mix Pie Chart -->
            <div class="chart-box">
              <h4 class="chart-title">NPC-PSALM Capacity Mix</h4>
              <div class="chart-wrapper">
                <Pie :data="capacityMixData" :options="pieChartOptions" />
              </div>
              <div class="chart-legend">
                <span class="legend-item">
                  <span class="legend-color" style="background: #4472C4;"></span>
                  Hydro
                </span>
                <span class="legend-item">
                  <span class="legend-color" style="background: #ED7D31;"></span>
                  Coal Fired Thermal
                </span>
              </div>
            </div>

            <!-- MinGen Forecasted Load Share Bar Chart -->
            <div class="chart-box">
              <h4 class="chart-title">MinGen Forecasted Load Share (MW), @6pm Today</h4>
              <div class="chart-wrapper">
                <Bar :data="loadShareData" :options="barChartOptions" />
              </div>
            </div>
          </div>
        </div>

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
                      <button 
                        @click="openESignatureModal(sig)" 
                        class="btn-e-signature"
                        :class="{ 'has-signature': signatures[sig.name] }"
                        :title="signatures[sig.name] ? 'Edit E-Signature' : 'Add E-Signature'"
                      >
                        <i :class="signatures[sig.name] ? 'pi pi-pencil' : 'pi pi-plus'"></i>
                        <span>{{ signatures[sig.name] ? 'edit' : 'e-signature' }}</span>
                      </button>
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
                      <button 
                        @click="openESignatureModal(sig)" 
                        class="btn-e-signature"
                        :class="{ 'has-signature': signatures[sig.name] }"
                        :title="signatures[sig.name] ? 'Edit E-Signature' : 'Add E-Signature'"
                      >
                        <i :class="signatures[sig.name] ? 'pi pi-pencil' : 'pi pi-plus'"></i>
                        <span>{{ signatures[sig.name] ? 'edit' : 'e-signature' }}</span>
                      </button>
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

        <!-- Middle Content (Center Column) -->
        <div class="middle-content-center">
          <div class="middle-summary-table">
            <table class="center-summary-table">
              <tbody>
                <tr>
                  <td class="center-summary-cell">60.0</td>
                  <td class="center-summary-cell">136.0</td>
                </tr>
                <tr>
                  <td class="center-summary-cell">123.0</td>
                  <td class="center-summary-cell">647.0</td>
                </tr>
                <tr>
                  <td class="center-summary-cell">105.0</td>
                  <td class="center-summary-cell">647.0</td>
                </tr>
                <tr>
                  <td class="center-summary-cell">40.0</td>
                  <td class="center-summary-cell">647.0</td>
                </tr>
                <tr>
                  <td class="center-summary-cell">184.0</td>
                  <td class="center-summary-cell">647.0</td>
                </tr>
                <tr>
                  <td class="center-summary-cell">35.0</td>
                  <td class="center-summary-cell">647.0</td>
                </tr>
                <tr class="center-total-row">
                  <td class="center-total-cell">547.0</td>
                  <td class="center-total-cell">3,371.0</td>
                </tr>
                <tr>
                  <td class="center-summary-cell">100.0</td>
                  <td class="center-summary-cell">647.0</td>
                </tr>
                <tr class="center-final-row">
                  <td class="center-final-cell">647.0</td>
                  <td class="center-final-cell"></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Right Side Content -->
        <div class="right-side-content">
          <!-- Gate Operations & Elevation Table -->
          <div class="gate-operations-table">
            <table class="gate-table">
              <thead>
                <tr class="gate-header-row">
                  <th class="gate-th">GATE#1</th>
                  <th class="gate-th">GATE#2</th>
                  <th class="gate-th">GATE#3</th>
                  <th class="gate-th">GATE#4</th>
                  <th class="gate-th">GATE#5</th>
                  <th class="gate-th">GATE#6</th>
                  <th class="gate-th elevation-header">ELEVATION</th>
                  <th class="gate-th remarks-header">REMARKS</th>
                </tr>
              </thead>
              <tbody>
                <!-- AGUS 1 -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.100</td>
                  <td class="gate-cell">0.100</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell elevation-value">701.190</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.10 m</td>
                  <td class="gate-note-cell">G2: 0.10 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                </tr>

                <!-- AGUS 2 -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell elevation-value">637.800</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.00 m</td>
                  <td class="gate-note-cell">G2: 0.00 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                </tr>

                <!-- AGUS 4 -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.500</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell elevation-value">358.800</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.50 m</td>
                  <td class="gate-note-cell">G2: 0.00 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">Dependable Capacity = Pmax</td>
                </tr>

                <!-- AGUS 5 -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.550</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.100</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell elevation-value">243.300</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.55 m</td>
                  <td class="gate-note-cell">G2: 0.00 m</td>
                  <td class="gate-note-cell">G3: 0.10 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                </tr>

                <!-- AGUS 6 -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.200</td>
                  <td class="gate-cell">0.200</td>
                  <td class="gate-cell">0.200</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell elevation-value">199.800</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.20 m</td>
                  <td class="gate-note-cell">G2: 0.20 m</td>
                  <td class="gate-note-cell">G3: 0.20 m</td>
                  <td class="gate-note-cell">G4: 0.00 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                </tr>

                <!-- AGUS 7 -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell">-</td>
                  <td class="gate-cell elevation-value">34.100</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.00 m</td>
                  <td class="gate-note-cell">G2: 0.00 m</td>
                  <td class="gate-note-cell">G3: 0.00 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                </tr>

                <!-- PULANGI IV -->
                <tr class="gate-data-row">
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell">0.000</td>
                  <td class="gate-cell elevation-value">285.450</td>
                  <td class="gate-cell">-</td>
                </tr>
                <tr class="gate-note-row">
                  <td class="gate-note-cell">G1: 0.00 m</td>
                  <td class="gate-note-cell">G2: 0.00 m</td>
                  <td class="gate-note-cell">G3: 0.00 m</td>
                  <td class="gate-note-cell">G4: 0.00 m</td>
                  <td class="gate-note-cell">G5: 0.00 m</td>
                  <td class="gate-note-cell">G6: 0.00 m</td>
                  <td class="gate-note-cell">-</td>
                  <td class="gate-note-cell">-</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Chart Section Below Gate Table -->
          <div class="gate-chart-section">
            <div class="chart-container">
              <div class="chart-wrapper">
                <Bar :data="gateChartData" :options="gateChartOptions" />
              </div>
            </div>
          </div>

          <!-- Full Pondage Storage Section Below Chart -->
          <div class="pondage-storage-section" style="margin-top: 30px; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 11px; color: #000; width: 100%;">
            <!-- Title -->
            <div style="text-align: center; font-weight: bold; margin-bottom: 10px; font-size: 13px;">
              PONDAGE STORAGE OF MinGen HEP
            </div>
            
            <!-- Table Container -->
            <div style="display: flex; justify-content: flex-start; margin-bottom: 15px;">
              <table style="border-collapse: collapse; border: 2px solid #000; text-align: right; margin-left: 10%;">
                <thead>
                  <tr>
                    <th style="border: 1px solid #000; padding: 4px; background: #fff;"></th>
                    <th style="border: 1px solid #000; padding: 4px; background: #fff;"></th>
                    <th style="border: 1px solid #000; padding: 4px; border-bottom: none; text-align: center;">MIN</th>
                    <th style="border: 1px solid #000; padding: 4px; border-bottom: none; text-align: center;">MAX</th>
                    <th style="border: none; padding: 4px; padding-left: 15px; text-align: left;" colspan="2">Usable Volume of pondage area (MCM)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Agus 1 Elevation</td>
                    <td style="border: 1px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-right: none;">698.15</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-left: none;">702.00</td>
                    <td style="border: none; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">1,327.97</td>
                    <td style="border: none;"></td>
                  </tr>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Agus 2 Elevation</td>
                    <td style="border: 1px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-right: none;">635.00</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-left: none;">637.00</td>
                    <td style="border: none; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">12.98</td>
                    <td style="border: none;"></td>
                  </tr>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Agus 4 Elevation</td>
                    <td style="border: 1px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-right: none;">357.00</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-left: none;">360.50</td>
                    <td style="border: none; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">11.70</td>
                    <td style="border: none; text-align: left; padding-left: 10px; font-weight: bold; white-space: nowrap;">Lake Lanao Elevation is 0.000 m.a.s.l (MLRD Total Gate Opening: 0.00 m)</td>
                  </tr>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Agus 5 Elevation</td>
                    <td style="border: 1px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-right: none;">242.00</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-left: none;">243.50</td>
                    <td style="border: none; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">3.81</td>
                    <td style="border: none;"></td>
                  </tr>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Agus 6 Elevation</td>
                    <td style="border: 1px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-right: none;">200.00</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-left: none;">202.10</td>
                    <td style="border: none; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">0.25</td>
                    <td style="border: none;"></td>
                  </tr>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Agus 7 Elevation</td>
                    <td style="border: 1px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-right: none;">33.00</td>
                    <td style="border: 1px solid #000; padding: 4px 8px; border-left: none;">35.40</td>
                    <td style="border: none; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">4.85</td>
                    <td style="border: none;"></td>
                  </tr>
                  <tr>
                    <td style="border: 1px solid #000; border-right: 2px solid #000; border-bottom: 2px solid #000; padding: 4px 8px; background: #ffff00; color: #0000ff; font-weight: bold; text-align: left;">Pulangi 4 Elevation</td>
                    <td style="border: 1px solid #000; border-bottom: 2px solid #000; padding: 4px 12px; color: red;">0.000</td>
                    <td style="border: 1px solid #000; border-bottom: 2px solid #000; padding: 4px 8px; border-right: none;">278.00</td>
                    <td style="border: 1px solid #000; border-bottom: 2px solid #000; padding: 4px 8px; border-left: none;">285.50</td>
                    <td style="border: none; border-bottom: 2px solid #000; padding: 4px 15px; padding-left: 30px; text-align: right; border-right: 2px solid #000;">22.64</td>
                    <td style="border: none;"></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Elevations List -->
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-weight: 500; margin-left: 6%;">
              <div style="line-height: 1.8;">
                <div><span style="color: blue;">AGUS 1</span> Lake Lanao Elevation is 0 m.a.s.l.</div>
                <div><span style="color: blue;">Pulangi 4</span> Reservoir Level is 0 m.a.s.l.</div>
                <div><span style="color: blue;">Agus 7</span> Forebay Elevation is 0 m.a.s.l.</div>
                <div><span style="color: blue;">Agus 6</span> Forebay Elevation is 0 m.a.s.l.</div>
                <div><span style="color: blue;">Agus 5</span> Forebay Elevation is 0 m.a.s.l.</div>
                <div><span style="color: blue;">Agus 4</span> Forebay Elevation is 0 m.a.s.l.</div>
                <div><span style="color: blue;">Agus 2</span> Forebay Elevation is 0 m.a.s.l.</div>
              </div>
              <div style="text-align: left; padding-top: 55px; margin-right: 15%;">
                <div style="font-weight: bold; margin-bottom: 6px;">Forebay Elevation is 0.00 m.a.s.l (SPILLAGE as of <span v-if="reportDate">{{ new Date(reportDate).toLocaleDateString('en-US') }}</span><span v-else>6/13/19</span>: 0.0200 MCM)</div>
                <div>Forebay Elevation is 0.000 m.a.s.l</div>
              </div>
            </div>

            <!-- Note and Conversion Rates -->
            <div style="display: flex; justify-content: space-between; margin-bottom: 40px; margin-left: 6%;">
              <!-- Note Block -->
              <div style="display: flex; flex: 1;">
                <div style="font-weight: bold; margin-right: 5px;">Note:</div>
                <div style="line-height: 1.6;">
                  <div style="margin-bottom: 10px;"><span style="color: blue; font-weight: bold;">MLRD</span> means Marawi Lake Regulation Dam</div>
                  <div style="margin-bottom: 15px;"><span style="color: blue; font-weight: 500;">Pulangi IV</span> must not be load from 40MW to 60 MW due to hunting of turbine generators.</div>
                  <div>Lake Lanao Maximum Allowable Level is <span style="color: blue;">702.0 masl</span></div>
                  <div style="margin-top: 15px;">Lake Lanao Maximum Operating Level is <span style="color: blue;">701.65 masl</span></div>
                  <div>Lake Lanao Minimum Operating Level is <span style="color: blue;">699.15 masl</span></div>
                  <div style="margin-bottom: 15px; background-color: yellow; padding: 5px 10px; display: inline-block;">Lake Lanao Minimum Allowable Level is <span style="color: blue;">698.15 masl</span></div>
                  <div>
                    MCM = Millions per Cubic Meter
                  </div>
                  <div style="margin-top: 10px; background-color: yellow; padding: 5px 10px; display: inline-flex; align-items: center;">
                    <span style="margin-right: 20px;"> </span>
                    <span style="border: 2px solid blue; width: 60px; height: 16px; margin-right: 20px; display: inline-block;"></span>
                    <span style="font-weight: bold; line-height: 1;">Lake Lanao Elevation is 0.000 m.a.s.l (SPILLAGE: 0.0200 MCM)</span>
                  </div>
                </div>
              </div>

              <!-- Conversion Rates Block -->
              <div style="margin-right: 10%; text-align: right;">
                <table style="border-collapse: collapse; border: none; font-size: 11px; text-align: right;">
                  <thead>
                    <tr>
                      <th colspan="4" style="text-align: center; font-weight: bold; padding-bottom: 8px;">CONVERSION RATE RIPARIAN FLOW</th>
                    </tr>
                    <tr>
                      <th style="padding: 4px 10px;"></th>
                      <th style="padding: 4px 10px; font-weight: bold;">CMS/MW</th>
                      <th style="padding: 4px 10px; font-weight: bold;">CMS</th>
                      <th style="padding: 4px 10px; font-weight: normal;">eg. Ave.Cap</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style="padding: 4px 10px; text-align: left;">AGUS 1</td>
                      <td style="padding: 4px 10px;">1.984</td>
                      <td style="padding: 4px 10px;">10</td>
                      <td style="padding: 4px 10px;">10.16</td>
                    </tr>
                    <tr>
                      <td style="padding: 4px 10px; text-align: left; padding-top: 8px;">AGUS 2</td>
                      <td style="padding: 4px 10px; padding-top: 8px;">1.078</td>
                      <td style="padding: 4px 10px; padding-top: 8px;">3.5</td>
                      <td style="padding: 4px 10px;"></td>
                    </tr>
                    <tr>
                      <td style="padding: 4px 10px; text-align: left;">AGUS 4</td>
                      <td style="padding: 4px 10px;">1.078</td>
                      <td style="padding: 4px 10px;">0.25</td>
                      <td style="padding: 4px 10px;"></td>
                    </tr>
                    <tr>
                      <td style="padding: 4px 10px; text-align: left;">AGUS 5</td>
                      <td style="padding: 4px 10px;">3.03</td>
                      <td style="padding: 4px 10px;">10</td>
                      <td style="padding: 4px 10px;"></td>
                    </tr>
                    <tr>
                      <td style="padding: 4px 10px; text-align: left; padding-top: 15px;">AGUS 6</td>
                      <td style="padding: 4px 10px; padding-top: 15px;">0.736</td>
                      <td style="padding: 4px 10px; padding-top: 15px;">0.44</td>
                      <td style="padding: 4px 10px;"></td>
                    </tr>
                    <tr>
                      <td style="padding: 4px 10px; text-align: left;">AGUS 7</td>
                      <td style="padding: 4px 10px;">3.79</td>
                      <td style="padding: 4px 10px;">3.33</td>
                      <td style="padding: 4px 10px;"></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <!-- MLRD GATES OPENING and SPILLAGE Input Blocks -->
          <div style="display: flex; justify-content: flex-start; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 11px;">
            <div style="width: 5%;"></div>
            <!-- MLRD GATES OPENING -->
            <div style="margin-right: 40px; margin-top: 20px;">
              <div style="font-weight: bold; margin-bottom: 5px; font-size: 12px; margin-left: 20px;">MLRD GATES OPENING</div>
              <div style="border: 1px solid #000; padding: 10px; width: 180px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                  <span>Gate 1 opening:</span>
                  <span style="color: yellow; font-weight: bold;">0</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                  <span>Gate 2 opening:</span>
                  <span style="color: yellow; font-weight: bold;">0.05</span>
                </div>
              </div>
              <div style="text-align: right; width: 180px; font-weight: bold; margin-top: 5px;">
                0.05
              </div>
            </div>

            <!-- SPILLAGE (MCM) INPUT 2 -->
            <div>
              <div style="font-weight: bold; color: red; margin-bottom: 5px; font-size: 12px;">SPILLAGE (MCM) INPUT 2</div>
              <div style="border: 1px solid #000; padding: 10px 20px; width: 330px; display: flex;">
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: blue;">AGUS 1</span>
                    <span style="color: yellow; font-weight: bold;">0</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: blue;">Agus 2</span>
                    <span style="color: yellow; font-weight: bold;">0</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: blue;">Agus 4</span>
                    <span style="color: yellow; font-weight: bold;">0.02</span>
                  </div>
                  <div style="display: flex; justify-content: space-between;">
                    <span style="color: blue;">Agus 5</span>
                    <span style="color: yellow; font-weight: bold;">0.864</span>
                  </div>
                </div>
                <div style="width: 40px;"></div>
                <div style="flex: 1;">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: blue;">Agus 6</span>
                    <span style="color: yellow; font-weight: bold;">1.15</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: blue;">Agus 7</span>
                    <span style="color: yellow; font-weight: bold;">0</span>
                  </div>
                  <div style="display: flex; justify-content: space-between;">
                    <span style="color: blue;">Pulangi</span>
                    <span style="color: yellow; font-weight: bold;">0</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
            
          </div>

          <!-- Workflow Diagram Section -->
          <div class="workflow-diagram-section">
            <div class="workflow-header">
              <span class="workflow-input-label">INPUT From JMM-DCM/CPN today Thursday, 12 March 2026</span>
            </div>
            
            <div class="workflow-steps">
              <div class="workflow-step">
                <div class="workflow-box step1">
                  <div class="step-text">Copy & paste the data for plant generation from AGUS-PULANGI Plant operation</div>
                </div>
                <div class="workflow-arrow">→</div>
              </div>
              
              <div class="workflow-step">
                <div class="workflow-box step2">
                  <div class="step-text">Update data in 2nd GenTask worksheet using NGCP's System Generation Data & edit the Dependable Capacity (e.g. GOMP, etc.)</div>
                </div>
                <div class="workflow-arrow">→</div>
              </div>
              
              <div class="workflow-step">
                <div class="workflow-box step3">
                  <div class="step-text">Update recent info in INPUT.xlsx 1. Receiving worksheets are: 2. Paste data from: 3. Update the Dependable Capacity (Dependable Item list)</div>
                </div>
                <div class="workflow-arrow">→</div>
              </div>
              
              <div class="workflow-step">
                <div class="workflow-box step4">
                  <div class="step-text">Update worksheets data at PSR-PSALM's 1. "GenStart" - request the actual sys 2. "AGUS" - Agus Actual System 3. "PULANGI" - Pulangi System assess at...</div>
                </div>
                <div class="workflow-arrow">→</div>
              </div>
              
              <div class="workflow-step">
                <div class="workflow-box step5">
                  <div class="step-text">1. Copy & paste the data for Ave. Available Capacity (MW) for the current day and day-ahead 2. Copy & paste the report of ALL AGUS 3. Copy & paste the report of PULANGI for the Agus-Pulangi Plant operation</div>
                </div>
                <div class="workflow-arrow">→</div>
              </div>
              
              <div class="workflow-step">
                <div class="workflow-box step6">
                  <div class="step-text">PRINT REPORT from "Report" worksheet in "Report Revised Final PSALM PSR.xlsx"</div>
                </div>
              </div>
            </div>
            
            <div class="workflow-input-section">
              <div class="input-label">INPUT 1</div>
              <div class="input-box">
                <span class="input-text">Total load is IHEM peak: </span>
                <span class="input-value">650.80 MW</span>
              </div>
            </div>
          </div>

          <!-- Data Tables Section -->
          <div class="data-tables-section">
            <!-- Top Row Tables -->
            <div class="tables-row">
              <!-- Left Table: Agus-Pulangi Load Share -->
              <div class="data-table-container">
                <div class="table-header">Agus-Pulangi Load Share @ 6 PM today</div>
                <table class="data-table">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Load</th>
                      <th>#DIV/0!</th>
                      <th>0.00</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>AGUS 1</td><td>60.0</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>AGUS 2</td><td>120.0</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>AGUS 4</td><td>96.0</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>AGUS 5</td><td>40.0</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>AGUS 6</td><td>144.8</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>AGUS 7</td><td>40.0</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>PULANGI IV</td><td>150.0</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>Other Shares</td><td>650.8</td><td>#DIV/0!</td><td></td></tr>
                    <tr><td>Agus only</td><td>500.8</td><td></td><td>0.00</td></tr>
                    <tr><td>Agus + Pulangi</td><td></td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>STEAG 1</td><td>105.00</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>MAGFP1</td><td>0.00</td><td>#DIV/0!</td><td>0.00</td></tr>
                    <tr><td>MAGFP2</td><td>0.00</td><td>#DIV/0!</td><td>0.00</td></tr>
                  </tbody>
                </table>
              </div>

              <!-- Right Table: Rated Dependable Capacity -->
              <div class="data-table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th></th>
                      <th>Rated</th>
                      <th>Dependable C.</th>
                      <th>0800H Load</th>
                      <th>Pmin</th>
                      <th>Pmax</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>AGUS 1</td><td>80.0</td><td>70.0</td><td>136 CMS @ 60</td><td>u1 &u2=12</td><td>u1=25 & u2=30</td></tr>
                    <tr><td>AGUS 2</td><td>180.0</td><td>165.0</td><td>123 MW</td><td>u1,u2,&u3=10</td><td>u1,u2,&u3=40</td></tr>
                    <tr><td>AGUS 4</td><td>158.1</td><td>105.4</td><td>105 MW</td><td>u1=20, u2=30 & u3=20</td><td>u1,u2,&u3=52.7</td></tr>
                    <tr><td>AGUS 5</td><td>55.0</td><td>53.0</td><td>40 MW</td><td>u1 & u2=10</td><td>u1 & u2=27.5</td></tr>
                    <tr><td>AGUS 6</td><td>219.0</td><td>144.8</td><td>184 MW</td><td>u3, u4 & u5=10</td><td>u3=15, u4 =25 & u5 = 42</td></tr>
                    <tr><td>AGUS 7</td><td>54.0</td><td>48.1</td><td>35 MW</td><td>u1=6 & u2=10</td><td>u1=26; u2=20</td></tr>
                    <tr><td>PULANGI IV</td><td>255.0</td><td>225.0</td><td>100 MW</td><td>u1,u2,&u3=10</td><td>u1,u2,&u3=75</td></tr>
                    <tr><td>STEAG1</td><td>116.0</td><td>105.0</td><td>105.0</td><td></td><td></td></tr>
                    <tr><td>STEAG 2</td><td>116.0</td><td>105.0</td><td>105.0</td><td></td><td></td></tr>
                    <tr><td>MAGFP1</td><td>0.0</td><td>0.0</td><td>0.0</td><td></td><td></td></tr>
                    <tr><td>MAGFP2</td><td>0.0</td><td>0.0</td><td>0.0</td><td></td><td></td></tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Bottom Row Tables -->
            <div class="tables-row">
              <!-- Left Bottom Tables -->
              <div class="left-bottom-tables">
                <!-- Colight Table -->
                <div class="small-table-container">
                  <table class="data-table small">
                    <tbody>
                      <tr><td>Colight</td><td>#REF!</td><td>#REF!</td></tr>
                      <tr><td>NGCP Forecasted System Peak</td><td>0.00</td><td></td></tr>
                    </tbody>
                  </table>
                </div>

                <!-- Agus/Pulangi Table -->
                <div class="small-table-container">
                  <table class="data-table small">
                    <tbody>
                      <tr><td>Agus</td><td>✓</td><td>#DIV/0!</td></tr>
                      <tr><td>Pulangi IV</td><td>✓</td><td>#DIV/0!</td></tr>
                      <tr><td>Agus & Pulangi</td><td>✓</td><td>#DIV/0!</td></tr>
                    </tbody>
                  </table>
                </div>

                <!-- Hydro/Geothermal Table -->
                <div class="small-table-container">
                  <table class="data-table small">
                    <tbody>
                      <tr><td>Hydro</td><td>1,001.10</td><td>81.19%</td></tr>
                      <tr><td>Geothermal</td><td>0.00</td><td>0.00%</td></tr>
                      <tr><td>Hydro</td><td>1,001.10</td><td>81.19%</td></tr>
                      <tr><td>Coal Fired Thermal</td><td>232.00</td><td>18.81%</td></tr>
                      <tr><td></td><td>1,233.10</td><td>100.00%</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Right Bottom Tables -->
              <div class="right-bottom-tables">
                <!-- MAGFP2 Table -->
                <div class="small-table-container">
                  <table class="data-table small">
                    <tbody>
                      <tr><td>MAGFP2</td><td>0.00</td><td>0.00</td><td>0.00</td></tr>
                      <tr><td>AGUS 7</td><td>54.00</td><td>48.14</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 5</td><td>55.00</td><td>53.00</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 4</td><td>158.10</td><td>105.40</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 2</td><td>180.00</td><td>165.00</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 1</td><td>80.00</td><td>70.00</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>Total</td><td>527.10</td><td>441.54</td><td>0.00</td><td>0.0%</td></tr>
                    </tbody>
                  </table>
                </div>

                <!-- Plant List -->
                <!-- Removed plant list section -->

                <!-- Yesterday's Peak Table -->
                <div class="small-table-container">
                  <div class="table-header">Rated Dependable C.Yesterday's Pe %</div>
                  <table class="data-table small">
                    <tbody>
                      <tr><td>AGUS 1</td><td>80.00</td><td>70.00</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 2</td><td>180.00</td><td>165.00</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 4</td><td>158.10</td><td>105.40</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 5</td><td>55.00</td><td>53.00</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>AGUS 6</td><td>#REF!</td><td>#REF!</td><td>#REF!</td><td>#REF!</td></tr>
                      <tr><td>AGUS 7</td><td>54.00</td><td>48.14</td><td>0.00</td><td>0.0%</td></tr>
                      <tr><td>PULANGI IV</td><td>#REF!</td><td>#REF!</td><td>#REF!</td><td>#REF!</td></tr>
                    </tbody>
                  </table>
                  <div class="table-number">14.67</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Additional Chart Section -->
          <div class="additional-chart-section">
            <div class="chart-note">
              Agus 2 HEP is limited to 40 MW/per unit due to water constraint and as per Environmental Compliance Certificate "that Agus 2 shall not be operated at full capacity..." This is to prevent risk of flooding at lakeshores areas and Balo-i plains.
            </div>
            
            <div class="additional-chart-container">
              <div class="chart-wrapper">
                <Bar :data="additionalChartData" :options="additionalChartOptions" />
              </div>
            </div>
          </div>

        </div> <!-- Close right-side-content -->
        </div> <!-- Close preview-content-wrapper -->
      </div>
    </div>

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
      },
      immediate: false
    }
  },
  
  computed: {
    canGenerate() {
      // Require both report date and plants to be loaded
      return this.reportDate && this.selectedPlants && this.selectedPlants.length > 0;
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
    this.loadPlants();
    this.loadGenerationHistory();
    this.loadSavedSignatures(); // Load user's saved signatures
    
    // Load signatures if we already have a report date
    if (this.reportDate) {
      this.loadReportSignatures();
    }
    
    document.addEventListener('click', this.closeMenu);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeMenu);
  },
  methods: {
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

      console.log('Generating report preview with data:', {
        plant_codes: this.selectedPlants,
        start_date: this.reportDate,
        end_date: this.reportDate,
        report_type: this.reportType,
      });

      this.generating = true;

      try {
        const response = await api.previewReport({
          plant_codes: this.selectedPlants,
          start_date: this.reportDate,
          end_date: this.reportDate,
          report_type: this.reportType,
        });

        this.reportPreview = response.data;
        this.showPreview = true;
        
        // Load signatures for this report date
        await this.loadReportSignatures();
        
        // Scroll to preview section
        this.$nextTick(() => {
          const previewElement = document.querySelector('.preview-card');
          if (previewElement) {
            previewElement.scrollIntoView({ behavior: 'smooth' });
          }
        });

        toast.success('Report preview loaded successfully!');
      } catch (error) {
        console.error('Generate report preview error:', error);
        console.error('Error response:', error.response);
        console.error('Error response data:', error.response?.data);
        
        let errorMsg = 'Failed to generate report preview';
        
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
            errorMsg = data.error;
            if (errorMsg.includes('No data found')) {
              errorMsg += '. Please upload Excel files first in the Upload Excel Reports page.';
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

    async downloadExcel() {
      if (!this.reportPreview) return;

      this.generating = true;
      toast.info('Generating Excel file...');

      try {
        const response = await api.generateReport({
          plant_codes: this.selectedPlants,
          start_date: this.reportDate,
          end_date: this.reportDate,
          report_type: this.reportType,
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        
        // Set filename based on report date
        const dateStr = this.reportDate.replace(/-/g, '');
        const filename = `PLANT_STATUS_${dateStr}.xlsx`;
        
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        // Save to history
        const selectedPlantNames = this.plants
          .filter(p => this.selectedPlants.includes(p.code))
          .map(p => p.name)
          .join(', ');
        const reportTypeName = this.reportTypes.find(t => t.value === this.reportType)?.label || this.reportType;
        
        this.saveToHistory({
          filename,
          plantCode: this.selectedPlants.join(','),
          plantName: selectedPlantNames,
          reportDate: this.reportDate,
          reportType: this.reportType,
          reportTypeName,
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

/* Preview content wrapper */
.preview-content-wrapper {
  display: flex; /* Use flexbox for side-by-side layout */
  gap: 2rem;
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
  padding: 6px 10px;
  font-size: 15px;
  font-weight: bold;
  color: #000;
  text-align: left;
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
  gap: 0.5rem;
}

.name-text {
  font-size: 13px;
  font-weight: bold;
  color: #000;
}

.btn-e-signature {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.3rem 0.6rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
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
  font-size: 10px;
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
</style>
