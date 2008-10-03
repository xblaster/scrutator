import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *
from scrutator.core.factory import *


class TestXMLBeanFactory(unittest.TestCase):
	
	def testLoad(self):
		xmlbe = XMLBeanFactory('resource/beans_sample.xml')
		eventSender = CoreManager().getBean('eventSender')
		event = SimpleEvent()
		#reactor.callLater(1, print, "hello")
		
		xeml = XmlEventManagerLoader()
		em = CoreManager().getBean('mainEventManager')
		xeml.load('resource/test_bean_factory_trigger.xml', em)
		
		
		
		reactor.callLater(0.2, eventSender.push, event)
		#reactor.callLater(0.4, reactor.stop)
		reactor.run()
		
		em.unbindAll()
	