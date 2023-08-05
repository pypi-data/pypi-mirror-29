#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'httplib2==0.9.1',
    'oauth2==1.9.0.post1'
]

test_requirements = [
    'coverage==4.0',
    'mock',  # ==1.3.0',
    'nose',  # ==1.3.7',
    'spec==1.3.1',
]

setup(
    name='readwise-pyinstapaper',
    version='0.1.3',
    description="A Python wrapper for the full Instapaper API.",
    long_description=readme + '\n\n' + history,
    author="Matt Dorn",
    author_email='mdorn@textmethod.com',
    url='https://github.com/mdorn/pyinstapaper',
    packages=[
        'pyinstapaper',
    ],
    package_dir={'pyinstapaper':
                 'pyinstapaper'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pyinstapaper',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
