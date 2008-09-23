# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys
from twisted.internet import task

from scrutmodel import *

import pprint

import random

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """A logging IRC bot."""
    
    def updater(self):
        self.botname = self.nickname
    
        print "updater "+str(self.factory.server.name)
        d = dict()
        channels_res = dict()
        for channel in self.channels:
            elt = dict()
            elt['status'] = self.channels[channel].status
            channels_res[self.channels[channel].name] = elt
        
        d[self.factory.server.name] = channels_res
        pprint.pprint(d)
        server = xmlrpclib.ServerProxy("http://scrutator.lo2k.net/index.php?ctrl=API&action=index", verbose =1)
        lo2kObj = server.lo2k
        #try:
        needjoin = lo2kObj.update_channels(self.botname, d)
        
        for chan in needjoin:
            if not chan in self.channels:
                print "discover channel "+chan
                c = Channel()
                c.name = chan
                c.status = "offline"
                self.channels[chan] = c
            self.join(chan)

        for channel in self.channels:
            if self.channels[channel].verbose==1:
                #try to rejoin channel
                self.join(channel)
                

        
    def connectionMade(self):
        self.nickname = self.factory.server.nickname
        
        self.channels = self.factory.server.channels
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        l = task.LoopingCall(self.updater)
        l.start(360.0)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.setNick(self.nickname)
        
        for channel in self.factory.server.channels:
            self.join(str(self.factory.server.channels[channel].name))
        
    def joined(self, channel):
        self.factory.wait = 20
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)
        self.channels[channel].status = "online"
        self.updater()

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        
        
        # Check to see if they're sending me a private message
        """if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I am a log bot" % user
            self.msg(channel, msg)
            self.logger.log("<%s> %s" % (self.nickname, msg))
        """
        
        if not channel.startswith('#'):
            return
        #print channel
        self.channels[channel].status = "online"
        
        link = detectLink(msg)
        
        if self.channels[channel].canLearn != 0:
            learn(msg)

        if msg.startswith(self.nickname + ":"):
            self.msg(channel, user+": "+doreply(msg))
        elif self.nickname in msg and self.channels[channel].canTalk != 0:
            self.msg(channel, doreply(msg))
        
        #speak randomly
        if self.channels[channel].canTalk != 0 and random.randint(0,200)==1:
            self.msg(channel, user+": "+doreply(msg))
        
        if (link != None):
            res = addLink(link, user, channel, get_comment(msg), str(self.factory.server.name))
            if res != 'default':
                if self.channels[channel].verbose == 1:
                    self.msg(channel, res.split(':',1)[1])

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))
    
    def kickedFrom(self, channel, kicker, message):
        self.join(channel)
        self.channels[channel].status = "offline"
        self.updater()
        
    def left(self, channel):
        self.channels[channel].status = "offline"
        self.updater()


class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = LogBot

    def __init__(self, server):
        self.server = server
        self.filename = str(server.name)+".log"
        self.wait = 20

        
    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        self.wait *=2
        if (self.wait > 3600):
            self.wait = 3600
        
        reactor.callLater(self.wait, connector.connect())

    def clientConnectionFailed(self, connector, reason):
        self.wait *=2
        if (self.wait > 3600):
            self.wait = 3600
        reactor.callLater(self.wait, connector.connect())
