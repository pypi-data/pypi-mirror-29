#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'azurebatchmon',
    version = '0.1.0b2',
    description='Python tools for easy job submission to Azure Batch',
    url = 'https://github.com/Genomon-Project/azurebatchmon',
    author = 'Kenichi Chiba and Yuichi Shiraishi',
    author_email = 'genomon.devel@gamil.com',
    license = 'GPLv3',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],

    install_requires=[
        'azure-batch',
        'azure-storage'
    ],

    packages = find_packages(exclude = ['*.pyc']),
    package_data={'azurebatchmon': ['*']},

    entry_points = {'console_scripts': ['azurebatchmon = azurebatchmon:main']}

)


