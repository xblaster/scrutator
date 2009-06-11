import scrutator.core.listener
import scrutator.core.sync.event 

class FileRequestListener(scrutator.core.listener.SimpleListener):
	""" base of all listener"""
	def __init__(self):
		pass

	def action(self, eventObj, evtMgr):
		try:
			f = open(eventObj.getArgEntry('file'))
		except IOError:
			return evtMgr.push(scrutator.core.sync.event.FileRequestError())
		
		event = scrutator.core.sync.event.FileContent()
		event.setArgEntry('content', f.read())
		event.setArgEntry('filename', eventObj.getArgEntry('file'))
		evtMgr.push(event)
		
		f.close()
		
		

class FileContentListener(scrutator.core.listener.SimpleListener):
	""" base of all listener"""
	def __init__(self):
		self.upload_dir = "upload/"
		pass

	def action(self, eventObj, evtMgr):
		#create dirs
		xpld = eventObj.filename.split('.')
		pyfile = xpld.pop()
		directory = str('.').join(xpld)
		
		#create uploaded file
		import os
		try:
			os.makedirs(self.upload_dir+directory)
		except:
			pass
		
		f = open(self.upload_dir+eventObj.filename,'w+')
		f.write(eventObj.content)
		f.close()