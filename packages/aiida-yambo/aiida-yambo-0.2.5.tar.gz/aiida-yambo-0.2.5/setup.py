#!/usr/bin/env python
import re
from setuptools import setup, find_packages
import json

if __name__ == '__main__':
    with open('setup.json', 'r') as info:
        kwargs = json.load(info)
    setup(
        include_package_data=True,
        setup_requires=[
            'reentry'
        ],
        reentry_register=True,
        packages=find_packages(where='.', exclude=( "gw.*", "parser.*","gw*","parser*")),
        **kwargs
    )
