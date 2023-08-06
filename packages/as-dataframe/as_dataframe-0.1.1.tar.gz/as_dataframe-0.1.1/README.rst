as-dataframe
============

Convert dictionaries to dataframes.


Installation
============

.. code-block:: pycon

    pip install as-dataframe

Examples
========

Convert a plain dictionary into a dataframe:

.. code-block:: pycon

    >>> from as_dataframe import as_dataframe
    >>> plain_dict = {'first name': 'John', 'last name': 'Doe'}
    >>> print(as_dataframe(plain_dict))
      first name last name
    0       John       Doe


Dictionaries with list values are supported too of course:

.. code-block:: pycon

    >>> from as_dataframe import as_dataframe
    >>> dict_with_list_values = {'first name': ['John', 'Alice'], 'last name': ['Doe', 'Doe']}
    >>> print(as_dataframe(dict_with_list_values))
      first name last name
    0       John       Doe
    1      Alice       Doe


Convert a nested dictionary into a dataframe:

.. code-block:: pycon

    >>> from as_dataframe import as_dataframe
    >>> nested_dict = {'names': {'first': ['John', 'Alice'], 'last': ['Doe', 'Doe']}}
    >>> print(as_dataframe(nested_dict))
      names.first names.last
    0        John        Doe
    1       Alice        Doe


Convert a list of nested dictionaries into a dataframe:

.. code-block:: pycon

    >>> from as_dataframe import as_dataframe
    >>> nested_dicts = [{'a': {'b': [1, 2], 'c': [3, 4]}}, {'a': {'b': [5, 6], 'c': [7, 8]}}]
    >>> print(as_dataframe(nested_dicts))
       a.b  a.c
    0    1    3
    1    2    4
    2    5    7
    3    6    8
