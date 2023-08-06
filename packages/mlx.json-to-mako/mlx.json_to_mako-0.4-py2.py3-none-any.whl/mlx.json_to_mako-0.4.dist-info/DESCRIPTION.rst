.. image:: https://img.shields.io/hexpm/l/plug.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0
    :alt: Apache2 License

.. image:: https://badge.fury.io/py/mlx.json-to-mako.svg
    :target: https://badge.fury.io/py/mlx.json-to-mako
    :alt: Pypi packaged release

.. image:: https://travis-ci.org/melexis/json-to-mako.svg?branch=master
    :target: https://travis-ci.org/melexis/json-to-mako
    :alt: Build status

.. image:: https://codecov.io/gh/melexis/json-to-mako/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/melexis/json-to-mako
    :alt: Code Coverage

.. image:: https://codeclimate.com/github/melexis/json-to-mako/badges/gpa.svg
    :target: https://codeclimate.com/github/melexis/json-to-mako
    :alt: Code Climate Status

.. image:: https://codeclimate.com/github/melexis/json-to-mako/badges/issue_count.svg
    :target: https://codeclimate.com/github/melexis/json-to-mako
    :alt: Issue Count

.. image:: https://requires.io/github/melexis/json-to-mako/requirements.svg?branch=master
    :target: https://requires.io/github/melexis/json-to-mako/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
    :target: https://github.com/melexis/json-to-mako/issues
    :alt: Contributions welcome

======================
JSON to MAKO generator
======================

Python script that converts JSON database(s) to any templated output using MAKO templates.

.. _json_to_mako_installing:

----------
Installing
----------

.. code-block::

    pip3 install mlx.json_to_mako

.. _json_to_mako_usage:

-----
Usage
-----

The script takes multiple JSON input files, combines them in a python list, and renders the
data through a provided template. No data-parsing functionality is provided by the script:
the complexity of 'interpreting' the data is done in the MAKO templates.

Example
=======

General use:

.. code-block:: bash

    json-to-mako --input database.json --template rendering.mako --output rendered.html

The MAKO-template should match the dataformat of the JSON input file. The script adds

- a list at the top level: multiple input JSON files are appended to a list,
- some metadata in order to identify the input source

The usage on how to match the dataformat between JSON and MAKO is explained through an
example in the *example/* directory.

Multiple input files
====================

The `--input` flag can be provided multiple times in order to provide multiple JSON databases. This
is explained by the example.

.. code-block:: bash

    json-to-mako --input database1.json --input database2.json--template rendering.mako --output rendered.html

The multiple JSON databases are appended into a python list. Your MAKO-template needs to incorporate this by e.g.
looping over the different databases. See example/ folder for details.


