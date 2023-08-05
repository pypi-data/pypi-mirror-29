#!/usr/bin/env python

from distutils.core import setup
import sys

# We must use setuptools, not distutils, because we need to use the
# namespace_packages option for the "google" package.
try:
    from setuptools import setup, Extension, find_packages
except ImportError:
    try:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup, Extension, find_packages
    except ImportError:
        sys.stderr.write(
            "Could not import setuptools; make sure you have setuptools or "
            "ez_setup installed.\n"
        )
        raise

from distutils.command.clean import clean

if sys.version_info[0] == 3:
    # Python 3
    from distutils.command.build_py import build_py_2to3 as build_py
else:
    # Python 2
    from distutils.command.build_py import build_py as build_py
from distutils.spawn import find_executable


if __name__ == '__main__':
    setup(name="pymachinetalk",
          version="0.9.101",
          description="Python bindings for Machinetalk",
          author="Alexander Roessler",
          author_email="alex@machinekoder.com",
          url="https://github.com/machinekit/pymachinetalk",
          namespace_packages=['pymachinetalk'],
          packages=find_packages(),
          install_requires=['setuptools', 'pyzmq', 'zeroconf', 'machinetalk-protobuf', 'fysom'],
          cmdclass={
              'clean': clean,
              'build_py': build_py,
          }
          )
