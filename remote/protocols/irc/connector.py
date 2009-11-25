'''
Created on 25 Nov 2009

@author: wax
'''

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from remote.protocols.event import DisconnectEvent

class IrcBot(irc.IRCClient):
    
#    def updater(self):
#        self.botname = self.nickname
#    
#        print "updater " + str(self.factory.server.name)
#        d = dict()
#        channels_res = dict()
#        for channel in self.channels:
#            elt = dict()
#            elt['status'] = self.channels[channel].status
#            channels_res[self.channels[channel].name] = elt
#        
#        d[self.factory.server.name] = channels_res
#        pprint.pprint(d)
#        server = xmlrpclib.ServerProxy("http://scrutator.lo2k.net/index.php?ctrl=API&action=index", verbose=1)
#        lo2kObj = server.lo2k
#        #try:
#        needjoin = lo2kObj.update_channels(self.botname, d)
#        
#        for chan in needjoin:
#            if not chan in self.channels:
#                print "discover channel " + chan
#                c = Channel()
#                c.name = chan
#                c.status = "offline"
#                self.channels[chan] = c
#            self.join(chan)
#
#        for channel in self.channels:
#            if self.channels[channel].verbose == 1:
#                #try to rejoin channel
#                self.join(channel)
                

        
    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        pass
        
    def joined(self, channel):
        pass

    def privmsg(self, user, channel, msg):
        if not channel.startswith('#'):
            return
        #print channel

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        pass

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        #old_nick = prefix.split('!')[0]
        #new_nick = params[0]
        #self.logger.log("%s is now known as %s" % (old_nick, new_nick))
    
    def kickedFrom(self, channel, kicker, message):
        pass
        
    def left(self, channel):
        pass


class BotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = IrcBot

    def __init__(self, server):
        pass

        
    def clientConnectionLost(self, connector, reason):
        self.pushToMaster(DisconnectEvent())

    def clientConnectionFailed(self, connector, reason):
        pass
