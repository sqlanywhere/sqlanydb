.. ***************************************************************************
.. Copyright (c) 2017 SAP SE or an SAP affiliate company. All rights reserved.
.. ***************************************************************************

sqlanydb
========

This package provides a python interface to the SQL Anywhere database
server. This interface conforms to PEP 249.

Requirements
------------
Before installing the sqlanydb interface please make sure the
following components are installed on your system.

* Python 2.4 or greater (including Python 3.x)
* Python ctypes module if missing
* SQL Anywhere 10 or higher

Installing the sqlanydb module
------------------------------
Run the following command as an administrative user to install
sqlanydb::

    python setup.py install

Alternatively, you can use pip::

    pip install sqlanydb

Converter Functions
-------------------
This library wraps around the sqlanydb ``dbcapi`` C library. When retrieving 
values from the database, the C API returns one of these types:

* A_INVALID_TYPE
* A_BINARY      
* A_STRING      
* A_DOUBLE      
* A_VAL64       
* A_UVAL64      
* A_VAL32       
* A_UVAL32      
* A_VAL16       
* A_UVAL16      
* A_VAL8        
* A_UVAL8       

Other types are returned as the above types. For example, the NUMERIC type is 
returned as a string. 

To have ``sqlanydb`` return a different or custom python object, you can register 
callbacks with the ``sqlanydb`` module, using 
``register_converter(datatype, callback)``. Callback is a function that takes
one argument, the type to be converted, and should return the converted value.
Datatype is one of the ``DT_`` variables present in the module.

The types available to register a converter for:

* DT_NOTYPE       
* DT_DATE         
* DT_TIME         
* DT_TIMESTAMP    
* DT_VARCHAR      
* DT_FIXCHAR      
* DT_LONGVARCHAR  
* DT_STRING       
* DT_DOUBLE       
* DT_FLOAT        
* DT_DECIMAL      
* DT_INT          
* DT_SMALLINT     
* DT_BINARY       
* DT_LONGBINARY   
* DT_TINYINT      
* DT_BIGINT       
* DT_UNSINT       
* DT_UNSSMALLINT  
* DT_UNSBIGINT    
* DT_BIT          
* DT_LONGNVARCHAR 

For example, to have NUMERIC types be returned as a python Decimal object::


    import decimal

    def decimal_callback(valueToConvert):
        return decimal.Decimal(valueToConvert)

    sqlanydb.register_converter(sqlanydb.DT_DECIMAL, decimal_callback)


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
This package is licensed under the terms of the Apache License, Version 2.0. See
the LICENSE file for details.

Feedback and Questions
----------------------
For feedback on this project, or for general questions about using SQL Anywhere
please use the SQL Anywhere Forum at http://sqlanywhere-forum.sap.com/
