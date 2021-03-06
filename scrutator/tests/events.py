import unittest
from scrutator.core.event import *

class TestEvents(unittest.TestCase):
	def setUp(self):
		pass
		
	def getMockupEvent(self):
		s = BanEvent(channel="#funradio", nickname="jdl")
		return s
	
	def testSimpleEvent(self):
		s = SimpleEvent()
		self.assertEqual(s.getType(), "scrutator.core.event.SimpleEvent")
		
	def testInheritedEvent(self):
		s = KickEvent()
		self.assertEqual(s.getType(), "scrutator.core.event.KickEvent")

	
	def testEventArgs(self):
		s = self.getMockupEvent()
		self.assertEqual(s.getArgEntry('channel'), "#funradio")
		
		s.setArgEntry('count', 4)
		self.assertEqual(s.getArgEntry('count'), 4)
		
		self.assertEqual(s.hasArgEntry('channel'), True)
		
	def testEventSerializerEvent2Arr(self):
		s = self.getMockupEvent()
		es = EventSerializer()
		res = es.event2array(s)
		self.assertEqual(res['type'], s.getType())
		#self.assertEqual(res['arg'], s.getArg())
		
		
	def testEventSerializerEvent2ArrWithNone(self):
		s = self.getMockupEvent()
		s.setArgEntry("plop", None)
		es = EventSerializer()
		res = es.event2array(s)
		
		s_reconstruct = es.array2event(res)
			
		if not isinstance(s_reconstruct, BanEvent):
			self.fail('Bad reconstruction :)')
	
	def testEventSerializerArr2Event(self):
		s = self.getMockupEvent()
		es = EventSerializer()
		res = es.event2array(s)
		
		s_reconstruct = es.array2event(res)
			
		if not isinstance(s_reconstruct, BanEvent):
			self.fail('Bad reconstruction :)')
			
			
	def testEventDelayedEventConst(self):
		mock = self.getMockupEvent()
		
		d = DelayedEvent(event=mock)
	
	def testGetAttribute(self):
		s = SimpleEvent(chan='prout')
		
		self.assertEqual('prout', s.chan)
		
	def testWrongGetAttribute(self):
		s = SimpleEvent(chan='prout')
		try:
			s.prim
		except EventAttributeError:
			return
		self.fail('EventAttributeError exception expected')
