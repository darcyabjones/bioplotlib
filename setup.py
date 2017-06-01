"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


config = {
    'name': 'bioplotlib',
    'version': '0.0.1',
    'description': long_description,
    'author': 'Darcy Jones',
    'author_email': 'darcy.ab.jones@gmail.com',
    'url': 'https://github.com/darcyabjones/bioplotlib',
    'download_url': 'https://github.com/darcyabjones/bioplotlib',
    'packages': find_packages(),
    'install_requires': ['numpy', 'matplotlib'],
    'scripts': [],
    'extras_require': {
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest', 'tox'],
        },
    'package_data': {
        'bioplotlib': ['data/*.json', 'data/*.csv', 'data/*.pkl'],
        },
    'include_package_data': True,
}


setup(**config)
