'''
Created on 20 Nov 2009

@author: wax
'''
from scrutator.core.event import SimpleEvent

class InfoRequestEvent(SimpleEvent):
    pass

class ConnectEvent(SimpleEvent):
    pass

class DisconnectEvent(SimpleEvent):
    pass


#action
class ConnectEventAction(SimpleEvent):
    pass

class DisconnectEventAction(SimpleEvent):
    pass
