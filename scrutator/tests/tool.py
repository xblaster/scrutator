import unittest
from scrutator.core.tool import *
import sys

class TestTool(unittest.TestCase):
		
	def testSmartLoad(self):
		if not isinstance(smart_load('scrutator.core.event.SimpleEvent')(), sys.modules['scrutator'].core.event.SimpleEvent):
			fail('smartLoad error')
		