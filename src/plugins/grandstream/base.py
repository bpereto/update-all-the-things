import logging
import os
import re
from io import BytesIO
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.core import files
from plugins.base import Plugin
from upd.models import Version

# pylint: disable=import-outside-toplevel,R0801

LOGGER = logging.getLogger(__name__)


class GrandstreamFirmwarePlugin(Plugin):
    """
    Grandstream Firmware Plugin
    """

    name = 'Grandstream Firmware Plugin'

    fw_url_pattern = 'http://firmware.grandstream.com/Release_{}_(.*).zip$'
    url_base = 'http://www.grandstream.com'
    url_path = '/support/firmware/'


    def get_available_versions(self, product):
        """
        get available versions of product
        :param product:
        :return:
        """
        url = self.url_base + self.url_path
        grandstream_product_name = self.plugin_config['grandstream_product_name']

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        href = re.compile(self.fw_url_pattern.format(grandstream_product_name))
        dl_links = soup.find_all('a', href=href)

        available_versions = []
        for link in dl_links:
            match = re.search(href, link.get('href'))
            LOGGER.debug('found fw version %s', str(match.group(1)))
            fw_version = match.group(1)
            available_versions.append(Version(version=fw_version, fw_link=link.get('href'), product=product))
        return available_versions

    def dl_fw(self, version):  # pylint: disable=no-self-use
        """
        download firmware
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
