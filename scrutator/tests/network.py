import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *
from scrutator.core.factory import *

from twisted.internet import defer

class NetworkTestManagerListener(SimpleListener):
	def __init__(self):
		super(NetworkTestManagerListener, self).__init__()
	
	def action(self, eventObj, evtMgr):
		storeMgr = CoreManager().getBean('StoreManager')
		
	def sendStop(dest):
		pass

class NetworkTest(unittest.TestCase):
		
	def testAsync(self):
		
		reactor.removeAll()
		
		xmlbe = XMLBeanFactory('resource/server_sample.xml')
		eventSender = CoreManager().getBean('bot1')
		event = SimpleEvent()
		#reactor.callLater(1, print, "hello")

		xeml = XmlEventManagerLoader()
		em = CoreManager().getBean('mainEventManager')
		xeml.load('resource/test_bean_factory_trigger.xml', em)

		#reactor.callLater(10, reactor.stop)

		reactor.callLater(0.01, eventSender.push, event)
		#reactor.run()
		#d = threads.deferToThread( self.fail, 'BAD')
		d = defer.Deferred()
		
		
		#reactor.wakeUp()

		em.unbindAll()
		return defer.fail(Exception('hoho'))
