#!/usr/bin/env python

from distutils.core import setup
import subprocess

# convert readme to rst format
try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except:
   long_description = ''

execfile("PodSixNet/version.py")

setup(
    version=__version__,
    name='PodSixNet',
    description='Multiplayer networking library for games',
    long_description=long_description,
    author='Chris McCormick',
    author_email='chris@mccormick.cx',
    url='https://github.com/chr15m/PodSixNet',
    packages=['PodSixNet'],
)
