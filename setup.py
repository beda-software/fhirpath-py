#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from io import open

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version("fhirpathpy")


with open("README.md") as f:
    long_description = f.read()


setup(
    name="fhirpathpy",
    version=version,
    description="FHIRPath implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="fhirpath",
    author="beda.software",
    author_email="fhirpath@beda.software",
    license="MIT",
    url="https://github.com/beda-software/fhirpath-py",
    project_urls={
        "Source Code": "https://github.com/beda-software/fhirpath-py",
        "Changelog": "https://github.com/beda-software/fhirpath-py/blob/master/CHANGELOG.md",
    },
    packages=["fhirpathpy"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["antlr4-python3-runtime==4.8"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
