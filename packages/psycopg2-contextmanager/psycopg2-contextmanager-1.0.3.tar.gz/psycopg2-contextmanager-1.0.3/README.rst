Installation
============

Run ``pip install psycopg2-contextmanager``

Usage
=====

::

    from psycopg2_contextmanager import database_connection

    with database_connection(<database_connection_string>) as cursor:
        cursor.execute(<query>)

Commits are handled automatically. If the query fails, the package will log the exception along with the line ``Unable to run query`` and re-raise it.
