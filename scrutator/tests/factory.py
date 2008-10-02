import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *
from scrutator.core.factory import *


class TestXMLBeanFactory(unittest.TestCase):
	
	def testLoad(self):
		xmlbe = XMLBeanFactory('resource/beans_sample.xml')
		eventSender = CoreManager().getBean('eventSender')
		event = KickEvent()
		#reactor.callLater(1, print, "hello")
		
		xeml = XmlEventManagerLoader()
		em = CoreManager().getBean('mainEventManager')
		xeml.load('resource/sample_debug.xml', em)
		
		
		
		reactor.callLater(0.2, eventSender.push, event)
		reactor.run()
	