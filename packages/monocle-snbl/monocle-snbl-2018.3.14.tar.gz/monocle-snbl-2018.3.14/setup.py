#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='monocle-snbl',
    version='2018.3.14',
    packages=[
        'monocle_snbl',
        'monocle_snbl.ui',
    ],
    url='https://hg.3lp.cx/monocle',
    license='GPLv3',
    author='Vadim Dyadkin',
    author_email='diadkin@esrf.fr',
    description='SNBL monochromator watchdog',
    entry_points={
        'gui_scripts': [
            'monocle=monocle_snbl:main',
        ],
        'console_scripts': [
            'monoclec=monocle_snbl:main',
        ]
    },
    install_requires=[
        'pyqtgraph',
        'aspic',
        'qtsnbl',
        'numpy',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
