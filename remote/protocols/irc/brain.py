'''
Created on 19 Nov 2009

@author: wax
'''

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from twisted.protocols.irc import *
from twisted.python import log

from scrutator.protocols.common import BasicClientBrain
from scrutator.core.event import SpawnEvent
from remote.protocols.irc.event import IrcEvent
from remote.protocols.genericbrain import GenericBrainClient
from remote.protocols.event import LinkEvent





class IrcBrainClient(BasicClientBrain):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainClient, self).__init__()
        
    def onInit(self):
        super(IrcBrainClient, self).onInit()
        self.pushToMaster(LinkEvent(url="http://diveintopython.adrahon.org/xml_processing/packages.html", author="test", channel="phantom"))
        
    def onThink(self):
        log.msg("ON THINK ! => ")
        
    def onConnectAction(self, event, evtMgr):
        f = BotFactory(cm.servers[server])
        reactor.connectTCP(cm.servers[server].host, 6667, f)
