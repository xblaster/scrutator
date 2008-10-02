from twisted.web import xmlrpc, server
from scrutator.core.event import *


class SCRTServices(xmlrpc.XMLRPC):
	"""An example object to be published."""

	manager = 0

	def __init__(self):
		pass
	
	def xmlrpc_push(self, obj_list, source):
		"""Push event"""
		es = EventSerializer()
		for obj in obj_list:
			res = es.event2array(obj_list)
			s_reconstruct = es.array2event(res)
			manager.push(s_reconstruct)

	def xmlrpc_pull(self, source):
		"""Pull event to a destination"""
		return null

class SCRTXMLRPC:
	def __init__(self, service, port, eventMgrObj):
		from twisted.internet import reactor
		r = service
		reactor.listenTCP(port, server.Site(r))

