import sys
import os
from setuptools import setup, find_packages

if sys.version_info[:2] < (2, 7):
    raise RuntimeError("Python version >= 2.7 required.")

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

setup(
    name=NAME,
    version='0.1.0',
    url=URL,
    author='Alex Drlica-Wagner',
    author_email='kadrlica@fnal.gov',
    scripts = [],
    install_requires=[
        'setuptools',
        'argparse',
        'logging',
    ],
    packages=find_packages(),
    package_data={},
    description=DESCR,
    long_description=LONG_DESCR,
    platforms='any',
    classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f]
)
