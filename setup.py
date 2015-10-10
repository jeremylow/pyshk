from setuptools import setup

setup(
    name='pyshk',
    packages=['pyshk'],
    version='0.0.1',
    author='Jeremy Low',
    url='https://github.com/jeremylow/pyshk',
    install_requires=['requests',
                      'requests-oauthlib',
                      'oauthlib'],
    license='MIT'
    )
