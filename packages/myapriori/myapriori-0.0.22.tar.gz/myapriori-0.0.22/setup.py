#!/usr/bin/env python

"""
Setting up program for Apyori.
"""

import version
import setuptools

setuptools.setup(
    name='myapriori',
    description='Simple Apriori algorithm Implementation.',
    version=version.__version__,
    author='jimmybow',
    author_email='jimmybow@hotmail.com.tw',
    url='https://github.com/jimmybow/myapriori',
    license='MIT',
    py_modules=['apyori', 'myapriori', 'version'],
    install_requires=[
        "pandas",
        "numpy",
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'mock'],
    entry_points={
        'console_scripts': [
            'apyori-run = apyori:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
