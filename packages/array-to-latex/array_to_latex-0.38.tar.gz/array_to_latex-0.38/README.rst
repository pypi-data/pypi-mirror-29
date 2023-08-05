Convert NumPy/SciPy arrays to formatted LaTeX arrays
====================================================

.. image:: https://badge.fury.io/py/array_to_latex.png/
    :target: http://badge.fury.io/py/array_to_latex

The package ``array_to_latex`` converts a NumPy/SciPy array to a LaTeX
array including `Python 3.x
style <https://mkaz.tech/python-string-format.html>`__ (or `alternatively <https://www.python-course.eu/python3_formatted_output.php>`__) formatting of the result.

*New in* 0.37: Now handles complex arrays.
*New in* 0.38: Aligns columns neatly.  

Install using ``pip install --user array_to_latex``

Please read the help which explains usage.

.. code:: python

    import numpy as np
    import array_to_latex as ar
    A = np.array([[1.23456, 23.45678],[456.23, 8.239521]])
    ar.to_ltx(A, frmt = '{:6.2f}', arraytype = 'array')

will print the LaTeX code to your ouput.

.. code:: python

    import numpy as np
    import array_to_latex as ar
    A = np.array([[1.23456, 23.45678],[456.23, 8.239521]])
    ar.to_clp(A, frmt = '{:6.2f}', arraytype = 'array')

will put the array onto your clipboard.

More detailed information on usage is in the help.

.. code:: python

    import array_to_latex as ar
    help(ar.to_ltx)

An interesting alternative approach is `np array to latex <https://github.com/bbercovici/np_array_to_latex>`_.
