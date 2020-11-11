import datetime
import logging
import os
from io import BytesIO
from urllib.parse import urlparse

import requests
from django.db.models.fields import files
from plugins.base import Plugin
from upd.models import Version

LOGGER = logging.getLogger(__name__)

# pylint: disable=import-outside-toplevel,R0801


class UbiquitiFirmwarePlugin(Plugin):
    """
    Ubiquiti Firmware Plugin
    """

    name = 'Ubiquiti Firmware Plugin'
    url_base = 'https://www.ui.com'
    url_pattern = '/download/?product={}'

    def get_available_versions(self, product):
        """
        get available versions for a product
        :param product:
        :return:
        """
        url = self.url_base + self.url_pattern.format(self.plugin_config['ubiquiti_product_filter'])
        r = requests.get(url, headers={'content-type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'})
        LOGGER.debug(r.json()['downloads'][0])

        available_versions = []
        for x in r.json()['downloads']:
            if len(x['version']) > 0:
                version = x['version'][1:]
                date_published = datetime.datetime.strptime(x['date_published'], '%Y-%m-%d')
                fw_link = self.url_base + '/' + x['file_path']
                available_versions.append(Version(version=version, fw_link=fw_link, date_published=date_published, product=product))

        LOGGER.debug(available_versions)
        return available_versions

    def dl_fw(self, version):  # pylint: disable=no-self-use
        """
        download fw
        :param version:
        :return:
        """
        filename = os.path.basename(urlparse(version.fw_link).path)
        response = requests.get(version.fw_link, allow_redirects=True, stream=True)
        response.raise_for_status()

        fp = BytesIO()
        fp.write(response.content)
        version.fw.save(filename, files.File(fp))
        version.save()
