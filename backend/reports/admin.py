from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Plant, Unit, UploadedFile, GenerationReport, 
    PlantCapacity, HistoricalData, WaterNomination, 
    ActualGeneration, Testimonial, UserProfile, AuditLog,
    PasswordResetRequest, ESignature, ReportSignature
)


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ['role', 'plant', 'phone', 'department', 'position', 
              'email_notifications', 'notify_on_upload', 'notify_on_approval', 'notify_daily_summary']


# Extend User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'profile__role']
    
    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else 'No Profile'
    get_role.short_description = 'Role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'capacity_mw', 'location', 'is_active']
    list_filter = ['is_active', 'code']
    search_fields = ['code', 'name', 'location']
    ordering = ['code']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['plant', 'unit_number', 'capacity_mw', 'is_active', 'commissioned_date']
    list_filter = ['plant', 'is_active']
    search_fields = ['plant__code', 'plant__name']
    ordering = ['plant', 'unit_number']


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'plant', 'uploaded_by', 'uploaded_at', 'status', 'records_imported']
    list_filter = ['status', 'plant', 'uploaded_at']
    search_fields = ['original_filename', 'plant__code', 'uploaded_by__username']
    readonly_fields = ['uploaded_at', 'checksum', 'file_size']
    ordering = ['-uploaded_at']


@admin.register(GenerationReport)
class GenerationReportAdmin(admin.ModelAdmin):
    list_display = ['plant', 'unit', 'report_date', 'generation_kwh', 'capacity_factor', 'availability_factor']
    list_filter = ['plant', 'report_date']
    search_fields = ['plant__code', 'unit__unit_number']
    date_hierarchy = 'report_date'
    ordering = ['-report_date', 'plant', 'unit']


@admin.register(PlantCapacity)
class PlantCapacityAdmin(admin.ModelAdmin):
    list_display = ['plant', 'installed_capacity', 'dependable_capacity', 'effective_date']
    list_filter = ['plant', 'effective_date']
    search_fields = ['plant__code', 'plant__name']
    date_hierarchy = 'effective_date'
    ordering = ['-effective_date', 'plant']


@admin.register(HistoricalData)
class HistoricalDataAdmin(admin.ModelAdmin):
    list_display = ['plant', 'date', 'generation_mwh', 'availability_percent', 'status']
    list_filter = ['plant', 'status', 'date']
    search_fields = ['plant__code', 'plant__name']
    date_hierarchy = 'date'
    ordering = ['-date', 'plant']


@admin.register(WaterNomination)
class WaterNominationAdmin(admin.ModelAdmin):
    list_display = ['plant', 'nomination_date', 'nomination_type', 'status', 
                   'total_nominated_mwh', 'submitted_by', 'approved_by']
    list_filter = ['status', 'nomination_type', 'plant', 'nomination_date']
    search_fields = ['plant__code', 'submitted_by__username', 'approved_by__username']
    date_hierarchy = 'nomination_date'
    readonly_fields = ['total_nominated_mw', 'total_nominated_mwh', 'submitted_at', 'approved_at']
    ordering = ['-nomination_date', 'plant']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('plant', 'nomination_date', 'nomination_type', 'status')
        }),
        ('Hourly Nomination (MW)', {
            'fields': (
                ('hour_00', 'hour_01', 'hour_02', 'hour_03'),
                ('hour_04', 'hour_05', 'hour_06', 'hour_07'),
                ('hour_08', 'hour_09', 'hour_10', 'hour_11'),
                ('hour_12', 'hour_13', 'hour_14', 'hour_15'),
                ('hour_16', 'hour_17', 'hour_18', 'hour_19'),
                ('hour_20', 'hour_21', 'hour_22', 'hour_23'),
            )
        }),
        ('Summary', {
            'fields': ('total_nominated_mw', 'total_nominated_mwh')
        }),
        ('Water Parameters', {
            'fields': ('reservoir_level_start', 'reservoir_level_end', 'water_flow_rate', 'inflow_rate'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('submitted_by', 'submitted_at', 'approved_by', 'approved_at', 'remarks')
        }),
    )


@admin.register(ActualGeneration)
class ActualGenerationAdmin(admin.ModelAdmin):
    list_display = ['plant', 'generation_date', 'total_actual_mwh', 'actual_water_flow', 'reservoir_level']
    list_filter = ['plant', 'generation_date']
    search_fields = ['plant__code', 'plant__name']
    date_hierarchy = 'generation_date'
    readonly_fields = ['total_actual_mw', 'total_actual_mwh']
    ordering = ['-generation_date', 'plant']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'plant', 'rating', 'is_active', 'order']
    list_filter = ['is_active', 'rating']
    search_fields = ['name', 'position', 'plant', 'testimonial']
    ordering = ['order', '-created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'plant', 'department', 'position', 'email_notifications']
    list_filter = ['role', 'plant', 'email_notifications']
    search_fields = ['user__username', 'user__email', 'department', 'position']
    ordering = ['user__username']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'plant')
        }),
        ('Contact Details', {
            'fields': ('phone', 'department', 'position')
        }),
        ('Notification Preferences', {
            'fields': ('email_notifications', 'notify_on_upload', 'notify_on_approval', 'notify_daily_summary')
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'description', 'ip_address']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 
                      'ip_address', 'user_agent', 'timestamp']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ['username', 'status', 'created_at', 'processed_by', 'processed_at']
    list_filter = ['status', 'created_at', 'processed_at']
    search_fields = ['username', 'reason', 'admin_notes']
    readonly_fields = ['username', 'reason', 'ip_address', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('username', 'reason', 'ip_address', 'status')
        }),
        ('Admin Actions', {
            'fields': ('processed_by', 'processed_at', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-set processed_by and processed_at when status changes"""
        if change and 'status' in form.changed_data:
            if obj.status in ['APPROVED', 'REJECTED', 'COMPLETED']:
                if not obj.processed_by:
                    obj.processed_by = request.user
                if not obj.processed_at:
                    from django.utils import timezone
                    obj.processed_at = timezone.now()
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_approved', 'mark_as_rejected', 'mark_as_completed']
    
    def mark_as_approved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='PENDING').update(
            status='APPROVED',
            processed_by=request.user,
            processed_at=timezone.now()
        )
        self.message_user(request, f'{updated} request(s) marked as approved.')
    mark_as_approved.short_description = 'Mark selected as Approved'
    
    def mark_as_rejected(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='PENDING').update(
            status='REJECTED',
            processed_by=request.user,
            processed_at=timezone.now()
        )
        self.message_user(request, f'{updated} request(s) marked as rejected.')
    mark_as_rejected.short_description = 'Mark selected as Rejected'
    
    def mark_as_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='APPROVED').update(
            status='COMPLETED',
            processed_at=timezone.now()
        )
        self.message_user(request, f'{updated} request(s) marked as completed.')
    mark_as_completed.short_description = 'Mark selected as Completed'


# Customize admin site
admin.site.site_header = "NPC Reporting System Administration"
admin.site.site_title = "NPC Admin"
admin.site.index_title = "Welcome to NPC Reporting System Administration"

@admin.register(ESignature)
class ESignatureAdmin(admin.ModelAdmin):
    list_display = ['signatory_name', 'signatory_title', 'signature_type', 'is_active', 'is_default', 'created_at']
    list_filter = ['signature_type', 'is_active', 'is_default', 'created_at']
    search_fields = ['signatory_name', 'signatory_title', 'signatory_role']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Signatory Information', {
            'fields': ['signatory_name', 'signatory_title', 'signatory_role']
        }),
        ('Signature Data', {
            'fields': ['signature_image', 'signature_type', 'signature_data']
        }),
        ('Settings', {
            'fields': ['is_active', 'is_default', 'created_by']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]


@admin.register(ReportSignature)
class ReportSignatureAdmin(admin.ModelAdmin):
    list_display = ['signatory_name', 'signatory_role', 'report_type', 'report_date', 'signed_at', 'is_verified']
    list_filter = ['report_type', 'signatory_role', 'is_verified', 'signed_at', 'report_date']
    search_fields = ['signatory_name', 'signatory_role']
    readonly_fields = ['signed_at', 'verification_hash']
    date_hierarchy = 'report_date'
    fieldsets = [
        ('Report Information', {
            'fields': ['report_date', 'report_type']
        }),
        ('Signature Information', {
            'fields': ['signature', 'signatory_name', 'signatory_role']
        }),
        ('Signing Details', {
            'fields': ['signed_by', 'signed_at', 'ip_address']
        }),
        ('Verification', {
            'fields': ['is_verified', 'verification_hash']
        })
    ]