'''
Created on 27 Nov 2009

@author: wax
'''

from remote.protocols.irc.model import IrcServices



def display(l):
    for line in l:
        print line

if __name__ == '__main__':
    serv = IrcServices()
    for server in serv.getModel():
        print server.host
        
        for chan in server.getChannels():
            print "*** "+chan.name 
    
    #d.addCallback(display)
    #reactor.run()