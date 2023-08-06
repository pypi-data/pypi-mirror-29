#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

from setuptools import setup

NAME = 'lsst-sphinx-bootstrap-theme'
VERSION = '0.1.2'


setup(
    name=NAME,
    version=VERSION,
    description='Sphinx theme for LSST Stack documentation built on '
                'Bootstrap and astropy-helpers',
    author='Jonathan Sick',
    author_email='jsick@lsst.org',
    license='BSD',
    url='https://github.com/lsst-sqre/lsst-sphinx-bootstrap-theme',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Sphinx :: Theme',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False,
    packages=['lsst_sphinx_bootstrap_theme'],
    package_data={'lsst_sphinx_bootstrap_theme': [
        'theme.conf',
        '*.html',
        'static/*.css',
        'static/*.js',
        'static/*.ico',
        'static/*.svg',
        'static/*.png',
        'templates/autosummary/*.rst'
    ]},
    include_package_data=True,
)
