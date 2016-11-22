#!/usr/bin/env python
from distutils.core import setup, Extension

MOD = 'mytest'
setup(name=MOD, ext_modules=[
              Extension(MOD, sources=['test.c'])])


