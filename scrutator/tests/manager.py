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
	def action(self, obj, evtMgr):
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
			self.fail("expected TestMockupException")
		
		self.manager.unbind(KickEvent().getType(), self.listenermock)
		self.manager.push(KickEvent())


class TestCoreManager(unittest.TestCase):
	def testSingleton(self):
		self.assertEquals(id(CoreManager()),id(CoreManager()))

class TestXml(unittest.TestCase):
	def testLoad(self):
		xeml = XmlEventManagerLoader()
		em = EventManager()
		xeml.load('resource/sample.xml', em)
		
		em.push(BanEvent())
		
		try: 
			em.push(KickEvent())
		except Exception:
			pass
		else:
			self.fail("expected an exception from ExceptionListener")
		