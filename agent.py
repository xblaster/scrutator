# -*- coding: utf-8 -*-
from scrutator.core.network import *
from scrutator.core.factory import *

if __name__ == '__main__':
	xmlbe = XMLBeanFactory('resource/impl/client.xml')
	
	eventSender = CoreManager().getBean('eventSender')
	#event = KickEvent()
	
	#eventSender.push(event)

	#cmd='from scrutator.core.tool import *'+"\n"
	#cmd='import scrutator.core.tool'+"\n"
	#cmd='exec(scrutator.core.tool)'+"\n"
	#cmd+='_safeimport(scrutator.core.event.SimpleEvent)'+"\n"
	#event = RawCommandEvent(cmd = cmd)
	#eventSender.push(event)

	#event = RawCommandEvent(cmd='from tmp.scrutator.core.network import *')
	#for i in range(10):
	#  event = RawCommandEvent(cmd='print "'+str(i)+'"')
	#  eventSender.push(event)
	#event = RawCommandEvent(cmd='sys.exit(0)')
	#eventSender.push(event)

	reactor.run()