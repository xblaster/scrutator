'''
Created on 17 Nov 2009

@author: wax
'''

from scrutator.protocols.common import Brain, BasicClientBrain, BasicServerBrain
from scrutator.protocols.identify.event import IdentifyEvent, IdentifyReceiveEvent, GlobalEvent

from scrutator.core.event import DieEvent, SpawnEvent, PingEvent

from twisted.internet import reactor
from scrutator.core.listener import SpawnListener

from scrutator.core.listener import PrintListener

class GlobalBrainServer(BasicServerBrain):
    transport_event = GlobalEvent
    
    def onInit(self):
        super(GlobalBrainServer, self).onInit()
        self.hostList = list()
        self.localbus.bind(IdentifyEvent().getType(), self.onIdentify)
        self.localbus.bind(PingEvent().getType(), self.onPing)
    
    def onPing(self, eventObj, evtMgr):
        source = eventObj.source
        if not source in self.hostList:
            self.hostList.append(source)    
    
    def onIdentify(self, eventObj, evtMgr):
        source = eventObj.source
        
    def getHostList(self):
        return self.hostList
        #self.sendTo(source,SpawnEvent(brain='scrutator.protocols.common.BasicClientBrain'))

class GlobalBrainClient(BasicClientBrain):
    
    transport_event = GlobalEvent
    def onInit(self):
        super(GlobalBrainClient, self).onInit()
        #self.pushToMaster(IdentifyEvent())

      
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
    