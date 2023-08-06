#!/usr/bin/env python

# Copyright (c) 2014 Johnny Wezel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

__version__ = '0.1a2'

setup(
    name='jw.ip-service',
    version=__version__,
    platforms='POSIX',
    url='https://pypi.python.org/pypi/jw.ip-service',
    download_url='https://pypi.python.org/packages/source/j/jw.ip-service/jw.ip-service-%s.tar.gz' % __version__,
    license='GPL',
    author='Johnny Wezel',
    author_email='dev-jay@wezel.name',
    description=(
        'A tool to set an IP to a network interface for as long as the program runs'
    ),
    long_description=open('README.rst').read(),
    keywords='IP, network, interface, utility',
    install_requires=[
        'setuptools',
        'sortedcontainers',
        'future',
        'jw.util'
    ],
    packages=find_packages(),
    namespace_packages=['jw'],
    entry_points={
        'console_scripts': [
            'ip-service=jw.ip_service.main:Main'
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Networking',
        'Topic :: Utilities'
    ]
)
