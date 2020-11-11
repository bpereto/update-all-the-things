import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from upd.lib import UpdateAllTheThings
from upd.models import Version
from django.contrib import messages

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

    def get(self, request, pk=None, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
        upd = UpdateAllTheThings()
        try:
            upd.update_metadata()
        except Exception as exc:
            LOGGER.exception(exc)
            messages.add_message(request, messages.ERROR, f'Failed to update metadata: {exc}')
        messages.add_message(request, messages.INFO, 'Updated Metadata')
        return redirect(reverse('dashboard'))
