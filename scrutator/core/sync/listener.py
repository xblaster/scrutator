import scrutator.core.listener
import scrutator.core.sync.event 

class FileRequestListener(scrutator.core.listener):
	""" base of all listener"""
	def __init__(self):
		pass

	def action(self, eventObj, evtMgr):
		try:
			f = open(eventObj.src)
		except IOError:
			return evtMgr.push(scrutator.core.sync.event.FileRequestError())
		
		event = scrutator.core.sync.event.FileContent()
		event.content = f.read()
		evtMgr.push(event)
		
		f.close()
		