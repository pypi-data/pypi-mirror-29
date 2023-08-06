#!/usr/bin/env python

from setuptools import setup

desc = r'Table-like formats to latex \table[H]'

setup(
    name='htable',
    version='0.1.0',
    description=desc,
    long_description=desc,
    url='https://github.com/cdown/htable',
    license='Public Domain',

    author='Chris Down',
    author_email='chris@chrisdown.name',

    py_modules=['htable'],

    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
    ],
)
