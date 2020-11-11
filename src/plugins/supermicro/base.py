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

# pylint: disable=import-outside-toplevel,duplicate-code

LOGGER = logging.getLogger(__name__)


class SupermicroBasePlugin:
    """
    Supermicro Base Plugin
    """

    name = 'Supermicro Base Plugin'

    url_base = 'https://www.supermicro.com'
    url_path = None
    fw_get_url = 'https://www.supermicro.com/support/resources/getfile.php?SoftwareItemID='
    plugin_config = {}

    def get_request_data(self, *args, **kwargs):  # pylint: disable=unused-argument,no-self-use
        """
        get the parameters for request
        :param args:
        :return:
        """
        return {}

    def get_available_versions(self, product):
        """
        get available versions for product
        :param product:
        :return:
        """
        url = self.url_base + self.url_path

        data = self.get_request_data(**self.plugin_config)

        req = requests.post(url, data)
        soup = BeautifulSoup(req.content, 'html.parser')

        # find bios fw product id
        pattern = r'\/about\/policies\/disclaimer\.cfm\?SoftwareItemID\=(.*)'
        href = re.compile(pattern)
        fw_links = soup.find_all('a', href=href)
        LOGGER.debug(fw_links)

        available_versions = []

        for link in fw_links:
            match = re.search(pattern, link.get('href'))
            fw_id = match.group(1)
            fw_version = link.find_parent().find_next('td', text=re.compile('.*Revision:.*')).find_next('td').text
            available_versions.append(Version(version=fw_version, fw_link=self.fw_get_url + fw_id, product=product))

        return available_versions


    def dl_fw(self, version):  # pylint: disable=no-self-use
        """
        download fw
        :param version:
        :return:
        """
        response = requests.get(version.fw_link, allow_redirects=True, stream=True)
        response.raise_for_status()

        filename = os.path.basename(urlparse(response.url).path)
        fp = BytesIO()
        fp.write(response.content)
        version.fw.save(filename, files.File(fp))
        version.save()


class SupermicroBIOSFirmwarePlugin(SupermicroBasePlugin, Plugin):
    """
    supermicro bios firmeware plugin
    """

    name = 'Supermicro BIOS Firmware Plugin'
    url_path = '/support/resources/results.aspx'

    def get_request_data(self, *args, **kwargs):
        return {
            'ProductName': kwargs['supermicro_product_name'],
            'Category': 'MB',
            'GetBIOS': 'Get+BIOS',
            'ProductID': kwargs['supermicro_product_id']
        }

class SupermicroBMCFirmwarePlugin(SupermicroBasePlugin, Plugin):
    """
    supermicro bmc firmware
    """

    name = 'Supermicro BMC Firmware Plugin'
    url_path = '/support/bios/firmware.aspx'

    def get_request_data(self, *args, **kwargs):
        return {
            'ProductName': kwargs['supermicro_product_name'],
            'Resource': 'BIOS',
            'GetBMC': 'Get+BMC+Firmware',
            'ProductID': kwargs['supermicro_product_id']
        }
