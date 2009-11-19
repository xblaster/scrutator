import xml.dom.minidom
import unittest
from scrutator.core.manager import EventManager
from scrutator.core.sync.listener import FileRequestListener,\
	FileContentListener
from scrutator.core.sync.event import FileContent
from scrutator.core.listener import PrintListener
from scrutator.core.event import KickEvent, BanEvent, DieEvent

from scrutator.minidi.tool import *
import sys
#



#import scrutator.core.sync

class TestTool(unittest.TestCase):
		
	def testSmartLoad(self):
		if not isinstance(smart_load('scrutator.core.event.SimpleEvent')(), sys.modules['scrutator'].core.event.SimpleEvent):
			self.fail('smartLoad error')
		
	def testInjection(self):
		f = open('scrutator/tests/tool.fakepy', 'r')
		
		content = f.read()
		
		bus = EventManager()
		bus.bind(FileContent().getType(),FileContentListener())
		bus.bind('all',PrintListener())
		
		
		bus.push(FileContent(filename="hello/world/nimp/__init__.py",content="print \"init\""))
		bus.push(FileContent(filename="fake/__init__.py",content="print \"init\""))
		bus.push(FileContent(filename="fake/fake.py",content=content))
		
		bus.push(DieEvent(test="hello"))
		import fake.fake
