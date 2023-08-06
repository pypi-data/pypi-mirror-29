#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path
import sys

__version__ = '0.0.1'

install_requires = [
    'steam[client]>=0.8.15',
    'gevent-eventemitter>=2.0',
    'gevent>=1.1',
    'protobuf>=3.0.0',
]

if sys.version_info < (3, 4):
    install_requires.append('enum34>=1.0.4')

setup(
    name='artifact',
    version=__version__,
    description='WIP',
    long_description='WIP',
    url='',
    author="Rossen Georgiev",
    author_email='rossen@rgp.io',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='valve steam artifact',
    packages=['artifact'] + ['artifact.'+x for x in find_packages(where='artifact')],
    install_requires=install_requires,
    zip_safe=True,
)
