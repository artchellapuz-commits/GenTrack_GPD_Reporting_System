from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, UnitViewSet, UploadedFileViewSet, GenerationReportViewSet

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'uploaded-files', UploadedFileViewSet, basename='uploadedfile')
router.register(r'generation-reports', GenerationReportViewSet, basename='generationreport')

urlpatterns = [
    path('', include(router.urls)),
]
