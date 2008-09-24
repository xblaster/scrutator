class EventManager:
    """ handle event in the application"""
    
    listeners_map = dict()
    
    def __init__(self):
        pass
        
    def bind(self, eventName, listener):
        if not isinstance(listener, SimpleListener):
            raise Exception("Not an SimpleListener")
        pass
