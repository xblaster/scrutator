'''
Created on 1 Dec 2009

@author: wax
'''

from remote.protocols.irc.model import *
from scrutator.core.manager import EventManager
from remote.protocols.event import InfoContentEvent
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
    
class IrcMockRessourceManager(IrcRessourceManager):
    def __init__(self):
        super(IrcMockRessourceManager, self).__init__()
        self.request = getMockModel()
        
        self.docked = list()
        
        for server in self.request:
            self.docked.append(server.emptyClone())
            
    def getRootAgents(self):
        res = list()
        res.append("Maury/154648646")
        res.append("Prio/154648646")
        return res
            

class TestIrcRessouce(unittest.TestCase):
    def testBest(self):
        manager = IrcMockRessourceManager()
        self.assertEqual(None,manager.bestAgentFor("#scrutator", "irc.epiknet.org"))
        
    def testBestWithRunning(self):     
        manager = IrcMockRessourceManager()
        agent = Agent()
        agent.name = "Prio/15616-1531561"
        agent.server = "irc.epiknet.org"
        manager.onRegisterAgent(agent)
        
        self.assertEqual(agent,manager.bestAgentFor("#scrutator", "irc.epiknet.org"))
        
    def testBestWithRunningButFull(self):     
        manager = IrcMockRessourceManager()
        agent = Agent()
        agent.name = "Prio/15616-1531561"
        agent.server = "irc.epiknet.org"
        agent.nbchan = 99
        manager.onRegisterAgent(agent)
        
        agent = Agent()
        agent.name = "Prio/14488645616-1531561"
        agent.server = "irc.worldnet.org"
        agent.nbchan = 0
        manager.onRegisterAgent(agent)
        
        self.assertEqual(None,manager.bestAgentFor("#scrutator", "irc.epiknet.org"))
    
    def testOnInfoContent(self):
        manager = IrcMockRessourceManager()
        agent = Agent()
        agent.name = "Prio/15616-1531561"
        agent.server = "irc.epiknet.org"
        agent.nbchan = 99
        manager.onRegisterAgent(agent)
        
        agent = Agent()
        agent.name = "Prio/14488645616-1531561"
        agent.server = "irc.worldnet.org"
        agent.nbchan = 0
        manager.onRegisterAgent(agent)
        
        #create content
        server = IrcServer()
        server.host = "irc.epiknet.org"
        
        channel = IrcChannel()
        channel.name = "#funradio"
        server.addChannel(channel)
        
        channelfun3 = IrcChannel()
        channelfun3.name = "#funradio3"
        server.addChannel(channelfun3)
        
        manager.onInfoContent(InfoContentEvent(server=server, source="sample/546846486"), EventManager())
        
        serv = manager.getDockedServerFor("irc.epiknet.org")
        self.assertEqual(True, serv.hasChannel(channel))
        self.assertEqual(True, serv.hasChannel(channelfun3))
        
        channelunk = IrcChannel()
        channelunk.name = "#unknown"
        server.addChannel(channelunk)
        
        self.assertEqual(False, serv.hasChannel(channelunk))
        
    def testOnInfoContentRemove(self):
        manager = IrcMockRessourceManager()
        agent = Agent()
        agent.name = "Prio/15616-1531561"
        agent.server = "irc.epiknet.org"
        agent.nbchan = 99
        manager.onRegisterAgent(agent)
        
        agent = Agent()
        agent.name = "Prio/14488645616-1531561"
        agent.server = "irc.worldnet.org"
        agent.nbchan = 0
        manager.onRegisterAgent(agent)
        
        #create content
        server = IrcServer()
        server.host = "irc.epiknet.org"
        
        channel = IrcChannel()
        channel.name = "#funradio"
        server.addChannel(channel)
        
        channelfun3 = IrcChannel()
        channelfun3.name = "#funradio3"
        server.addChannel(channelfun3)
        
        manager.onInfoContent(InfoContentEvent(server=server, source="sample/546846486"), EventManager())
        
        serv = manager.getDockedServerFor("irc.epiknet.org")
        self.assertEqual(True, serv.hasChannel(channel))
        self.assertEqual(True, serv.hasChannel(channelfun3))
        
        channelunk = IrcChannel()
        channelunk.name = "#unknown"
        server.addChannel(channelunk)
        
        self.assertEqual(False, serv.hasChannel(channelunk))
        
        #remove now
        #create content
        server = IrcServer()
        server.host = "irc.epiknet.org"
        
        channelfun3 = IrcChannel()
        channelfun3.name = "#funradio3"
        server.addChannel(channelfun3)

        channelscrut = IrcChannel()
        channelscrut.name = "#scrut"
        server.addChannel(channelscrut)
        
        manager.onInfoContent(InfoContentEvent(server=server, source="sample/546846486"), EventManager())
        
        serv = manager.getDockedServerFor("irc.epiknet.org")
        self.assertEqual(False, serv.hasChannel(channel))
        self.assertEqual(True, serv.hasChannel(channelscrut))

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
    
        chan2 = IrcChannel()
        chan2.name = "#scrutator"
        server.addChannel(chan2)
        
        server.removeChannel(chan2)
        
        self.assertEqual(1, len(server.getChannels()))
        
        chan_test = server.getChannels().pop()
        self.assertEqual(chan,chan_test);
        
    def testIrcChanGet(self):
        server = IrcServer()
        server.host = "irc.epiknet.org"
    
        chan = IrcChannel()
        chan.name = "#funradio"
        server.addChannel(chan)
    
        chan2 = IrcChannel()
        chan2.name = "#scrutator"
        server.addChannel(chan2)
        
        self.assertEqual(chan2, server.getChannel(chan2))
        self.assertEqual(chan2, server.getChannel("#scrutator"))
        
        
        
        