#! /usr/bin/python

import httplib2
import json
import MySQLdb
import socket
import sys
from threading import Thread, Lock
import time
import urllib2

db_host = 'localhost'
db_name = 'spaceapi'
db_user = 'spaceapi'
db_pass = 'spaceapi'

con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
con2 = MySQLdb.connect(db_host, db_user, db_pass, db_name)
cur = con.cursor()
cur2 = con2.cursor()
cur.execute('SELECT `key`, name FROM spaces ORDER BY name')
print('<table>')
print('<tr><th>space</th><th>percentage open</th></tr>')
for row in cur.fetchall():
    cur2.execute('SELECT sum(open)/count(*) * 100 from data_' + row[0])
    row2 = cur2.fetchone()
    print('<tr><td>%s</td><td>%s%%</td></tr>' % (row[1], row2[0]))
print('</table>')

con2.close()
con.close()
