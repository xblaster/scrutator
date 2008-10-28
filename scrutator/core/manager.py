from scrutator.core.listener import *
from scrutator.core.event import *

from scrutator.core.tool import *

from twisted.internet import threads, reactor


def default_callback(value):
	pass

class EventManager(object):
	""" handle event in the application"""

	def __init__(self):
		self.listeners_map = dict()
		pass
		
	def bind(self, eventName, listener):
		if not isinstance(listener, SimpleListener):
			raise Exception("Not a SimpleListener inherited object "+str(listener))
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
		if not isinstance(eventObj, SimpleEvent):
			raise Exception("Not a SimpleEvent inherited object")
		for listener_obj in self.__getListenerMap(eventObj.getType()):
			#threads.deferToThread(listener_obj.action(eventObj)).addCallback(default_callback)
			listener_obj.action(eventObj, self)
		
		for listener_obj in self.__getListenerMap('all'):
			#threads.deferToThread(listener_obj.action(eventObj)).addCallback(default_callback)
			listener_obj.action(eventObj, self)
			
		return None
			
	def __getListenerMap(self, mapname):
		""""
		return a listener map name for bindings
		"""
		if not self.listeners_map.has_key(mapname):
			self.listeners_map[mapname] = list()
		return self.listeners_map[mapname]

class AsyncEventManager(EventManager):
	def __init__(self):
		super(AsyncEventManager, self).__init__()
		self.buffer = list()
	
	def push(self, eventObj):
		self.buffer.append(eventObj)
		
	def getStoredEvent(self):
		buf = self.buffer
		self.buffer = list
		return buf
		

class CoreManager:
	""" A python singleton """

	class __CoreManagerimpl:
		""" Implementation of the singleton interface """
		
		beans_list = dict()
		
		eventManager = EventManager()
		
		def __init__(self):
			pass
		
		def push(self, eventObj):
			return self.eventManager.push(eventObj)
			
		def getEventManager(self):
			return self.eventManager
			
		def getBean(self, beanName):
			if self.beans_list.has_key(beanName):
				return self.beans_list[beanName]
			raise Exception('This bean does not exist')
	
		def setBean(self, beanName, beanObj):
			self.beans_list[beanName] = beanObj


	# storage for the instance reference
	__instance = None

	def __init__(self):
		""" Create singleton instance """
		# Check whether we already have an instance
		if CoreManager.__instance is None:
			# Create and remember instance
			CoreManager.__instance = CoreManager.__CoreManagerimpl()
		
		# Store instance reference as the only member in the handle
		self.__dict__['_Singleton__instance'] = CoreManager.__instance

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)
	
	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)



class XmlEventManagerLoader:
	
	def getListener(self, xmlNode):
		if xmlNode.hasAttribute('listener'):
			listenerName = xmlNode.getAttribute('listener')
			listenerClass = smart_load(listenerName)()
			return listenerClass
			
		if xmlNode.hasAttribute('bean'):
			beanName = xmlNode.getAttribute('bean')
			listenerClass = CoreManager().getBean(beanName)
			return listenerClass
		raise Exception('listener or bean')

	
	def load(self, filename, eventManager):
		from xml.dom.minidom import parse
		doc = parse(filename)
		for trigger in doc.getElementsByTagName('trigger'):
			eventName = trigger.getAttribute('event')

			
			#if it's not "all" events
			if not eventName=='all':
				eventName = smart_load(eventName)().getType()
			
			
			eventManager.bind(eventName,self.getListener(trigger))
