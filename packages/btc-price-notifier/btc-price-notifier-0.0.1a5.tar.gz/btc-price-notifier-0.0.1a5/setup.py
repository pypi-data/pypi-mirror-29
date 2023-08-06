# -*- coding: utf-8 -*-
"""
Copyright (C) 2018, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of MIT license

<https://opensource.org/licenses/MIT>
"""
from setuptools import setup,find_packages

with open("README.txt") as file:
    long_description = file.read()

setup(
    name = "btc-price-notifier",
    version = "0.0.1a5",
    author = "MuChu Hsu",
    author_email = "muchu1983@gmail.com",
    maintainer = "MuChu Hsu",
    maintainer_email = "muchu1983@gmail.com",
    url = "https://github.com/muchu1983/btc-price-notifier",
    description = "Bitcoin price notifier",
    long_description = long_description,
    download_url = "https://pypi.python.org/pypi/btc-price-notifier",
    platforms = "python 3.6",
    license = "MIT License",
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        "selenium>=3.10.0"
    ],
    entry_points = {
        "console_scripts":[
            "bpn=bpn.launcher:entry_point"
        ]
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
