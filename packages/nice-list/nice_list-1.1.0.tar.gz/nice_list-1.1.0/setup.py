from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nice_list',
    version='1.1.0',

    description='Pretty prints Python lists',
    long_description=long_description,
    author='Philipp Ploder',
    url='https://github.com/Fylipp/nice-list',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='lists',

    packages=['nice_list']
)
