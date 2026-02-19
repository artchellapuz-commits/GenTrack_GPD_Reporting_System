"""
Custom Middleware for Audit Logging and Request Tracking
"""

from .models import AuditLog
import logging

logger = logging.getLogger(__name__)


class AuditLogMiddleware:
    """
    Middleware to log user actions for audit trail
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Log important actions
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.log_action(request, response)
        
        return response
    
    def log_action(self, request, response):
        """Log user action to audit trail"""
        try:
            # Only log successful actions
            if response.status_code < 400:
                action = self.get_action_type(request.method)
                model_name = self.extract_model_name(request.path)
                
                if action and model_name:
                    AuditLog.objects.create(
                        user=request.user,
                        action=action,
                        model_name=model_name,
                        description=f"{action} {model_name} via {request.method} {request.path}",
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
                    )
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
    
    def get_action_type(self, method):
        """Map HTTP method to action type"""
        mapping = {
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE',
        }
        return mapping.get(method)
    
    def extract_model_name(self, path):
        """Extract model name from request path"""
        # Simple extraction from path like /api/plants/ -> Plant
        parts = path.strip('/').split('/')
        if len(parts) >= 2:
            model = parts[1].rstrip('s').capitalize()
            return model
        return 'Unknown'
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
