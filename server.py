from scrutator.core.network import *
from scrutator.core.factory import *

if __name__ == '__main__':

	xmlbe = XMLBeanFactory('resource/beans_sample.xml')
	
	xeml = XmlEventManagerLoader()
	em = CoreManager().getBean('mainEventManager')
	xeml.load('resource/sample_debug.xml', em)
	
	eventSender = CoreManager().getBean('eventSender')
	event = SimpleEvent()

	reactor.run()
	