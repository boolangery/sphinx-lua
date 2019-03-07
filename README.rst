sphinx-lua
===============================================================================

.. image:: https://img.shields.io/pypi/v/sphinx-lua.svg
    :target: https://pypi.python.org/pypi/sphinx-lua/
.. image:: https://img.shields.io/pypi/pyversions/sphinx-lua.svg
    :target: https://pypi.python.org/pypi/sphinx-lua/

A lua-autodoc tool for Sphinx.
Generate a beautiful sphinx doc using lua doc comment.

It use `emmylua <https://emmylua.github.io/annotations/class.html>`_ as primary doc syntax but it is also
compatible with some `ldoc <https://stevedonovan.github.io/ldoc/manual/doc.md.html>`_ tags.


Installation
-------------------------------------------------------------------------------

.. code-block:: bash

    $ pip install sphinx-lua

Dependencies:

    * Jinja2 (to render rst template)
    * luadoc (to parse lua comments)
    * sphinxcontrib-luadomain (to add lua domain to sphinx)


Sphinx integration
-------------------------------------------------------------------------------

Add the following to your conf.py:

.. code-block:: python

    extensions = ['sphinx_lua', 'sphinxcontrib.luadomain']

Available sphinx directives
-------------------------------------------------------------------------------

The following directives are available:

.. code-block:: rst

    .. lua:autoclass:: pl.List

    .. lua:automodule:: pl.stringx


You can also use directove provided by ``sphinxcontrib.luadomain``:

https://github.com/boolangery/sphinx-luadomain#available-sphinx-directives
