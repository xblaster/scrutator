# -*- coding: utf-8 -*-
__old_import__ = __import__

def new_import(name, globals={}, locals={}, fromlist=[], level=-1):
	print name
	return __old_import(name, globals, locals, fromlist, level)

__import__ = new_import



print __import__


from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install()

from scrutator.core.network import *
from scrutator.core.factory import *


"""class Reply(SimpleListener):
	
	def action(self, eventObj, evtMgr):
		#event = KickEvent(plop=eventObj)
		evtMgr.push(eventObj)
		reactor.callLater(10,evtMgr.push, eventObj)"""

if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/impl/server.xml')
	
	eventSender = CoreManager().getBean('mainEventManager')
	 
	eventReceiver = CoreManager().getBean('eventReceiver')
	
	#initiatie GTK
	from scrutator.core.gtk_listener.gtk_debug import *
	debug_listener = GtkDebugListener()
	eventSender.bind('all', debug_listener)
	
	from scrutator.core.log.listener import *
	listener = SQLLogListener()
	eventSender.bind('all',listener)
	
	#eventSender.bind('all', Reply())

	#debug_listener2 = GtkDebugListener()
	#eventSender.bind('scrutator.core.event.KickEvent', debug_listener2)
	
	#msg = SimpleEvent(plop="plop")
	
	#eventReceiver.getMessageBoxManager().push(SimpleEvent(to='bot1', msg=msg))
	

	"""for i in range(100):
		#event = KickEvent(frome="bidule", to="bidule")
		evt = SimpleEvent(to='bot1', msg=msg)
		reactor.callLater(i, eventReceiver.getMessageBoxManager().push, evt)
		#reactor.callLater(i/3,eventSender.push, event)
		#event = SimpleEvent(frome="bidule", to="bidule")
		#reactor.callLater(i/3,eventSender.push, event)"""
	reactor.run()
	