# -*- coding: utf-8 -*-
class CallbackObject(object):
	""" base of all callback"""
	def __init__(self):
		pass

	def callback(self, eventObj):
		return eventObj


class AddArgCallback(CallbackObject):
	""" base of all callback"""
	def __init__(self, argName, argValue):
		self.argName = argName
		self.argValue = argValue

	def callback(self, eventObj):
		eventObj.setArgEntry(self.argName, self.argValue)
		return eventObj

class ToMessageBoxManagerCallback(CallbackObject):
	""" base of all callback"""
	def __init__(self, to):
		self.to = to
		

	def callback(self, eventObj):
		from scrutator.core.event import SimpleEvent
		event = SimpleEvent(to=self.to, msg=eventObj)
		return event
