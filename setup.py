# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='fetch_nju_news',
      version='0.1',
      description='Get latest announcements from nju websites, then package them.',
      url='http://github.com/brillliantz/fetch_nju_news',
      author='William Liu',
      author_email='brillliantz@outlook.com',
      license='MIT',
      packages=['fetch_nju_news'],
      # dependecies
      install_requires=[
        'requests',
        'bs4',
        ],      
      zip_safe=False)