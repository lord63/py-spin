#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup

import pyspin


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md') as f:
        long_description = f.read()


setup(
    name='pyspin',
    version=pyspin.__version__,
    description='Little terminal spinner lib.',
    long_description=long_description,
    url='http://github.com/lord63/py-spin',
    author='lord63',
    author_email='lord63.j@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='terminal spin spinner',
    packages=['pyspin'],
    include_package_data=True
)
