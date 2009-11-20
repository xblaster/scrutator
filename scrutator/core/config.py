'''
Created on 16 Nov 2009

@author: wax
'''

from scrutator.core.sync.listener import *
from scrutator.core.listener import *
from scrutator.minidi.injector import PythonConfig

from scrutator.core.manager import *
from scrutator.core.network import *
from scrutator.core.sync.event import FileContent, FileRequest


class AgentConfig(PythonConfig):
    def fileContentListener(self):
        return FileContentListener()
    
    def eventSender(self):
        return XMLRPCClient(self.getContext().getObject('distantURI'),self.getContext().getObject('mainEventManager'))
    
    def mainEventManager(self):
        mm = EventManager()
        #mm.loadXMLMap('resource/impl/client.xml', self.getContext())
        mm.bind(FileContent().getType(),FileContentListener())
        
        return mm
    
    def distantURI(self):
        return "http://localhost:7080"

class ServerConfig(PythonConfig):
    def requestListener(self):
        return FileRequestListener()
    
    def rawCommandListener(self):
        return RawCommandListener()
    
    def defaultLogListener(self):
        return PrintListener
    
    def servicesObj(self):
        so = SCRTServices()
        so.manager = self.getContext().getBean('mainEventManager')
        return so
        
    def eventReceiver(self):
        return XMLRPCServer(self.getContext().getBean('servicesObj'),7080,self.getContext().getBean('mainEventManager'))    
    
    def mainEventManager(self):
        am = AsyncEventManager()
        #am.loadXMLMap('resource/impl/server_map.xml',self.getContext())
        am.bind(FileRequest().getType(),FileRequestListener())
        return am
    
    
