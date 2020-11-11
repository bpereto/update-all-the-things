from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView
from upd.views.dashboad import DashboardView, FWPullView, RefreshMetadata

urlpatterns = [
    path('', RedirectView.as_view(url='dashboard', permanent=False), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('version/<int:pk>/pull', FWPullView.as_view(), name='fw-pull'),
    path('metadata/refresh', RefreshMetadata.as_view(), name='refresh-metadata'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
