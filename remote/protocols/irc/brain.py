'''
Created on 19 Nov 2009

@author: wax
'''

from twisted.protocols.irc import *
from twisted.python import log

from scrutator.protocols.common import BasicClientBrain
from scrutator.core.event import SpawnEvent
from remote.protocols.irc.event import IrcEvent
from remote.protocols.genericbrain import GenericBrainClient
from remote.protocols.event import LinkEvent





class IrcBrainClient(BasicClientBrain):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainClient, self).__init__()
        
    def onInit(self):
        super(IrcBrainClient, self).onInit()
        self.pushToMaster(LinkEvent(url="http://http://www.google.lu/search?q=py2exe+reactor.iterate&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:fr:official&client=firefox-a"))
        
    def onThink(self):
        log.msg("ON THINK ! => ")