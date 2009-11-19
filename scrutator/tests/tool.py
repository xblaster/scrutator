from scrutator.core.manager import EventManager
from scrutator.core.sync.listener import FileRequestListener
#from scrutator.core.sync.event import FileContent
import unittest
from scrutator.minidi.tool import *
import sys
import xml.dom.minidom



#import scrutator.core.sync

class TestTool(unittest.TestCase):
		
	def testSmartLoad(self):
		if not isinstance(smart_load('scrutator.core.event.SimpleEvent')(), sys.modules['scrutator'].core.event.SimpleEvent):
			self.fail('smartLoad error')
		
	def testInjection(self):
		f = open('scrutator/tests/tool.fakepy', 'r')
		
		content = f.read()
		
		#bus = EventManager()
		#FileRequestListener()
		#bus.bind(FileContent().getType(),FileRequestListener())
