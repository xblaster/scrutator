# -*- coding: utf-8 -*-
import scrutator.core.exception
from scrutator.minidi.tool import smart_load


class EventSerializer(object):
	def __init__(self):
		pass
	
	def event2array(self, obj):
		if not isinstance(obj, SimpleEvent):
			raise scrutator.core.exception.BadTypeException("Not a SimpleEvent")
		#return dict(type=obj.getType(), arg=obj.getArg())
		
		import pickle
		return dict(type=obj.getType(), arg=pickle.dumps(obj.getArg()))
		
	def array2event(self, refDict):
		if not refDict.has_key('type'):
			raise scrutator.core.exception.BadTypeException("Do not contain a type for reconstruction")
		try:
			recons = smart_load(refDict['type'])()
		except TypeError:
			raise Exception(refDict['type']+" can't be unserialize")
			
		import pickle
		recons.setArg(pickle.loads(refDict['arg']))
		
		return recons

class EventAttributeError(AttributeError):
	pass

class SimpleEvent(object):
	"""simple event
	base class of all event"""
	def __init__(self, **arg):
		self.setArg(arg)

	def getType(self):
		"""return the type of the object (containing module name and class name)"""
		return self.__class__.__module__ + '.' + self.__class__.__name__
		
	def getArg(self):
		return self.arg
	
	def getArgs(self):
		return self.getArg()
		
	def setArg(self, argDict):
		self.arg = argDict
	
	def getArgEntry(self, entry):
		return self.arg[entry]
	
	def setArgEntry(self, entryname, entry):
		self.arg[entryname] = entry
		
	def hasArgEntry(self, argname):
		return self.getArg().has_key(argname)

	def getString(self):
	    str_res = self.__class__.__module__ + '.' + self.__class__.__name__ + ': {'
	    keys = list()
	    for k in self.getArgs():
	      keys.append(str(k) + ' => ' + str(self.getArgEntry(k)))
	    str_res += ", ".join(keys) + "}"
	    return str_res
	
	def __getattribute__(self, name):
		
		if name =="arg":
			return super(SimpleEvent, self).__getattribute__('arg') 
		try:
			return super(SimpleEvent, self).__getattribute__(name)
		except AttributeError:
			pass
		if self.hasArgEntry(name):
			return self.getArgEntry(name)
		raise EventAttributeError(name + ' does not appear to be an attribute of ' + str(self) + ' event')

class DelayedEvent(SimpleEvent):
	delay = 1
	
	def __init__(self, **arg):
		super(DelayedEvent, self).__init__(**arg)
		if not self.arg.has_key('event'):
			raise Exception('not event arg in dict')
		
		if not isinstance(self.arg['event'], SimpleEvent):
			raise Exception('event arg is not an inherited SimpleEvent object')
		
class KickEvent(SimpleEvent):
	pass

class RawCommandEvent(SimpleEvent):
	pass
	
class BanEvent(SimpleEvent):
	pass

#specific message event
class MessageBoxEvent(SimpleEvent):
	def __init__(self, **arg):
		super(MessageBoxEvent, self).__init__(**arg)
		if not self.arg.has_key('to'):
			raise Exception('not "to" arg in dict')
		
		if not isinstance(self.arg['msg'], SimpleEvent):
			raise Exception('event "msg" is not an inherited SimpleEvent object')

#definition of all common event

class ConnectionMade(SimpleEvent):
	pass

class ConnectionLost(SimpleEvent):
	pass

class DieEvent(SimpleEvent):
	pass

class SpawnEvent(SimpleEvent):
	pass

class PingEvent(SimpleEvent):
	pass

class ContainerEvent(SimpleEvent):
	pass
