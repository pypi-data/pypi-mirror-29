#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
from setuptools import setup, find_packages

__version__ = "0.1.19"


def read_file(filename):
    with open(filename) as f:
        return f.read()


# run setup
# take metadata from setup.cfg
setup(
    name="numericalmodel",
    description="abstract classes to set up and run a numerical model",
    author="Yann Büchau",
    author_email="yann.buechau@web.de",
    keywords="modelling",
    license="GPLv3",
    version=__version__,
    url='https://gitlab.com/nobodyinperson/python3-numericalmodel',
    long_description=read_file("README.rst"),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3.5',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=['numpy>=1.13'],
    extras_require={
        "gui": ["matplotlib", "cairocffi", "statsmodels"],
        "cli": ["IPython", "matplotlib", "statsmodels"],
        "full": ["matplotlib", "cairocffi", "IPython", "statsmodels"]
    },
    install_requires=['numpy>=1.13', 'scipy>=1'],
    packages=find_packages(exclude=['tests']),
    package_data={'numericalmodel.ui.gui': ["*.glade", "*.mo", "*.png"]},
    include_package_data=True,
)
