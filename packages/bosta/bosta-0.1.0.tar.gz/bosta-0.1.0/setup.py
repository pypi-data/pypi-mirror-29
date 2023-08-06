"""Setup script for Bosta Python SDK."""

from setuptools import setup

import io


with io.open('README.rst', encoding='utf-8') as f:
    README = f.read()

setup(
    name='bosta',
    version='0.1.0',
    description='Bosta Python SDK',
    long_description=README,
    license='BSD',
    url='https://github.com/Zbooni/bosta-sdk-python',
    author='Zbooni',
    author_email='tech@zbooni.com',
    packages=['bosta'],
    install_requires=[
        'requests>=2.18',
    ],
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
