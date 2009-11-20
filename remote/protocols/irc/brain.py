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





class IrcBrainClient(BasicClientBrain):
    transport_event = IrcEvent
    def __init__(self):
        super(IrcBrainClient, self).__init__()
        
    def onInit(self):
        super(IrcBrainClient, self).onInit()
        
    def onThink(self):
        log.msg("ON THINK ! => ")