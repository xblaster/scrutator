'''
Created on 17 Nov 2009

@author: wax
'''

from scrutator.protocols.common import Brain
from scrutator.protocols.identify.event import IdentifyEvent, IdentifyReceiveEvent

from scrutator.core.event import DieEvent, SpawnEvent

from twisted.internet import reactor
from scrutator.core.listener import SpawnListener
import scrutator

class GlobalBrainServer(Brain):
    
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        self.hostList = list()
        self.bus.bind(IdentifyEvent().getType(), self.onIdentify)
        

    def onIdentify(self, eventObj, evtMgr):
        source = eventObj.source
        if not source in self.hostList:
            self.hostList.append(source)
            evtMgr.push(IdentifyReceiveEvent())
            evtMgr.push(SpawnEvent(brain='scrutator.protocols.common.BasicClientBrain'))

class GlobalBrainClient(Brain):
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        self.sender = self.getContext().getBean('eventSender')
        self.sender.push(IdentifyEvent())

      
class MinimalBrainClient(Brain):
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        self.bus.bind(DieEvent().getType(), self.onDieEvent)
        self.bus.bind(SpawnEvent().getType(), SpawnListener())

    def onDieEvent(self, eventObj, evtMgr):
        print "DIEEEEEE !!!"
        reactor.stop()
    