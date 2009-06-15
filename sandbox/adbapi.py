# -*- coding: utf-8 -*-
# Using the "dbmodule" from the previous example, create a ConnectionPool 
from twisted.enterprise import adbapi 
from twisted.internet import reactor
import MySQLdb
import MySQLdb.cursors

dbpool = adbapi.ConnectionPool("MySQLdb", 
			       host='127.0.0.1', 
			       user='root', 
			       passwd='blah', 
			       db="scrutator",
			       cursorclass = MySQLdb.cursors.DictCursor
)

def getServers():
    #return dbpool.runQuery("SELECT * FROM servers WHERE name = ?", user)
    return dbpool.runQuery("SELECT * FROM servers")

def printResult(l):
    for line in l:
      print line
    return 1

def shutdown(result):
    reactor.stop()

d = getServers()
d.addCallback(printResult)
d.addBoth(shutdown)

reactor.run()
