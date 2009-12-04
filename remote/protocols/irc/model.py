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
    
    def getRequestServerFor(self, host):
        for pserver in self.request:
            if pserver.host == host:
                return pserver
        return None
                
    def getDockedServerFor(self, host):
        for pserver in self.docked:
            if pserver.host == host:
                return pserver
        return None
        
    
    def addDockedChannel(self, channel, host):
        print "add docked "+channel.name+"/"+host
        persistent_dockserver = self.getDockedServerFor(host)
        persistent_requestserver = self.getRequestServerFor(host)
        
        persistent_dockserver.addChannel(channel)
        persistent_requestserver.removeChannel(channel)
        
    def addRequestChannel(self, channel, host):
        print "add request "+channel.name+"/"+host
        persistent_dockserver = self.getDockedServerFor(host)
        persistent_requestserver = self.getRequestServerFor(host)
        
        persistent_dockserver.removeChannel(channel)
        persistent_requestserver.addChannel(channel)
        
     
    def onInfoContent(self, eventObj, evtMgr):
        source = eventObj.source
        server = eventObj.server
        
        persistent_server = self.getDockedServerFor(server.host)
        
        if persistent_server == None:
            raise "Nhiii ? Which server is it ?"
        
        
        for channel in server.getChannels():
            if persistent_server.hasChannel(channel):
                persistent_channel = persistent_server.getChannel(channel)
                if not (persistent_channel.bot == source):
                    #implement two bots on the same chan 
                    pass 
            else:
                channel.bot = source
                self.addDockedChannel(channel, server.host)
                agent = self.getAgentByName(source)
                agent.server = server.host
                agent.nbchan = agent.nbchan +1

        for channel in persistent_server.getChannels():
            if channel.bot == source:
                if not server.hasChannel(channel):
                    #remove channel if not present in infoRequest
                    self.addRequestChannel(channel, server.host)
                    agent = self.getAgentByName(source)
                    agent.server = server.host
                    agent.nbchan = agent.nbchan  -1
        
        
    def getRootAgents(self):
        raise "Not implemented"
    
    def getRunnningAgents(self):
        return self.running_agents.values()    
    
    def requestNewAgent(self, allowed, server):
         pass

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
            self.requestNewAgent(allowed, server)
            return None
         
        return candidate.pop()
    
    def getAgentByName(self, name):
        if not self.running_agents.has_key(name):
            self.running_agents[name] = Agent()
            
        if self.running_agents[name] == None:
            self.running_agents[name] = Agent()
        
        return self.running_agents[name]
    
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
        self.bot =""

class IrcServer(object):
    def __init__(self):
        self.name = "unknown"
        self.host = "unknown"
        self.channels = dict()
        self.nickname = "red_abzeu"

    def addChannel(self, channel):
        if self.channels.has_key(channel.name):
            raise "this channel already exist"
        
        self.channels[str(channel.name)] = channel
    
    def hasChannel(self, channel):
        if self.channels.has_key(channel.name):
            return True
        return False
    
    def getChannels(self):
        return self.channels.values()
    
    def getChannel(self,name):
        if isinstance(name, IrcChannel):
            name = str(name.name)
        return self.channels[name]
    
    def removeChannel(self, channel):
        try:
            del self.channels[str(channel.name)]
        except:
            pass
        
    def emptyClone(self):
        serv = IrcServer()
        serv.name = self.name
        serv.host = self.host
        
        return serv
        


                
        
         