# -*- coding: UTF-8 -*-

"""
This file is part of SenSE.
(c) 2023- Thomas Weiß, Alexander Löw
For COPYING and LICENSE details, please refer to the LICENSE file
"""

from setuptools import setup, find_packages
import io
import os
from os.path import dirname, join

# Get the version from sense/version.py
__version__ = None
with open('sense/version.py') as f:
    exec(f.read())  # Safely execute version.py to get __version__

# Function to read files with UTF-8 encoding
def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

# Get the absolute path of the current directory
this_directory = os.path.abspath(os.path.dirname(__file__))

# Read the requirements from docs/requirements.txt
with open(os.path.join(this_directory, 'docs/requirements.txt')) as f:
    required = f.read().splitlines()

# Setup configuration
setup(
    name='sense',
    version=__version__,
    description='SenSE - Community SAR ScattEring model',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='GNU license',
    author='Thomas Weiß, Alexander Löw',
    author_email='weiss.thomas@lmu.de',
    url='https://github.com/McWhity/sense',
    packages=find_packages(include=['sense', 'sense.surface', 'sense.dielectric']),
    install_requires=required,
    package_data={},
    include_package_data=True,
    zip_safe=False,
)
