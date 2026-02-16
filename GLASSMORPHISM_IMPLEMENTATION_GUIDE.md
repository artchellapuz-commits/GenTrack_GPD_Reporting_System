# Glassmorphism Design Implementation Guide

## Overview
This guide explains how to implement the glassmorphism (water glass morphic) design across the NPC Reporting System.

## What is Glassmorphism?
Glassmorphism is a modern UI design trend featuring:
- Frosted glass effect with backdrop blur
- Semi-transparent backgrounds
- Subtle borders and shadows
- Vibrant gradient backgrounds
- Floating elements with depth

## Files Created
1. `frontend/src/assets/glassmorphism.css` - Complete glassmorphism design system

## Implementation Steps

### Step 1: Import Glassmorphism CSS

Add to `frontend/src/main.js`:
```javascript
import './assets/glassmorphism.css'
```

### Step 2: Apply to Each Page

#### Dashboard (Dashboard.vue)
Replace the page wrapper class:
```vue
<div class="dashboard-page glass-page">
```

Update card classes:
```vue
<div class="card glass-card">
<div class="stat-card glass-stat-card">
```

Update buttons:
```vue
<button class="btn-primary glass-btn glass-btn-primary">
<button class="btn-secondary glass-btn glass-btn-secondary">
```

#### Upload Excel (UploadExcel.vue)
```vue
<div class="upload-page glass-page">
<div class="card glass-card-strong">
<div class="drag-drop-zone glass-card">
<button class="btn btn-primary glass-btn glass-btn-primary">
```

#### View Reports (ViewReports.vue)
```vue
<div class="view-reports-page glass-page">
<div class="card glass-card">
<div class="summary-card glass-card-strong">
<table class="glass-table">
```

#### Generate Report (GenerateReport.vue)
```vue
<div class="generate-report-page glass-page">
<div class="card glass-card">
<button class="btn-primary glass-btn glass-btn-primary">
```

### Step 3: Update Text Colors

Add glass text classes:
```vue
<h2 class="page-title glass-text-primary">
<p class="page-description glass-text-secondary">
<label class="form-label glass-text-primary">
```

### Step 4: Update Inputs

Replace input classes:
```vue
<input class="date-input glass-input">
<select class="rows-select glass-input">
```

### Step 5: Update Modals

```vue
<div class="modal-overlay glass-modal-overlay">
<div class="comparison-modal glass-modal">
```

## CSS Class Reference

### Cards
- `.glass-card` - Standard glass card
- `.glass-card-strong` - Stronger glass effect
- `.glass-stat-card` - Stat card with top border

### Buttons
- `.glass-btn` - Base glass button
- `.glass-btn-primary` - Primary gradient button
- `.glass-btn-secondary` - Secondary gradient button

### Inputs
- `.glass-input` - Glass input field
- `.glass-dropdown` - Glass dropdown menu

### Text
- `.glass-text-primary` - Primary text (95% white)
- `.glass-text-secondary` - Secondary text (80% white)
- `.glass-text-muted` - Muted text (60% white)

### Tables
- `.glass-table` - Glass table with blur

### Badges
- `.glass-badge` - Glass badge/tag

### Alerts
- `.glass-alert` - Base alert
- `.glass-alert-success` - Success alert
- `.glass-alert-error` - Error alert
- `.glass-alert-info` - Info alert

### Effects
- `.glass-glow` - Glow effect
- `.glass-float` - Floating animation
- `.glass-shimmer` - Shimmer effect

## Quick Implementation Example

### Before:
```vue
<template>
  <div class="dashboard-page">
    <div class="card">
      <h2 class="page-title">Dashboard</h2>
      <button class="btn btn-primary">Click Me</button>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  background: white;
}
.card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
}
</style>
```

### After:
```vue
<template>
  <div class="dashboard-page glass-page">
    <div class="card glass-card glass-float">
      <h2 class="page-title glass-text-primary">Dashboard</h2>
      <button class="btn glass-btn glass-btn-primary glass-glow">
        Click Me
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Remove background styles - handled by glassmorphism.css */
.dashboard-page {
  padding: 2rem;
}
</style>
```

## Color Customization

Edit `glassmorphism.css` variables:
```css
:root {
  --glass-white: rgba(255, 255, 255, 0.1); /* Adjust transparency */
  --blur-md: blur(12px); /* Adjust blur amount */
}
```

## Background Gradient

The animated gradient background is automatically applied to `<body>`.

To customize colors, edit in `glassmorphism.css`:
```css
body {
  background: linear-gradient(
    135deg, 
    #667eea 0%,    /* Purple */
    #764ba2 25%,   /* Dark purple */
    #f093fb 50%,   /* Pink */
    #4facfe 75%,   /* Blue */
    #00f2fe 100%   /* Cyan */
  );
}
```

## Browser Support

Glassmorphism requires:
- Chrome 76+
- Firefox 103+
- Safari 9+
- Edge 79+

Fallback for older browsers:
```css
@supports not (backdrop-filter: blur(10px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.9);
  }
}
```

## Performance Tips

1. **Limit Blur Layers**: Too many blurred elements can slow performance
2. **Use Transform**: Prefer `transform` over `top/left` for animations
3. **Reduce Complexity**: Simplify gradients on mobile devices
4. **Test on Devices**: Check performance on target devices

## Mobile Optimization

Glassmorphism automatically adjusts for mobile:
```css
@media (max-width: 768px) {
  .glass-card {
    backdrop-filter: blur(8px); /* Reduced blur */
  }
}
```

## Accessibility

Ensure text contrast:
```css
.glass-text-primary {
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Improves readability */
}
```

## Examples

### Glass Stat Card
```vue
<div class="glass-stat-card glass-float">
  <div class="stat-icon">
    <i class="pi pi-bolt"></i>
  </div>
  <div class="stat-content">
    <label class="glass-text-secondary">Total Generation</label>
    <span class="glass-text-primary">1,234,567 kWh</span>
  </div>
</div>
```

### Glass Button with Glow
```vue
<button class="glass-btn glass-btn-primary glass-glow">
  <i class="pi pi-upload"></i>
  Upload File
</button>
```

### Glass Table
```vue
<table class="glass-table">
  <thead>
    <tr>
      <th class="glass-text-primary">Date</th>
      <th class="glass-text-primary">Plant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="glass-text-secondary">2024-02-16</td>
      <td class="glass-text-secondary">AGUS1</td>
    </tr>
  </tbody>
</table>
```

### Glass Modal
```vue
<div class="glass-modal-overlay">
  <div class="glass-modal">
    <div class="modal-header">
      <h2 class="glass-text-primary">Comparison</h2>
    </div>
    <div class="modal-body">
      <!-- Content -->
    </div>
  </div>
</div>
```

## Troubleshooting

### Issue: Blur not working
**Solution**: Check browser support for `backdrop-filter`

### Issue: Performance lag
**Solution**: Reduce number of blurred elements or blur intensity

### Issue: Text hard to read
**Solution**: Increase text shadow or use darker text colors

### Issue: Background too bright
**Solution**: Adjust `--glass-white` opacity in CSS variables

## Next Steps

1. Import glassmorphism.css in main.js
2. Apply glass classes to Dashboard
3. Apply glass classes to Upload Excel
4. Apply glass classes to View Reports
5. Apply glass classes to Generate Report
6. Test on different browsers
7. Optimize for mobile devices
8. Adjust colors and blur to preference

## Resources

- [Glassmorphism Generator](https://hype4.academy/tools/glassmorphism-generator)
- [CSS Backdrop Filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)
- [Glassmorphism UI](https://ui.glass/)

## Support

For issues or questions:
1. Check browser compatibility
2. Verify CSS import in main.js
3. Test with reduced blur values
4. Check console for errors
