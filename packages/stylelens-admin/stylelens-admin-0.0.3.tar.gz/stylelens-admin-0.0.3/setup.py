# coding: utf-8

"""
    stylelans-admin

    This is a API document for Admin DB

    Contact: master@bluehack.net
"""


import sys
from setuptools import setup, find_packages

NAME = "stylelens-admin"
VERSION = "0.0.3"
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
    description="db-admin",
    author_email="master@bluehack.net",
    url="",
    keywords=["BlueLens", "db-admin"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This is a API document for Product DB
    """
)
