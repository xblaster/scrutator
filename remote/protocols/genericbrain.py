'''
Created on 20 Nov 2009

@author: wax
'''
from scrutator.protocols.common import BasicClientBrain, BasicServerBrain
from remote.protocols.event import LinkEvent
from twisted.python import log
import xmlrpclib

class GenericBrainClient(BasicClientBrain):
    pass

class GenericBrainServer(BasicServerBrain):
    pass

    def onInit(self):
        super(GenericBrainServer, self).onInit()
        self.localbus.bind(LinkEvent().getType(), self.addLink)

    def addLink(self, linkEvent, evtMgr):
        #url, author, channel, desc, network
        from remote.services.xmlrpc import addLink
        log.msg()
        log.msg()
        log.msg("RECORD LINK "+linkEvent.url)
        log.msg()
        log.msg()
        log.msg()
        addLink(linkEvent) 
