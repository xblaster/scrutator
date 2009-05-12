# -*- coding: utf-8 -*-
from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install()

from scrutator.core.network import *
from scrutator.core.factory import *


if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/impl/server.xml')
	
	eventSender = CoreManager().getBean('mainEventManager')
	 
	eventReceiver = CoreManager().getBean('eventReceiver')
	
	#initiatie GTK
	from scrutator.core.gtk_listener.gtk_debug import *
	debug_listener = GtkDebugListener()
	eventSender.bind('all', debug_listener)

	debug_listener2 = GtkDebugListener()
	eventSender.bind('scrutator.core.event.KickEvent', debug_listener2)
	
	msg = SimpleEvent(plop="plop")
	
	#print eventReceiver.getMessageBoxManager().push(SimpleEvent(to='bot1', msg=msg))
	

	for i in range(100):
		event = KickEvent(frome="bidule", to="bidule")
		reactor.callLater(i/3,eventSender.push, event)
		event = SimpleEvent(frome="bidule", to="bidule")
		reactor.callLater(i/3,eventSender.push, event)
	reactor.run()
	