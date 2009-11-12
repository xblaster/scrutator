import unittest


from twisted.internet import defer
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *
from scrutator.core.factory import *
from twisted.internet import threads

class TestXMLBeanFactory(unittest.TestCase):
	
	def testLoadBeanAndNetwork(self):
		xmlbe = XMLBeanFactory('resource/beans_sample.xml')
		eventSender = CoreManager().getBean('eventSender')
		event = SimpleEvent()
		#reactor.callLater(1, print, "hello")
		
		xeml = XmlEventManagerLoader()
		em = CoreManager().getBean('mainEventManager')
		xeml.load('resource/test_bean_factory_trigger.xml', em)
		
		#d = defer.Deferred
		
		#reactor.callLater(0.01, eventSender.push, event)

		d = threads.deferToThread(eventSender.push, event)
		
		def fail_func():
			self.fail("FAIL !!")
		
		d.addCallback(em.unbindAll, fail_func)
		
		#self.fail("Need to reimplement")
		#reactor.callLater(10, reactor.stop)
		#reactor.run()
		
		
		
		#em.unbindAll()
