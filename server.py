# -*- coding: utf-8 -*-
"""
__old_import__ = __import__

def new_import(name, globals={}, locals={}, fromlist=[], level= -1):
	print name
	return __old_import(name, globals, locals, fromlist, level)

__import__ = new_import



print __import__
"""
#from twisted.internet import gtk2reactor # for gtk-2.0
#gtk2reactor.install()

from scrutator.core.network import *
from scrutator.core.factory import *


from scrutator.protocols.identify.brain import *

from scrutator.core.config import ServerConfig
from scrutator.minidi.injector import Context
from scrutator.protocols.example.sandbox import SandboxBrainServer



"""class Reply(SimpleListener):
	
	def action(self, eventObj, evtMgr):
		#event = KickEvent(plop=eventObj)
		evtMgr.push(eventObj)
		reactor.callLater(10,evtMgr.push, eventObj)"""

if __name__ == '__main__':

	#CoreManager().addConfig(XMLConfig("resource/impl/server.xml"))
	context = Context() 
	context.addConfig(ServerConfig())
	
	#ask retrieve due to lazy init
	#context.getBean('mainEventManager')
	context.getBean('eventReceiver')
	#eventSender = context.getBean('eventSender')
	
	#init the brain
	ic = GlobalBrainServer()
	context.setBean('RegistryBrain',ic)
	
	sb = SandboxBrainServer()
	context.setBean('SandboxBrain',sb)
	
	reactor.run()
	
