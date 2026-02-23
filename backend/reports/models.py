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



class WaterNomination(models.Model):
    """Water nomination and dispatch scheduling for hydroelectric plants"""
    
    NOMINATION_TYPE_CHOICES = [
        ('DAY_AHEAD', 'Day-Ahead'),
        ('HOUR_AHEAD', 'Hour-Ahead'),
        ('REAL_TIME', 'Real-Time'),
    ]
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]
    
    # Basic Information
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='water_nominations')
    nomination_date = models.DateField(help_text="Date for which nomination is made")
    nomination_type = models.CharField(max_length=20, choices=NOMINATION_TYPE_CHOICES, default='DAY_AHEAD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    # Hourly Nomination (24 hours)
    hour_00 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 00:00-01:00")
    hour_01 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 01:00-02:00")
    hour_02 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 02:00-03:00")
    hour_03 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 03:00-04:00")
    hour_04 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 04:00-05:00")
    hour_05 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 05:00-06:00")
    hour_06 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 06:00-07:00")
    hour_07 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 07:00-08:00")
    hour_08 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 08:00-09:00")
    hour_09 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 09:00-10:00")
    hour_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 10:00-11:00")
    hour_11 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 11:00-12:00")
    hour_12 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 12:00-13:00")
    hour_13 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 13:00-14:00")
    hour_14 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 14:00-15:00")
    hour_15 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 15:00-16:00")
    hour_16 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 16:00-17:00")
    hour_17 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 17:00-18:00")
    hour_18 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 18:00-19:00")
    hour_19 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 19:00-20:00")
    hour_20 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 20:00-21:00")
    hour_21 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 21:00-22:00")
    hour_22 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 22:00-23:00")
    hour_23 = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Nominated MW for 23:00-24:00")
    
    # Summary Fields
    total_nominated_mw = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Total nominated MW for the day")
    total_nominated_mwh = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Total nominated MWh for the day")
    
    # Water Parameters (Optional - can be customized)
    reservoir_level_start = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Reservoir level at start (meters)")
    reservoir_level_end = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Reservoir level at end (meters)")
    water_flow_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Average water flow rate (m³/s)")
    inflow_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Water inflow rate (m³/s)")
    
    # Tracking
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submitted_nominations')
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_nominations')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'water_nominations'
        unique_together = ['plant', 'nomination_date', 'nomination_type']
        ordering = ['-nomination_date', 'plant']
        indexes = [
            models.Index(fields=['plant', 'nomination_date']),
            models.Index(fields=['nomination_date']),
            models.Index(fields=['status']),
            models.Index(fields=['submitted_by']),
        ]
    
    def __str__(self):
        return f"{self.plant.code} - {self.nomination_date} ({self.nomination_type})"
    
    def save(self, *args, **kwargs):
        # Calculate totals
        hourly_values = [
            float(getattr(self, f'hour_{str(i).zfill(2)}', 0) or 0)
            for i in range(24)
        ]
        self.total_nominated_mw = sum(hourly_values)
        self.total_nominated_mwh = sum(hourly_values)  # Each hour = 1 MWh per MW
        
        super().save(*args, **kwargs)
    
    def get_hourly_data(self):
        """Return hourly nomination data as a list"""
        return [
            {
                'hour': i,
                'time': f"{str(i).zfill(2)}:00-{str(i+1).zfill(2)}:00",
                'nominated_mw': float(getattr(self, f'hour_{str(i).zfill(2)}', 0) or 0)
            }
            for i in range(24)
        ]


class ActualGeneration(models.Model):
    """Actual hourly generation data for comparison with nominations"""
    
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='actual_generations')
    generation_date = models.DateField()
    
    # Hourly Actual Generation (24 hours)
    hour_00 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_01 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_02 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_03 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_04 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_05 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_06 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_07 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_08 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_09 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_11 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_12 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_13 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_14 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_15 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_16 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_17 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_18 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_19 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_20 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_21 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_22 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hour_23 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Summary
    total_actual_mw = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_actual_mwh = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Water Parameters
    actual_water_flow = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reservoir_level = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'actual_generations'
        unique_together = ['plant', 'generation_date']
        ordering = ['-generation_date', 'plant']
        indexes = [
            models.Index(fields=['plant', 'generation_date']),
            models.Index(fields=['generation_date']),
        ]
    
    def __str__(self):
        return f"{self.plant.code} - {self.generation_date} (Actual)"
    
    def save(self, *args, **kwargs):
        # Calculate totals
        hourly_values = [
            float(getattr(self, f'hour_{str(i).zfill(2)}', 0) or 0)
            for i in range(24)
        ]
        self.total_actual_mw = sum(hourly_values)
        self.total_actual_mwh = sum(hourly_values)
        
        super().save(*args, **kwargs)
    
    def get_hourly_data(self):
        """Return hourly actual data as a list"""
        return [
            {
                'hour': i,
                'time': f"{str(i).zfill(2)}:00-{str(i+1).zfill(2)}:00",
                'actual_mw': float(getattr(self, f'hour_{str(i).zfill(2)}', 0) or 0)
            }
            for i in range(24)
        ]


class Testimonial(models.Model):
    """User testimonials for the landing page"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    plant = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'testimonials'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class UserProfile(models.Model):
    """Extended user profile with role-based permissions"""

    ROLE_CHOICES = [
        ('VIEWER', 'Viewer'),
        ('OPERATOR', 'Operator'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEWER')
    plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text="Assigned plant for operators")
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    notify_on_upload = models.BooleanField(default=True)
    notify_on_approval = models.BooleanField(default=True)
    notify_daily_summary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        ordering = ['user__username']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['plant']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def can_upload_data(self):
        """Check if user can upload data"""
        return self.role in ['OPERATOR', 'MANAGER', 'ADMIN'] or self.user.is_staff

    def can_approve_data(self):
        """Check if user can approve data"""
        return self.role in ['MANAGER', 'ADMIN'] or self.user.is_staff

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role == 'ADMIN' or self.user.is_staff

    def can_export_data(self):
        """Check if user can export data"""
        return True  # All authenticated users can export


class AuditLog(models.Model):
    """Audit trail for all important actions"""
    
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('UPLOAD', 'Upload'),
        ('EXPORT', 'Export'),
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Approximate location based on IP")
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.action} - {self.timestamp}"

