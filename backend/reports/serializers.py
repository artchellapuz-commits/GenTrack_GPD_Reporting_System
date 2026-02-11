from rest_framework import serializers
from .models import Plant, Unit, UploadedFile, GenerationReport


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    
    class Meta:
        model = Unit
        fields = '__all__'


class UploadedFileSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at', 'status', 'records_imported', 'checksum']


class GenerationReportSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    plant_code = serializers.CharField(source='plant.code', read_only=True)
    unit_number = serializers.IntegerField(source='unit.unit_number', read_only=True)
    
    class Meta:
        model = GenerationReport
        fields = '__all__'


class GenerationReportListSerializer(serializers.ModelSerializer):
    """Optimized serializer for list views"""
    plant_code = serializers.CharField(source='plant.code')
    unit_number = serializers.IntegerField(source='unit.unit_number')
    
    class Meta:
        model = GenerationReport
        fields = ['id', 'plant_code', 'unit_number', 'report_date', 'generation_kwh', 
                  'operating_hours', 'capacity_factor', 'availability_factor']


class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    plant_code = serializers.ChoiceField(choices=['AGUS1', 'AGUS2', 'AGUS4', 'AGUS5', 'AGUS6', 'AGUS7'])
    
    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Only .xlsx files are allowed")
        
        if value.size > 10485760:  # 10MB
            raise serializers.ValidationError("File size must not exceed 10MB")
        
        return value


class ReportGenerationSerializer(serializers.Serializer):
    plant_codes = serializers.ListField(
        child=serializers.ChoiceField(choices=['AGUS1', 'AGUS2', 'AGUS4', 'AGUS5', 'AGUS6', 'AGUS7']),
        allow_empty=False
    )
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    report_type = serializers.ChoiceField(choices=['daily', 'monthly', 'consolidated'])
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start_date must be before end_date")
        return data
