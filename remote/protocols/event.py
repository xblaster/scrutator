'''
Created on 20 Nov 2009

@author: wax
'''
from scrutator.core.event import SimpleEvent

class InfoRequestEvent(SimpleEvent):
    pass

class InfoContentEvent(SimpleEvent):
    pass

class ConnectEvent(SimpleEvent):
    pass

class DisconnectEvent(SimpleEvent):
    pass


class LinkEvent(SimpleEvent):
    #param url, author, channel, desc, network
    pass


#action
class ConnectEventAction(SimpleEvent):
    pass

class DisconnectEventAction(SimpleEvent):
    pass
