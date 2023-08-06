.. image:: https://readthedocs.org/projects/trio_mysql/badge/?version=latest
    :target: http://trio_mysql.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/python-trio/trio-mysql.svg?branch=master
    :target: https://travis-ci.org/python-trio/trio-mysql

.. image:: https://coveralls.io/repos/python-trio/trio-mysql/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/python-trio/trio-mysql?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/python-trio/trio-mysql/blob/master/LICENSE


Trio-MySQL
==========

.. contents:: Table of Contents
   :local:

This package contains a pure-Python and Trio-enhanced MySQL client library.
It is a mostly-straightforward clone of PyMySQL, adding async methods
compatible with the Trio framework.

NOTE: Trio-MySQL tries to adhere to (an async version of) the high level
database APIs defined in `PEP 249`_. Some differences, however, are
unavoidable.

.. _`PEP 249`: https://www.python.org/dev/peps/pep-0249/

Requirements
-------------

* Python -- one of the following:

  - CPython_ >= 3.5
  - PyPy_ >= 5.5

* MySQL Server -- one of the following:

  - MySQL_ >= 4.1  (tested with only 5.5~)
  - MariaDB_ >= 5.1

.. _CPython: http://www.python.org/
.. _PyPy: http://pypy.org/
.. _MySQL: http://www.mysql.com/
.. _MariaDB: https://mariadb.org/


Installation
------------

The last stable release is available on PyPI and can be installed with ``pip``::

    $ pip install trio_mysql


Documentation
-------------

Documentation is available online: http://trio_mysql.readthedocs.io/

For support, please refer to the `StackOverflow
<http://stackoverflow.com/questions/tagged/trio_mysql>`_.

Example
-------

The following examples make use of a simple table

.. code:: sql

   CREATE TABLE `users` (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `email` varchar(255) COLLATE utf8_bin NOT NULL,
       `password` varchar(255) COLLATE utf8_bin NOT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
   AUTO_INCREMENT=1 ;


.. code:: python

    import trio_mysql.cursors

    # Connect to the database
    connection = trio_mysql.connect(host='localhost',
                                 user='user',
                                 password='passwd',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=trio_mysql.cursors.DictCursor)

    async with connection as conn:
        async with conn.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            await cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        conn.commit()

        # Alternately, you can set up a transaction:
        async with conn.transaction():
            async with conn.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                await cursor.execute(sql, ('webmistress@python.org', 'totally-secret'))

        async with conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            await cursor.execute(sql, ('webmaster@python.org',))
            result = await cursor.fetchone()
            print(result)

This example will print:

.. code:: python

    {'password': 'very-secret', 'id': 1}


Resources
---------

DB-API 2.0: http://www.python.org/dev/peps/pep-0249

MySQL Reference Manuals: http://dev.mysql.com/doc/

MySQL client/server protocol:
http://dev.mysql.com/doc/internals/en/client-server-protocol.html

Trio chat: https://gitter.im/python-trio/general

License
-------

Trio-MySQL is released under the MIT License. See LICENSE for more information.
