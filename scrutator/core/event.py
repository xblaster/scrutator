import scrutator.core.exception
from scrutator.core.tool import smart_load

class EventSerializer(object):
	def __init__(self):
		pass
	
	def event2array(self, obj):
		if not isinstance(obj, SimpleEvent):
			raise scrutator.core.exception.BadTypeException("Not a SimpleEvent")
		return dict(type = obj.getType(), arg = obj.getArg())
		
	def array2event(self, refDict):
		if not refDict.has_key('type'):
			raise scrutator.core.exception.BadTypeException("Do not contain a type for reconstruction")
		recons = smart_load(refDict['type'])()
		recons.setArg(refDict['arg'])
		
		return recons

class SimpleEvent(object):
	"""simple event
	base class of all event"""
	def __init__(self, **arg):
		self.setArg(arg)

	def getType(self):
		"""return the type of the object (containing module name and class name)"""
		return self.__class__.__module__+'.'+self.__class__.__name__
		
	def getArg(self):
		return self.arg
		
	def setArg(self,argDict):
		self.arg = argDict
	
	def getArgEntry(self, entry):
		return self.arg[entry]
	
	def setArgEntry(self, entryname, entry):
		self.arg[entryname] = entry

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
	
class BanEvent(SimpleEvent):
	pass

#definition of all common event

class ConnectionMade(SimpleEvent):
	pass

class ConnectionLost(SimpleEvent):
	pass


