# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0'
description = 'Sistema de Ouvidoria do Portal Modelo do Interlegis.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.portalmodelo.ombudsman',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interlegis transparency portalmodelo',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.portalmodelo.ombudsman',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Acquisition',
        'collective.watcherlist',
        'collective.z3cform.datagridfield',
        'five.grok',
        'interlegis.portalmodelo.api',
        'plone.api',
        'plone.app.content',
        'plone.app.dexterity [grok]',
        'plone.app.referenceablebehavior',
        'plone.autoform',
        'plone.dexterity',
        'plone.directives.dexterity',
        'plone.directives.form',
        'plone.i18n',
        'plone.memoize',
        'plone.supermodel',
        'Products.BrFieldsAndWidgets',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'plone.uuid',
            'Products.statusmessages',
            'robotsuite',
            'transaction',
        ],
    },
)
