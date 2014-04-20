# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Chinese RFID Access Control Library',
    version='0.0.1',
    description='A library for interfacing with the cheapest and most common Chinese RFID Access Control System.',
    long_description=readme,
    author='Paul Brown',
    author_email='paul90brown@gmail.com',
    url='https://github.com/pawl/Chinese-RFID-Access-Control-Library',
    license=license,
	keywords = ['rfid', 'access control'],
    py_modules = ['rfid']
)

