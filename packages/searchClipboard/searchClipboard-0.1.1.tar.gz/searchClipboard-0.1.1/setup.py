# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='searchClipboard',
    version='0.1.1',
    description='search google for current clipboard contents',
    long_description=readme,
    author='Aashray Anand',
    author_email='aashrayanand01@gmail.com',
    url='https://github.com/AashrayAnand/searchClipboard',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['bin/search-Clipboard'],
    install_requires=['pyperclip',],
)

