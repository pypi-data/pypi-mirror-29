from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'linux_daemon',
    version = '0.1.3',
    scripts = ['linux_daemon.py'],
    author = 'Victor Claessen',
    author_email = 'victor@victorclaessen.nl',
    url = 'http://www.victorclaessen.nl',
    description = 'A linux daemon wrapper',
    long_description = long_description,
    license = 'Free For Educational Use',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = 'linux daemon framework wrapper',
    packages = {'linux_daemon':'linux_daemon'},
)
