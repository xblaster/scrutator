import unittest
from scrutator.core.event import *

class TestEvents(unittest.TestCase):
    def setUp(self):
        pass
        
    def testSimpleEvent(self):
        s = SimpleEvent()
        self.assertEqual( s.getType(), "SimpleEvent")
        
    def testInheritedEvent(self):
        s = KickEvent()
        self.assertEqual( s.getType(), "KickEvent")
        
