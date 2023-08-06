#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import zwift

from setuptools import setup, find_packages

version = zwift.__version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'fitparse',
    'protobuf',
    'requests',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='zwift-client',
    version=version,
    description="Zwift Mobile API client.",
    long_description=readme + '\n\n' + history,
    author="Sander Smits",
    author_email='jhmsmits@gmail.com',
    url='https://github.com/jsmits/zwift-client',
    packages=find_packages(include=['zwift']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='zwift',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
