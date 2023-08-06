#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for swapdate.

    This file was generated with PyScaffold 2.5.6, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup


def setup_package():
    setup(name='swapdate',
			version='0.4',
			author = 'Vijay Lingam',
			author_email = 'jvlingam@gmail.com',
			url = 'https://github.com/jvlingam/swapdate',
			description = "Swap the current date from one format into different format",
			license="VijayLingam",
			platforms='All',
			long_description = """
			========
			swapdate
			========


			Library to convert and get different format of date & time


			Description
			===========

			Library to convert and get different format of date & time

			Available Formats
			==================

			# Days (D) – 173 (Julian) # European (E) – 22/06/16 # European (EX) – 22/06/2016 # Month (M) – Jun # Month (MX) – June # Normal (N) – 22 Jun 2002 # Normal (NX) – 22 June 2002 # Ordered (O) – 16/06/22 # Ordered (OX) – 2016/06/22 # Standard (S) – 160622 # Standard (SX) – 20160622 # USA (U) – 06/22/16 # USA (UX) – 06/22/2016 # Weekday (W) – Sat # Weekday (WX) – Saturday # Time (T12) – 01:56 PM # Time (T12X) – 01:56:00 PM # Time (T12XX) – 01:56:00:000000 PM # Time (T24) – 13:56 PM # Time (T24X) – 13:56:00 PM # Time (T24XX) – 13:56:00:000000 PM # Default – 03/23/16 14:23:56

			Example
			========

			swapdate.get(“E”)
			output –> 22/06/16
			""",
			include_package_data=True,
			packages = ['swapdate'],
			setup_requires=[])


if __name__ == "__main__":
    setup_package()
