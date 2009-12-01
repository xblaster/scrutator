'''
Created on 1 Dec 2009

@author: wax
'''

from remote.protocols.irc.model import *
import unittest


def getMockModel():
    servers = dict()
    
    server = IrcServer()
    server.host = "irc.epiknet.org"
    
    chan = IrcChannel()
    chan.name = "#funradio"
    server.addChannel(chan)
    
    chan = IrcChannel()
    chan.name = "#scrutator"
    server.addChannel(chan)
    
    servers["irc.epiknet.org"] = server
    
    server = IrcServer()
    server.host = "irc.worldnet.org"
    
    chan = IrcChannel()
    chan.name = "#funradio"
    server.addChannel(chan)
    
    chan = IrcChannel()
    chan.name = "#chouchou"
    server.addChannel(chan)
    
    servers["irc.worldnet.org"] = server
    
    return servers.values()
    

class TestIrcModel(unittest.TestCase):
        
    def testIrcChan(self):
        server = IrcServer()
        server.host = "irc.epiknet.org"
    
        chan = IrcChannel()
        chan.name = "#funradio"
        server.addChannel(chan)
    
        chan = IrcChannel()
        chan.name = "#scrutator"
        server.addChannel(chan)
        
        self.assertEqual(2, len(server.getChannels()))
        
    def testIrcChanWithRemove(self):
        server = IrcServer()
        server.host = "irc.epiknet.org"
    
        chan = IrcChannel()
        chan.name = "#funradio"
        server.addChannel(chan)
    
        chan = IrcChannel()
        chan.name = "#scrutator"
        server.addChannel(chan)
        
        server.removeChannel(chan)
        
        self.assertEqual(1, len(server.getChannels()))
        
        
        
        