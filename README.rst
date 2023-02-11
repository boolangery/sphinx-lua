###############################################################################
sphinx-lua
###############################################################################

.. image:: https://img.shields.io/pypi/v/sphinx-lua.svg
    :target: https://pypi.python.org/pypi/sphinx-lua/
.. image:: https://img.shields.io/pypi/pyversions/sphinx-lua.svg
    :target: https://pypi.python.org/pypi/sphinx-lua/

A lua-autodoc tool for Sphinx.
Generate a beautiful sphinx doc using lua doc comment.

It use `emmylua <https://emmylua.github.io/annotations/class.html>`_ as primary doc syntax but it is also
compatible with some `ldoc <https://stevedonovan.github.io/ldoc/manual/doc.md.html>`_ tags.


Installation
===============================================================================

.. code-block:: bash

    $ pip install sphinx-lua

Dependencies:

    * Jinja2 (to render rst template)
    * luadoc (to parse lua comments)
    * sphinxcontrib-luadomain (to add lua domain to sphinx)


Sphinx integration
===============================================================================

Add the following to your conf.py:

.. code-block:: python

    extensions = [
        'sphinxcontrib.luadomain', 
        'sphinx_lua'
        ]
        
    # Available options and default values
    lua_source_path = ["./"]
    lua_source_encoding = 'utf8'
    lua_source_comment_prefix = '---'
    lua_source_use_emmy_lua_syntax = True
    lua_source_private_prefix = '_'

    
The ``lua_source_path`` configuration value tells to sphinx-lua where to find
lua source code.

With above configuration, if `main.lua` is located in `../src/lua/main.lua`, and it's content
is:

.. code-block:: lua

    --- Define a car.
    --- @class MyOrg.Car
    local cls = class()

    --- @param foo number
    function cls:test(foo)
    end

You can autodoc it in sphinx with the following directive:

.. code-block:: rst

    .. lua:autoclass:: MyOrg.Car


Troubleshooting
===============================================================================

Sphinx-lua use the documentation model extracted from luadoc (https://github.com/boolangery/py-lua-doc)

So you can print this model out using the command line tool:

.. code-block:: bash

    $ luadoc ../src/lua/my_problematic_source_file.lua


Available sphinx directives
===============================================================================

The following directives are available:

.. code-block:: rst

    .. lua:autoclass:: pl.List

    .. lua:automodule:: pl.stringx

    .. lua:autoclasssummary:: ^pl.


You can also use directive provided by ``sphinxcontrib.luadomain``:

https://github.com/boolangery/sphinx-luadomain#available-sphinx-directives


Showing original source code
-------------------------------------------------------------------------------

You can display method source code appending the flag ``show-source``:

.. code-block:: rst

    .. lua:autoclass:: pl.List
        :show-source:
