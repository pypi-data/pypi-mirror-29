#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys
from io import open as io_open

# Main setup.py config #

# Get version from csg_dicoms_anonymizer/_version.py
__version__ = None
version_file = os.path.join(os.path.dirname(__file__), 'csg_dicoms_anonymizer', '_version.py')
with io_open(version_file, mode='r') as fd:
    exec(fd.read())


# Python package config #

README_rst = ''
fndoc = os.path.join(os.path.dirname(__file__), 'README.rst')
with io_open(fndoc, mode='r', encoding='utf-8') as fd:
    README_rst = fd.read()

setup(
    name='csg_dicoms_anonymizer',
    version=__version__,
    description='Robust and easy to use generic dicoms anonymizer with demographics csv spreadsheet anonymization by hashed ids',
    license='MIT Licence',
    author='Stephen Larroque',
    author_email='lrq3000@gmail.com',
    url='https://github.com/LRQ3000/csg_dicoms_anonymizer',
    maintainer='Stephen Larroque',
    maintainer_email='lrq3000@gmail.com',
    platforms=['any'],
    entry_points={'console_scripts': ['csg_dicoms_anonymizer=csg_dicoms_anonymizer.csg_dicoms_anonymizer:main'], },
    packages=['csg_dicoms_anonymizer'],
    long_description=README_rst,
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
    ],
    keywords='dicom neuroimage neuroimagery utility anonymizer fuzzy matching',
    test_suite='nose.collector',
    tests_require=['nose', 'coverage'],
)
