from scrutator.core.network import *
from scrutator.core.factory import *

if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/impl/server.xml')
	
	eventSender = CoreManager().getBean('mainEventManager')
	print eventSender
	event = SimpleEvent()
	reactor.callLater(3,eventSender.push, event)

	reactor.run()
	