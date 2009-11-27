'''
Created on 19 Nov 2009

@author: wax
'''

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from twisted.protocols.irc import *

from scrutator.protocols.common import BasicClientBrain
from scrutator.core.event import SpawnEvent
from remote.protocols.irc.event import IrcEvent
from remote.protocols.genericbrain import GenericBrainClient
from remote.protocols.event import LinkEvent, ConnectEventAction

from remote.protocols.irc.connector import BotFactory


from twisted.protocols import basic

class RapidIdentServer(basic.LineOnlyReceiver):
    def lineReceived(self, line):
        parts = line.split(',')
        if len(parts) != 2:
            return
        self.sendLine('%d, %d : USERID : %s : %s' % (parts[1], parts[0], "UNIX", "scrutator"))
    def doStart(self):
        pass
    
    def doStop(self):
        pass
                    

class IrcBrainClient(BasicClientBrain):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainClient, self).__init__()
        
    def onInit(self):
        super(IrcBrainClient, self).onInit()
        #self.pushToMaster(LinkEvent(url="http://diveintopython.adrahon.org/xml_processing/packages.html", author="test", channel="phantom"))
        #self.bus.bind(DieEvent().getType(), self.onDieEvent)
        self.bus.bind(ConnectEventAction().getType(), self.onConnectAction)
        
    def onThink(self):
        super(IrcBrainClient, self).onThink()
        #log.msg("ON THINK ! => ")
        pass
        
    def onConnectAction(self, event, evtMgr):
        print ""
        print "CONNECTING !!!!"
        f = BotFactory(event.nickname, event.server)
        f.bus = self.bus
        f.pushToMaster = self.pushToMaster
        print "connect "+event.nickname+"@"+event.server+":"+str(event.port)
        
        #reactor.listenTCP(113, RapidIdentServer())
        reactor.connectTCP(event.server, event.port, f)
        
        #from twisted.protocols.ident import IdentServer
        
        #reactor.run()
