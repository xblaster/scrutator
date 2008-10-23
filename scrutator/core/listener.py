class SimpleListener(object):
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
		
class GateListener(SimpleListener):
	def __init(self,evtMagr):
		super(GateListener, self).__init__()
		self.evtMgr = evtMagr
	
	def action(self, eventObj, evtMgr):
		evtMgr.push(eventObj)

class LoggerListerner(SimpleListener, filename):
	"""log event in a file"""
	def action(self, eventObj, evtMgr):
		pass

class ExceptionListener(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg = []):
		self.arg = arg
	def action(self, obj, evtMgr):
		raise Exception("ACTION !!!")

class DelayListener(SimpleListener):
	def action(self, obj, evtMgr):
		from twisted.internet import reactor
		reactor.callLater(evtMgr.push, obj)
		
class DoReactorStopListener(SimpleListener):
	def action(self,obj, evtMgr):
		from twisted.internet import reactor
		reactor.callLater(0.1, reactor.stop)
		
class PingListener(SimpleListener):
	"""
	Simply resend the object (testing purpose)
	"""
	def action(self, obj, evtMgr):
		evtMgr.push(obj)