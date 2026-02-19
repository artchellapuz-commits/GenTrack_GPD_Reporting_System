from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from .models_scheduled import ScheduledReport, ReportExecution
from .serializers_scheduled import ScheduledReportSerializer, ReportExecutionSerializer
from .services.automated_reports import AutomatedReportService
import logging

logger = logging.getLogger(__name__)


class ScheduledReportViewSet(viewsets.ModelViewSet):
    """ViewSet for managing scheduled reports"""
    queryset = ScheduledReport.objects.all()
    serializer_class = ScheduledReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter reports based on user permissions"""
        user = self.request.user
        
        # Admins and managers see all reports
        if user.is_staff or (hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'MANAGER']):
            return ScheduledReport.objects.all()
        
        # Others see reports they created or are recipients of
        return ScheduledReport.objects.filter(
            models.Q(created_by=user) | models.Q(recipients=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Set created_by when creating report"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        """Manually trigger report execution"""
        try:
            scheduled_report = self.get_object()
            service = AutomatedReportService()
            
            success = service.execute_report(scheduled_report)
            
            if success:
                return Response({
                    'message': 'Report execution started successfully',
                    'report_id': scheduled_report.id
                })
            else:
                return Response({
                    'error': 'Report execution failed'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Manual report execution error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def executions(self, request, pk=None):
        """Get execution history for a report"""
        try:
            scheduled_report = self.get_object()
            executions = ReportExecution.objects.filter(
                scheduled_report=scheduled_report
            ).order_by('-started_at')[:50]
            
            serializer = ReportExecutionSerializer(executions, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Get executions error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing report execution history"""
    queryset = ReportExecution.objects.all()
    serializer_class = ReportExecutionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter executions based on user permissions"""
        user = self.request.user
        
        # Admins and managers see all executions
        if user.is_staff or (hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'MANAGER']):
            return ReportExecution.objects.all()
        
        # Others see executions of reports they have access to
        return ReportExecution.objects.filter(
            models.Q(scheduled_report__created_by=user) | 
            models.Q(scheduled_report__recipients=user)
        ).distinct()
