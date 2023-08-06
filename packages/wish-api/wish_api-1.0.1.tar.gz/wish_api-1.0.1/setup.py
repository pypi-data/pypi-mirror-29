from setuptools import setup, find_packages
from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='wish_api',
    version='1.0.1',
    description='simple python wish partner api client',
    long_description=long_description,
    url='https://github.com/ketu/wish_api',
    author='ketu.lai',
    author_email='ketu.lai@gmail.com',
    license='MIT',
    keywords='wish api',
    packages= find_packages(),
    install_requires=[],
    tests_require=[],
)
