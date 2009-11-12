import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *

class TestMockupException(Exception):
	pass

class ListenerMockup(SimpleListener):
	"""docstring for EventMockup"""
	def __init__(self, arg=[]):
		self.arg = arg
	def action(self, obj, evtMgr):
		raise TestMockupException("ACTION !!!")
		

class TestEventManager(unittest.TestCase):
	def setUp(self):
		self.manager = EventManager()
		self.listenermock = ListenerMockup()
		
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
		
	def testGatePush(self):
		self.manager = EventManager()
		self.listenermock = ListenerMockup()
		
		initialManager = EventManager()
		gate = GateListener(self.manager)
		initialManager.bind('all', gate)
		
		self.manager.bind(KickEvent().getType(), self.listenermock)
		try:
			#should pass through initialManager to testmanager
			initialManager.push(KickEvent())
		except TestMockupException: 
			pass
		else:
			self.fail("expected TestMockupException")

		self.manager.unbind(KickEvent().getType(), self.listenermock)
		self.manager.push(KickEvent())
		initialManager.unbindAll()
		self.manager.unbindAll()
		
	def testDispatcherPush(self):
		self.manager = EventManager()
		self.listenermock = ListenerMockup()

		initialManager = EventManager()
		dispatcher = DispatcherListener()
		initialManager.bind('all', dispatcher)
		
		dispatchList = dict()
		dispatchList['distant'] = self.manager
		
		dispatcher.setDispatcher(dispatchList)

		self.manager.bind(KickEvent().getType(), self.listenermock)
		try:
			#should pass through initialManager to testmanager
			ke = KickEvent(to="distant")
			initialManager.push(ke)
		except TestMockupException: 
			pass
		else:
			self.fail("expected TestMockupException")

		self.manager.unbind(KickEvent().getType(), self.listenermock)
		self.manager.push(KickEvent())
		initialManager.unbindAll()
		self.manager.unbindAll()
	

class TestMessageBoxManager(unittest.TestCase):
	def testMessageBoxManager(self):
		mboxMgr = MessageBoxManager()
		sevent = SimpleEvent()
		
		mbox = MessageBoxEvent(to="coin", msg=sevent)
		
		mboxMgr.push(mbox)
		
		self.assertEqual(mboxMgr.getMessagesFor('coin')[0], sevent)
		self.assertEqual(mboxMgr.getMessagesFor('coin')[0], sevent)
	
	def testFlush(self):
		mboxMgr = MessageBoxManager()
		sevent = SimpleEvent()
		
		mbox = MessageBoxEvent(to="coin", msg=sevent)
		
		mboxMgr.push(mbox)
		
		self.assertEqual(mboxMgr.getMessagesFor('coin')[0], sevent)
		mboxMgr.flushMessagesFor('coin')
		self.assertEqual(mboxMgr.getMessagesFor('coin'), list())
		
	def testPop(self):
		mboxMgr = MessageBoxManager()
		sevent = SimpleEvent()

		mbox = MessageBoxEvent(to="coin", msg=sevent)

		mboxMgr.push(mbox)

		self.assertEqual(mboxMgr.getMessagesFor('coin')[0], sevent)
		self.assertEqual(mboxMgr.popMessagesFor('coin')[0], sevent)
		self.assertEqual(mboxMgr.popMessagesFor('coin'), list())

"""class TestAsyncManager(unittest.TestCase):
	#DEPRECATED
	def testAsyncManager(self):
		asyncMgr = AsyncEventManager()
		l = list()
		
		l.append(BanEvent(source="bot1"))
		l.append(KickEvent(source="bot1"))
		l.append(KickEvent(chan="#funradio", source="bot1"))
		
		for evt in l:
			asyncMgr.push(evt)

		self.assertEquals(asyncMgr.getStoredEvent(), l)
		self.assertEquals(asyncMgr.getStoredEvent(), list())"""

from scrutator.minidi.injector import *
		
class TestCoreManager(unittest.TestCase):
	def testSingleton(self):
		self.assertEquals(id(CoreManager()), id(CoreManager()))

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
		
