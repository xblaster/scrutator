import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *
from scrutator.core.factory import *


class TestXMLBeanFactory(unittest.TestCase):
	
	def testLoadBeanAndNetwork(self):
		xmlbe = XMLBeanFactory('resource/beans_sample.xml')
		eventSender = CoreManager().getBean('eventSender')
		event = SimpleEvent()
		#reactor.callLater(1, print, "hello")
		
		xeml = XmlEventManagerLoader()
		em = CoreManager().getBean('mainEventManager')
		xeml.load('resource/test_bean_factory_trigger.xml', em)
		
		reactor.callLater(0.01, eventSender.push, event)
		
		#self.fail("Need to reimplement")
		reactor.callLater(10, reactor.stop)
		reactor.run()
		
		
		
		em.unbindAll()