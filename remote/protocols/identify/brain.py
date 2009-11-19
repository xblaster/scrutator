'''
Created on 17 Nov 2009

@author: wax
'''
from twisted.internet import reactor
from twisted.python import log

from scrutator.protocols.common import Brain, BasicClientBrain, BasicServerBrain
from scrutator.core.event import DieEvent, SpawnEvent, PingEvent
from scrutator.core.listener import SpawnListener
from scrutator.core.listener import PrintListener

from remote.protocols.identify.event import IdentifyEvent, IdentifyReceiveEvent, GlobalEvent



class GlobalBrainServer(BasicServerBrain):
    transport_event = GlobalEvent
    
    def onInit(self):
        super(GlobalBrainServer, self).onInit()
    
    #def onIdentify(self, eventObj, evtMgr):
    #    source = eventObj.source

        #self.sendTo(source,SpawnEvent(brain='scrutator.protocols.common.BasicClientBrain'))

class GlobalBrainClient(BasicClientBrain):
    
    transport_event = GlobalEvent
    def onInit(self):
        super(GlobalBrainClient, self).onInit()
        self.pushToMaster(IdentifyEvent())

      

    