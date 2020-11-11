import tempfile

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from prettytable import PrettyTable
from distutils.version import LooseVersion

import os
import logging
from django.conf import settings
from django.utils.module_loading import import_string

from upd.models import Version, Product
from plugins.base import PluginCollection

LOGGER = logging.getLogger(__name__)

class UpdateAllTheThings:

    def __init__(self):
        # load plugins
        self.plugin_collection = PluginCollection('plugins')

    def update_metadata(self):
        products = Product.objects.all()

        print('')
        print(self.plugin_collection.plugins)

        for product in products:
            LOGGER.info(f'Get latest Firmware Version of {product.name}:')
            plugin = import_string(product.plugin)(product.plugin_config)

            available_versions = plugin.get_available_versions(product)
            LOGGER.debug(available_versions)

            for version in available_versions:
                try:
                    Version.objects.get(product=version.product, version=version.version)
                except ObjectDoesNotExist:
                    version.save()

    def get_latest(self, product_name):
        product = Product.objects.get(name=product_name)
        qs_versions = Version.objects.filter(product_id=product.id)
        if len(qs_versions) > 0:
            versions = list(qs_versions.values_list('version', flat=True))
            LOGGER.debug(versions)
            versions.sort(key=LooseVersion, reverse=True)
            return Version.objects.get(product=product, version=versions[0])
        return None

    def get_all_latest(self):
        all_latest = []
        for product in Product.objects.all():
            latest = self.get_latest(product.name)
            if latest:
                all_latest.append(latest)
        return all_latest

    def download_fw_version(self, version):
        plugin_cls = version.product.plugin
        LOGGER.debug(plugin_cls)
        plugin_cls = import_string(plugin_cls)

        print(version)
        print(plugin_cls)

        plugin_cls().dl_fw(version)

        version.last_pulled = timezone.now()
        version.save()
        return version.get_fw_filename()
