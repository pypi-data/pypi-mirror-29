#coding:utf-8

from distutils.core import setup
from setuptools import find_packages


PACKAGE = "vcode_api"
NAME = "vcode_api"
DESCRIPTION = "API of Vcode."
AUTHOR = "UlionTse"
AUTHOR_EMAIL = "shinalone@outlook.com"
URL = "https://github.com/shinalone/vcode_api"
VERSION = __import__(PACKAGE).__version__

with open('README.rst','r',encoding='utf-8') as file:
    long_description = file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    keywords=['vcode_api','Vcode','vcode','VcodeApi','vcodeAPI'],
    install_requires=[
        'pillow>=3.3.1',
        'numpy>=1.13.3'
    ],
    zip_safe=False,
)