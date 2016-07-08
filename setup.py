
from os.path import join, dirname
from setuptools import setup


setup(
    name='pyd2s',
    version='0.0.0',

    description='a python library to read and write diablo 2 save files',
    long_description=open(join(dirname(__file__), 'README.md')).read(),

    packages=[
        'pyd2s',
    ],

    install_requires=[],

    test_suite='tests',
    tests_require=[
        'pytest',
    ],

    setup_requires=['pytest_runner'],
)
