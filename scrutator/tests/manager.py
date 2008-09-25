import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *

class EventMockup(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg = []):
		self.arg = arg
	def action(self):
		print "test"
		

class TestEventManager(unittest.TestCase):
	def setUp(self):
		self.manager = EventManager()
		
	def testSimpleBind(self):
		self.manager.bind('all', EventMockup())
		pass