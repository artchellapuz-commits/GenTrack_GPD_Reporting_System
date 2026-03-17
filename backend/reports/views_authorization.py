"""Views for user-friendly signatory authorization requests"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import SignatoryAuthorization, SignatoryAuthorizationRequest
from .serializers_security import SignatoryAuthorizationSerializer
from .permissions import CanManageSignatureAuthorizations


class SignatoryAuthorizationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing signatory authorizations with user-friendly requests"""
    queryset = SignatoryAuthorization.objects.all()
    serializer_class = SignatoryAuthorizationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter based on user permissions"""
        if self.request.user.is_superuser:
            return self.queryset
        
        # Regular users can only see their own authorizations
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='my-authorizations')
    def my_authorizations(self, request):
        """Get current user's authorizations"""
        authorizations = SignatoryAuthorization.objects.filter(
            user=request.user
        ).order_by('-authorization_date')
        
        serializer = self.get_serializer(authorizations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='my-requests')
    def my_requests(self, request):
        """Get current user's authorization requests"""
        from .serializers_security import SignatoryAuthorizationRequestSerializer
        
        requests = SignatoryAuthorizationRequest.objects.filter(
            user=request.user
        ).order_by('-created_at')
        
        serializer = SignatoryAuthorizationRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='request')
    def request_authorization(self, request):
        """Submit a new authorization request"""
        from .serializers_security import SignatoryAuthorizationRequestSerializer
        
        data = request.data.copy()
        
        # Check if user already has this authorization
        existing_auth = SignatoryAuthorization.objects.filter(
            user=request.user,
            signatory_name=data.get('signatory_name'),
            is_active=True
        ).first()
        
        if existing_auth and existing_auth.is_valid():
            return Response(
                {'error': 'You already have active authorization for this signatory'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Allow multiple requests, but limit to prevent spam
        # Check if user has submitted more than 3 requests for the same signatory in the last 24 hours
        from datetime import timedelta
        recent_requests = SignatoryAuthorizationRequest.objects.filter(
            user=request.user,
            signatory_name=data.get('signatory_name'),
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        if recent_requests >= 3:
            return Response(
                {'error': 'You have reached the maximum number of requests for this signatory today. Please wait 24 hours before submitting another request.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = SignatoryAuthorizationRequestSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            auth_request = serializer.save(user=request.user)
            
            # Send notification to admins
            self._notify_admins_of_request(auth_request)
            
            # Send confirmation email to user
            self._send_confirmation_email(auth_request)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='pending-requests', 
            permission_classes=[IsAuthenticated, CanManageSignatureAuthorizations])
    def pending_requests(self, request):
        """Get all pending authorization requests (admin only)"""
        from .serializers_security import SignatoryAuthorizationRequestSerializer
        
        requests = SignatoryAuthorizationRequest.objects.filter(
            status='PENDING'
        ).order_by('-created_at')
        
        serializer = SignatoryAuthorizationRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='approve-request/(?P<request_id>[^/.]+)',
            permission_classes=[IsAuthenticated, CanManageSignatureAuthorizations])
    def approve_request(self, request, request_id=None):
        """Approve an authorization request (admin only)"""
        try:
            auth_request = SignatoryAuthorizationRequest.objects.get(
                id=request_id,
                status='PENDING'
            )
        except SignatoryAuthorizationRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found or already processed'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        admin_notes = request.data.get('admin_notes', '')
        requires_2fa = request.data.get('requires_2fa', True)
        expiry_date = request.data.get('expiry_date')
        
        # Set expiry date if provided
        if expiry_date:
            from datetime import datetime
            auth_request.expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
        
        auth_request.requires_2fa = requires_2fa
        
        # Approve the request
        authorization = auth_request.approve(request.user, admin_notes)
        
        # Send notification to user
        self._notify_user_of_approval(auth_request, authorization)
        
        # Return the created authorization
        serializer = self.get_serializer(authorization)
        return Response({
            'message': 'Request approved successfully',
            'authorization': serializer.data
        })
    
    @action(detail=False, methods=['post'], url_path='reject-request/(?P<request_id>[^/.]+)',
            permission_classes=[IsAuthenticated, CanManageSignatureAuthorizations])
    def reject_request(self, request, request_id=None):
        """Reject an authorization request (admin only)"""
        try:
            auth_request = SignatoryAuthorizationRequest.objects.get(
                id=request_id,
                status='PENDING'
            )
        except SignatoryAuthorizationRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found or already processed'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        admin_notes = request.data.get('admin_notes', 'Request rejected by administrator')
        
        # Reject the request
        auth_request.reject(request.user, admin_notes)
        
        # Send notification to user
        self._notify_user_of_rejection(auth_request)
        
        return Response({'message': 'Request rejected successfully'})
    
    @action(detail=False, methods=['post'], url_path='cancel-request/(?P<request_id>[^/.]+)')
    def cancel_request(self, request, request_id=None):
        """Cancel an authorization request (user can cancel their own requests)"""
        try:
            auth_request = SignatoryAuthorizationRequest.objects.get(
                id=request_id,
                status='PENDING'
            )
        except SignatoryAuthorizationRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found or already processed'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user can cancel this request
        if auth_request.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only cancel your own requests'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update request status to cancelled
        auth_request.status = 'CANCELLED'
        auth_request.reviewed_by = request.user
        auth_request.reviewed_at = timezone.now()
        auth_request.admin_notes = 'Request cancelled by user'
        auth_request.save()
        
        return Response({'message': 'Request cancelled successfully'})
    
    def _notify_admins_of_request(self, auth_request):
        """Send email notification to admins about new request"""
        try:
            from django.contrib.auth.models import User
            
            # Get all admin users
            admin_users = User.objects.filter(
                is_staff=True,
                is_active=True,
                email__isnull=False
            ).exclude(email='')
            
            admin_emails = [user.email for user in admin_users]
            
            if not admin_emails:
                print("Warning: No admin emails found for notification")
                return
            
            subject = f'New E-Signature Authorization Request - {auth_request.signatory_name}'
            message = f"""
Dear Data Manager/System Administrator,

A new e-signature authorization request has been submitted and requires your review:

Requestor Information:
- Name: {auth_request.user.get_full_name() or auth_request.user.username}
- Email: {auth_request.email}
- Requested Signatory Name: {auth_request.signatory_name}
- Role: {auth_request.role}

Justification for E-Signature Access:
{auth_request.justification}

Action Required:
Please review and approve/reject this e-signature authorization request in the admin panel:
{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000'}/admin/reports/signatoryauthorizationrequest/

Best regards,
NPC Reporting System
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@npc-reporting.com',
                admin_emails,
                fail_silently=True,
            )
            print(f"Admin notification sent to {len(admin_emails)} administrators")
        except Exception as e:
            print(f"Failed to send admin notification: {e}")
    
    def _send_confirmation_email(self, auth_request):
        """Send confirmation email to user that request was received"""
        try:
            recipient_email = auth_request.email or auth_request.user.email
            if not recipient_email:
                return
            
            # Extract last name from signatory name for professional greeting
            signatory_parts = auth_request.signatory_name.split()
            if len(signatory_parts) > 1:
                # Get the last part before any suffix (JR., SR., etc.)
                last_name = signatory_parts[-1]
                if last_name.upper() in ['JR.', 'JR', 'SR.', 'SR', 'III', 'II']:
                    last_name = signatory_parts[-2] if len(signatory_parts) > 2 else signatory_parts[0]
                greeting = f"Dear {last_name},"
            else:
                greeting = f"Dear {auth_request.signatory_name},"
            
            subject = f'E-Signature Required - {auth_request.signatory_name}'
            message = f"""
{greeting}

The NPC Reporting System requires your e-signature for the following:

Signatory Name: {auth_request.signatory_name}
Role: {auth_request.role}

Reason for E-Signature Request:
{auth_request.justification}

Please coordinate with the Data Manager or System Administrator to complete your e-signature setup for the reporting system.

Best regards,
NPC Reporting System
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@npc-reporting.com',
                [recipient_email],
                fail_silently=True,
            )
            print(f"Confirmation email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send confirmation email: {e}")
    
    def _notify_user_of_approval(self, auth_request, authorization):
        """Send email notification to user about approval"""
        try:
            # Use email from request, fallback to user.email
            recipient_email = auth_request.email or auth_request.user.email
            if not recipient_email:
                return
            
            subject = f'E-Signature Authorization APPROVED - {auth_request.signatory_name}'
            message = f"""
Hello {auth_request.user.get_full_name() or auth_request.user.username},

Great news! Your e-signature authorization request has been APPROVED by the Data Manager/System Administrator!

E-Signature Authorization Details:
- Signatory Name: {auth_request.signatory_name}
- Role: {auth_request.role}
- 2FA Security Required: {'Yes' if authorization.requires_2fa else 'No'}
- Authorization Expires: {authorization.expiry_date.strftime('%B %d, %Y') if authorization.expiry_date else 'Never'}

Your Original Justification:
{auth_request.justification}

You can now use your e-signature:
1. Go to the Generate Report page
2. Click the "e-signature" button next to your name
3. Create your digital e-signature
4. Sign reports electronically with secure 2FA verification

Data Manager/System Administrator Notes: {auth_request.admin_notes}

Your e-signature is now ready for use in the NPC Reporting System!

Best regards,
NPC Reporting System
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@npc-reporting.com',
                [recipient_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send user approval notification: {e}")
    
    def _notify_user_of_rejection(self, auth_request):
        """Send email notification to user about rejection"""
        try:
            # Use email from request, fallback to user.email
            recipient_email = auth_request.email or auth_request.user.email
            if not recipient_email:
                return
            
            subject = f'E-Signature Authorization Request - Additional Information Required'
            message = f"""
Hello {auth_request.user.get_full_name() or auth_request.user.username},

Your e-signature authorization request requires additional information or has been declined by the Data Manager/System Administrator.

E-Signature Request Details:
- Requested Signatory Name: {auth_request.signatory_name}
- Role: {auth_request.role}

Your Original Justification:
{auth_request.justification}

Data Manager/System Administrator Notes: {auth_request.admin_notes}

Next Steps:
- Review the administrator's notes above
- If you need to resubmit your e-signature request with additional information, you can do so through the system
- Contact the Data Manager or System Administrator if you need clarification

If you believe this decision is an error or need further clarification about your e-signature request, please contact the Data Manager or System Administrator directly.

Best regards,
NPC Reporting System
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@npc-reporting.com',
                [recipient_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send user rejection notification: {e}")