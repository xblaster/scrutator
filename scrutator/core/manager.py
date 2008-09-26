from scrutator.core.listener import *
from scrutator.core.event import *

from scrutator.core.tool import *

from twisted.internet import threads, reactor

"""   
def getPersonnes(self):

        if self.__personneList__ != None:

            return 

        self.__personneList__ = []

        for personnes in self.getRootElement().getElementsByTagName("personne"):

            if personnes.nodeType == personnes.ELEMENT_NODE:

                p = Personne()

                try:

                    p.nom = self.getText(personnes.getElementsByTagName("nom")[0])

                    p.prenom = self.getText(personnes.getElementsByTagName("prenom")[0])

                    p.adresse = self.getAdresse(personnes.getElementsByTagName("adresse")[0])

                except:

                    print 'Un des TAGS suivant est manquents : nom, prenom, adresse'

                self.__personneList__.append(p)

        return self.__personneList__
"""


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

class CoreManager:
	""" A python singleton """

	class __CoreManagerimpl:
		""" Implementation of the singleton interface """
		
		eventManager = EventManager()
		
		def __init__(self):
			pass
		
		def push(self, eventObj):
			return self.eventManager.push(eventObj)
			
		def getEventManager(self):
			return self.eventManager

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
	pass
	
	def load(self, filename, eventManager):
		from xml.dom.minidom import parse
		doc = parse(filename)
		for trigger in doc.getElementsByTagName('trigger'):
			eventName = trigger.getAttribute('event')
			listenerName = trigger.getAttribute('listener')
			
			eventClass = smart_load(eventName)()
			listenerClass = smart_load(listenerName)()
			
