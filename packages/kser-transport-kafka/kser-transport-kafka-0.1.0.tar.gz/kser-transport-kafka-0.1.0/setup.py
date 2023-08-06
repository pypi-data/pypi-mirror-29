# /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

"""

from setuptools import setup, find_packages

setup(
    name='kser-transport-kafka',
    version=open('VERSION', 'r').read().strip(),
    description="Kser librdkafka producer/consumer",
    long_description=open('README.rst', 'r').read().strip(),
    classifiers=["Programming Language :: Python", ],
    keywords='',
    author='Cedric DUMAY',
    author_email='cedric.dumay@gmail.com',
    url='https://github.com/cdumay/kser-transport-kafka',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    install_requires=open('requirements.txt', 'r').read().strip(),
    entry_points="""
""",
)
