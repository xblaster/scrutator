class Filter(object):
	def callback(self, value):
		return value
		

class AddArgFilter(Filter):

	def __init__(self, arg, value):
		super(AddArgFilter, self).__init__()
		self.arg = arg
		self.value = value
	
	def callback(self, event)
		event.setArgEntry(arg, value)
		return event
