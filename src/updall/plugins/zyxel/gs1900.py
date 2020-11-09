import logging
import os
from io import BytesIO

import requests
import re
from bs4 import BeautifulSoup
from django.core import files

from upd.models import Version
from plugins.base import Plugin

LOGGER = logging.getLogger(__name__)


class ZyxelGS1900(Plugin):

    name = 'ZyXEL GS1900'

    version = '[a-z0-9]+'
    fw_domain = 'https://www.zyxel.ch'
    fw_index = f'{fw_domain}/de/business-products/switches/gs1900-series/downlods'
    fw_found = False

    def __init__(self, version='8', fw_index=None):
        self.version = version
        if fw_index:
            self.fw_index = fw_index

    @staticmethod
    def _get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename="(.+)"', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def get_available_versions(self):
        req = requests.get(self.fw_index)
        soup = BeautifulSoup(req.content, 'html.parser')
        dl_links = soup.find_all('a', attrs={'data-type': 'Download firmware'})

        # pattern = ZyXEL GS1900-10HP, Firmware, Version 2.60(AAZI.2)C0
        pattern = '^({}-{}), Firmware, Version (.*)$'.format(self.name, self.version)
        available_versions = []
        for link in dl_links:
            LOGGER.debug(link.text)
            match = re.search(pattern, link.text)
            if match:
                LOGGER.debug('found: ' + str(link))
                fw_version = match.group(2)
                available_versions.append(Version(version=fw_version, fw_link=self.fw_domain + '/' + link.get('href')))

        LOGGER.debug(available_versions)
        return available_versions

    def dl_fw(self, version):
        response = requests.get(version.fw_link, allow_redirects=True, stream=True)
        response.raise_for_status()
        filename = ZyxelGS1900._get_filename_from_cd(response.headers.get('content-disposition'))

        fp = BytesIO()
        fp.write(response.content)
        version.fw.save(filename, files.File(fp))
        version.save()