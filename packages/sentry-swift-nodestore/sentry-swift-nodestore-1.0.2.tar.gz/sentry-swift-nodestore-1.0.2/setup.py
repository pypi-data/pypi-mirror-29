#!/usr/bin/env python
"""
sentry-swift-nodestore
==============
An extension for Sentry which implements an Openstack Swift NodeStorage backend
"""
from setuptools import setup

install_requires = [
    'sentry>=8.19.0',
    'python-swiftclient>=3.5.0'
]

setup(
    name='sentry-swift-nodestore',
    version='1.0.2',
    author='Phillip Couto',
    author_email='pcouto@eckler.ca',
    url='https://gitlab.fs.eckler.ca/pcouto/sentry-swift-nodestore',
    description='A Sentry extension to add Swift as a NodeStore backend.',
    long_description=__doc__,
    packages=['sentry_swift_nodestore'],
    license='BSD',
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)