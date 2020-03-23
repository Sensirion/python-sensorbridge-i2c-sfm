# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import os
import re


# Read version number from version.py
version_line = open("sensirion_i2c_sfm/version.py", "rt").read()
result = re.search(r"^version = ['\"]([^'\"]*)['\"]", version_line, re.M)
if result:
    version_string = result.group(1)
else:
    raise RuntimeError("Unable to find version string")


# Use README.rst and CHANGELOG.rst as package description
root_path = os.path.dirname(__file__)
readme = open(os.path.join(root_path, 'README.rst')).read()
changelog = open(os.path.join(root_path, 'CHANGELOG.rst')).read()
long_description = readme.strip() + "\n\n" + changelog.strip() + "\n"


setup(
    name='sensirion-i2c-sfm',
    version=version_string,
    author='Daniel Straessler',
    author_email='daniel.straessler@sensirion.com',
    description='I2C Driver for Sensirion Flow Sensors',
    license='BSD',
    keywords='sensirion i2c driver sfm sfm3019',
    url='http://developer.sensirion.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    long_description=long_description,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    setup_requires=[
        'pytest-runner~=4.2',
    ],
    install_requires=[
        'enum34;python_version<"3.4"',
        'sensirion-shdlc-sensorbridge~=0.1.2',
    ],
    extras_require={
        'test': [
            'flake8~=3.6.0',
            'mock~=3.0.0',
            'pytest~=3.10.0',
            'pytest-cov~=2.6.0',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Hardware :: Hardware Drivers'
    ]
)
