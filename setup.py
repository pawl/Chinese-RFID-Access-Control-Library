# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

tests_require = ['mock']

setup(
    name='Chinese-RFID-Access-Control-Library',
    version='0.1.2',
    description='A library for interfacing with one of the most common RFID Access Control System sold in China.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Paul Brown',
    author_email='paul90brown@gmail.com',
    url='https://github.com/pawl/Chinese-RFID-Access-Control-Library',
    license='MIT',
    download_url='https://pypi.python.org/pypi/Chinese-RFID-Access-Control-Library',
    keywords=['rfid', 'access control'],
    py_modules=['rfid'],
    test_suite="tests",
    tests_require=tests_require,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
