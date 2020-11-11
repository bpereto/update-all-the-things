import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from upd.models import Version
from upd.models.notifications import Notification

LOGGER = logging.getLogger(__name__)


@receiver(post_save, sender=Version)
def notify_new_version(sender, instance, created, **kwargs):
    """create notification when version is created"""
    message = f"{instance.product} has a new Release: {instance}"
    if created:
        for notification in Notification.objects.all():
            LOGGER.info(f'send {notification} for {instance}')
            notification.notify(subject=instance, message=message)