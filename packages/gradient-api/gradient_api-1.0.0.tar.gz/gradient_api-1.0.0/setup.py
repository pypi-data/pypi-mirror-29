#coding:utf-8

from distutils.core import setup
from setuptools import find_packages


PACKAGE = "gradient_api"
NAME = "gradient_api"
DESCRIPTION = "API of gradient."
AUTHOR = "UlionTse"
AUTHOR_EMAIL = "shinalone@outlook.com"
URL = "https://github.com/shinalone/gradient_api"
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
    keywords=['gradient_api','Gradient','gradient','GradientApi','gradientAPI'],
    install_requires=[
        'numpy>=1.13.3',
        'sympy>=1.0',
        'matplotlib>=1.5.3'
    ],
    zip_safe=False,
)

