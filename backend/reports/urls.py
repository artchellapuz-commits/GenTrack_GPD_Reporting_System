from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlantViewSet, UnitViewSet, UploadedFileViewSet, 
    GenerationReportViewSet, HistoricalDataViewSet, PlantCapacityViewSet,
    WaterNominationViewSet, ActualGenerationViewSet, TestimonialViewSet, AuditLogViewSet
)
from .auth_views import AuthViewSet, UserViewSet

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
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
