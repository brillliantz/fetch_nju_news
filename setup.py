# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='fetch_nju_news',
      version='0.1',
      description='Get latest announcements from nju websites, then package them.',
      long_description=readme(),
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