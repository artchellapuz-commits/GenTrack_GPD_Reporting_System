from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services.analytics_service import AnalyticsService
import logging

logger = logging.getLogger(__name__)
analytics_service = AnalyticsService()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_trends(request):
    """Get performance trends over time"""
    try:
        plant_id = request.GET.get('plant_id')
        days = int(request.GET.get('days', 30))
        
        data = analytics_service.get_performance_trends(plant_id, days)
        return Response(data)
    except Exception as e:
        logger.error(f"Performance trends error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plant_comparison(request):
    """Compare performance across plants"""
    try:
        from datetime import datetime, timedelta
        
        end_date = request.GET.get('end_date')
        start_date = request.GET.get('start_date')
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        data = analytics_service.get_plant_comparison(start_date, end_date)
        return Response(data)
    except Exception as e:
        logger.error(f"Plant comparison error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predictive_insights(request):
    """Get predictive insights for a plant"""
    try:
        plant_id = request.GET.get('plant_id')
        if not plant_id:
            return Response({'error': 'plant_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        days_ahead = int(request.GET.get('days_ahead', 7))
        
        data = analytics_service.get_predictive_insights(plant_id, days_ahead)
        return Response(data)
    except Exception as e:
        logger.error(f"Predictive insights error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def anomaly_detection(request):
    """Detect anomalies in generation data"""
    try:
        plant_id = request.GET.get('plant_id')
        days = int(request.GET.get('days', 30))
        
        data = analytics_service.get_anomaly_detection(plant_id, days)
        return Response(data)
    except Exception as e:
        logger.error(f"Anomaly detection error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def efficiency_analysis(request):
    """Analyze operational efficiency"""
    try:
        plant_id = request.GET.get('plant_id')
        days = int(request.GET.get('days', 30))
        
        data = analytics_service.get_efficiency_analysis(plant_id, days)
        return Response(data)
    except Exception as e:
        logger.error(f"Efficiency analysis error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def water_nomination_analysis(request):
    """Analyze water nomination vs actual generation"""
    try:
        plant_id = request.GET.get('plant_id')
        days = int(request.GET.get('days', 30))
        
        data = analytics_service.get_water_nomination_analysis(plant_id, days)
        return Response(data)
    except Exception as e:
        logger.error(f"Water nomination analysis error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
