'''
Created on 17 Nov 2009

@author: wax
'''

from twisted.internet import reactor
from scrutator.core.manager import EventManager

from scrutator.core.event import PingEvent

class Brain(object):
    def __init__(self):
        reactor.callLater(0.2, self.onInit)
        
    def onInit(self):
        raise Exception("must be implemented")
    

class BasicBrain(Brain):
    think_period = 10
    
    def __init__(self):
        super(BasicBrain, self).__init__()
        self.localbus = EventManager()
        
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        reactor.callLater(self.think_period,self.__cycle)
        
    def __cycle(self):
        reactor.callLater(self.think_period,self.__cycle)
        self.onThink()
    
    def onThink(self):
        pass
        
        
class BasicServerBrain(BasicBrain):
    def __init__(self):
        super(BasicServerBrain, self).__init__()
        #self.localbus.bind(PingEvent().getType(), self.onPing)
    
class BasicClientBrain(BasicBrain):
    def __init__(self):
        super(BasicClientBrain, self).__init__()
        
    def onInit(self):
        self.senderbus = self.getContext().getBean("eventSender")
        super(BasicClientBrain, self).onInit()

    
    def onThink(self):
        super(BasicClientBrain, self).onThink()
        self.senderbus.push(PingEvent())