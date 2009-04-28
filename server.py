from scrutator.core.network import *
from scrutator.core.factory import *

if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/impl/server.xml')
	
	eventSender = CoreManager().getBean('mainEventManager')
	print eventSender
	 
	eventReceiver = CoreManager().getBean('eventReceiver')
	
	msg = SimpleEvent(plop="plop")
	
	print eventReceiver.getMessageBoxManager().push(SimpleEvent(to='bot1', msg=msg))
	
	event = SimpleEvent()
	reactor.callLater(3,eventSender.push, event)

	reactor.run()
	