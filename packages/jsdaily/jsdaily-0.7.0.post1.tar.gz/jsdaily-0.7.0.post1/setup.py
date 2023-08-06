#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import platform
import setuptools
import sys


# check platform
if platform.system() != 'Darwin':
    if platform.system() != 'Windows':
        # terminal display
        red = 'tput setaf 1'    # blush / red
        bold = 'tput bold'      # bold
        under = 'tput smul'     # underline
        reset = 'tput sgr0'     # reset

        # unsupported OS
        os.system(f'echo "Package $({under})jsdaily$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
    else:
        # unsupported OS
        print('Package "jsdaily" runs only on macOS.')
    sys.exit(1)


# README
with open('./README.rst', 'r') as file:
    long_desc = file.read()


# set-up script for pip distribution
setuptools.setup(
    name = 'jsdaily',
    version = '0.7.0.post1',
    author = 'Jarry Shaw',
    author_email = 'jarryshaw@icloud.com',
    url = 'https://github.com/JarryShaw/jsdaily/',
    license = 'GNU General Public License v3 (GPLv3)',
    keywords = 'daily utility script',
    description = 'Some useful daily utility scripts.',
    long_description = long_desc,
    python_requires = '>=3.6',
    extras_require = {
        'pipdeptree': ['pipdeptree']
    },
    entry_points = {
        'console_scripts': [
            'update = jsdaily:update',
            'uninstall = jsdaily:uninstall',
            'reinstall = jsdaily:reinstall',
            'postinstall = jsdaily:postinstall',
            'dependency = jsdaily:dependency',
            'logging = jsdaily:logging',
        ]
    },
    packages = [
        'jsdaily',
        'jsdaily.libupdate',
        'jsdaily.libuninstall',
        'jsdaily.libprinstall',
        'jsdaily.libdependency',
        'jsdaily.liblogging',
    ],
    package_data = {
        '': [
            'LICENSE.txt',
            'README.md',
            'README.rst',
        ],
        'jsdaily.libupdate': ['*.py', '*.sh'],
        'jsdaily.libuninstall': ['*.py', '*.sh'],
        'jsdaily.libprinstall': ['*.py', '*.sh'],
        'jsdaily.libdependency': ['*.py', '*.sh'],
        'jsdaily.liblogging': ['*.py', '*.sh'],
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Unix Shell',
        'Topic :: Utilities',
    ]
)
