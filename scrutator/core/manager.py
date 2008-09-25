from scrutator.core.listener import *


class EventManager:
	""" handle event in the application"""
	
	listeners_map = dict()

	def __init__(self):
		pass
		
	def bind(self, eventName, listener):
		if not isinstance(listener, SimpleListener):
			raise Exception("Not an SimpleListener")
		self.__getListenerMap(str(eventName)).append(listener)
	
	def __getListenerMap(self, mapname):
		""""
		return a listener map name for bindings
		"""
		if not self.listeners_map.has_key(mapname):
			self.listeners_map[mapname] = list()
		return self.listeners_map[mapname]
