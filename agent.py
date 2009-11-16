# -*- coding: utf-8 -*-
from scrutator.core.network import *
from scrutator.core.factory import *

from scrutator.core.sync.event import *

from scrutator.minidi.tool import *

if __name__ == '__main__':
	
	CoreManager().addConfig(XMLConfig('resource/impl/client.xml'))
	
	eventSender = CoreManager().getBean('eventSender')
	define_smart_load_bus(eventSender)
	
	#eventSender.push(event)

	#cmd='from scrutator.minidi.tool import *'+"\n"
	#cmd='import scrutator.minidi.tool'+"\n"
	#cmd='exec(scrutator.minidi.tool)'+"\n"
	#cmd+='_safeimport(scrutator.core.event.SimpleEvent)'+"\n"
	#event = RawCommandEvent(cmd = cmd)
	#eventSender.push(event)

	#event = RawCommandEvent(cmd='from tmp.scrutator.core.manager import EventManager')
	#event = FileRequest(file='scrutator/core/listener.py')
	#for i in range(10):
	#  event = RawCommandEvent(cmd='print "'+str(i)+'"')
	#  eventSender.push(event)
	#event = RawCommandEvent(cmd='sys.exit(0)')
	reactor.callLater(1, smart_import, 'services.irc')
	#eventSender.push(event)
	
	reactor.run()
