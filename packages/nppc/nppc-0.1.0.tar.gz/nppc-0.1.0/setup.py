#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Maarten",
    author_email='ikmaarten@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="NPPC, Nagios Plug-in Process Controller, is a set of scripts and configuration files that let you periodically runs Nagios_ Plug-in parallel using systemd_ and systemd.timer_. Results can be posted via HTTPS to a NSCAweb_ server.",
    entry_points={
        'console_scripts': [
            'nppc=nppc.cli:main',
        ],
    },
    install_requires=requirements,
    license="ISC license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nppc',
    name='nppc',
    packages=find_packages(include=['nppc']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/maartenq/nppc',
    version='0.1.0',
    zip_safe=False,
)
