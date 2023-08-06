# -*- coding: utf-8 -*-
import pkg_resources
from swapdate import get

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
