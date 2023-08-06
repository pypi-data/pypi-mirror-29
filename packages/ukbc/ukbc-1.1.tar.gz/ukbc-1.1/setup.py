#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:18:24 2017

@author: Joe Necus
"""

from setuptools import setup,find_packages

setup(name='ukbc',
      version='1.1',
      description='Interface to faciliate filtering of UKBioBank data',
      include_package_data=True,
      url='http://github.com/jnecus/ukbcrunch',
      author='Joe Necus',
      author_email='j.necus2@ncl.ac.uk',
      license='MIT',
      install_requires=['appjar'],
      zip_safe=False,
      packages=find_packages(),
      package_data={'ukbc.coding_files': ['*'],
                        'ukbc.images': ['*'],
				'ukbc.data': ['*']})
