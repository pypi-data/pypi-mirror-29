from setuptools import setup

from codecs import open
from os import path

# Get the long description from the README file
long_description = ''
try:
    with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
        long_description = f.read()
except IOError:
    print("could not locate README")
    pass


setup(
    name='pfycat',
    version='0.0.1',
    packages=['pfycat'],
    url='https://gitlab.com/wotanii/pfycat',
    long_description=long_description,
    license='',
    author=u'wotaini',
    author_email='pypi@wotanii.de',
    description='python wrapper for gfycat',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['requests'],
)