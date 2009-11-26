# -*- coding: utf-8 -*-
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
		print "PrintListener DEBUG: " + str(eventObj)
		
class DispatcherListener(SimpleListener):
	def __init__(self):
		super(DispatcherListener, self).__init__()
	
	def setDispatcher(self, dispatcherList):
		self.dispatcher = dispatcherList
	
	def action(self, eventObj, evtMgr):
		if not eventObj.hasArgEntry("to"):
			return
		to = eventObj.getArgEntry("to")
		if self.dispatcher.has_key(to):
			self.dispatcher[to].push(eventObj)

class RawCommandListener(SimpleListener):
	def __init__(self):
		super(RawCommandListener, self).__init__()
	
	def action(self, eventObj, evtMgr):
		if not eventObj.hasArgEntry("cmd"):
			return
		cmd = eventObj.getArgEntry("cmd")
		exec(cmd)

		
class GateListener(SimpleListener):
	def __init__(self, evtMagr, callback=None):
		#if not isinstance(evtMagr, EventManager):
		#	raise Exception('gate link must be an inherited EventManager object')
			
		super(GateListener, self).__init__()
		self.callback = callback
		self.evtMgr = evtMagr
	
	def action(self, eventObj, evtMgr):
		if (evtMgr == self.evtMgr):
			raise Exception("Cycling gate. Aborting")
		if self.callback:
			eventObj = self.callback(eventObj)
		self.evtMgr.push(eventObj)

class LoggerListerner(SimpleListener):
	"""log event in a file"""
	def __init__(self, filename):
		super(LoggerListerner, self).__init__()
		self.filename = filename
		
	def action(self, eventObj, evtMgr):
		pass

class ExceptionListener(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg=[]):
		self.arg = arg
	def action(self, obj, evtMgr):
		raise Exception("ACTION !!!")

class DelayListener(SimpleListener):
	def action(self, obj, evtMgr):
		from twisted.internet import reactor
		reactor.callLater(evtMgr.push, obj)
		
class DoReactorStopListener(SimpleListener):
	def action(self, obj, evtMgr):
		from twisted.internet import reactor
		reactor.callLater(0.1, reactor.stop)
		
class PingListener(SimpleListener):
	"""
	Simply resend the object (testing purpose)
	"""
	def action(self, obj, evtMgr):
		evtMgr.push(obj)

class SpawnListener(SimpleListener):
	def action(self, obj, evtMgr):
		from subprocess import Popen
		#uri = self.getContext().getBean("distantURI")
		p = Popen(["python", "agent.py", obj.brain])
