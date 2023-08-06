#!/usr/bin/env python
from setuptools import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

setup(
    name='SuchTree',
    version='0.3',
    description='A Python library for doing fast, thread-safe computations on phylogenetic trees.',
    url='http://github.com/ryneches/SuchTree',
    author='Russell Neches',
    author_email='ryneches@ucdavis.edu',
    license='BSD',
    packages=['SuchTree'],
    download_url='https://github.com/ryneches/SuchTree/archive/0.3.tar.gz',
    install_requires=[
        'scipy>=0.18',
        'numpy',
        'dendropy',
        'cython'
    ],
    zip_safe=False,
    ext_modules = cythonize( [ "SuchTree/SuchTree.pyx" ] ),
    test_suite = 'nose.collector'
)
