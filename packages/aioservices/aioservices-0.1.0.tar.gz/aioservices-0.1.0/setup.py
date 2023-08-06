"""`Aioservices` setup script."""

import os
import re

from setuptools import setup


# Getting description:
# with open('README.rst') as readme_file:
#     description = readme_file.read()
description = 'Python 3 asyncio microservices framework'

# Getting requirements:
# with open('requirements.txt') as requirements_file:
#     requirements = requirements_file.readlines()
requirements = []

# Getting version:
with open('src/aioservices/__init__.py') as init_file:
    version = re.search('__version__ = \'(.*?)\'', init_file.read()).group(1)

setup(name='aioservices',
      version=version,
      description='Python 3 asyncio microservices framework',
      long_description=description,
      author='ETS Labs',
      author_email='rmogilatov@gmail.com',
      maintainer='Roman Mogilatov',
      maintainer_email='rmogilatov@gmail.com',
      # url='https://github.com/ets-labs/python-dependency-injector',
      # download_url='https://pypi.python.org/pypi/dependency_injector',
      install_requires=requirements,
      packages=[
          'aioservices',
      ],
      package_dir={
          '': 'src',
      },
      zip_safe=True,
      license='BSD New',
      platforms=['any'],
      keywords=[
          'asyncio',
          'microservice',
          'framework',
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Framework :: AsyncIO',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
