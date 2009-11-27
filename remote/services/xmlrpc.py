'''
Created on 25 Nov 2009

@author: wax
'''

import sys

sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')

from remote.protocols.event import LinkEvent

import xmlrpclib


def addLink(linkEvent): 
    for arg in ["url", "author", "channel", "network"]:
            if not linkEvent.hasArgEntry(arg):
                linkEvent.setArgEntry(arg,"unknown")
    server = xmlrpclib.ServerProxy("http://scrutator.lo2k.net/index.php?ctrl=API&action=index")
    lo2kObj = server.lo2k
    return lo2kObj.add_link(linkEvent.url, linkEvent.author, linkEvent.channel, linkEvent.desc, linkEvent.network, 'scrutator2', 'coincoin')


#if __name__ == '__main__':
#    addLink(LinkEvent(url="http://www.google.lu"))