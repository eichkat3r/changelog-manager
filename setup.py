#!/usr/bin/env python3

from setuptools import setup

setup(
    name='ChangelogManager',
    version='0.1.0',
    author='eichkat3r',
    author_email='eichkat3r@computerwerk.org',
    packages=['app'],
    entry_points={
        'console_scripts': [
            'chanman = app.chanman:main'
        ]
    },
    url='https://github.com/eichkat3r/changelog-manager',
    description='',
)
