"""
Authentication Views
Handles user login, logout, registration, and profile management
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
from .utils import get_location_from_ip, get_client_ip


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view with user details and profile"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = User.objects.get(username=request.data.get('username'))
            # Use UserProfileSerializer to include role and permissions
            from .serializers import UserProfileSerializer
            response.data['user'] = UserProfileSerializer(user).data
            
            # Create audit log for successful login
            from .models import AuditLog
            ip_address = get_client_ip(request)
            location = get_location_from_ip(ip_address)
            
            AuditLog.objects.create(
                user=user,
                action='LOGIN',
                model_name='User',
                description=f'User {user.username} logged in successfully',
                ip_address=ip_address,
                location=location
            )
            
        return response


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints"""
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user by blacklisting refresh token"""
        try:
            # Create audit log for logout
            from .models import AuditLog
            ip_address = get_client_ip(request)
            location = get_location_from_ip(ip_address)
            
            AuditLog.objects.create(
                user=request.user,
                action='LOGOUT',
                model_name='User',
                description=f'User {request.user.username} logged out',
                ip_address=ip_address,
                location=location
            )
            
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Get current user profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update user profile"""
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response({
                    'old_password': ['Wrong password']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.data.get('new_password'))
            user.save()
            
            return Response({
                'message': 'Password updated successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints (admin only)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on permissions"""
        user = self.request.user
        
        # Only admins can see all users
        if user.is_staff or (hasattr(user, 'profile') and user.profile.role == 'ADMIN'):
            return User.objects.all().select_related('profile')
        else:
            # Regular users can only see themselves
            return User.objects.filter(id=user.id).select_related('profile')
    
    def get_permissions(self):
        """Only admins can create, update, or delete users"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            from .permissions import CanManageUsers
            return [CanManageUsers()]
        return super().get_permissions()
