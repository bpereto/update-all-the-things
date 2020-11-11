import logging
from datetime import datetime
from ftplib import FTP

from plugins.base import Plugin

LOGGER = logging.getLogger(__name__)

# TODO: WIP.
# pylint: skip-file

class ZyxelFirmwareFTPPlugin():
    """
    Zyxel Firmware FTP Plugin
    """

    name = 'ZyXEL FTP Firmware Plugin'

    ftp_url = 'ftp.zyxel.com'

    def _parse_ftp_dir(self, line):  # pylint: disable=no-self-use
        """
        parse ftp output of "LIST"
        :param line:
        :return:
        """
        words = line.split()
        filename = words[8]
        size = int(words[4])
        t = words[7].split(':')
        ts = words[5] + '-' + words[6] + '-' + datetime.datetime.now().strftime('%Y') + ' ' + t[0] + ':' + t[1]
        timestamp = datetime.datetime.strptime(ts, '%b-%d-%Y %H:%M')

    def get_available_versions(self, product):
        """
        get available versions
        :param product:
        :return:
        """
        zyxel_product_name = self.plugin_config['zyxel_product_name']

        ftp = FTP(self.ftp_url)
        ftp.login(user='anonymous', passwd='anonymous')
        ftp.cwd(zyxel_product_name + '/' + 'firmware')

        ftp.retrlines('LIST', callback=self.parse_dir_line)

    def dl_fw(self, version):
        """
        download firmware
        :param version:
        :return:
        """
        pass
