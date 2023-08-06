#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import find_packages, setup

# Package meta-data.
NAME = 'ftw.aare'
DESCRIPTION = 'A Shell Command which displays the current temperature of the Aare in Bern, Switzerland'
LONG_DESCRIPTION = 'For more information please visit https://github.com/4teamwork/ftw.aare'
EMAIL = 'info@4teamwork.ch'
MAINTAINER = "Steven Pilatschek"
AUTHOR = '4teamwork AG'
URL = "https://github.com/4teamwork/ftw.aare"
version = '1.2'

# What packages are required for this module to be executed?
REQUIRED = [
    'requests', 'click'
]

EXTRAS = {'tests': ['pytest', 'path.py']}

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=MAINTAINER,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
         'console_scripts': ['aare=aare.aare:aare'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
