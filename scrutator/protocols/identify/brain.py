'''
Created on 17 Nov 2009

@author: wax
'''

from scrutator.protocols.common import Brain, BasicClientBrain, BasicServerBrain
from scrutator.protocols.identify.event import IdentifyEvent, IdentifyReceiveEvent, GlobalEvent

from scrutator.core.event import DieEvent, SpawnEvent

from twisted.internet import reactor
from scrutator.core.listener import SpawnListener

from scrutator.core.listener import PrintListener

class GlobalBrainServer(BasicServerBrain):
    transport_event = GlobalEvent
    def onInit(self):
        super(GlobalBrainServer, self).onInit()
        self.hostList = list()
        self.localbus.bind(IdentifyEvent().getType(), self.onIdentify)
        
    def onIdentify(self, eventObj, evtMgr):
        source = eventObj.source
        print "identify !!!"
        if not source in self.hostList:
            
            self.hostList.append(source)
            self.sendTo(source,IdentifyReceiveEvent())
            self.sendTo(source,SpawnEvent(brain='scrutator.protocols.common.BasicClientBrain'))

class GlobalBrainClient(BasicClientBrain):
    
    transport_event = GlobalEvent
    def onInit(self):
        super(GlobalBrainClient, self).onInit()
        #self.bus = self.getContext().getBean("mainEventManager")
        #self.sender = self.getContext().getBean('eventSender')
        print "init global brain"
        self.pushToMaster(IdentifyEvent())

      
class MinimalBrainClient(BasicClientBrain):
    transport_event = GlobalEvent
    def onInit(self):
        super(MinimalBrainClient, self).onInit()
        self.bus = self.getContext().getBean("mainEventManager")
        self.bus.bind(DieEvent().getType(), self.onDieEvent)
        self.bus.bind(SpawnEvent().getType(), SpawnListener())

    def onDieEvent(self, eventObj, evtMgr):
        print "DIEEEEEE !!!"
        reactor.stop()
    