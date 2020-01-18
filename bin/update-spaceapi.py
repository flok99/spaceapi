#! /usr/bin/python

# retrieve https://raw.githubusercontent.com/SpaceApi/directory/master/directory.json

# for each k/v: generate md5 of key, check if a table with that key exists
# if not, create it

# write new list to /home/space/bin/spaces.json

import json
import md5
import MySQLdb
import sys
import urllib2

db_host = 'localhost'
db_name = 'spaceapi'
db_user = 'spaceapi'
db_pass = 'spaceapi'

con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
cur = con.cursor()

def check_table_exists(dbcon, tablename):
    cursor = dbcon.cursor()

    stmt = "SHOW TABLES LIKE '%s'" % tablename
    cursor.execute(stmt)
    result = cursor.fetchone()

    cursor.close()

    if result:
        return True

    return False

def add_space(key, name, value):
    try:
        cur.execute("CREATE TABLE data_%s(ts DATETIME NOT NULL, open INT(3) NOT NULL DEFAULT '0')" % key)

        cur.execute("INSERT INTO spaces(`key`, name, url, logo) VALUES(%s, %s, %s, '')", (key, name, value))

        con.commit()

    except MySQLdb.IntegrityError, e:
        print 'mysql failure: %s' % (e)
        sys.exit(1)

contents = urllib2.urlopen("https://raw.githubusercontent.com/SpaceApi/directory/master/directory.json").read()
js = json.loads(contents)

for key in js:
    m = md5.new()
    m.update(key.encode('utf-8'))
    key_md5 = m.hexdigest()

    if not check_table_exists(con, 'data_%s' % key_md5):
        add_space(key_md5, key.encode('utf-8'), js[key])
        print key, key_md5
