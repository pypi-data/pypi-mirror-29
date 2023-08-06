# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='eb2csv',
    version='0.1.3',
    author='GILDEMEISTER energy efficiency GmbH',
    author_email='energyefficiency@gildemeister.com',
    description='A Python (3.6) CLI tool for recording measurement data from Gildemeister Energy Box data loggers into csv files.',
    long_description=open('README.md').read(),
    license='MIT',
    url='https://bitbucket.org/gildemeisterenergyefficiency/eb2csv/',
    packages=['eb2csv'],
    package_dir={'eb2csv': 'eb2csv'},
    package_data={'eb2csv': []},
    include_package_data=True,
    install_requires=[
        'click', 'arrow', 'requests',
    ],
    entry_points='''
        [console_scripts]
        eb2csv=eb2csv.eb2csv:cli
    ''',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
