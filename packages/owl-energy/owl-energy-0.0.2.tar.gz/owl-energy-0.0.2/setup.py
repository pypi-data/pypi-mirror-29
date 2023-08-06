from setuptools import setup
import re

owlinit = open('owlenergy/__init__.py').read()
author = re.search("__author__ = '([^']+)'", owlinit).group(1)
author_email = re.search("__author_email__ = '([^']+)'", owlinit).group(1)
version = re.search("__version__ = '([^']+)'", owlinit).group(1)

setup(
    name='owl-energy',
    version=version,
    long_description=open('README.md').read(),
    packages=['owlenergy'],
    url='https://stretchproject.org',
    license='MIT',
    author=author,
    author_email=author_email,
    description='A python package for OWL energy monitor using sockets',
    keywords='owl energy monitor consumption current',
)
