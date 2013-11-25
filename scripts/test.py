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

import sqlanydb

con = sqlanydb.connect(userid='dba', password='sql')
cur = con.cursor()
cur.execute('select count(*) from Employees')
assert cur.fetchone()[0] > 0
con.close()
print('sqlanydb successfully installed.')
