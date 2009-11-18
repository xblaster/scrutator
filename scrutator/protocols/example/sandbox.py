'''
Created on 18 Nov 2009

@author: wax
'''

from scrutator.protocols.common import BasicClientBrain, BasicServerBrain
from scrutator.core.event import PingEvent

class SandboxBrain(BasicClientBrain):
    think_period = 100
    def __init__(self):
        super(SandboxBrain, self).__init__()
        
    def onInit(self):
        super(SandboxBrain, self).onInit()
        print "init brain !"
    
    def onThink(self):
        super(SandboxBrain, self).onThink()
        print "thinking !!!"
        self.pushToMaster(PingEvent())
        
class SandboxBrainServer(BasicServerBrain):
    think_period = 2
    def __init__(self):
        super(SandboxBrainServer, self).__init__()
        
    def onInit(self):
        super(SandboxBrainServer, self).onInit()
    
    def onThink(self):
        super(SandboxBrainServer, self).onThink()
        print "LIST :"
        for name in self.getContext().getBean('RegistryBrain').getHostList():
            print name
        #print "thinking !!!"
        
