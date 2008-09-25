from scrutator.core.listener import *
from scrutator.core.event import *

from twisted.internet import threads, reactor

class EventManager:
	""" handle event in the application"""
	
	listeners_map = dict()

	def __init__(self):
		pass
		
	def bind(self, eventName, listener):
		if not isinstance(listener, SimpleListener):
			raise Exception("Not an SimpleListener inherited object")
		self.__getListenerMap(str(eventName)).append(listener)
	
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
			threads.deferToThread(listener_obj.action(eventObj))
		
		for listener_obj in self.__getListenerMap('all'):
			threads.deferToThread(listener_obj.action(eventObj))
			
	
	def __getListenerMap(self, mapname):
		""""
		return a listener map name for bindings
		"""
		if not self.listeners_map.has_key(mapname):
			self.listeners_map[mapname] = list()
		return self.listeners_map[mapname]
