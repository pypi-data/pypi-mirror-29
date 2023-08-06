# -*- coding: utf-8 -*-
#
# Copyright 2017 Gehirn Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from setuptools import (
    find_packages,
    setup,
)

here = os.path.dirname(__file__)
requires = [
    'ghoauth >= 0.6.1, < 1.0',
    'jwt >= 0.5.2',
]

try:
    import typing
except ImportError:
    requires.append('typing == 3.5.3.0')
else:
    del typing

setup(
    name='ghopenid',
    version='0.3.4',

    description='OpenID Provider Library for Python 3',
    url='https://github.com/GehirnInc/ghopenid',

    author='Kohei YOSHIDA',
    author_email='kohei.yoshida@gehirn.co.jp',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
    ],

    packages=find_packages(),

    install_requires=requires,
)
