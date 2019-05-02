#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get long description from README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='PyDV',
        version='2.4.2.1',
        description='PyDV: Python Data Visualizer',
        long_description=long_description,
        author='Kevin Griffin',
        author_email='griffin28@llnl.gov',
        license='BSD',
        url='https://github.com/griffin28/PyDV',
        packages=find_packages(),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: BSD License',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
        ],
        install_requires=[
            'numpy',
            'matplotlib',
            'scipy',
        ],
        # GUI icons
        package_data={
            'pydv': ['img/*'],
        },
        # PyDV start script
        entry_points={
            'console_scripts': [
                'pdv=pydv.pdv:main',
            ],  
        },
)
