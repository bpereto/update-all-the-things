from django.apps import AppConfig
from django.apps import apps
from django.contrib import admin


class UpdConfig(AppConfig):
    name = 'upd'

    def ready(self):
        models = apps.get_models()

        for model in models:
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass