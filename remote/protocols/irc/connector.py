'''
Created on 25 Nov 2009

@author: wax
'''

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from remote.protocols.event import DisconnectEvent, ConnectEvent
from remote.protocols.irc.event import JoinActionEvent, PartEvent, JoinEvent
from scrutator.core.event import KickEvent

class IrcBot(irc.IRCClient):
     
     
    def onInit(self):
        self.pushToMaster = self.factory.pushToMaster 
     
    def created(self, when):
        self.nickname = self.factory.nickname
        self.pushToMaster = self.factory.pushToMaster
        self.bus = self.factory.bus
        
        #bus binding
        self.bus.bind(JoinActionEvent().getType(), self.onJoinEvent)
        
    def onJoinEvent(self, eventObj, evtMgr):
        
        if not eventObj.hasArgEntry("key"):
            eventObj.key = None;
        
        self.join(eventObj.channel, eventObj.key)

        
    def connectionMade(self):
        self.onInit()
        self.pushToMaster(ConnectEvent())

    def connectionLost(self, reason):
        pass


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        print "signed on !!!!!!!!!!!!!"
        self.setNick(self.nickname)
        self.pushToMaster(ConnectEvent())
        
    def joined(self, channel):
        self.pushToMaster(JoinEvent(channel=channel))

    def privmsg(self, user, channel, msg):
        #self.logger.log("* %s %s %s" % (user, channel, msg))
        self.setNick(self.nickname)
        print "* "+user+" "+channel+" "+msg
        if not channel.startswith('#'):
            return
        #print channel

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        #pass
        user = user.split('!', 1)[0]
        #log.msg("* %s %s" % (user, msg))
        print user +" "+msg

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        #old_nick = prefix.split('!')[0]
        #new_nick = params[0]
        #self.logger.log("%s is now known as %s" % (old_nick, new_nick))
    
    def kickedFrom(self, channel, kicker, message):
        self.pushToMaster(KickEvent(channel=channel, kicker=kicker, message=message))
        
    def left(self, channel):
        self.pushToMaster(PartEvent(channel=channel))


class BotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = IrcBot

    def __init__(self, nickname, server):
        self.server = server
        self.nickname = nickname

        
    def clientConnectionLost(self, connector, reason):
        self.pushToMaster(DisconnectEvent())

    def clientConnectionFailed(self, connector, reason):
        print "REASON: "+str(reason)
        self.pushToMaster(DisconnectEvent(reason="arg"))
