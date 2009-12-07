'''
Created on 1 Dec 2009

@author: wax
'''
from remote.protocols.irc.model import IrcServer, IrcChannel
import ConfigParser, os


import MySQLdb
import MySQLdb.cursors

class IrcServices:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        #config.readfp(open('default.cfg'))
        config.read('default.cfg')
        #print config.get("database", "username")
        self.dbpool = MySQLdb.connect( 
                   host= config.get("database", "host"), 
                   user= config.get("database", "username"), 
                   passwd= config.get("database", "passwd"), 
                   db=config.get("database", "db"),
                   cursorclass = MySQLdb.cursors.DictCursor
        ).cursor()
                   
    def getServerList(self):
        self.dbpool.execute("SELECT * FROM servers")
        return self.dbpool.fetchall()
    
    def getModel(self):
        self.dbpool.execute("SELECT * FROM `channels`, servers WHERE server_id = servers.id AND (server_id=3 OR server_id=2 OR server_id=1 OR server_id=4 OR server_id=8)")
        
        servers = dict()
        
        for elt in self.dbpool.fetchall():
            
            host = elt["host"]
            
            if not servers.has_key(host):
                server = IrcServer()
                server.host = host
                servers[host] = server
            
            server = servers[host]
            
            channel = IrcChannel()
            channel.name = elt["name"]
            
            server.addChannel(channel)
            
        return servers.values()
    
    def setChanStatus(self, channel):
        self.dbpool.execute("UPDATE `channels` SET `status` = '"+channel.bot+"', `lastupdate` = '"+getNowInMysql()+"' WHERE `name` ='"+channel.name+"' LIMIT 1")


def getNowInMysql():
    from datetime import datetime
    from time import strftime
    newdate = datetime.now()
    mysqldate = strftime("%Y-%m-%d %H:%M:%S", newdate.timetuple()) 
    
    return mysqldate    