#!/usr/bin/env python3

from setuptools import setup


setup(
    name = 'plover_python_dictionary',
    version = '0.5.2',
    description = 'Python dictionaries support for Plover',
    author = 'Benoit Pierre',
    author_email = 'benoit.pierre@gmail.com',
    license = 'GNU General Public License v2 or later (GPLv2+)',
    url = 'https://github.com/benoit-pierre/plover_python_dictionary',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords = 'plover',
    setup_requires = [
        'setuptools-scm',
    ],
    install_requires = [
        'plover>=4.0.0.dev0',
    ],
    py_modules = [
        'plover_python_dictionary',
    ],
    entry_points = '''

    [plover.dictionary]
    py = plover_python_dictionary

    ''',
    zip_safe = True,
)
