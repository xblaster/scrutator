'''
Created on 19 Nov 2009

@author: wax
'''
from scrutator.core.event import SimpleEvent

class IrcEvent(SimpleEvent):
    pass

class JoinActionEvent(SimpleEvent):
    pass

class PartActionEvent(SimpleEvent):
    pass

class SpeakActionEvent(SimpleEvent):
    pass


class PartEvent(SimpleEvent):
    pass 

class JoinEvent(SimpleEvent):
    pass