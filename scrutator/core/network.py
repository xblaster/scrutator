from twisted.web import xmlrpc, server
from scrutator.core.event import *
from twisted.internet import threads, reactor
from twisted.web.xmlrpc import Proxy

from scrutator.core.manager import *


#from twisted.web import soap, server
"""
from twisted.web import soap
import os

def getQuote():
    return "That beverage, sir, is off the hizzy."

class Quoter(soap.SOAPPublisher):
    Publish one method, 'quote'.

    def soap_quote(self):
        return getQuote()

resource = Quoter()
"""
"""
class SoapServices(soap.SOAPPublisher):

	manager = 0

	def __init__(self):
		pass
	
	def soap_push(self, obj_list, source):
		es = EventSerializer()
		for obj in obj_list:
			res = es.array2event(obj_list)
			s_reconstruct = es.array2event(res)
			manager.push(s_reconstruct)

	def soap_pull(self, source):
		return null
"""

class SCRTServices(xmlrpc.XMLRPC):
	"""An example object to be published."""

	manager = 0
	mboxManager = None
	allowNone = True

	def __init__(self):
		self.mboxManager = MessageBoxManager()
		pass
	
	def xmlrpc_push(self, obj_list, source):
		"""Push event"""
		return self.push(obj_list, source)


	def push(self, obj_list, source):
		es = EventSerializer()
		for obj in obj_list:
			res = es.array2event(obj)
			#print "RES "+str(res)
			res.setArgEntry('source',source)
			self.manager.push(res)
			#threads.deferToThread(self.manager.push, res)
			#threads.deferToThread(True)
		
		result = list()
		
		for msg in self.mboxManager.getMessagesFor(source):
			result.append(es.event2array(msg))
		return result

	def xmlrpc_pull(self, source):
		"""Pull event to a destination"""
		return self.pull(source)
	
	def pull(self,source):
		pass

def printValue(value):
	#print "YES !!! "+str(value)
	pass

def printError(value):
	print "ERROR !!! "+str(value)
	#pass

"""class SoapClient:
	def __init__(self, serviceuri):
		self.soap_connect = soap.Proxy(serviceuri)
	

	
	def push(self, eventObj):
		es = EventSerializer()
		res = es.event2array(eventObj)
		send_list = list()
		send_list.append(res)
		
		self.soap_connect.callRemote(send_list).addCallbacks(printValue, printError)
		#threads.deferToThread(self.xmlrpc_connect.push(send_list))
"""
		
class XMLRPCClient:
	
	source = "default"
	
	def __init__(self, serviceuri):
		import xmlrpclib
		self.xmlrpc_connect = Proxy(str(serviceuri))



	def push(self, eventObj):
		es = EventSerializer()
		res = es.event2array(eventObj)
		send_list = list()
		send_list.append(res)
		
		self.xmlrpc_connect.callRemote('push',send_list, self.source).addCallbacks(printValue, printError)
		#self.xmlrpc_connect.callRemote(send_list).addCallbacks(printValue, printError)
		#threads.deferToThread(self.xmlrpc_connect.push(send_list))

class XMLRPCServer:
	def __init__(self, service, port, eventMgrObj):
		from twisted.internet import reactor
		r = service
		reactor.listenTCP(port, server.Site(r))

