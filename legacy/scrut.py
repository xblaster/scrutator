# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.




"""An example IRC log bot - logs a channel's events to a file.

If someone says the bot's name in the channel followed by a ':',
e.g.

  <foo> logbot: hello!

the bot will reply:

  <logbot> foo: I am a log bot

Run this script with two arguments, the channel name the bot should
connect to, and file to log to, e.g.:

  $ python ircLogBot.py test test.log

will log channel #test to the file 'test.log'.
"""

import ConfigParser

from scrutcore import *
from scrutmodel import *

def update(reactor):
    print "echo"
    reactor.callLater(360, testecho, reactor)

if __name__ == '__main__':
    # initialize logging
    #log.startLogging(sys.stdout)
    
    # create factory protocol and application
    #f = LogBotFactory(sys.argv[1], sys.argv[2])
    
    cm = XmlAdapter().createConnectionManager()

    for server in cm.servers:
        
        f = LogBotFactory(cm.servers[server])
        
        #print cm.servers[server]
    
        # connect factory to this host and port
        reactor.connectTCP(cm.servers[server].host, 6667, f)

    # run bot
    
    reactor.run()
