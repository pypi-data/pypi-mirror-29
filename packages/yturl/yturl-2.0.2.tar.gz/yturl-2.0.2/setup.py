#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as readme_f:
    README = readme_f.read()

with open('requirements.txt') as requirements_f:
    REQUIREMENTS = requirements_f.readlines()


setup(
    name='yturl',
    version='2.0.2',
    description='Gets direct media URLs to YouTube media',
    long_description=README,
    url='https://github.com/cdown/yturl',
    license='Public Domain',

    author='Chris Down',
    author_email='chris@chrisdown.name',

    py_modules=['yturl'],

    entry_points={
        'console_scripts': ['yturl=yturl:main'],
    },

    keywords='youtube media video',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia',
        'Topic :: Internet',
        'Topic :: Utilities',
    ],

    install_requires=REQUIREMENTS,
)
