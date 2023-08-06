#!/usr/bin/env python
import os
import codecs
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

PACKAGE_NAME = 'student_portal_crawler'

install_requires = [
    'beautifulsoup4>=4.5.0',
    'lxml>=4.0.0',
    'requests>=2.15.0'
]

tests_require = [
    'nose>=1.3.7',
    'coverage'
]

about_module = dict()
with codecs.open(os.path.join(HERE, PACKAGE_NAME, '__version__.py'), 'r', 'utf-8') as fp:
    exec(fp.read(), about_module)

setup(
    name=PACKAGE_NAME,
    version=about_module['__version__'],
    description=about_module['__description__'],
    author=about_module['__author__'],
    author_email=about_module['__author_email__'],
    url=about_module['__url__'],
    packages=find_packages(exclude=('doc', 'venv')),
    package_data={'': ['LICENSE']},
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires='>=3.5',
    setup_requires=['nose>=1.3'],
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet'
    ),
    test_suite='nose.collector'
)
