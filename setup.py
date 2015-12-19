from setuptools import setup, find_packages
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyshk',
    version='1.1.0',
    description='A python wrapper for the mlkshk API.',
    long_description=long_description,
    author='Jeremy Low',
    author_email='jeremy@hrhs.co.uk',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='mlkshk pyshk api',
    packages=find_packages(exclude=['tests', 'docs']),
    url='https://github.com/jeremylow/pyshk',
    install_requires=['requests',
                      'requests-oauthlib',
                      'requests_toolbelt',
                      'oauthlib',
                      'six'],
    )
