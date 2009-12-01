'''
Created on 20 Nov 2009

@author: wax
'''
from remote.protocols.genericbrain import GenericBrainServer
from remote.protocols.irc.event import IrcEvent, JoinActionEvent
from scrutator.core.event import SpawnEvent, DieEvent
from remote.protocols.event import ConnectEventAction, ConnectEvent,\
    DisconnectEvent






class IrcBrainServer(GenericBrainServer):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainServer, self).__init__()
        self.spawned = list()
        
    def onInit(self):
        super(IrcBrainServer, self).onInit()
        
        self.localbus.bind(ConnectEvent().getType(), self.onConnectEvent)
        self.localbus.bind(DisconnectEvent().getType(), self.onDisconnectEvent)
        
    
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