# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup


VERSION = '1.1.1'

AUTHOR = "cn"

AUTHOR_EMAIL = "cnaafhvk@foxmail.com"

URL = "https://www.github.com/ShichaoMa/toolkit"

NAME = "toolkity"

DESCRIPTION = "simple function tools. "

try:
    LONG_DESCRIPTION = open("README.rst").read()
except UnicodeDecodeError:
    LONG_DESCRIPTION = open("README.rst", encoding="utf-8").read()

KEYWORDS = "tools function"

LICENSE = "MIT"

PACKAGES = ["toolkit"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=["psutil", "python-json-logger"],
    include_package_data=True,
    zip_safe=True,
)