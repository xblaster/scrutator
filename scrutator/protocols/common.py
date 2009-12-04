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
    think_period = 30
    
    
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
        
        

from datetime import datetime

class Agent:
    time = None

    def update(self):
        self.time = datetime.now() 
        
    def getLastPing(self):
        return (datetime.now()-self.time).seconds
        
class BasicServerBrain(BasicBrain):
    
    transport_event = ContainerEvent
    delay_first_init = 60
    launched = False
    
    def __init__(self):
        super(BasicServerBrain, self).__init__()
        self.hostDict = dict()
        self.localbus = EventManager()
        self.localbus.bind(PingEvent().getType(), self.onPing)
        
        reactor.callLater(self.delay_first_init, self.onLaunch)
        
        
    def garbageAgent(self):
        for agentName in self.hostDict:
            agent = self.hostDict[agentName]
            
            if agent.getLastPing() > 360:
                del(self.hostDict[agentName])
            
    def onLooseAgent(self,agentName):
        pass        
    
    def onLaunch(self):
        launched = True
    
    def onPing(self, eventObj, evtMgr):
        source = eventObj.source
        if not self.hostDict.has_key(source):
            self.hostDict[source] = Agent()
            self.onFirstPing(eventObj, evtMgr) 
            if self.launched:
                self.onFirstInit(eventObj, evtMgr)
        
        self.hostDict[source].update()
            
    def onFirstPing(self, eventObj, evtMgr):
        pass  
    
    def onFirstInit(self, eventObj, evtMgr):
        pass  
        
    def onInit(self):
        super(BasicServerBrain, self).onInit()
        from scrutator.core.callback import ToBasicBrainLocalbusCallback 
        callback = ToBasicBrainLocalbusCallback()
        gate_listener = GateListener(self.localbus, callback.callback)
        self.bus.bind(self.transport_event().getType(), gate_listener)
        
        self.localbus.bind('all', PrintListener())
        
        #garbage agent which not respond
        from twisted.internet.task import LoopingCall
        lc = LoopingCall(self.garbageAgent)
        lc.start(60)
    
    def sendTo(self, to, msg):
        self.bus.getMessageBoxManager().push(SimpleEvent(to=to, msg=msg))

    def getAgentList(self):
        return self.hostDict
        
    def getHostList(self):
        return self.hostDict.keys()

        
    
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
