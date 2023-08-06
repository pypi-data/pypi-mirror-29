#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for entree
'''
import os

# from distutils.core import setup
from setuptools import setup, find_packages

_USERNAME = os.getenv('SUDO_USER') or os.getenv('USER')
_HOME = os.path.expanduser('~'+_USERNAME)
_CONFIGDIR = os.path.join(_HOME, '.config')


def get_template_dirs(path, basename='templates'):
    '''Get all path names for template directories
    '''
    dirs = []
    for fname in os.listdir(path):
        subpath = os.path.join(path, fname)
        if os.path.isdir(subpath):
            newbasename = os.path.join(basename, fname)
            dirs.append(newbasename)
            dirs.extend(get_template_dirs(subpath, basename=newbasename))
    return dirs

TEMPLATE_PATHS = [os.path.join(directory, '*')
                  for directory in ['templates'] +
                  get_template_dirs('entree/projects/templates')]
TEMPLATE_PATHS += [os.path.join(directory, '.gitignore')
                   for directory in ['templates'] +
                   get_template_dirs('entree/projects/templates')]

if os.path.exists(os.path.join(_CONFIGDIR, 'entree_config.json')):
    DATA_FILES = []
else:
    DATA_FILES = [(_CONFIGDIR, ['entree/entree_config.json'])]
DATA_FILES += [(_CONFIGDIR, ['entree_autocomplete'])]

setup(
    # Package information
    name='entree',
    version='2.3.3',
    description='Tool to create skeleton files to start a programming project',
    long_description='''
    Simple module to create files and directory structure necessary to
    start a programming project.

    Supported project types: HTML5, Python, Flask, Large Flask App, SQLAlchemy.
    ''',
    license='MIT',

    # Author information
    author='Julien Spronck',
    author_email='github@frenetic.be',
    url='http://frenetic.be/',

    # Installation information
    packages=find_packages(),
    entry_points={
        'console_scripts': ['entree = entree:main']
    },
    data_files=DATA_FILES,
    package_data={
        'entree.projects': TEMPLATE_PATHS,
    },
    install_requires=[
        'certifi==2018.1.18',
        'chardet==3.0.4',
        'click==6.7',
        'Flask==0.12.2',
        'gunicorn==19.7.1',
        'idna==2.6',
        'itsdangerous==0.24',
        'Jinja2==2.10',
        'MarkupSafe==1.0',
        'requests==2.18.4',
        'six==1.11.0',
        'urllib3==1.22',
        'Werkzeug==0.14.1'
    ],
    download_url='https://github.com/frenetic-be/entree/archive/2.3.3.tar.gz',

    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],

    # What does your project relate to?
    keywords='software development productivity skeleton starter',

)
