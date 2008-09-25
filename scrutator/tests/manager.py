import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *

class TestMockupException(Exception):
	pass

class ListenerMockup(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg = []):
		self.arg = arg
	def action(self, obj):
		raise TestMockupException("ACTION !!!")
		

class TestEventManager(unittest.TestCase):
	def setUp(self):
		self.manager = EventManager()
		self.listenermock  = ListenerMockup()
		
	def testSimpleBindAndUnbind(self):
		self.manager.bind('all', self.listenermock)
		self.manager.unbind('all', self.listenermock)
		
	def testSimplePush(self):
		self.manager.bind(KickEvent().getType(), self.listenermock)
		try:
			self.manager.push(KickEvent())
		except TestMockupException: 
			pass
		else:
			fail("expected TestMockupException")
		
		self.manager.unbind(KickEvent().getType(), self.listenermock)
		self.manager.push(KickEvent())
		

