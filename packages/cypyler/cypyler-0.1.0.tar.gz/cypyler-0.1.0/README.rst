=======
Cypyler
=======


.. image:: https://img.shields.io/pypi/v/cypyler.svg
        :target: https://pypi.python.org/pypi/cypyler

.. image:: https://img.shields.io/travis/gpkc/cypyler.svg
        :target: https://travis-ci.org/gpkc/cypyler


.. image:: https://pyup.io/repos/github/gpkc/cypyler/shield.svg
     :target: https://pyup.io/repos/github/gpkc/cypyler/
     :alt: Updates



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


* Free software: MIT license
