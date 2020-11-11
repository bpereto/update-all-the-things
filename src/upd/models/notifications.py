import logging

from django.conf import settings
from django.core import mail
from django.db import models
from polymorphic.models import PolymorphicModel

from upd.lib.notification import Pushover

LOGGER = logging.getLogger(__name__)

# pylint: disable=arguments-differ,no-member
__all__ = [
    'Notification',
    'EmailNotification',
    'PushoverNotification'
]


class Notification(PolymorphicModel):
    """
    notification base class for notification types
    email, pushover, get/post webhooks
    """

    def notify(self, *args, **kwargs):
        '''
        execute notification
        '''
        raise NotImplementedError()


class EmailNotification(Notification):
    """
    email notification
    """
    # pylint: disable=R0201

    n_type = 'email'

    email = models.EmailField()

    def __str__(self):
        return 'EmailNotification: {}'.format(self.email)

    def get_test_params(self):
        """get params for test notification"""
        return {'subject': 'test notification', 'message': 'friendly test notification from update-all-the-things'}

    def notify(self, subject, message):
        """send email"""
        LOGGER.debug('send email notification: "%s" to %s',
                     subject, self.email)

        mail.send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[self.email],
            fail_silently=False
        )


class PushoverNotification(Notification):
    """
    pushover notification
    """
    # pylint: disable=R0201
    n_type = 'pushover'

    name = models.CharField(max_length=256)
    token = models.CharField(max_length=256)
    user = models.CharField(max_length=256)

    def __str__(self):
        return 'PushoverNotification: {}'.format(self.name)

    def get_test_params(self):
        """get params for test notification"""
        return {'message': 'friendly test notification from update-all-the-things'}

    def notify(self, message, *args, **kwargs):
        """pushover to the rescue"""
        LOGGER.debug('send pushover notification: "%s" to %s',
                     self.name, self.user)

        pushover = Pushover(self.user, self.token)
        pushover.push(message=message, *args, **kwargs)
