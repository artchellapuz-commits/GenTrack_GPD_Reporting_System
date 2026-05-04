/**
 * Export Utilities for Dashboard
 * Handles CSV and Excel export functionality
 */

/**
 * Format date to YYYY-MM-DD
 */
export function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Format number with 2 decimal places
 */
export function formatNumber(value) {
  if (!value && value !== 0) return '0.00';
  return parseFloat(value).toFixed(2);
}

/**
 * Escape CSV field (handle commas, quotes, newlines)
 */
export function escapeCSVField(field) {
  if (field === null || field === undefined) return '';
  
  const str = String(field);
  
  // If field contains comma, quote, or newline, wrap in quotes and escape quotes
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  
  return str;
}

/**
 * Create CSV content from array of objects
 */
export function createCSV(headers, rows) {
  const lines = [];
  
  // Add headers
  lines.push(headers.map(escapeCSVField).join(','));
  
  // Add rows
  rows.forEach(row => {
    lines.push(row.map(escapeCSVField).join(','));
  });
  
  return lines.join('\n');
}

/**
 * Download CSV file
 */
export function downloadCSV(content, filename) {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

/**
 * Download blob file (for Excel)
 */
export function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

/**
 * Export plant data to CSV
 */
export function exportPlantToCSV(plant, reports, plantCapacity) {
  const lines = [];
  
  // Header section
  lines.push('Plant Export Report');
  lines.push(`Generated: ${new Date().toLocaleString()}`);
  lines.push('');
  
  // Plant information
  lines.push('PLANT INFORMATION');
  lines.push(`Name,${escapeCSVField(plant.name)}`);
  lines.push(`Code,${escapeCSVField(plant.code)}`);
  lines.push(`Capacity,${plantCapacity} MW`);
  lines.push('');
  
  // Summary statistics
  lines.push('SUMMARY STATISTICS');
  lines.push(`Total Generation,${formatNumber(plant.generation)} kWh`);
  lines.push(`Average Capacity Factor,${formatNumber(plant.capacityFactor)}%`);
  lines.push(`Average Availability,${formatNumber(plant.availability)}%`);
  lines.push(`Total Records,${reports.length}`);
  lines.push('');
  
  // Date range
  if (reports.length > 0) {
    const dates = reports.map(r => new Date(r.date)).sort((a, b) => a - b);
    lines.push(`Date Range,${formatDate(dates[0])} to ${formatDate(dates[dates.length - 1])}`);
    lines.push('');
  }
  
  // Detailed data table
  lines.push('DETAILED GENERATION DATA');
  const headers = ['Date', 'Unit', 'Generation (kWh)', 'Operating Hours', 'Capacity Factor (%)', 'Availability Factor (%)', 'Remarks'];
  lines.push(headers.map(escapeCSVField).join(','));
  
  // Sort reports by date
  const sortedReports = [...reports].sort((a, b) => new Date(a.date) - new Date(b.date));
  
  sortedReports.forEach(report => {
    const row = [
      report.date,
      report.unit_name || report.unit_code || '',
      formatNumber(report.generation_kwh),
      formatNumber(report.operating_hours),
      formatNumber(report.capacity_factor),
      formatNumber(report.availability_factor),
      report.remarks || ''
    ];
    lines.push(row.map(escapeCSVField).join(','));
  });
  
  // Summary by unit
  lines.push('');
  lines.push('SUMMARY BY UNIT');
  const unitSummary = {};
  
  sortedReports.forEach(report => {
    const unitKey = report.unit_name || report.unit_code || 'Unknown';
    if (!unitSummary[unitKey]) {
      unitSummary[unitKey] = {
        generation: 0,
        hours: 0,
        count: 0
      };
    }
    unitSummary[unitKey].generation += parseFloat(report.generation_kwh || 0);
    unitSummary[unitKey].hours += parseFloat(report.operating_hours || 0);
    unitSummary[unitKey].count += 1;
  });
  
  lines.push('Unit,Total Generation (kWh),Total Operating Hours,Number of Records');
  Object.entries(unitSummary).forEach(([unit, data]) => {
    lines.push([
      unit,
      formatNumber(data.generation),
      formatNumber(data.hours),
      data.count
    ].map(escapeCSVField).join(','));
  });
  
  return lines.join('\n');
}

/**
 * Export comparison data to CSV
 */
export function exportComparisonToCSV(plants, getPlantCapacity) {
  const headers = ['Metric', ...plants.map(p => p.name)];
  const rows = [
    ['Code', ...plants.map(p => p.code)],
    ['Capacity (MW)', ...plants.map(p => getPlantCapacity(p.code))],
    ['Generation (kWh)', ...plants.map(p => formatNumber(p.generation))],
    ['Capacity Factor (%)', ...plants.map(p => formatNumber(p.capacityFactor))],
    ['Availability (%)', ...plants.map(p => formatNumber(p.availability))],
  ];
  
  return createCSV(headers, rows);
}

/**
 * Export all dashboard data to CSV
 */
export function exportDashboardToCSV(stats, plantsData, getPlantCapacity) {
  const lines = [];
  
  // Header
  lines.push('NPC Reporting System - Dashboard Export');
  lines.push(`Generated: ${new Date().toLocaleString()}`);
  lines.push('');
  
  // Overall statistics
  lines.push('OVERALL STATISTICS');
  lines.push(`Total Generation,${formatNumber(stats.totalGeneration)} kWh`);
  lines.push(`Average Capacity Factor,${formatNumber(stats.avgCapacityFactor)}%`);
  lines.push(`Average Availability,${formatNumber(stats.avgAvailability)}%`);
  lines.push(`Total Operating Hours,${formatNumber(stats.totalOperatingHours)} hrs`);
  lines.push('');
  
  // Plants summary
  lines.push('PLANTS SUMMARY');
  const headers = ['Plant Name', 'Code', 'Capacity (MW)', 'Generation (kWh)', 'Capacity Factor (%)', 'Availability (%)', 'Status'];
  lines.push(headers.map(escapeCSVField).join(','));
  
  plantsData.forEach(plant => {
    const row = [
      plant.name,
      plant.code,
      getPlantCapacity(plant.code),
      formatNumber(plant.generation),
      formatNumber(plant.capacityFactor),
      formatNumber(plant.availability),
      plant.hasData ? 'Active' : 'No Data'
    ];
    lines.push(row.map(escapeCSVField).join(','));
  });
  
  return lines.join('\n');
}
