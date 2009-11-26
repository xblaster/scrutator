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
        



from twisted.python import log




class CleanUpObserver(object):

    def __init__(self, loggerName="twisted"):
        pass
    
    def emit(self, eventDict):
        if 'logLevel' in eventDict:
            level = eventDict['logLevel']
        elif eventDict['isError']:
            level = log.logging.ERROR
        else:
            level = log.logging.INFO
        text = log.textFromEventDict(eventDict)
        if text is None:
            return
        if "twisted.web.xmlrpc._QueryFactory" in text:
            return
        self.logger.log(level, text)
   
log.observers=[]
log.addObserver(CleanUpObserver)
print ""
print ""
print ""
print "change observer"
