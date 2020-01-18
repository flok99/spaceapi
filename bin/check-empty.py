#! /usr/bin/python

import md5
import MySQLdb
import sys
import urllib2

db_host = 'localhost'
db_name = 'spaceapi'
db_user = 'spaceapi'
db_pass = 'spaceapi'

con = MySQLdb.connect(db_host, db_user, db_pass, db_name)

cursor = con.cursor()
stmt = "SHOW TABLES"
cursor.execute(stmt)
for row in cursor.fetchall():
    if row[0][0:4] != 'data':
        continue

    cursor2 = con.cursor()
    cursor2.execute('SELECT COUNT(*) FROM %s' % row[0])
    row2 = cursor2.fetchone()

    if row2[0] == 0:
        cursor2.execute('SELECT name FROM spaces WHERE `key`="%s"' % row[0][5:])
        row3 = cursor2.fetchone()

        if row3 == None:
            print row[0]

    cursor2.close()
