import logging
import os
from io import BytesIO

import requests
import datetime
from urllib.parse import urlparse

from django.db.models.fields import files

from upd.models import Version

from plugins.base import Plugin

LOGGER = logging.getLogger(__name__)


class UbiquitiBasePlugin:

    url_base = 'https://www.ui.com'
    url = None

    def get_available_versions(self):
        r = requests.get(self.url, headers={'content-type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'})
        LOGGER.debug(r.json()['downloads'][0])

        available_versions = []
        for x in r.json()['downloads']:
            if len(x['version']) > 0:
                version = x['version'][1:]
                date_published = datetime.datetime.strptime(x['date_published'], '%Y-%m-%d')
                fw_link = self.url_base + '/' + x['file_path']
                available_versions.append(Version(version=version, fw_link=fw_link, date_published=date_published))

        LOGGER.debug(available_versions)
        return available_versions

    def dl_fw(self, version):
        filename = os.path.basename(urlparse(version.fw_link).path)
        response = requests.get(version.fw_link, allow_redirects=True, stream=True)
        response.raise_for_status()

        fp = BytesIO()
        fp.write(response.content)
        version.fw.save(filename, files.File(fp))
        version.save()