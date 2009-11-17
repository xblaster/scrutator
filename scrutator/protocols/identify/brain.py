'''
Created on 17 Nov 2009

@author: wax
'''

from scrutator.core.protocols.common import *

def IdentifyServerBrain(Brain):
    def onInit(self):
        self.bus = self.getContext().getBean("mainEventManager")
        self.hostList = list()
        self.bus.bind()