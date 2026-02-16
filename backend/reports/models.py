from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Plant(models.Model):
    """Agus and Pulangi Hydroelectric Plants"""
    PLANT_CHOICES = [
        ('AGUS1', 'Agus 1'),
        ('AGUS2', 'Agus 2'),
        ('AGUS4', 'Agus 4'),
        ('AGUS5', 'Agus 5'),
        ('AGUS6', 'Agus 6'),
        ('AGUS7', 'Agus 7'),
        ('PULANGI4', 'Pulangi 4'),
    ]
    
    code = models.CharField(max_length=10, choices=PLANT_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    capacity_mw = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    commissioned_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plants'
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Unit(models.Model):
    """Generation units within each plant"""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='units')
    unit_number = models.IntegerField(validators=[MinValueValidator(1)])
    capacity_mw = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    commissioned_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'units'
        unique_together = ['plant', 'unit_number']
        ordering = ['plant', 'unit_number']
        indexes = [
            models.Index(fields=['plant', 'unit_number']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.plant.code} - Unit {self.unit_number}"


class UploadedFile(models.Model):
    """Audit trail for uploaded Excel files"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    file = models.FileField(upload_to='uploads/%Y/%m/')
    original_filename = models.CharField(max_length=255)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    records_imported = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    file_size = models.IntegerField()
    checksum = models.CharField(max_length=64)
    
    class Meta:
        db_table = 'uploaded_files'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['plant', 'uploaded_at']),
            models.Index(fields=['status']),
            models.Index(fields=['uploaded_by']),
        ]
    
    def __str__(self):
        return f"{self.original_filename} - {self.uploaded_at}"


class GenerationReport(models.Model):
    """Daily generation data for each unit"""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='generation_reports')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='generation_reports')
    report_date = models.DateField()
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='generation_reports')
    
    # Generation data
    generation_kwh = models.DecimalField(max_digits=15, decimal_places=2)
    operating_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(24)])
    availability_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(24)])
    forced_outage_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    scheduled_outage_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Performance metrics
    capacity_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    availability_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Additional fields
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'generation_reports'
        unique_together = ['plant', 'unit', 'report_date']
        ordering = ['-report_date', 'plant', 'unit']
        indexes = [
            models.Index(fields=['plant', 'report_date']),
            models.Index(fields=['report_date']),
            models.Index(fields=['unit', 'report_date']),
            models.Index(fields=['uploaded_file']),
        ]
    
    def __str__(self):
        return f"{self.plant.code} - Unit {self.unit.unit_number} - {self.report_date}"
    
    def save(self, *args, **kwargs):
        # Calculate capacity factor
        if self.unit.capacity_mw > 0:
            max_generation = float(self.unit.capacity_mw) * 24
            self.capacity_factor = (float(self.generation_kwh) / 1000 / max_generation) * 100
        
        # Calculate availability factor
        if self.availability_hours > 0:
            self.availability_factor = (float(self.availability_hours) / 24) * 100
        
        super().save(*args, **kwargs)


class PlantCapacity(models.Model):
    """Historical capacity data for plants"""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='capacity_records')
    installed_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    dependable_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plant_capacity'
        unique_together = ['plant', 'effective_date']
        ordering = ['-effective_date', 'plant']
        indexes = [
            models.Index(fields=['plant', 'effective_date']),
        ]
    
    def __str__(self):
        return f"{self.plant.code} - {self.effective_date}"


class HistoricalData(models.Model):
    """Historical operational data imported from legacy systems"""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='historical_data')
    date = models.DateField()
    generation_mwh = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    availability_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default='Operating')
    remarks = models.TextField(blank=True)
    sheet_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'historical_data'
        unique_together = ['plant', 'date']
        ordering = ['-date', 'plant']
        indexes = [
            models.Index(fields=['plant', 'date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.plant.code} - {self.date}"

