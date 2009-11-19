'''
Created on 17 Nov 2009

@author: wax
'''

from twisted.internet import reactor
from scrutator.core.manager import EventManager
from scrutator.core.listener import GateListener, PrintListener

from scrutator.core.event import PingEvent, ContainerEvent, SimpleEvent
from scrutator.core.event import DieEvent, SpawnEvent, PingEvent

from twisted.internet import reactor
from scrutator.core.listener import SpawnListener
from scrutator.core.sync.listener import FileContentListener
from scrutator.core.sync.event import FileContent

class Brain(object):
    def __init__(self):
        reactor.callLater(0.2, self.onInit)
        
    def onInit(self):
        raise Exception("must be implemented")
    

class BasicBrain(Brain):
    think_period = 10
    
    
    def __init__(self):
        super(BasicBrain, self).__init__()
        
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        reactor.callLater(self.think_period,self.__cycle)
        
    def __cycle(self):
        reactor.callLater(self.think_period,self.__cycle)
        self.onThink()
    
    def onThink(self):
        pass
        
        


        
class BasicServerBrain(BasicBrain):
    
    transport_event = ContainerEvent
    
    def __init__(self):
        super(BasicServerBrain, self).__init__()
        self.localbus = EventManager()
        
    def onInit(self):
        
        super(BasicServerBrain, self).onInit()
        from scrutator.core.callback import ToBasicBrainLocalbusCallback 
        callback = ToBasicBrainLocalbusCallback()
        gate_listener = GateListener(self.localbus, callback.callback)
        self.bus.bind(self.transport_event().getType(), gate_listener)
        
    def sendTo(self, to, msg):
        self.bus.getMessageBoxManager().push(SimpleEvent(to=to, msg=msg))
        
    
class BasicClientBrain(BasicBrain):
    transport_event = ContainerEvent
    
    def __init__(self):
        super(BasicClientBrain, self).__init__()
        
    def onInit(self):
        self.senderbus = self.getContext().getBean("eventSender")
        super(BasicClientBrain, self).onInit()

    
    def onThink(self):
        super(BasicClientBrain, self).onThink()
        #self.senderbus.push(PingEvent())
        self.pushToMaster(PingEvent())
        
    def pushToMaster(self, param_event):
        event = self.transport_event()
        event.setArgEntry('content', param_event)
        self.senderbus.push(event)
        
        
class MinimalBrainClient(BasicClientBrain):
    def onInit(self):
        super(MinimalBrainClient, self).onInit()
        self.bus = self.getContext().getBean("mainEventManager")
        self.bus.bind(DieEvent().getType(), self.onDieEvent)
        self.bus.bind(SpawnEvent().getType(), SpawnListener())
        #<trigger event="scrutator.core.sync.event.FileContent" bean="fileContentListener"></trigger>
        self.bus.bind(FileContent().getType(), FileContentListener())
        self.bus.bind('all', PrintListener())

    def onDieEvent(self, eventObj, evtMgr):
        print "DIEEEEEE !!!"
        reactor.stop()
