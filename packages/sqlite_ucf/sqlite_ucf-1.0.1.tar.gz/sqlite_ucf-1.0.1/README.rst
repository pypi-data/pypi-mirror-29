==========
sqlite_ucf
==========
An alternate sqlite3.connect function that adds unicode case folding functionality.

.. image:: https://travis-ci.org/tim-mitchell/sqlite_ucf.svg?branch=master
    :target: https://travis-ci.org/tim-mitchell/sqlite_ucf

The builtin sqlite3 module provides access to sqlite databases which
support unicode characters::

    >>> conn = sqlite3.connect(':memory:')
    >>> cur = conn.cursor()
    >>> cur.execute('CREATE TABLE test (a text COLLATE NOCASE)')
    >>> data = ['A', 'a', 'Á', 'á']
    >>> cur.executemany('INSERT INTO test VALUES (?)', [(x,) for x in data])
    
    >>> cur.execute('SELECT * from test').fetchall()
    [('A',), ('a',), ('Á',), ('á',)]
    
However the sqlite functions ``lower()``, ``upper()``, ``like()`` and the ``nocase`` collation
only implement ascii case folding.  That is [A-Z] maps to [a-z] and vice versa.
This can lead to unexpected results::

    >>> cur.execute('SELECT lower(a) from test').fetchall()
    [('a',), ('a',), ('Á',), ('á',)]
    
    cur.execute('SELECT DISTINCT a from test').fetchall()
    [('A',), ('Á',), ('á',)]
    
The sqlite_ucf (SQLITE Unicode Case Folding) wrapper uses 
``sqlite3.Connection.create_function`` to override the built-in ``lower``, ``upper`` and ``like`` functions, 
and ``sqlite3.Connection.create_collation`` to override the built-in ``nocase`` collation.

There are 2 ways to enable unicode case folding. 
Using the ``sqlite_ucf.connect`` method with ``unicode_case_folding=True``::

    >>> conn = sqlite_ucf.connect(':memory:', unicode_case_folding=True, ...)

or by setting the module variable ``unicode_case_folding_default`` to ``True``::

    >>> sqlite_ucf.unicode_case_folding_default = True
    
which will then make all ``sqlite_ucf.connect`` calls add unicode case folding to the 
connection::

    >>> conn = sqlite_ucf.connect(':memory:')
    >>> cur.execute('SELECT lower(a) from test').fetchall()
    [('a',), ('a',), ('á',), ('á',)]
    
    cur.execute('SELECT DISTINCT a from test').fetchall()
    [('A',), ('Á',)]

You can still use your own ``sqlite3.Connection`` subclass with the ``factory`` key-word.

-------
Caveats
-------
Note that the default value for ``unicode_case_folding_default`` is ``False`` which is the 
same as using sqlite3 directly.  This is because unicode case folding makes the 
sqlite database non-portable to other languages for which sqlite bindings exist.  
A unique index on a text column with a nocase collation which is unique when 
created with sqlite in another language may not be unique with the python unicode 
case-folding collation function installed.  Unicode case folding is not safe to use 
with databases that will be opened by other non-python applications.

