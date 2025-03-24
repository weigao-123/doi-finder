#!/usr/bin/env python
"""
setup.py file for the doi-finder package.
This is for compatibility with older versions of pip.
Most configuration is in pyproject.toml.
"""

from setuptools import setup

# This setup.py is only for compatibility with older pip versions
# All configuration is in pyproject.toml
setup(
    name="doi-finder",
    version="0.1.0",
    packages=["doi_finder"],
    entry_points={
        'console_scripts': [
            'doi-finder=doi_finder.cli:main',
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "bibtexparser>=2.0.0b8",
    ],
) 