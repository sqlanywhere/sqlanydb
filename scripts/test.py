# ***************************************************************************
# Copyright (c) 2024 SAP SE or an SAP affiliate company. All rights reserved.
# ***************************************************************************
# This sample code is provided AS IS, without warranty or liability
# of any kind.
# 
# You may use, reproduce, modify and distribute this sample code
# without limitation, on the condition that you retain the foregoing
# copyright notice and disclaimer as to the original code.
# 
# ***************************************************************************
import sqlanydb
try: input = raw_input
except NameError: pass
myuid = input("Enter your user ID: ")
mypwd = input("Enter your password: ")
con = sqlanydb.connect(userid=myuid, pwd=mypwd)
cur = con.cursor()
cur.execute('select count(*) from Employees')
assert cur.fetchone()[0] > 0
con.close()
print('sqlanydb successfully installed.')
