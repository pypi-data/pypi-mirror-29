#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SetupTools Script
#
# Copyright (C) 2017-2018 Chris Caron <lead2gold@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

import os
try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

from setuptools import find_packages

# This chunk of code allows us to fetch our version
import sys
from os.path import abspath
from os.path import dirname
from os.path import join
sys.path.insert(0, join(abspath(dirname(__file__)), 'apprise'))
from apprise import __version__ as version


install_options = os.environ.get("APPRISE_INSTALL", "").split(",")
libonly_flags = set(["lib-only", "libonly", "no-cli", "without-cli"])
if libonly_flags.intersection(install_options):
    console_scripts = []
else:
    console_scripts = ['apprise = apprise:_main']

setup(
    name='apprise',
    version=version,
    description='A universal notification service',
    license='GPLv3',
    long_description=open('README').read(),
    url='https://github.com/caronc/apprise',
    keywords='push notifications email boxcar faast growl Join KODI '
        'Mattermost NotifyMyAndroid Prowl Pushalot PushBullet Pushjet '
        'Pushover Rocket.Chat Slack Toasty Telegram Twitter XBMC Stride '
        'Emby IFTTT',
    author='Chris Caron',
    author_email='lead2gold@gmail.com',
    packages=find_packages(),
    package_data={
        'apprise': [
            'assets/NotifyXML-1.0.xsd',
            'assets/themes/default/*.png',
        ],
    },
    scripts=['cli/notify.py', ],
    install_requires=open('requirements.txt').readlines(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ),
    entry_points={'console_scripts': console_scripts},
    python_requires='>=2.7',
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'coverage', 'pytest-cov', 'pycodestyle', 'tox'],
)
