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

influx_server = '172.29.0.1'
influx_port = 2003

url_ok_open = 0
url_ok_closed = 0
url_fail = 0

def push_influx(key, value):
    message = '%s %s %d\n' % (key, value, int(time.time()))

    sock = socket.socket()
    sock.connect((influx_server, influx_port))
    sock.sendall(message)
    sock.close()

def fetch_space(row):
    global url_ok_open
    global url_ok_closed
    global url_fail

    try:
        #print 'Fetching %s for %s' % (row[2], row[1])

        resp, data_in = httplib2.Http(timeout=10, disable_ssl_certificate_validation=True).request(row[2])
        #print '\t=> %s' % resp['status']

        data = json.loads(data_in)

        logo = data.get('logo', 'no-logo.png')

        state = False

        if 'state' in data:
            state = data['state']['open']
        else:
            state = data['open']

        add = 0
        if state:
            add = 1
            url_ok_open += 1

        else:
            url_ok_closed += 1

        try:
            mutex.acquire()

            con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
            cur = con.cursor()
            cur.execute("INSERT INTO data_%s(ts, open) VALUES(NOW(), %d)" % (row[0], add))
            cur.execute("UPDATE spaces SET logo=%s, get_ok=get_ok + 1, get_total=get_total + 1, sa=%s, lns=%s WHERE `key`=%s", (logo, data_in, add, row[0]))
            con.commit()
            con.close()

        except MySQLdb.IntegrityError, e:
            print 'mysql failure: %s' % (e)

        finally:
            mutex.release()

    except Exception as e:
        print '\t%s failed: %s %s' % (row[1], e, row[2])

        url_fail += 1

        try:
            mutex.acquire()

            con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
            cur = con.cursor()
            # assume space is closed if could not reach it ("lns")
            cur.execute("UPDATE spaces SET get_err=get_err + 1, get_total=get_total + 1, lns=0 WHERE `key`='%s'" % row[0])
            con.commit()
            con.close()

        except MySQLdb.IntegrityError, e:
            print 'mysql failure: %s' % (e)

        finally:
            mutex.release()

con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
cur = con.cursor()
cur.execute('SELECT `key`, name, url, logo FROM spaces ORDER BY RAND()')

tl = []

for row in cur.fetchall():
    #if row[0] == 'aeba17f028b269dbb92582ab21a53f7d':
    #    print row
        t = Thread(target=fetch_space, args=(row,))
        t.start()
        tl.append(t)

for t in tl:
    t.join()

push_influx('spaceapi.ok.open', url_ok_open)
push_influx('spaceapi.ok.closed', url_ok_closed)
push_influx('spaceapi.fail', url_fail)
