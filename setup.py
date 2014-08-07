# !/usr/bin/env python
import setuptools
from distutils.core import setup

setup(
    name='Kit',
    description='The project manager C never had.',
    author='Adam Smith',
    author_email='dsmith2@wpi.edu',
    version='0.1',
    packages=['kit',],
    license='MIT',
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': [
            'kit = kit.main:run_cli']
    }
)