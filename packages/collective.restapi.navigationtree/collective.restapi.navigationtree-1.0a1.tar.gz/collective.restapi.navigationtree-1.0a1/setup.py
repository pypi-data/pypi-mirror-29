# -*- coding: utf-8 -*-
"""Installer for the collective.restapi.navigationtree package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.restapi.navigationtree',
    version='1.0a1',
    description='Provides a REST endpoint to query the site\'s navigation tree',
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='Python Plone rest restful api json',
    author='Fulvio Casali',
    author_email='fulviocasali@gmail.com',
    url='https://pypi.python.org/pypi/collective.restapi.navigationtree',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.restapi'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'plone.api',
        'Products.GenericSetup>=1.8.2',
        'setuptools',
        'plone.restapi',
        'webcouturier.dropdownmenu',
    ],
    extras_require={
        'test': [
            'Products.Archetypes',
            'plone.app.contenttypes',
            'plone.restapi[test]',
            'plone.app.testing',
            'plone.app.robotframework[debug]',
            'plone.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
