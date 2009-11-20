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
        
        #for arg in ["url", "author", "channel", "desc", "network"]:
        #    if not linkEvent.hasArgEntry(arg):
        #        linkEvent.setArgEntry(arg,"unknown")
        
        server = xmlrpclib.ServerProxy("http://scrutator.lo2k.net/index.php?ctrl=API&action=index")
        lo2kObj = server.lo2k
        log.msg("**********************")
        log.msg("REGISTERINGGGG LINK "+linkEvent.url)
        return lo2kObj.add_link(linkEvent.url, linkEvent.author, linkEvent.channel, linkEvent.desc, linkEvent.network, 'scrutator2', 'coincoin')
