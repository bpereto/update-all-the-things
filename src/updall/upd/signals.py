import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from upd.models import Version
from upd.models.notifications import Notification

# pylint: disable=unused-argument
LOGGER = logging.getLogger(__name__)


@receiver(post_save, sender=Version)
def notify_new_version(sender, instance, created, **kwargs):
    """create notification when version is created"""
    message = f"{instance.product} has a new Release: {instance}"
    if created:
        for notification in Notification.objects.all():
            LOGGER.info('send %s for %s', notification, instance)
            notification.notify(subject=instance, message=message)
