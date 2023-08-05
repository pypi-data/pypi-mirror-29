#!/usr/bin/env python
from __future__ import print_function

from setuptools import setup, find_packages
import os
import platform
import sys

__version__ = '0.1.39'

install_requires = [ 'PyLD', 'future', 'prov', 'unicodecsv', 'progressbar2',
    'requests', 'wget', 'argparse==1.1', 'topicexplorer>=1.0b194']
# TODO: migrate to docs confix:, 'sphinx-argparse', 'sphinxcontrib-fulltoc']
if sys.version_info.major == 2:
    install_requires.append('configparser')
    install_requires.append('mock')

try:
    import wget
    print("Downloading .htrc file...")
    wget.download('https://analytics.hathitrust.org/files/.htrc',
        out=os.path.expanduser('~/.htrc'))
    print("\n")
except ImportError:
    print(".htrc file not downloaded due to missing wget.")

setup(
    name='htrc',
    version=__version__,
    description='HathiTrust Research Center API Access',
    author = "HathiTrust Research Center",
    author_email = "htrc@indiana.edu",
    url='http://analytics.hathitrust.org',
    download_url='http://github.com/htrc/HTRC-PythonSDK',
    keywords = [],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    data_files=[('htrc/mock/volumes/', ['htrc/mock/volumes/example.zip']),
                ('htrc/', ['htrc/.htrc.default'])],
    zip_safe=False,
    entry_points={
        'console_scripts' : ['htrc = htrc.__main__:main']
    },
    test_suite="unittest2.collector",
    tests_require=['unittest2']
)

