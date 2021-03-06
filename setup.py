#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for pylogd."""

from setuptools import setup, find_packages

# some trove classifiers:

from pylogd import VERSION
version = '.'.join(map(str, VERSION))

# License :: OSI Approved :: MIT License
# Intended Audience :: Developers
# Operating System :: POSIX

setup(
    name='pylogd',
    version=version,
    description="logd python library",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ],
    keywords='logd python udp logging server client',
    author='Jason Moiron',
    author_email='jason@hiidef.com',
    url="'http://github.com/hiidef/logd'",
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    # -*- Extra requirements: -*-
    install_requires=[
        'msgpack-python',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
