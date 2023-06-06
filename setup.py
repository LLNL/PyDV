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
        version='3.1.8',
        description='PyDV: Python Data Visualizer',
        long_description=long_description,
        author=['Sarah El-Jurf', 'Jorge Moreno',],
        author_email=['eljur1@llnl.gov', 'moreno45@llnl.gov'],
        license='BSD',
        url='https://github.com/LLNL/PyDV',
        packages=find_packages(),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: BSD License',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        install_requires=[
            'numpy',
            'matplotlib',
            'scipy',
            'PySide2',
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
