'''
Created on 17 Nov 2009

@author: wax
'''

from twisted.internet import reactor


def Brain(object):
    def __init__(self):
        reactor.callLater(1, self.onInit)
        
    def onInit(self):
        raise Exception("must be implemented")
    

        
        
    