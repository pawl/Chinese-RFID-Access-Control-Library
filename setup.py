# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Chinese-RFID-Access-Control-Library',
    version='0.0.6',
    description='A library for interfacing with one of the most common RFID Access Control System sold in China.',
    long_description=readme,
    author='Paul Brown',
    author_email='paul90brown@gmail.com',
    url='https://github.com/pawl/Chinese-RFID-Access-Control-Library',
    license=license,
	download_url = ['https://github.com/pawl/Chinese-RFID-Access-Control-Library/tarball/master#egg=package-0.0.6'],
	keywords = ['rfid', 'access control'],
    py_modules = ['rfid']
)

