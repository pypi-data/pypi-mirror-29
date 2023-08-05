#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import os.path
import sys

sys.path.insert(0, os.path.abspath('.'))
from exopy_hqc_legacy.version import __version__


def long_description():
    """Read the project description from the README file.

    """
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


setup(
    name='exopy_hqc_legacy',
    description='Transitional package between HQCMeas and Exopy',
    long_description=long_description(),
    version=__version__,
    author='see AUTHORS',
    author_email='m.dartiailh@gmail.com',
    url='https://github.com/exopy/exopy_hqc_legacy',
    download_url='https://github.com/exopy/exopy_hqc_legacy/tarball/master',
    keywords='experiment automation GUI',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
    zip_safe=False,
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'': ['*.enaml']},
    requires=['exopy', 'pyvisa', 'h5py', 'numpy', 'pyclibrary'],
    install_requires=['setuptools', 'exopy', 'pyvisa', 'h5py', 'numpy'],
    entry_points={
        'gui_scripts':
        'hqcmeas_to_exopy = exopy_hqc_legacy.conversion.__main__:main',
        'exopy_package_extension':
        'exopy_hqc_legacy = exopy_hqc_legacy:list_manifests'}
)
