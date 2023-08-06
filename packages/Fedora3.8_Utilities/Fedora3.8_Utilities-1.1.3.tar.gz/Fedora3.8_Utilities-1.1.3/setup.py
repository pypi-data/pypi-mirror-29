"""Setup module for Colorado College Fedora 3.8 Utilities

See:
https://github.com/Tutt-Library/fedora38-utilities
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as fo:
    long_description = fo.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as fo:
    version = fo.read()

setup(
    name='Fedora3.8_Utilities',
    version=version,
    description='Utilities for legacy Fedora 3.8 repository',
    long_description = long_description, 
    url='https://github.com/Tutt-Library/fedora38-utilities',
    author='Jeremy Nelson',
    author_email='jermnelson@gmail.com',
    license='Apache2',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python', 
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='fedora3.8 library',
    packages=find_packages(exclude=("instance",)),
    install_requires=['elasticsearch',
                      'Flask',
                      'Flask-WTF',
                      'rdflib',
                      'requests'] 
)

    
