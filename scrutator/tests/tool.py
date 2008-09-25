import unittest
from scrutator.core.tool import *
class TestTool(unittest.TestCase):
		
	def testSmartLoad(self):
		if not isinstance(smart_load('scrutator.core.event.SimpleEvent')(), scrutator.core.event.SimpleEvent):
			fail('smartLoad error')
		