from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlantViewSet, UnitViewSet, UploadedFileViewSet, 
    GenerationReportViewSet, HistoricalDataViewSet, PlantCapacityViewSet,
    WaterNominationViewSet, ActualGenerationViewSet, TestimonialViewSet, AuditLogViewSet,
    ESignatureViewSet, ReportSignatureViewSet
)
from .views_authorization import SignatoryAuthorizationViewSet
from .views_signature import DocumentViewSet, SignatureRequestViewSet, DigitalSignatureViewSet, SigningViewSet
from .auth_views import AuthViewSet, UserViewSet, PasswordResetRequestViewSet
from .views_scheduled import ScheduledReportViewSet, ReportExecutionViewSet
from .views_analytics import (
    performance_trends, plant_comparison, predictive_insights,
    anomaly_detection, efficiency_analysis, water_nomination_analysis
)

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'uploaded-files', UploadedFileViewSet, basename='uploadedfile')
router.register(r'generation-reports', GenerationReportViewSet, basename='generationreport')
router.register(r'historical-data', HistoricalDataViewSet, basename='historicaldata')
router.register(r'plant-capacity', PlantCapacityViewSet, basename='plantcapacity')
router.register(r'water-nominations', WaterNominationViewSet, basename='waternomination')
router.register(r'actual-generations', ActualGenerationViewSet, basename='actualgeneration')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')
router.register(r'e-signatures', ESignatureViewSet, basename='esignature')
router.register(r'report-signatures', ReportSignatureViewSet, basename='reportsignature')
router.register(r'signatory-authorizations', SignatoryAuthorizationViewSet, basename='signatoryauthorization')

# E-signature workflow routes
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'signature-requests', SignatureRequestViewSet, basename='signaturerequest')
router.register(r'digital-signatures', DigitalSignatureViewSet, basename='digitalsignature')
router.register(r'signing', SigningViewSet, basename='signing')

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='user')
router.register(r'password-reset-requests', PasswordResetRequestViewSet, basename='password-reset-request')
router.register(r'scheduled-reports', ScheduledReportViewSet, basename='scheduledreport')
router.register(r'report-executions', ReportExecutionViewSet, basename='reportexecution')

urlpatterns = [
    path('', include(router.urls)),
    # Analytics endpoints
    path('analytics/trends/', performance_trends, name='analytics-trends'),
    path('analytics/comparison/', plant_comparison, name='analytics-comparison'),
    path('analytics/predictions/', predictive_insights, name='analytics-predictions'),
    path('analytics/anomalies/', anomaly_detection, name='analytics-anomalies'),
    path('analytics/efficiency/', efficiency_analysis, name='analytics-efficiency'),
    path('analytics/water-nomination/', water_nomination_analysis, name='analytics-water-nomination'),
]
