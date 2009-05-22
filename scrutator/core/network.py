# -*- coding: utf-8 -*-
from twisted.web import xmlrpc, server
from scrutator.core.event import *
from twisted.internet import threads, reactor
from twisted.web.xmlrpc import Proxy

from scrutator.core.manager import *



class SCRTServices(xmlrpc.XMLRPC):
	"""An example object to be published."""

	manager = None
	mboxManager = None
	allowNone = True
	
	def getMessageBoxManager(self):
		return self.manager.getMessageBoxManager()

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
		
		return self.pull(source)


	def xmlrpc_pull(self, source):
		"""Pull event to a destination"""
		return self.pull(source)
	
	def pull(self,source):
		result = list()
		es = EventSerializer()
		for msg in self.mboxManager.popMessagesFor(source):
			result.append(es.event2array(msg))
		return result

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

class XMLRPCServer:
	def __init__(self, service, port, eventMgrObj):
		from twisted.internet import reactor
		self.service = service
		reactor.listenTCP(port, server.Site(self.service))
		
	def getMessageBoxManager(self):
		return self.service.getMessageBoxManager()
		
class XMLRPCClient:
	
	source = "default"
	
	def __init__(self, serviceuri, eventMgr):
		import xmlrpclib
		self.xmlrpc_connect = Proxy(str(serviceuri))
		self.manager = eventMgr
		
		self.retryPullTimer = 5
		self.maxPullTimer = 5
				
		reactor.callLater(5, self.pull)

	def reinject(self, msgList):
		es = EventSerializer()
		
		for obj in msgList:
			res = es.array2event(obj)
			print "REINJECT" + str(res)
			self.manager.push(res)
	
	def handleError(self, error):
		#need to rework that
		print "ERROR !!! "+str(error)
	
	def preprocessResult(self, result):
		
		if (len(result) == 0):
			self.retryPullTimer *= 1.5
			if self.retryPullTimer < self.maxPullTimer:
				self.retryPullTimer = self.maxPullTimer
		else:
			self.retryPullTimer = self.retryPullTimer/1.5
		
		reactor.callLater(self.retryPullTimer, self.pull)
		
		return result
	
	def pull(self):
		d = self.xmlrpc_connect.callRemote('pull', self.source).addCallback(self.preprocessResult)
		d.addCallbacks(self.reinject, self.handleError)
		
		return d
		
	def push(self, eventObj):
		es = EventSerializer()
		res = es.event2array(eventObj)
		send_list = list()
		send_list.append(res)
		
		return self.xmlrpc_connect.callRemote('push',send_list, self.source).addCallbacks(self.reinject, self.handleError)
		#self.xmlrpc_connect.callRemote(send_list).addCallbacks(printValue, printError)
		#threads.deferToThread(self.xmlrpc_connect.push(send_list))

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



