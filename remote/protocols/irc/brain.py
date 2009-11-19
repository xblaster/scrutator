'''
Created on 19 Nov 2009

@author: wax
'''
from scrutator.protocols.common import BasicServerBrain, BasicClientBrain
from scrutator.core.event import SpawnEvent
from remote.protocols.irc.event import IrcEvent

class IrcBrainServer(BasicServerBrain):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainServer, self).__init__()
        self.spawned = list()
    
    def onFirstPing(self, eventObj, evtMgr):
        #print "NEW CLIENT !!!!!!!!"
        pass
     
    def onThink(self):
        self.launchClient()
    
    def launchClient(self):
        for source in self.getContext().getBean('RegistryBrain').getHostList():
            if not source in self.spawned:
                self.sendTo(source,SpawnEvent(brain='remote.protocols.irc.brain.IrcBrainClient'))
                self.spawned.append(source)


class IrcBrainClient(BasicClientBrain):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainClient, self).__init__()
        
    def onInit(self):
        super(IrcBrainClient, self).onInit()