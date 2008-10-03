from scrutator.core.network import *
from scrutator.core.factory import *

if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/distant_node.xml')
	
	xeml = XmlEventManagerLoader()
	em = CoreManager().getBean('mainEventManager')
	xeml.load('resource/sample_debug.xml', em)
	
	eventSender = CoreManager().getBean('eventSender')
	event = SimpleEvent()
	
	eventSender.push(event)

	reactor.run()
	