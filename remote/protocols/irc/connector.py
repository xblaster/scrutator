'''
Created on 25 Nov 2009

@author: wax
'''

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from remote.protocols.event import DisconnectEvent, ConnectEvent, LinkEvent, InfoRequestEvent, InfoContentEvent
from remote.protocols.irc.event import JoinActionEvent, PartEvent, JoinEvent
from scrutator.core.event import KickEvent
from scrutator.helpers import url
from remote.protocols.irc.model import IrcServer, IrcChannel
from twisted.internet.task import LoopingCall



class LogBot(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def onInit(self):
        self.server = IrcServer()
        self.server.host = self.factory.server
        
        self.nickname = self.factory.nickname
        self.pushToMaster = self.factory.pushToMaster
        #bus binding
        self.bus = self.factory.bus
        self.bus.bind(JoinActionEvent().getType(), self.onJoinEvent) 
        self.bus.bind(InfoRequestEvent().getType(), self.onInfoRequest)
        
        lc = LoopingCall(self.onInfoRequest)
        lc.start(30)
        

#     
#    #def created(self, when):
#    #    self.pushToMaster = self.factory.pushToMaster
#    #    self.bus = self.factory.bus
#    #    
#        
#     
    def onInfoRequest(self, event = None, evtMgr = None):  
        self.pushToMaster(InfoContentEvent(server=self.server))  
        log.msg("sending info request ***")
        for chan in self.server.getChannels():
            log.msg("--> on chan "+ str(chan.name))
            
   
    def onJoinEvent(self, eventObj, evtMgr):
        
        if not eventObj.hasArgEntry("key"):
            eventObj.key = None;
        
        self.join(eventObj.channel, eventObj.key)
#
#        
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.onInit()
        self.pushToMaster(ConnectEvent())
#
#    def connectionLost(self, reason):
#        pass
#
#
#    # callbacks for events
#
    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        #print "signed on !!!!!!!!!!!!!"
        #self.onInit()
        self.setNick(self.nickname)
        self.pushToMaster(ConnectEvent())
        self.onInfoRequest()
#        
    def joined(self, channel):
        self.pushToMaster(JoinEvent(channel=channel))
        
        chan = IrcChannel()
        chan.name = channel
        
        self.server.addChannel(chan)
        
        self.pushToMaster(InfoContentEvent(server=self.server))
        
#
    def privmsg(self, user, channel, msg):
        #self.logger.log("* %s %s %s" % (user, channel, msg))
        log.msg("* %s %s %s" % (user, channel, msg))
        #self.setNick(self.nickname)
        user = user.split('!', 1)[0]
        #print "* "+user+" "+channel+" "+msg
        if not channel.startswith('#'):
            return
        
        address = url.detect_link(msg)
        
        if address != None:
            comment = url.get_comment(msg)
            if comment == None:
                self.pushToMaster(LinkEvent(author=user, channel=channel, url=address, desc="",server= self.factory.server))
            else:
                self.pushToMaster(LinkEvent(author=user, channel=channel, url=address, desc=comment,server= self.factory.server))
            
        if msg.startswith(self.nickname + ":"):
            self.msg(channel, user + ": " + doreply(msg))
        
        
        
        #print channel
#
#    def action(self, user, channel, msg):
#        """This will get called when the bot sees someone do an action."""
#        #pass
#        user = user.split('!', 1)[0]
#        #log.msg("* %s %s" % (user, msg))
#        print user +" "+msg
#
#    # irc callbacks
#
#    def irc_NICK(self, prefix, params):
#        """Called when an IRC user changes their nickname."""
#        #old_nick = prefix.split('!')[0]
#        #new_nick = params[0]
#        #self.logger.log("%s is now known as %s" % (old_nick, new_nick))
#    
    def kickedFrom(self, channel, kicker, message):
        self.pushToMaster(KickEvent(channel=channel, kicker=kicker, message=message))
        chan_obj = IrcChannel()
        chan_obj.name = channel
        self.server.removeChannel(chan_obj)
        self.pushToMaster(InfoContentEvent(server=self.server))
#        
#    def left(self, channel):
#        self.pushToMaster(PartEvent(channel=channel))


class BotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = LogBot

    def __init__(self, nickname, server):
        self.server = server
        self.nickname = nickname

        
    def clientConnectionLost(self, connector, reason):
        self.pushToMaster(DisconnectEvent())
        
    def clientConnectionFailed(self, connector, reason):
        print "CONNECTION FAILED REASON: "+str(reason)
        self.pushToMaster(DisconnectEvent(reason="arg"))
        
import xmlrpclib
        
def learn(message):        
    server = xmlrpclib.ServerProxy("http://srv.lo2k.net:2217")
    return server.learn(message)
    
def doreply(message):
    server = xmlrpclib.ServerProxy("http://srv.lo2k.net:2217")
    return server.doreply(message)
