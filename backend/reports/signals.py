"""
Django Signals for automated actions
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UploadedFile, WaterNomination
from .email_service import EmailService
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create user profile when user is created
    """
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f"Created profile for user: {instance.username}")
        
        # Send welcome email
        if instance.email:
            EmailService.notify_user_registered(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save user profile when user is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=UploadedFile)
def notify_upload_status(sender, instance, created, **kwargs):
    """
    Send email notification when file upload status changes
    """
    if not created and instance.uploaded_by:
        # Check if user wants notifications
        if hasattr(instance.uploaded_by, 'profile') and instance.uploaded_by.profile.notify_on_upload:
            if instance.status == 'COMPLETED':
                EmailService.notify_upload_success(instance, instance.uploaded_by)
            elif instance.status == 'FAILED':
                EmailService.notify_upload_failure(instance, instance.uploaded_by, instance.error_message)


@receiver(post_save, sender=WaterNomination)
def notify_nomination_status(sender, instance, created, **kwargs):
    """
    Send email notification when nomination status changes
    """
    if not created:
        # Nomination approved
        if instance.status == 'APPROVED' and instance.approved_by:
            if hasattr(instance.submitted_by, 'profile') and instance.submitted_by.profile.notify_on_approval:
                EmailService.notify_nomination_approved(instance, instance.approved_by)
        
        # Nomination submitted
        elif instance.status == 'SUBMITTED':
            EmailService.notify_nomination_submitted(instance, instance.submitted_by)
