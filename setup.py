#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

version = '0.01'

setup(name='Puzzled',
      version=version,
      description="A game",
      long_description="""A game""",
      author='Oliver Dashiell Bunyan',
      author_email='puzzled@blueshed.co.uk',
      url='http://www.blueshed.co.uk/puzzled',
      packages=find_packages('src',exclude=['*tests*']),
      package_dir = {'':'src'},
      include_package_data = True, 
      exclude_package_data = { '': ['tests/*'] },
      install_requires = [
        'setuptools',
        'tornado>=2.4',
        'sqlalchemy'
      ],
      entry_points = {
      'console_scripts' : [
                           'puzzled = puzzled.web_server:main'
                           ]
      })