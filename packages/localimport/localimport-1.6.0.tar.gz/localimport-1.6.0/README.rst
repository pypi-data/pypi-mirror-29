.. raw:: html

   <p align="center">

localimport allows you to import Python modules in an isolated
environment, preserving the global importer state.

.. raw:: html

   </p>

Features
========

-  Emulates an isolated environment for Python module imports
-  Evaluates ``*.pth`` files
-  Compatible with ``pkg_resources`` namespaces
-  Mocks ``pkgutil.extend_path()`` to support zipped Python eggs

Example
=======

Given your Python script, application or plugin comes with a directory
that contains modules for import, you can use localimport to keep the
global importer state clean.

::

    app.py
    res/modules/
      some_package/
        __init__.py

.. code:: python

    # app.py
    with localimport('res/modules') as _importer:
      import some_package
    assert 'some_package' not in sys.modules

    **Important**: You must keep the reference to the ``localimport``
    object alive, especially if you use ``from xx import yy`` imports.

Usage
=====

| In most cases it would not make sense to use ``localimport`` as a
  Python module when you actually want to import Python modules since
  the import of the ``localimport`` module itself would not be isolated.
| The solution is to use the ``localimport`` source code directly in
  your application code. Usually you will use a minified version.

Pre-minified versions of ``localimport`` can be found in this
`Gist <http://bitly.com/localimport-min>`__. Of course you can minify
the code by yourself, for example using the
```nr`` <https://github.com/NiklasRosenstein/py-nr>`__ command-line
tools.

::

    nr py.blob localimport.py -cm > localimport-gzb64-w80.py

Depending on your application, you may want to use a bootstrapper entry
point.

.. code:: python

    # @@@ minified localimport here @@@

    with localimport('.') as _importer:
      _importer.disable('my_application_package')
      from my_application_package.__main__ import main
      main()

--------------

.. raw:: html

   <p align="center">

Copyright © 2018 Niklas Rosenstein

.. raw:: html

   </p>
