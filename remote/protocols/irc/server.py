'''
Created on 20 Nov 2009

@author: wax
'''
from remote.protocols.genericbrain import GenericBrainServer
from remote.protocols.irc.event import IrcEvent, JoinActionEvent
from scrutator.core.event import SpawnEvent, DieEvent
from remote.protocols.event import ConnectEventAction, ConnectEvent,\
    DisconnectEvent, InfoContentEvent
from remote.protocols.irc.services import IrcServices
from remote.protocols.irc.model import IrcRessourceManager
from remote.services.helpers import getComputername




class IrcSQLRessourceManager(IrcRessourceManager):
    def __init__(self):
        super(IrcSQLRessourceManager, self).__init__()
        services = IrcServices()
        self.request = services.getModel()
        
        self.docked = list()
        
        for server in self.request:
            self.docked = server.emptyClone()
            
       
    
    def getRootAgents(self):
        return self.getContext().getBean('RegistryBrain').getHostList()
    


class IrcBrainServer(GenericBrainServer):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainServer, self).__init__()
        self.spawned = list()
        self.resManager = IrcRessourceManager()
        
        
    def onInit(self):
        super(IrcBrainServer, self).onInit()
        
        self.localbus.bind(ConnectEvent().getType(), self.onConnectEvent)
        self.localbus.bind(DisconnectEvent().getType(), self.onDisconnectEvent)
        self.localbus.bind(InfoContentEvent().getType(), self.resManager.onInfoContent)
        
    def onFirstPing(self, eventObj, evtMgr):
        print "NEW CLIENT !!!!!!!!"
        source = eventObj.source
        self.sendTo(source, ConnectEventAction(nickname="scrutator", server="irc.worldnet.net", port=6667))
        #self.sendTo(source, ConnectEventAction(nickname="ERNEST", server="irc.worldnet.net", port=6667))
     
    def onDisconnectEvent(self, eventObj, evtMgr):
        source = eventObj.source
        self.sendTo(source, DieEvent())
     
    def onConnectEvent(self, eventObj, evtMgr):
        source = eventObj.source
        self.sendTo(source, JoinActionEvent(channel="#funradio"))
        self.sendTo(source, JoinActionEvent(channel="#cochonne"))
        self.sendTo(source, JoinActionEvent(channel="#scrutator"))
 
     
    def onThink(self):
        self.launchClient()
    
    def launchClient(self):
        for source in self.getContext().getBean('RegistryBrain').getHostList():
            if not source in self.spawned:
                self.sendTo(source,SpawnEvent(brain='remote.protocols.irc.brain.IrcBrainClient'))
                self.spawned.append(source)