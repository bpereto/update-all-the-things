import logging
import os
import re
from datetime import datetime
from io import BytesIO
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.core import files
from plugins.base import Plugin
from upd.models import Version

LOGGER = logging.getLogger(__name__)


class ZyxelFirmwareHTTPPlugin(Plugin):
    """
    zyxel firmware http plugin
    """

    name = 'ZyXEL HTTP Firmware Plugin'

    url_base = 'https://www.zyxel.com'
    url_path = '/support/DownloadLandingSR.shtml?c=gb&l=en&md={}'

    def get_available_versions(self, product):
        """
        get available versions
        :param product:
        :return:
        """
        zyxel_product_name = self.plugin_config['zyxel_product_name']
        url = self.url_base + self.url_path.format(zyxel_product_name)

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        dl_links = soup.find_all('a', attrs={'data-target': '#downloadModal', 'data-filelink': re.compile('.*')})

        available_versions = []
        for link in dl_links:
            LOGGER.debug(link)
            fw_version = link.get('data-version')
            # rd=Sep 29, 2020
            fw_date_published = datetime.strptime(re.match('.*&rd=(.*)&.*', link.get('onclick')).group(1), '%b %d, %Y')
            available_versions.append(Version(version=fw_version, fw_link=link.get('data-filelink'), date_published=fw_date_published, product=product))

        return available_versions

    def dl_fw(self, version):  # pylint: disable=no-self-use
        """
        download fw
        :param version:
        :return:
        """
        response = requests.get(version.fw_link, allow_redirects=True, stream=True)
        response.raise_for_status()
        filename = os.path.basename(urlparse(version.fw_link).path)

        fp = BytesIO()
        fp.write(response.content)
        version.fw.save(filename, files.File(fp))
        version.save()
