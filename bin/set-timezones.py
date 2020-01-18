#! /usr/bin/python

import httplib2
import json
import MySQLdb
import socket
import sys
from threading import Thread, Lock
import time
import urllib2

mutex = Lock()

db_host = 'localhost'
db_name = 'spaceapi'
db_user = 'spaceapi'
db_pass = 'spaceapi'

con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
cur = con.cursor()
cur.execute('SELECT `key`, sa FROM spaces WHERE timezone IS NULL')
#cur.execute('SELECT `key`, sa FROM spaces')

for row in cur.fetchall():
    if row[1] == '':
        continue

    js = json.loads(row[1])

    if 'location' in js:
        if 'lat' in js['location'] and 'lon' in js['location']:
            lat = js['location']['lat']
            lon = js['location']['lon']
        elif 'latitude' in js['location'] and 'longitude' in js['location']:
            lat = js['location']['latitude']
            lon = js['location']['longitude']
        else:
            continue
    elif 'lat' in js and 'lon' in js:
        lat = js['lat']
        lon = js['lon']
    else:
        continue

    contents = urllib2.urlopen('http://api.timezonedb.com/v2.1/get-time-zone?key=PLEASE_SET_YOUR_OWN_KEY_HERE&format=json&by=position&lat=%s&lng=%s' % (lat, lon)).read()
    jstz = None
    try:
        jstz = json.loads(contents)
    except:
        print contents
        sys.exit(1)

    str_ = jstz['zoneName']
    if str_ == None:
        continue

    print row[0], lat, lon, str_

    cur.execute("UPDATE spaces SET timezone=%s, timezone_long=%s, offset=%s WHERE `key`=%s", (str_, contents, jstz['gmtOffset'], row[0]))
    con.commit()

    time.sleep(1.1)
