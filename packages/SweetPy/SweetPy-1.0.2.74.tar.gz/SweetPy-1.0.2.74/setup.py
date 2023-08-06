#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
# from setuptools import find_package_data
import sys

setup(
    name="SweetPy",
    version="1.0.2.74",
    author="inflower",
    author_email="inflowers@126.com",
    description="A micro service launcher",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://pypi.python.org/pypi/SweetPy",
    packages=find_packages(exclude=["*.*"]),
    include_package_data=True,
    py_modules = ['SweetPy','SweetPy.extend','SweetPy.django_middleware','SweetPy.sweet_framework','SweetPy.sweet_framework_cloud'],
    # package_dir = {'': ''},
    # package_data = {'': ['*.txt'], 'mypkg': ['data/*.dat'],},
    # data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #                   ('config', ['cfg/data.cfg']),
    #                   ('/etc/init.d', ['init-script'])],
    install_requires=[
        "django == 1.11.7",
        "djangorestframework == 3.7.3",
        "pygments == 2.2.0",
        "markdown == 2.6.9",
        "django-filter == 1.1.0",
        "django-rest-swagger == 2.1.2",
        "kazoo == 2.4.0",
        "pika == 0.11.2",
        "requests == 2.18.4",
        "apscheduler == 3.4.0",
        "python-dateutil == 2.6.1"
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
