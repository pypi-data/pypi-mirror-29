#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages
import os
from os.path import abspath, dirname

# allow setup.py to be ran from anywhere
os.chdir(dirname(abspath(__file__)))

setup(
	name='allib',
	version='1.1',
	license='MIT',
	description='Personal library of useful stuff.',
	long_description=("Collection of modules that I personally find useful. "
		"You probably don't want to add it to your requirements, but feel free "
		"to copy-paste code from the Github source code."),
	author='Andreas Lutro',
	author_email='anlutro@gmail.com',
	url='https://github.com/anlutro/allib.py',
	packages=find_packages(include=('allib', 'allib.*')),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
	keywords=['personal', 'library', 'utils'],
)
