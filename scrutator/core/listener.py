class SimpleListener:
    """ base of all listener"""
    def __init__(self):
        pass
    
    def action(self, eventObj):
        """ implement this method with your listener
        eventObj -- event object to handle
        """
        pass

class PrintListener(SimpleListener):
	def action(self, eventObj):
		print "PrintListener DEBUG: "+str(eventObj)


class ExceptionListener(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg = []):
		self.arg = arg
	def action(self, obj):
		raise Exception("ACTION !!!")