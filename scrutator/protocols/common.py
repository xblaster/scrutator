'''
Created on 17 Nov 2009

@author: wax
'''

from twisted.internet import reactor


class Brain(object):
    def __init__(self):
        reactor.callLater(10, self.onInit)
        
    def onInit(self):
        raise Exception("must be implemented")
    

        
        
    