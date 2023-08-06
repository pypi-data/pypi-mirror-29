#!/usr/bin/env python

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root
# for license information.

import os
import os.path
import sys

from setuptools import setup, Extension


ROOT = os.path.dirname(os.path.abspath(__file__))


# Add pydevd files as data files for this package. They are not treated
# as a package of their own, because we don't actually want to provide
# pydevd - just use our own copy internally.
def get_pydevd_package_data():
    ptvsd_prefix = os.path.join(ROOT, 'ptvsd')
    pydevd_prefix = os.path.join(ptvsd_prefix, 'pydevd')
    for root, dirs, files in os.walk(pydevd_prefix):
        # From the root of pydevd repo, we want only scripts and
        # subdirectories that constitute the package itself (not helper
        # scripts, tests etc). But when walking down into those
        # subdirectories, we want everything below.
        if os.path.normcase(root) == os.path.normcase(pydevd_prefix):
            dirs[:] = [d
                       for d in dirs
                       if d.startswith('pydev') or d.startswith('_pydev')]
            files[:] = [f
                        for f in files
                        if f.endswith('.py') and 'pydev' in f]
        for f in files:
            yield os.path.join(root[len(ptvsd_prefix) + 1:], f)


cmdclass = {}

if sys.version_info[0] == 2:
    from setuptools.command.build_ext import build_ext

    class build_optional_ext(build_ext):
        def build_extension(self, ext):
            try:
                super(build_optional_ext, self).build_extension(ext)
            except Exception:
                pass
    cmdclass = {'build_ext': build_optional_ext}

setup(
    name='ptvsd',
    version='4.0.0a1',
    description='Visual Studio remote debugging server for Python',
    license='MIT',
    author='Microsoft Corporation',
    author_email='ptvshelp@microsoft.com',
    url='https://aka.ms/ptvs',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    packages=['ptvsd'],
    package_data={
        'ptvsd': list(get_pydevd_package_data()) + [
            'ThirdPartyNotices.txt',
         ],
    },
    ext_modules=[
        Extension('ptvsd.pydevd._pydevd_bundle.pydevd_cython',
                  ['ptvsd/pydevd/_pydevd_bundle/pydevd_cython.c'],
                  optional=True),
    ],
    cmdclass=cmdclass,
)
