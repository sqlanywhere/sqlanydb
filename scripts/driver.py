# ***************************************************************************
# Copyright (c) 2024 SAP SE or an SAP affiliate company. All rights reserved.
# ***************************************************************************
# This sample program contains a hard-coded userid and password
# to connect to the demo database. This is done to simplify the
# sample program. The use of hard-coded passwords is strongly
# discouraged in production code.  A best practice for production
# code would be to prompt the user for the userid and password.
# ***************************************************************************
import sqlanydb
import os, unittest
from runtests import test_sqlanydb

dbname = 'test'

def removedb(name):
    fname = name if name[-3:] == '.db' else name + '.db'
    if os.path.exists(fname):
        ret = os.system('dberase -y %s' % fname)
        if ret != 0:
            raise Exception('dberase failed (%d)' % ret)

def cleandb(name):
    removedb(name)
    ret = os.system('dbinit %s -dba dba,sqlanydb_pw' % name)
    if ret != 0:
        raise Exception('dbinit failed (%d)' % ret)

def stopdb(name):
    ret = os.system('dbstop -y -c "uid=dba;pwd=sqlanydb_pw"')
    if ret != 0:
        raise Exception('dbstop failed (%d)' % ret)

if __name__ == '__main__':
    cleandb(dbname)
    # Auto-start engine
    c = sqlanydb.connect(uid='dba', pwd='sqlanydb_pw', dbf=dbname)
    results = open('summary.out', 'w+')
    unittest.main(testRunner=unittest.TextTestRunner(results))
    results.close()
    # to cover bug272737, don't call c.close() to explicitly close the connection with
    # the driver that does not have the fix, the test will crash with the error like
    # Exception WindowsError: 'exception: access violation writing 0x0000000000000024' in
    #   <bound method Connection.__del__ of <sqlanydb.Connection object at 0x0000000002DFD198>> ignored
    # with the new one, the driver will close all outstanding connections before exit.
    # c.close()

    stopdb(dbname)
    removedb(dbname)
