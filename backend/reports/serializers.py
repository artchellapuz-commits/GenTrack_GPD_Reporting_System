from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Plant, Unit, UploadedFile, GenerationReport, PlantCapacity, HistoricalData


class UserSerializer(serializers.ModelSerializer):
    """User serializer for basic user info"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Password fields did not match'
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile with additional info"""
    uploads_count = serializers.SerializerMethodField()
    last_upload = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active', 'date_joined', 'last_login',
            'uploads_count', 'last_upload'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login', 'uploads_count', 'last_upload']
    
    def get_uploads_count(self, obj):
        return obj.uploadedfile_set.count()
    
    def get_last_upload(self, obj):
        last_upload = obj.uploadedfile_set.order_by('-uploaded_at').first()
        if last_upload:
            return {
                'filename': last_upload.original_filename,
                'date': last_upload.uploaded_at,
                'plant': last_upload.plant.code
            }
        return None


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'new_password': 'Password fields did not match'
            })
        return attrs


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


class PlantCapacitySerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    plant_code = serializers.CharField(source='plant.code', read_only=True)
    
    class Meta:
        model = PlantCapacity
        fields = '__all__'


class HistoricalDataSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    plant_code = serializers.CharField(source='plant.code', read_only=True)
    
    class Meta:
        model = HistoricalData
        fields = '__all__'


class HistoricalDataUploadSerializer(serializers.Serializer):
    capacity_file = serializers.FileField(required=False, allow_null=True)
    historical_file = serializers.FileField(required=False, allow_null=True)
    
    def validate(self, data):
        if not data.get('capacity_file') and not data.get('historical_file'):
            raise serializers.ValidationError("At least one file must be provided")
        
        for field in ['capacity_file', 'historical_file']:
            file = data.get(field)
            if file:
                if not file.name.endswith('.xlsx'):
                    raise serializers.ValidationError(f"{field}: Only .xlsx files are allowed")
                if file.size > 52428800:  # 50MB for historical data
                    raise serializers.ValidationError(f"{field}: File size must not exceed 50MB")
        
        return data
