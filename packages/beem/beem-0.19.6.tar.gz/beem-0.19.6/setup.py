#!/usr/bin/env python3

import os
import sys
import subprocess
from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.19.6'


def write_version_py(filename):
    cnt = """
# THIS FILE IS GENERATED FROM beem SETUP.PY
version = '%(version)s'
"""
    with open(filename, 'w') as a:
        a.write(cnt % {'version': VERSION})


if __name__ == '__main__':

    # Rewrite the version file everytime
    write_version_py('beem/version.py')
    write_version_py('beembase/version.py')
    write_version_py('beemapi/version.py')

    setup(
        name='beem',
        version=VERSION,
        description='Unofficial Python library for STEEM',
        long_description=open('README.rst').read(),
        download_url='https://github.com/holgern/beem/tarball/' + VERSION,
        author='Holger Nahrstaedt',
        author_email='holger@nahrstaedt.de',
        maintainer='Holger Nahrstaedt',
        maintainer_email='holger@nahrstaedt.de',
        url='http://www.github.com/holgern/beem',
        keywords=['steem', 'library', 'api', 'rpc'],
        packages=[
            "beem",
            "beemapi",
            "beembase"
        ],
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry',
            'Topic :: Office/Business :: Financial',
        ],
        install_requires=[
            "graphenelib>=0.5.9",
            "websockets",
            "appdirs",
            "Events",
            "scrypt",
            "pycryptodome",  # for AES, installed through graphenelib already
        ],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        include_package_data=True,
    )
