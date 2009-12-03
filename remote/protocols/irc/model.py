'''
Created on 27 Nov 2009

@author: wax
'''
from remote.services.helpers import getComputername

class Agent(object):
    def __init__(self):
        self.name = ""
        self.server =""
        self.chan = list()
        self.nbchan = 0 

class IrcRessourceManager(object):
    def __init__(self):
        self.request = list()
        self.docked = list()
        self.running_agents = dict()
        
    def onInfoContent(self, eventObj, evtMgr):
        source = eventObj.source
        server = eventObj.server
        
    def getRootAgents(self):
        raise "Not implemented"
    
    def getRunnningAgents(self):
        return self.running_agents.values()     

    def bestAgentFor(self, channel, server):
        allowed = self.getRootAgents()        
        
        candidate = list()
        
        for agent in self.getRunnningAgents():
            if agent.server == server:    
                if agent.nbchan < 8:
                    candidate.append(agent)
                for root_agent in allowed:
                    if getComputername(root_agent)==getComputername(agent.name):
                        allowed.remove(root_agent) 
        
        #if no candidate
        if len(candidate)==0:
            print allowed
            return None
         
        return candidate.pop()
                
    def onRegisterAgent(self, agent):
        self.running_agents[agent.name] = agent
        
    def onUnregisterAgent(self,agent):
        del self.running_agents[agent.name]
        

class IrcChannel(object):
    def __init__(self):
        self.name = "unknown"
        self.verbose = 0
        self.canTalk = 0
        self.canLearn = 0
        self.status = "offline"

class IrcServer(object):
    def __init__(self):
        self.name = "unknown"
        self.host = "unknown"
        self.channels = dict()
        self.nickname = "red_abzeu"

    def addChannel(self, channel):
        if self.channels.has_key(channel.name):
            raise "this server already exist"
        
        self.channels[str(channel.name)] = channel
        
    def getChannels(self):
        return self.channels.values()
    
    def getChannel(self,name):
        if isinstance(name, IrcChannel):
            name = str(name.name)
        return self.channels[name]
    
    def removeChannel(self, channel):
        del self.channels[str(channel.name)]
        
    def emptyClone(self):
        serv = IrcServer()
        serv.name = self.name
        serv.host = self.host
        


                
        
         