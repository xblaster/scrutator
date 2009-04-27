from scrutator.core.network import *
from scrutator.core.factory import *

if __name__ == '__main__':
	xmlbe = XMLBeanFactory('resource/impl/client.xml')
	
	eventSender = CoreManager().getBean('eventSender')
	event = KickEvent()
	
	eventSender.push(event)

	reactor.run()