#!/usr/bin/env python
# ***************************************************************************
# Copyright (c) 2013 SAP AG or an SAP affiliate company. All rights reserved.
# ***************************************************************************
#######################################################################
# This sample code is provided AS IS, without warranty or liability
# of any kind.
# 
# You may use, reproduce, modify and distribute this sample code
# without limitation, on the condition that you retain the foregoing
# copyright notice and disclaimer as to the original code.
# 
#######################################################################
# 
# This sample program contains a hard-coded userid and password
# to connect to the demo database. This is done to simplify the
# sample program. The use of hard-coded passwords is strongly
# discouraged in production code.  A best practice for production
# code would be to prompt the user for the userid and password.
#
#######################################################################
import sys
import sqlanydb
import dbapi20
import unittest

class test_sqlanydb(dbapi20.DatabaseAPI20Test):
    driver = sqlanydb
    connect_args = ()
    connect_kw_args = dict(userid='dba', password='sql')

    def test_setoutputsize(self): pass
    def test_setoutputsize_basic(self): pass

if __name__ == '__main__':
    unittest.main()
    print('''Done''')
