"""conport - Python generator of continuous testing report
"""
import io
import sys

import setuptools
from distutils.core import setup

version = '0.0.6'

setup(
    include_package_data=True,
    name='conport',
    version=version,
    packages=['conport'],
    install_requires=[
        "jinja2>=2.7",
        "matplotlib",
        "python-jenkins",
        "url"
    ],
    long_description=io.open('README.md', encoding='utf8').read(),
    entry_points={
        'console_scripts': [
            'conport = conport.conport:conport',
        ]
    },
    url='https://github.com/slxiao/contport',
    license='MIT',
    author='slxiao',
    author_email='shliangxiao@gmail.com',
    description='Generate continuous testing report',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)