"""Serializers for signature security models"""
from rest_framework import serializers
from .models import (
    SignatoryAuthorization, SignatureAuditLog, 
    SignatureVerificationToken, SignatureSecuritySettings,
    SignatoryAuthorizationRequest
)


class SignatoryAuthorizationSerializer(serializers.ModelSerializer):
    """Serializer for signatory authorizations"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    authorized_by_username = serializers.CharField(source='authorized_by.username', read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = SignatoryAuthorization
        fields = [
            'id', 'user', 'user_username', 'signatory_name',
            'authorized_by', 'authorized_by_username', 'authorization_date',
            'expiry_date', 'is_active', 'requires_2fa', 'notes', 'is_valid'
        ]
        read_only_fields = ['id', 'authorization_date', 'user_username', 'authorized_by_username']
    
    def get_is_valid(self, obj):
        """Check if authorization is currently valid"""
        return obj.is_valid()


class SignatureAuditLogSerializer(serializers.ModelSerializer):
    """Serializer for signature audit logs"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = SignatureAuditLog
        fields = [
            'id', 'user', 'user_username', 'action', 'action_display',
            'signature', 'report_signature', 'ip_address', 'user_agent',
            'device_fingerprint', 'geolocation', 'success', 'failure_reason',
            'additional_data', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp', 'user_username', 'action_display']


class SignatureVerificationTokenSerializer(serializers.ModelSerializer):
    """Serializer for 2FA verification tokens"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = SignatureVerificationToken
        fields = [
            'id', 'user', 'user_username', 'token', 'signature_intent',
            'created_at', 'expires_at', 'is_used', 'verified_at',
            'attempts', 'max_attempts', 'ip_address', 'is_valid'
        ]
        read_only_fields = ['id', 'created_at', 'user_username', 'is_valid']
        extra_kwargs = {
            'secret': {'write_only': True},
            'token': {'write_only': True}
        }
    
    def get_is_valid(self, obj):
        """Check if token is still valid"""
        return obj.is_valid()


class SignatureSecuritySettingsSerializer(serializers.ModelSerializer):
    """Serializer for signature security settings"""
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    
    class Meta:
        model = SignatureSecuritySettings
        fields = [
            'id', 'require_2fa_for_all', 'otp_validity_minutes', 'max_otp_attempts',
            'max_signatures_per_hour', 'max_signatures_per_day',
            'audit_retention_days', 'log_geolocation',
            'enable_encryption', 'enable_verification_hash', 'require_device_fingerprint',
            'notify_on_signature', 'notify_on_suspicious',
            'updated_at', 'updated_by', 'updated_by_username'
        ]
        read_only_fields = ['id', 'updated_at', 'updated_by_username']


class Request2FASerializer(serializers.Serializer):
    """Serializer for requesting 2FA code"""
    signatory_name = serializers.CharField(max_length=100)
    signature_intent = serializers.JSONField()


class Verify2FASerializer(serializers.Serializer):
    """Serializer for verifying 2FA code"""
    token_id = serializers.IntegerField()
    otp_code = serializers.CharField(max_length=6)
    device_fingerprint = serializers.CharField(required=False, allow_blank=True)


class SignatoryAuthorizationRequestSerializer(serializers.ModelSerializer):
    """Serializer for user-friendly authorization requests"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SignatoryAuthorizationRequest
        fields = [
            'id', 'user', 'user_username', 'user_full_name', 'email',
            'signatory_name', 'role', 'justification', 'status', 'status_display',
            'reviewed_by', 'reviewed_by_username', 'reviewed_at', 'admin_notes',
            'requires_2fa', 'expiry_date', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_username', 'user_full_name',
            'status', 'status_display', 'reviewed_by', 'reviewed_by_username', 
            'reviewed_at', 'admin_notes', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        # User is passed from the view, don't override it
        return super().create(validated_data)
