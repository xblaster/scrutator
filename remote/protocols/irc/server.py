'''
Created on 20 Nov 2009

@author: wax
'''
from remote.protocols.genericbrain import GenericBrainServer
from remote.protocols.irc.event import IrcEvent, JoinActionEvent, InitEvent
from scrutator.core.event import SpawnEvent, DieEvent, SimpleEvent
from remote.protocols.event import ConnectEventAction, ConnectEvent, DisconnectEvent, InfoContentEvent
from remote.protocols.irc.services import IrcServices
from remote.protocols.irc.model import IrcRessourceManager, Agent
from remote.services.helpers import getComputername, getNickName

from twisted.python import log
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class IrcSQLRessourceManager(IrcRessourceManager):
    def __init__(self):
        super(IrcSQLRessourceManager, self).__init__()
        self.services = IrcServices()
        self.request = self.services.getModel()
        
        self.docked = list()
        self.spawnRequest= dict()
        for server in self.request:
            self.docked.append(server.emptyClone())
         
         
    def addDockedChannel(self, channel, host):
        super(IrcSQLRessourceManager, self).addDockedChannel(channel, host)
        self.services.setChanStatus(channel)
        
    def addRequestChannel(self, channel, host):
        channel.bot = "offline"
        super(IrcSQLRessourceManager, self).addRequestChannel(channel, host)
        self.services.setChanStatus(channel)
    
    def addSpawnRequest(self, agentname, server):
        if not self.spawnRequest.has_key(getComputername(agentname)):
            self.spawnRequest[getComputername(agentname)] = list()
        if not server in self.spawnRequest[getComputername(agentname)]:
            self.spawnRequest[getComputername(agentname)].append(server)
            self.sendTo(agentname,SpawnEvent(brain='remote.protocols.irc.brain.IrcBrainClient'))
            
        
    def hasSpawnRequest(self, agentname):
        if not self.spawnRequest.has_key(getComputername(agentname)):
            return False
        else:
            if len(self.spawnRequest[getComputername(agentname)]) == 0:
                return False
        return True
        
    
    def getSpawnRequest(self,agentname):
        return self.spawnRequest[getComputername(agentname)].pop()
    
    def requestNewAgent(self, allowed, server):
        if len(allowed) == 0:
            return
        
        from random import Random
        rnd = Random()

        agentname = allowed[rnd.randint(0, len(allowed)-1)]
        
        self.addSpawnRequest(agentname, server)
       
    
    def getRootAgents(self):
        try:
            return self.getContext().getBean('RegistryBrain').getHostList()
        except:
            return list()
    
    def onClientInit(self, eventObj, evtMgr):
        source = eventObj.source
        
        print "SPAWNNN: "+str(self.spawnRequest)
        
        if self.hasSpawnRequest(source):
            server = self.getSpawnRequest(source)
            if server=="irc.worldnet.net" and getComputername(source)=='oil-ocean':
                self.sendTo(source, ConnectEventAction(nickname="scrutator", server="irc.worldnet.net", port=6667))
            else:
                self.sendTo(source, ConnectEventAction(nickname=getNickName(), server=server, port=6667))
            
            agent = Agent()
            agent.name = source
            agent.server = server
            
            self.onRegisterAgent(agent)
            
        else:
            print "DIE !!!"
            self.sendTo(source, DieEvent())
        #self.sendTo(source, JoinActionEvent(channel="#funradio"))
        #self.sendTo(source, JoinActionEvent(channel="#cochonne"))
        #self.sendTo(source, JoinActionEvent(channel="#scrutator"))
    
    def hasRunnningAgentsWithName(self, name):
        for agent in self.getRunnningAgents():
            if agent.name == name:
                return True
        return False
    
    def manageChannel(self):
        log.msg("Manage Channel")
        for server in self.request:
            log.msg("--> server "+server.host)
            for channel in server.getChannels():
                log.msg("---> channel "+channel.name)
                agent = self.bestAgentFor(channel, server.host)
                if agent != None:
                    self.sendTo(agent.name, JoinActionEvent(channel=channel.name))
        
        #garbage collector chan
        for server in self.docked:
            for channel in server.getChannels():
                #print "bot name "+channel.bot
                #print "runnin" +str(self.getRunnningAgents())
                notfound = True
                if not self.hasRunnningAgentsWithName(channel.bot):
                    log.msg("Garbage collector chan "+channel.name)
                    self.addRequestChannel(channel, server.host) 
        
        print self.spawnRequest
        
    


class IrcBrainServer(GenericBrainServer):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainServer, self).__init__()
        self.spawned = list()
        self.resManager = IrcSQLRessourceManager()
        
        self.resManager.sendTo = self.sendTo
        
        
    def onInit(self):
        super(IrcBrainServer, self).onInit()
        self.resManager.getContext = self.getContext
        self.localbus.bind(ConnectEvent().getType(), self.onConnectEvent)
        self.localbus.bind(DisconnectEvent().getType(), self.onDisconnectEvent)
        self.localbus.bind(InfoContentEvent().getType(), self.resManager.onInfoContent)
        self.localbus.bind(InitEvent().getType(), self.resManager.onClientInit)
        #self.resManager.pushToMaster = self.pushToMaster
        
        reactor.callLater(60,self.launchManagerChannel)
    
    def onLooseAgent(self,agentName):
        a = Agent()
        a.name = agentName
        self.resManager.onUnregisterAgent(a)
        
    def launchManagerChannel(self):
        lc = LoopingCall(self.resManager.manageChannel)
        lc.start(30)
        
    def onFirstPing(self, eventObj, evtMgr):
        print "NEW CLIENT !!!!!!!!"
        source = eventObj.source
        
        #give that to res manager
        #self.sendTo(source, ConnectEventAction(nickname="scrutator", server="irc.worldnet.net", port=6667))
        #self.sendTo(source, ConnectEventAction(nickname="ERNEST", server="irc.worldnet.net", port=6667))
     
    def onDisconnectEvent(self, eventObj, evtMgr):
        source = eventObj.source
        self.sendTo(source, DieEvent())
     
    def onConnectEvent(self, eventObj, evtMgr):
        source = eventObj.source
        #self.sendTo(source, JoinActionEvent(channel="#funradio"))
        #self.sendTo(source, JoinActionEvent(channel="#cochonne"))
        #self.sendTo(source, JoinActionEvent(channel="#scrutator"))
 
     
    def onThink(self):
        self.launchClient()
    
    def launchClient(self):
        for source in self.getContext().getBean('RegistryBrain').getHostList():
            if not source in self.spawned:
                self.sendTo(source,SpawnEvent(brain='remote.protocols.irc.brain.IrcBrainClient'))
                self.spawned.append(source)