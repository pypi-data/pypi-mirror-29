#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Carmen Bianca Bakker <carmen@carmenbianca.eu>
#
# This file is part of En Pyssant, available from its original location:
# <https://gitlab.com/carmenbianca/en-pyssant>.
#
# En Pyssant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# En Pyssant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with En Pyssant.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0+

import sys

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

requirements = [
]

if sys.version_info < (3, 5):
    requirements.append('typing')

test_requirements = [
    'pytest',
]

if __name__ == '__main__':
    setup(
        name='en-pyssant',
        version='0.1.5',
        url='https://gitlab.com/carmenbianca/en-pyssant',
        license='GPL-3.0+',

        author='Carmen Bianca Bakker',
        author_email='carmen@carmenbianca.eu',

        description="En Pyssant is a chess implementation and engine",
        long_description=readme + '\n\n' + history,

        package_dir={
            '': 'src'
        },
        packages=[
            'en_pyssant',
        ],

        entry_points={
            'console_scripts': [
                'en-pyssant-cli = en_pyssant._cli:main',
            ],
        },

        install_requires=requirements,
        tests_require=test_requirements,

        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: '
            'GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )
