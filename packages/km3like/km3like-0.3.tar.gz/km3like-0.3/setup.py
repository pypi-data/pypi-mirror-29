#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:

from setuptools import setup
from km3like import __version__


setup(
    name='km3like',
    version=__version__,
    description='Likelihood Utils',
    url='http://git.km3net.de/moritz/km3like',
    author='Moritz Lotze',
    author_email='mlotze@km3net.de',
    license='BSD-3',
    packages=['km3like', ],
    install_requires=[
        'numpy>=1.12',
        'pandas',
        'seaborn',
        'statsmodels',
        'km3pipe[full]>=7.0',
        'km3astro',
        'km3flux',
        'tables',
    ]
)
