from twisted.web import xmlrpc, server
from scrutator.core.event import *
from twisted.internet import threads, reactor
from twisted.web.xmlrpc import Proxy

class SCRTServices(xmlrpc.XMLRPC):
	"""An example object to be published."""

	manager = 0

	def __init__(self):
		pass
	
	def xmlrpc_push(self, obj_list, source):
		"""Push event"""
		es = EventSerializer()
		for obj in obj_list:
			res = es.array2event(obj_list)
			s_reconstruct = es.array2event(res)
			manager.push(s_reconstruct)

	def xmlrpc_pull(self, source):
		"""Pull event to a destination"""
		return null

def printValue(value):
	print value

def printError(value):
	print value

class XMLRPCClient:
	def __init__(self, serviceuri):
		import xmlrpclib
		self.xmlrpc_connect = Proxy(serviceuri)
	

	
	def push(self, eventObj):
		es = EventSerializer()
		res = es.event2array(eventObj)
		send_list = list()
		send_list.append(res)
		
		self.xmlrpc_connect.callRemote(send_list).addCallbacks(printValue, printError)
		#threads.deferToThread(self.xmlrpc_connect.push(send_list))

class XMLRPCServer:
	def __init__(self, service, port, eventMgrObj):
		from twisted.internet import reactor
		r = service
		reactor.listenTCP(port, server.Site(r))

