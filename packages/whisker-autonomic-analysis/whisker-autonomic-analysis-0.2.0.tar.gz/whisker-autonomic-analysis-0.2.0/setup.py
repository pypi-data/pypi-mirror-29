#!/usr/bin/env python
# setup.py

"""
whisker_autonomic_analysis setup file

To use:

    python setup.py sdist

    twine upload dist/*

To install in development mode:

    pip install -e .

"""
# https://packaging.python.org/en/latest/distributing/#working-in-development-mode
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
# http://jtushman.github.io/blog/2013/06/17/sharing-code-across-applications-with-python/  # noqa

from setuptools import setup
from codecs import open
from os import path

from whisker_autonomic_analysis.version import VERSION

here = path.abspath(path.dirname(__file__))

# -----------------------------------------------------------------------------
# Get the long description from the README file
# -----------------------------------------------------------------------------
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

# -----------------------------------------------------------------------------
# setup args
# -----------------------------------------------------------------------------
setup(
    name='whisker-autonomic-analysis',

    version=VERSION,

    description='Analysis of telemetry data for Whisker tasks',
    long_description=long_description,

    # The project's main homepage.
    url='http://www.whiskercontrol.com/',

    # Author details
    author='Rudolf Cardinal',
    author_email='rudolf@pobox.com',

    # Choose your license
    license='GNU General Public License v3 or later (GPLv3+)',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa

        'Natural Language :: English',

        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Topic :: Software Development :: Libraries',
    ],

    keywords='autonomic cardinal whisker',

    packages=['whisker_autonomic_analysis'],  # what to include?

    install_requires=[
        'cardinal_pythonlib==1.0.12',
        'colorlog',
        'matplotlib',
        'numpy',
        'pendulum',
        'scipy',
        'sqlalchemy>=1.0.0',
    ],

    entry_points={
        'console_scripts': [
            # Format is 'script=module:function".
            'whisker_autonomic_analysis=whisker_autonomic_analysis.main:main',  # noqa
        ],
    },
)
