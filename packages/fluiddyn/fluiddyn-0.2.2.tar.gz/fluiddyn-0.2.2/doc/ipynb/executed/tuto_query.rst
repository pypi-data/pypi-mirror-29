
Query
=====

This notebook should demonstrate how the functions of the module :mod:`fluiddyn.io.query` can be used. 

This functions are useful to query things to the user with a simple interaction through text. So for this notebook, we need to interact manually.

.. code:: ipython3

    from fluiddyn.io.query import query, query_number, query_yes_no

.. code:: ipython3

    query_yes_no('Would you like to continue?')


.. parsed-literal::

    Would you like to continue? [Y/n] 



.. parsed-literal::

    True



.. code:: ipython3

    query_yes_no('Would you like to continue?', default='no')


.. parsed-literal::

    Would you like to continue? [y/N] 



.. parsed-literal::

    False



.. code:: ipython3

    query_yes_no('Would you like to continue?')


.. parsed-literal::

    Would you like to continue? [Y/n] 



.. parsed-literal::

    True



.. code:: ipython3

    query_yes_no('Would you like to continue?')


.. parsed-literal::

    Would you like to continue? [Y/n] Please respond with 'yes' or 'no' (or 'y' or 'n').
    Would you like to continue? [Y/n] 



.. parsed-literal::

    False



.. code:: ipython3

    query_number('Which number do you like?')


.. parsed-literal::

    Which number do you like? 



.. parsed-literal::

    1.2



.. code:: ipython3

    query('Hello, what is your name?')


.. parsed-literal::

    Hello, what is your name?



.. parsed-literal::

    'Boule'



...
