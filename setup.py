try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Plotting biological data in matplotlib.',
    'author': 'Darcy Jones',
    'url': 'https://github.com/darcyabjones/bioplotlib',
    'download_url': 'https://github.com/darcyabjones/bioplotlib',
    'author_email': 'darcy.ab.jones@gmail.com',
    'version': '0.1',
    'install_requires': ['numpy', 'matplotlib'],
    'packages': ['bioplotlib'],
    'scripts': [],
    'name': 'bioplotlib'
}

setup(**config)
