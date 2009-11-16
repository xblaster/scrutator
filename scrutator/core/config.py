'''
Created on 16 Nov 2009

@author: wax
'''

from scrutator.core.sync.listener import FileContentListener
from scrutator.minidi.injector import PythonConfig

from scrutator.core.manager import *
from scrutator.core.network import XMLRPCClient

class AgentConfig(PythonConfig):
    def fileContentListener(self):
        return FileContentListener()
    
    def eventSender(self):
        return XMLRPCClient(self.getContext().getObject('distantURI'),self.getContext().getObject('mainEventManager'))
    
    def mainEventManager(self):
        mm = EventManager()
        context = self.getContext()
        
        mm.loadXMLMap('resource/impl/client.xml', self.getContext())
        
        return mm
    
    def distantURI(self):
        return "http://localhost:7080"

