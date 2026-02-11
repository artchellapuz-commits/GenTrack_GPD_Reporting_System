# PrimeVue Icons Implementation

## Overview
All emoji icons throughout the NPC Reporting System have been replaced with professional PrimeVue icons for a consistent, modern look.

## Installation
```bash
npm install primeicons primevue
```

## Icons Used

### Navigation (App.vue)
- **Upload**: `pi pi-upload` (replaces 📤)
- **Reports**: `pi pi-chart-line` (replaces 📋)
- **Generate**: `pi pi-download` (replaces 📥)

### Upload Excel Component
- **Plant Selection**: `pi pi-building`
- **Excel File**: `pi pi-file-excel` (replaces 📄)
- **File Attachment**: `pi pi-paperclip` (replaces 📎)
- **Upload Button**: `pi pi-upload` (replaces 📤)
- **Location**: `pi pi-map-marker` (replaces 📍)
- **Capacity**: `pi pi-bolt` (replaces ⚡)
- **Dropdown Arrow**: `pi pi-chevron-down` (replaces ▼)
- **Selected Check**: `pi pi-check` (replaces ✓)
- **Recent Uploads**: `pi pi-history` (replaces 📜)
- **File Icon**: `pi pi-file` (replaces 📄)
- **Success Alert**: `pi pi-check-circle` (replaces ✅)
- **Error Alert**: `pi pi-times-circle` (replaces ❌)

### View Reports Component
- **Page Title**: `pi pi-chart-line`
- **Plant Filter**: `pi pi-building`
- **Date Filters**: `pi pi-calendar`
- **Apply Filters**: `pi pi-filter`
- **View Summary**: `pi pi-chart-bar`
- **Pagination Previous**: `pi pi-chevron-left`
- **Pagination Next**: `pi pi-chevron-right`
- **Loading**: `pi pi-spin pi-spinner`
- **No Data**: `pi pi-inbox`

### Generate Report Component
- **Page Title**: `pi pi-file-export`
- **Plant Selection**: `pi pi-building`
- **Date Fields**: `pi pi-calendar`
- **Report Type**: `pi pi-file`
- **Generate Button**: `pi pi-download`
- **Loading**: `pi pi-spin pi-spinner`
- **Success Alert**: `pi pi-check-circle`
- **Error Alert**: `pi pi-times-circle`

## Benefits
1. **Professional Appearance**: Consistent, scalable vector icons
2. **Better Accessibility**: Proper icon fonts with semantic meaning
3. **Customizable**: Easy to style with CSS (color, size, etc.)
4. **Performance**: Lightweight icon font vs emoji rendering
5. **Cross-browser Compatibility**: Consistent appearance across all browsers

## Usage Example
```vue
<!-- Basic Icon -->
<i class="pi pi-upload"></i>

<!-- With Custom Styling -->
<i class="pi pi-check" style="color: green; font-size: 1.5rem;"></i>

<!-- Spinning Icon (for loading states) -->
<i class="pi pi-spin pi-spinner"></i>
```

## Documentation
- PrimeIcons: https://primevue.org/icons/
- Full Icon List: https://primevue.org/icons/#list
