# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

tests_require = ['mock']

setup(
    name='Chinese-RFID-Access-Control-Library',
    version='0.1.0',
    description='A library for interfacing with one of the most common RFID Access Control System sold in China.',
    long_description=readme,
    author='Paul Brown',
    author_email='paul90brown@gmail.com',
    url='https://github.com/pawl/Chinese-RFID-Access-Control-Library',
    license=license,
    download_url=['https://github.com/pawl/Chinese-RFID-Access-Control-Library/tarball/master#egg=package-0.1.0'],
    keywords=['rfid', 'access control'],
    py_modules=['rfid'],
    test_suite="tests",
    tests_require=tests_require,
)
