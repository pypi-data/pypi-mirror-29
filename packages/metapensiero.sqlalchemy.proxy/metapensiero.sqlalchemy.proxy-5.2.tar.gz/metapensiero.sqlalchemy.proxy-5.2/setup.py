# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy
# :Created:   mar 11 ago 2009 14:18:40 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2009, 2010, 2012, 2013, 2014, 2015, 2016, 2017 Lele Gaifax
#

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name='metapensiero.sqlalchemy.proxy',
    version=VERSION,
    description="Expose SQLAlchemy's queries and their metadata to a webservice",
    long_description=README + '\n\n' + CHANGES,

    author='Lele Gaifax',
    author_email='lele@metapensiero.it',
    url="https://bitbucket.org/lele/metapensiero.sqlalchemy.proxy",

    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3 :: Only',
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Database",
    ],

    packages=['metapensiero.sqlalchemy.' + package
              for package in find_packages('src/metapensiero/sqlalchemy')],
    package_dir={'': 'src'},
    namespace_packages=['metapensiero', 'metapensiero.sqlalchemy'],

#    python_requires='>=3.5',
    install_requires=[
        'setuptools',
        'sqlalchemy',
    ],
    extras_require={
        'dev': [
            'metapensiero.tool.bump_version',
            'readme_rendered'
        ]
    },
)
