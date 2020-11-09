import logging

import requests
import re
from bs4 import BeautifulSoup

from plugins.base import Plugin
from plugins.ubiquiti.base import UbiquitiBasePlugin

LOGGER = logging.getLogger(__name__)


class UbiquitiEdgeRouterLite3(UbiquitiBasePlugin, Plugin):

    name = 'Ubiquiti EdgeMax EdgeRouter Lite 3'
    url = 'https://www.ui.com/download/?product=erlite3'