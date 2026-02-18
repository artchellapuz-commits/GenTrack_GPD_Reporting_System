from django.contrib import admin
from .models import Plant, Unit, UploadedFile, GenerationReport, Testimonial


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'capacity_mw', 'location', 'is_active']
    list_filter = ['is_active', 'code']
    search_fields = ['code', 'name', 'location']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['plant', 'unit_number', 'capacity_mw', 'is_active']
    list_filter = ['plant', 'is_active']
    search_fields = ['plant__code', 'unit_number']


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'plant', 'uploaded_by', 'uploaded_at', 'status', 'records_imported']
    list_filter = ['status', 'plant', 'uploaded_at']
    search_fields = ['original_filename', 'uploaded_by__username']
    readonly_fields = ['uploaded_at', 'checksum', 'file_size']


@admin.register(GenerationReport)
class GenerationReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'plant', 'unit', 'generation_kwh', 'capacity_factor', 'availability_factor']
    list_filter = ['plant', 'report_date', 'unit']
    search_fields = ['plant__code', 'unit__unit_number']
    date_hierarchy = 'report_date'
    readonly_fields = ['capacity_factor', 'availability_factor', 'created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'plant', 'rating', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'rating', 'created_at']
    search_fields = ['name', 'position', 'plant', 'testimonial']
    list_editable = ['is_active', 'order']
    ordering = ['order', '-created_at']
