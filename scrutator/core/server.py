from twisted.web import xmlrpc, server

class SCRTServices(xmlrpc.XMLRPC):
	"""An example object to be published."""

	def __init__(self):
		pass
	
	def xmlrpc_push(self, obj_list, source):
		"""Push event"""
		return x

	def xmlrpc_pull(self, source):
		"""Pull event to a destination"""
		return a + b


