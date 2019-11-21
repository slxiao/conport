"""conport - Python generator of continuous testing report
"""
import io
import sys

import setuptools
from setuptools import setup

version = '1.1.8'

setup(
    include_package_data=True,
    name='conport',
    version=version,
    packages=['conport'],
    install_requires=[
        "jinja2>=2.7",
        "matplotlib",
        "python-jenkins"
    ],
    long_description=io.open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'conport = conport.conport:conport',
        ]
    },
    url='https://github.com/slxiao/contport',
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    data_files=[('', ['conport/cfg.ini', 'conport/template.html'])]
)
