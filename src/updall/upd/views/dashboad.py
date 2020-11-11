import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from upd.lib import UpdateAllTheThings
from upd.models import Version

# pylint: disable=broad-except
LOGGER = logging.getLogger(__name__)


class DashboardView(ListView):
    """dashboad view"""

    model = Version
    template_name = 'upd/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        upd = UpdateAllTheThings()
        context['object_latest'] = upd.get_all_latest()
        return context


class FWPullView(View):
    """
    view to pull fw
    """

    def get(self, request, *args,  pk=None, **kwargs):  # pylint: disable=unused-argument
        """pull fw"""
        version = Version.objects.get(id=pk)
        upd = UpdateAllTheThings()
        try:
            fw_name = upd.download_fw_version(version)
        except Exception as exc:
            LOGGER.exception(exc)
            messages.add_message(request, messages.ERROR, f'Failed to pull {version}')
        messages.add_message(request, messages.INFO, f'Pulled {fw_name}')
        return redirect(reverse('dashboard'))


class RefreshMetadata(View):
    """
    refresh metadata, fetch versions for products
    """

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """fetch metadata"""

        upd = UpdateAllTheThings()
        try:
            upd.update_metadata()
        except Exception as exc:
            LOGGER.exception(exc)
            messages.add_message(request, messages.ERROR, f'Failed to update metadata: {exc}')
        messages.add_message(request, messages.INFO, 'Updated Metadata')
        return redirect(reverse('dashboard'))
