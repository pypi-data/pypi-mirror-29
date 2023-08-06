#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='onlykey_agent',
    version='0.0.2',
    description='Using OnlyKey as hardware SSH agent',
    long_description=long_description,
    author='CryptoTrust',
    author_email='admin@crp.to',
    url='http://github.com/trustcrypto/onlykey-agent',
    packages=['onlykey_agent'],
    install_requires=['ecdsa>=0.13', 'ed25519>=1.4', 'Cython>=0.23.4', 'protobuf>=2.6.1', 'semver>=2.2'],
    platforms=['POSIX'],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Communications',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    entry_points={'console_scripts': [
        'onlykey-agent = onlykey_agent.__main__:run_agent',
    ]},
)
