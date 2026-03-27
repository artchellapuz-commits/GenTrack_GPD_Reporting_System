// PDF Export Utility for jsPDF v4.x
// Packages are installed: jspdf@4.1.0 and jspdf-autotable@5.0.7

import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

class PDFExporter {
  constructor() {
    this.jsPDF = jsPDF;
    this.autoTable = autoTable;
    this.isAvailable = true;
  }

  async init() {
    return this.isAvailable;
  }

  async exportDashboard(plants, options = {}) {
    const available = await this.init();
    
    if (!available) {
      throw new Error('PDF export not available. Please install: npm install jspdf jspdf-autotable');
    }
    
    const doc = new this.jsPDF();
    const title = options.title || 'NPC Dashboard Report';
    const date = new Date().toLocaleDateString();
    
    // Title
    doc.setFontSize(20);
    doc.setTextColor(30, 41, 59);
    doc.text(title, 14, 20);
    
    // Date
    doc.setFontSize(10);
    doc.setTextColor(100, 116, 139);
    doc.text(`Generated: ${date}`, 14, 28);
    
    // Summary Stats
    const totalGeneration = plants.reduce((sum, p) => sum + (p.total_generation || p.generation || 0), 0);
    const avgCapacity = plants.reduce((sum, p) => sum + (p.capacity_factor || p.capacityFactor || 0), 0) / plants.length;
    
    doc.setFontSize(12);
    doc.setTextColor(30, 41, 59);
    doc.text('Summary Statistics', 14, 40);
    
    doc.setFontSize(10);
    doc.text(`Total Plants: ${plants.length}`, 14, 48);
    doc.text(`Total Generation: ${totalGeneration.toLocaleString()} MWh`, 14, 54);
    doc.text(`Average Capacity Factor: ${avgCapacity.toFixed(2)}%`, 14, 60);
    
    // Plants Table
    const tableData = plants.map(plant => [
      plant.name || plant.plant_name,
      ((plant.total_generation || plant.generation || 0)).toLocaleString() + ' MWh',
      ((plant.capacity_factor || plant.capacityFactor || 0)).toFixed(2) + '%',
      ((plant.availability || 0)).toFixed(2) + '%',
      plant.status || 'Active'
    ]);
    
    // Use autoTable function directly (jspdf-autotable v5.x)
    autoTable(doc, {
      head: [['Plant Name', 'Generation', 'Capacity Factor', 'Availability', 'Status']],
      body: tableData,
      startY: 70,
      theme: 'grid',
      headStyles: {
        fillColor: [59, 130, 246],
        textColor: 255,
        fontStyle: 'bold'
      },
      alternateRowStyles: {
        fillColor: [248, 250, 252]
      },
      margin: { top: 70 }
    });
    
    // Footer
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setFontSize(8);
      doc.setTextColor(148, 163, 184);
      doc.text(
        `Page ${i} of ${pageCount}`,
        doc.internal.pageSize.getWidth() / 2,
        doc.internal.pageSize.getHeight() - 10,
        { align: 'center' }
      );
    }
    
    return doc;
  }

  async exportReport(data, options = {}) {
    const available = await this.init();
    
    if (!available) {
      throw new Error('PDF export not available. Please install: npm install jspdf jspdf-autotable');
    }
    
    const doc = new this.jsPDF();
    const title = options.title || 'NPC Generation Report';
    const date = new Date().toLocaleDateString();
    
    // Title
    doc.setFontSize(20);
    doc.text(title, 14, 20);
    
    // Date
    doc.setFontSize(10);
    doc.text(`Generated: ${date}`, 14, 28);
    
    // Data Table
    if (data && data.length > 0) {
      const headers = Object.keys(data[0]);
      const tableData = data.map(row => headers.map(h => row[h]));
      
      // Use autoTable function directly (jspdf-autotable v5.x)
      autoTable(doc, {
        head: [headers],
        body: tableData,
        startY: 35,
        theme: 'grid',
        headStyles: {
          fillColor: [59, 130, 246]
        }
      });
    }
    
    return doc;
  }

  async downloadPDF(doc, filename = 'report.pdf') {
    doc.save(filename);
  }
  
  checkAvailability() {
    return this.isAvailable;
  }
}

// Create singleton instance
const pdfExporter = new PDFExporter();

export default pdfExporter;
