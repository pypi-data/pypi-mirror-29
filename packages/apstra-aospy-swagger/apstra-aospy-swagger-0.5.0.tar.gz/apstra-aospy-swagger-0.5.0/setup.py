# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/eula

from setuptools import setup, find_packages

packages = find_packages()

setup(
    name="apstra-aospy-swagger",
    version="0.5.0",
    description="Python Swagger client for AOS Server",
    author="Apstra, Inc.",
    license="Apache 2.0",
    author_email="support@apstra.com",
    url="http://www.apstra.com",
    packages=packages,
    install_requires=[
        'bidict',
        'cached_property',
        'first',
        'halutz>=0.4.2',
        'inflection',
        'requests',
        'retrying',
        'six'
    ]
)
