'''
Created on 17 Nov 2009

@author: wax
'''

from scrutator.protocols.common import Brain
from scrutator.protocols.identify.event import IdentifyEvent, IdentifyReceiveEvent

class IdentifyBrainServer(Brain):
    
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        self.hostList = list()
        self.bus.bind(IdentifyEvent().getType(), self.onIdentify)
        

    def onIdentify(self, eventObj, evtMgr):
        source = eventObj.source
        if not source in self.hostList:
            self.hostList.append(source)
            evtMgr.push(IdentifyReceiveEvent())
            print "first contact from "+source

class IdentifyBrainClient(Brain):
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        self.sender = self.getContext().getBean('eventSender')
        self.sender.push(IdentifyEvent())
    