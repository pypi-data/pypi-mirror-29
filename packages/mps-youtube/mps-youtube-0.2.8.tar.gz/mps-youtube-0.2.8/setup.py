#!/usr/bin/python3

""" setup.py for mps-youtube.

https://np1.github.com/mps-youtube

python setup.py sdist bdist_wheel
"""

import sys
import os

if sys.version_info < (3,0):
    sys.exit("Mps-youtube requires python 3.")

from setuptools import setup

VERSION = "0.2.8"

options = dict(
    name="mps-youtube",
    version=VERSION,
    description="Terminal based YouTube player and downloader",
    keywords=["video", "music", "audio", "youtube", "stream", "download"],
    author="np1",
    author_email="np1nagev@gmail.com",
    url="https://github.com/mps-youtube/mps-youtube",
    download_url="https://github.com/mps-youtube/mps-youtube/archive/v%s.tar.gz" % VERSION,
    packages=['mps_youtube', 'mps_youtube.commands', 'mps_youtube.listview'],
    entry_points={'console_scripts': ['mpsyt = mps_youtube:main.main']},
    install_requires=['pafy >= 0.3.82, != 0.4.0, != 0.4.1, != 0.4.2'],
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Multimedia :: Video",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS 9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: Microsoft :: Windows :: Windows Vista",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    options={
        "py2exe": {
            "excludes": ("readline, win32api, win32con, dbus, gi,"
                         " urllib.unquote_plus, urllib.urlencode,"
                         " PyQt4, gtk"),
            "bundle_files": 1
        }
    },
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    long_description=open("README.rst").read()
)

if sys.platform.startswith('linux'):
    # Install desktop file. Required for mpris on Ubuntu
    options['data_files'] = [('share/applications/', ['mps-youtube.desktop'])]

if os.name == "nt":
    try:
        import py2exe
        # Only setting these when py2exe imports successfully prevents warnings
        # in easy_install
        options['console'] = ['mpsyt']
        options['zipfile'] = None
    except ImportError:
        pass

setup(**options)
