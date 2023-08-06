"""This file sets up the package"""

from setuptools import setup, find_packages

setup(
    name='gitflow-easyrelease',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'git-easyrelease = gitflow_easyrelease.cli_file:cli'
        ]
    }
)
