# coding: utf-8

"""
    bl-db-video

    This is a API document for Video DB

    OpenAPI spec version: 0.0.1
    Contact: originman@bluehack.net
"""


import sys
from setuptools import setup, find_packages

NAME = "newitem-video"
VERSION = "0.0.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["pymongo"]

setup(
    name=NAME,
    version=VERSION,
    description="newitem-db-video",
    author_email="originman@bluehack.net",
    url="",
    keywords=["Newitem", "newitem-db-video"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This is a API document for Video DB
    """
)
