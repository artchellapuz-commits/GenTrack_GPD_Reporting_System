"""
Custom Permissions for Role-Based Access Control
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission for admin users only
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsManagerOrAdmin(permissions.BasePermission):
    """
    Permission for managers and admins
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user is admin
        if request.user.is_staff:
            return True
        
        # Check if user has manager role
        return hasattr(request.user, 'profile') and request.user.profile.role in ['MANAGER', 'ADMIN']


class IsOperatorOrAbove(permissions.BasePermission):
    """
    Permission for operators, managers, and admins
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins always have access
        if request.user.is_staff:
            return True
        
        # Check user role
        if hasattr(request.user, 'profile'):
            return request.user.profile.role in ['OPERATOR', 'MANAGER', 'ADMIN']
        
        return False


class CanUploadData(permissions.BasePermission):
    """
    Permission to upload data - operators and above
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True
        
        if hasattr(request.user, 'profile'):
            return request.user.profile.role in ['OPERATOR', 'MANAGER', 'ADMIN']
        
        return False


class CanApproveData(permissions.BasePermission):
    """
    Permission to approve data - managers and admins only
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True
        
        if hasattr(request.user, 'profile'):
            return request.user.profile.role in ['MANAGER', 'ADMIN']
        
        return False


class CanExportData(permissions.BasePermission):
    """
    Permission to export data - all authenticated users
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanManageUsers(permissions.BasePermission):
    """
    Permission to manage users - admins only
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner or admin
        if request.user.is_staff:
            return True
        
        # Check if object has uploaded_by or submitted_by field
        if hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        elif hasattr(obj, 'submitted_by'):
            return obj.submitted_by == request.user
        
        return False
