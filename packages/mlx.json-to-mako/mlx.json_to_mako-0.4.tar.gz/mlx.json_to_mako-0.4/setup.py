# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

project_url = 'https://github.com/melexis/json-to-mako'
exec(open('mlx/__version__.py').read())

requires = ['mako']

setup(
    name='mlx.json_to_mako',
    version=__version__,
    url=project_url,
    author='Stein Heselmans',
    author_email='teh@melexis.com',
    description='Convertor for JSON database(s) to MAKO templated output',
    long_description=open("README.rst").read(),
    zip_safe=False,
    license='Apache License, Version 2.0',
    platforms='any',
    packages=find_packages(exclude=['tests', 'example']),
    entry_points={'console_scripts': ['json-to-mako = mlx.json_to_mako:main']},
    install_requires=requires,
    namespace_packages=['mlx'],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords=['json', 'mako'],
)
