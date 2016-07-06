import sys
import os
from setuptools import setup

if sys.version_info[:2] < (2, 7):
    raise RuntimeError("Python version >= 2.7 required.")

import adwparse        

# To install on lower versions of Python, add argparse, logging,
# etc. to the install_requires
# install_requires = ['setuptools','argparse','logging']

NAME = 'adwparse'
CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Natural Language :: English
Topic :: Scientific/Engineering
"""
URL = 'https://github.com/kadrlica/adwparse'
DESCR = "Custom extension of the `argparse` module."
LONG_DESCR = "See %s for more details."%URL
VERSION = adwparse.__version__

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    author='Alex Drlica-Wagner',
    author_email='kadrlica@fnal.gov',
    py_modules=['adwparse'],
    package_data={},
    description=DESCR,
    long_description=LONG_DESCR,
    platforms='any',
    classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f]
)
