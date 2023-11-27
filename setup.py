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