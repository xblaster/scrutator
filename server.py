from twisted.internet import gtk2reactor # for gtk-2.0
gtk2reactor.install()

from scrutator.core.network import *
from scrutator.core.factory import *


if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/impl/server.xml')
	
	eventSender = CoreManager().getBean('mainEventManager')
	 
	eventReceiver = CoreManager().getBean('eventReceiver')
	
	#initiatie GTK
	from scrutator.core.gtk_listener.gtk import *
	debug_listener = GtkDebugListener(self.manager)
	eventSender.bind('all', debug_listener)
	
	msg = SimpleEvent(plop="plop")
	
	print eventReceiver.getMessageBoxManager().push(SimpleEvent(to='bot1', msg=msg))
	
	event = SimpleEvent()
	reactor.callLater(3,eventSender.push, event)

	reactor.run()
	