import unittest
from scrutator.core.manager import *
from scrutator.core.event import *
from scrutator.core.listener import *
from scrutator.core.factory import *


class TestXMLBeanFactory(unittest.TestCase):
	
	def testLoad(self):
		xmlbe = XMLBeanFactory('resource/beans_sample.xml')
	