==========
pysnippets
==========

Python Snippets

Installation
============

::

    pip install pysnippets


Usage
=====

dict::

    In [1]: import pysnippets.dictsnippets as dsn

    In [2]: dsn.filter({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'])
    Out[2]: {'c': 3, 'd': 4}

    In [3]: dsn.filter({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'], exec_eval=False)
    Out[3]: {'c': 3, 'd': '4'}

    In [4]: dsn.gets({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'])
    Out[4]: [3, 4]

    In [5]: dsn.gets({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'], exec_eval=False)
    Out[5]: [3, '4']


list::

    In [1]: import pysnippets.listsnippets as lsn

    In [2]: lsn.all([1, 2, 3], [1, 2])
    Out[2]: True

    In [3]: lsn.any([1, 2, 3], [1, 5])
    Out[3]: True


str::

    In [1]: import pysnippets.strsnippets as ssn

    In [2]: ssn.strip(None)

    In [3]: ssn.strip(' xyz ')
    Out[3]: 'xyz'

