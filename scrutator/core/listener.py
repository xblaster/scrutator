class SimpleListener:
	""" base of all listener"""
	def __init__(self):
		pass

	def action(self, eventObj, evtMgr):
		""" implement this method with your listener
		eventObj -- event object to handle
		"""
		self.action(eventObj)

class PrintListener(SimpleListener):
	def action(self, eventObj, evtMgr):
		print "PrintListener DEBUG: "+str(eventObj)


class ExceptionListener(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg = []):
		self.arg = arg
	def action(self, obj, evtMgr):
		raise Exception("ACTION !!!")
		
class DoReactorStopListener(SimpleListener):
	def action(self,obj, evtMgr):
		from twisted.internet import reactor
		#reactor.stop()
		reactor.callLater(0.1, reactor.stop)