#!/usr/bin/env python

"""
Copyright 2023 John Christian (MythicStack)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup, find_packages
import os

PACKAGE_NAME = "whoisrecon"

VER_MAJOR = 0
VER_MINOR = 1
VER_MAINT = 0

#Nabbed from the Impacket Source.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=PACKAGE_NAME,
    version="{}.{}.{}".format(VER_MAJOR, VER_MINOR, VER_MAINT),
    description="WHOIS Reconnaissance Tool",
    url="https://www.github.com/MythicStack/whoisrecon",
    author="John Christian (MythicStack)",
    maintainer="John Christian (MythicStack)",
    license="Apache License 2.0",
    maintainer_email="mythicstack@pm.me",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'whoisrecon=whoisrecon.whoisrecon:main',
        ],
    },
    packages=find_packages(exclude=['tests*']),
    python_requires=">=3",
    platforms=["Unix", "Windows"],
    install_requires=['setuptools', 'argparse', 'tabulate', 'requests',
                      'whois', 'bs4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent"
    ]
)