'''
Created on 27 Nov 2009

@author: wax
'''



class IrcChannel:
    def __init__(self):
        self.name = "unknown"
        self.verbose = 0
        self.canTalk = 0
        self.canLearn = 0
        self.status = "offline"

class IrcServer:
    def __init__(self):
        self.name = "unknown"
        self.host = "127.0.0.1"
        self.channels = dict()
        self.nickname = "red_abzeu"

    def addChannel(self, channel):
        if self.channels.has_key(channel.name):
            raise "this server already exist"
        
        self.channels[str(channel.name)] = channel
        
    def getChannels(self):
        return self.channels.values()
    
    def removeChannel(self, channel):
        del self.channels[str(channel.name)]


                
        
         