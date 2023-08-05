=======
Cypyler
=======


.. image:: https://img.shields.io/pypi/v/cypyler.svg
        :target: https://pypi.python.org/pypi/cypyler

.. image:: https://img.shields.io/travis/gpkc/Cypyler.svg
        :target: https://travis-ci.org/gpkc/Cypyler


A cython compiler for compiling source code in string form.

Example:

.. code:: python

    from cypyler import TMPCypyler

    code = """
    def add(x, y):
        return x + y
    """

    cp = TMPCypyler()
    built_module = cp.build(code)
    built_module.add(2, 3)


Usage
-----

Cypyler
~~~~~~~

Instantiation
^^^^^^^^^^^^^
.. code:: python

    from cypyler import Cypyler

    cp = Cypyler('<build_dir>', '<libraries>', '<include_dirs>')

Where ``build_dir`` is the desired directory (path) for the module to be built on.
The arguments ``libraries`` and ``include_dirs`` are lists containing libraries and include directories that should be passed to Cython when compiling.


Building
^^^^^^^^

.. code:: python

    cp.build('<code>', '<suffix>')

Where ``code`` is the code in string form. The ``suffix`` argument defaults to ``.pyx``.


TMPCypyler
~~~~~~~~~~

Instantiation
^^^^^^^^^^^^^

.. code:: python

    from cypyler import TMPCypyler

    cp = Cypyler('<build_dir_prefix>', '<libraries>', '<include_dirs>')

Where ``build_dir_prefix`` is a prefix for the temporary build directory.
The build directory is created using the ``tempfile.mkdtemp`` function from the Python standard library.


Building
^^^^^^^^

.. code:: python

    cp.build('<code>', '<suffix>')

Where ``code`` is the code in string form. The ``suffix`` argument defaults to ``.pyx``.


* Free software: MIT license


