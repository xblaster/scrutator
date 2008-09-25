class SimpleEvent:
    """simple event
    base class of all event"""
    def __init__(self, arg = []):
        self.arg = arg

    def getType(self):
        return self.__class__.__name__
        
class KickEvent(SimpleEvent):
    pass
    
class BanEvent(SimpleEvent):
    pass

