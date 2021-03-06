#!/usr/bin/env python

from setuptools import setup

setup(
    name='easy-pki',
    version='0.1.0',
    author='Tao Fei',
    author_email='filia.tao@gmail.com',

    url='https://pypi.python.org/pypi/easy-pki',
    license='GPLv3',
    description='A Simple Public-Key Infrastructure Manager',
    long_description=open('README.md').read(),

    install_requires=[
        'PyYAML',
        'docopt',
        'jinja2'
    ],

    packages=['easypki', 'ovpnconf'],

    package_data={'ovpnconf': ['ovpnconf/templates/*', 'ovpnconf/defaults/*']},

    entry_points = {
        'console_scripts': [
            'easy-pki = easypki.cli:main',
            'ovpnconf-gen = ovpnconf.gen:main',
        ]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GPL License',
    ],
)
