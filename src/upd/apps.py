from django.apps import AppConfig, apps
from django.contrib import admin


class UpdConfig(AppConfig):
    """
    appconfig
    """
    name = 'upd'

    def ready(self):
        import upd.signals  # pylint: disable=import-outside-toplevel,unused-import
        models = apps.get_models()

        for model in models:
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass
