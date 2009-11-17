# -*- coding: utf-8 -*-
from scrutator.minidi.tool import *


#smart_import('scrutator.core.listener')
from scrutator.core.listener import *
from scrutator.core.event import *

from twisted.python import log

from twisted.internet import threads, reactor


def default_callback(value):
	pass

class EventManager(object):
	""" handle event in the application"""

	def __init__(self, xml_bindings=None):


		self.listeners_map = dict()
		if xml_bindings != None: #load xml bindings
			self.loadXMLMap(xml_bindings)
			
	def loadXMLMap(self, xml_bindings, context = None):
		from scrutator.minidi.injector import *

		xeml = XmlEventManagerLoader()
		em = self
		
		if context != None:
			xeml.load(xml_bindings, self, context)
		else: 
		    xeml.load(xml_bindings, self)
		
	def bind(self, eventName, listener):
		self.__getListenerMap(str(eventName)).append(listener)
	
	def unbindAll(self):
		self.listeners_map = dict()
	
	def unbind(self, eventName, listener):
		if not listener in self.__getListenerMap(eventName):
			raise Exception("This listener is not binded")
		
		map_list = self.__getListenerMap(eventName)
		item_index = map_list.index(listener)
		del map_list[item_index]
	
	def push(self, eventObj):
		""" This push an event and activate action listener
		"""
		log.msg('push ' + str(eventObj) + ' on ' + str(self))
		if not isinstance(eventObj, SimpleEvent):
			raise Exception("Not a SimpleEvent inherited object")
		for listener_obj in self.__getListenerMap(eventObj.getType()):
			#if it's a "regular listener"
			self.execute_binding(listener_obj, eventObj)
		
		for listener_obj in self.__getListenerMap('all'):
			#threads.deferToThread(listener_obj.action(eventObj)).addCallback(default_callback)
			self.execute_binding(listener_obj, eventObj)
			
		return None
	
	def execute_binding(self, listener_obj, eventObj, manager = None):
		if manager == None:
			manager = self
		 
		if isinstance(listener_obj, scrutator.core.listener.SimpleListener):
			listener_obj.action(eventObj, manager)
			#else if it's directly a method binded
		else:
			listener_obj(eventObj, manager)		
	
	def __getListenerMap(self, mapname):
		""""
		return a listener map name for bindings
		"""
		if not self.listeners_map.has_key(mapname):
			self.listeners_map[mapname] = list()
		return self.listeners_map[mapname]
	
	def getListenerMap(self, mapname):
	    return self.__getListenerMap(mapname)


class AsyncEventManagerException(Exception):
	pass

class AsyncEventManager(EventManager):
	def __init__(self, xml_bindings=None):
		super(AsyncEventManager, self).__init__(xml_bindings)
		self.mboxMgr = MessageBoxManager()
	
	def getMessageBoxManager(self):
		return self.mboxMgr

	def push(self, eventObj):
		""" This push an event and activate action listener
		"""
		if not isinstance(eventObj, SimpleEvent):
			raise Exception("Not a SimpleEvent inherited object")

		if not eventObj.hasArgEntry('source'):
			raise AsyncEventManagerException("Event must contain a source")

		source = eventObj.getArgEntry('source')
		
		#create fake reply bus
		fakeReplyBus = EventManager()
    
		from callback import ToMessageBoxManagerCallback

		callback = ToMessageBoxManagerCallback(source)

		gate_listener = GateListener(self.mboxMgr, callback.callback)
		
		fakeReplyBus.bind('all', gate_listener)

		#normal behaviour
		for listener_obj in self.getListenerMap(eventObj.getType()):
			#listener_obj.action(eventObj, fakeReplyBus)
			self.execute_binding(listener_obj, eventObj, fakeReplyBus)
		
		for listener_obj in self.getListenerMap('all'):
			self.execute_binding(listener_obj, eventObj, fakeReplyBus)
			
		return None
		
class MessageBoxManagerException(Exception):
	pass
	
class MessageBoxManager(EventManager):
	""" improvement of the dispatcher listener."""

	def __init__(self):
		super(MessageBoxManager, self).__init__()
		self.__messageBox = dict()

	def push(self, eventObj):
		if not eventObj.hasArgEntry("to"):
			raise MessageBoxManagerException("no 'to' arg")

		if not eventObj.hasArgEntry("msg"):
			raise MessageBoxManagerException("no 'msg' arg")

		to = eventObj.getArgEntry("to")
		msg = eventObj.getArgEntry("msg")

		self.getMessageBox(to).append(msg)

	def getMessageBox(self, boxname):
		if not self.__messageBox.has_key(boxname):
			self.__messageBox[boxname] = list()
		return self.__messageBox[boxname]

	def getMessagesFor(self, boxname):
		return self.getMessageBox(boxname)
	
	def flushMessagesFor(self, boxname):
		self.__messageBox[boxname] = list()
	
	def popMessagesFor(self, boxname):
		mbox = self.getMessagesFor(boxname)
		self.flushMessagesFor(boxname)
		return mbox

