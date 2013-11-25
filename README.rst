.. ***************************************************************************
.. Copyright (c) 2013 SAP AG or an SAP affiliate company. All rights reserved.
.. ***************************************************************************

sqlanydb
========

This package provides a python interface to the SQL Anywhere database
server. This interface conforms to PEP 249.

Requirements
------------
Before installing the sqlanydb interface please make sure the
following components are installed on your system.

* Python 2.4 or greater
* Python ctypes module if missing
* SQL Anywhere 10 or higher

Installing the sqlanydb module
------------------------------
Run the following command as an administrative user to install
sqlanydb::

    python setup.py install

Alternatively, you can use pip::

    pip install sqlanydb

Testing the sqlanydb module
---------------------------
To test that the Python interface to SQL Anywhere is working correctly
first start the demo database included with your SQL Anywhere
installation and then create a file named test_sqlany.py with the
following contents::

    import sqlanydb
    conn = sqlanydb.connect(uid='dba', pwd='sql', eng='demo', dbn='demo' )
    curs = conn.cursor()
    curs.execute("select 'Hello, world!'")
    print "SQL Anywhere says: %s" % curs.fetchone()
    curs.close()
    conn.close()

Run the test script and ensure that you get the expected output::

    > python test_sqlany.py
    SQL Anywhere says: Hello, world!

License
-------
This package is licensed under the terms of the Apache License, Version 2.0

Feedback and Questions
----------------------
For feedback on this project, or for general questions about using SQL Anywhere
please use the SQL Anywhere Forum at http://sqlanywhere-forum.sybase.com/
