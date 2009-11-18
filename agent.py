# -*- coding: utf-8 -*-
from scrutator.core.network import *
from scrutator.core.factory import *

from scrutator.core.sync.event import *

from scrutator.minidi.tool import *
from scrutator.minidi.injector import *

from scrutator.protocols.identify.brain import GlobalBrainClient, MinimalBrainClient


from scrutator.core.config import AgentConfig


#import sys

if __name__ == '__main__':
	
		
	
	context = Context() 
	context.addConfig(AgentConfig())
	
	eventSender = context.getBean('eventSender')
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
	#reactor.callLater(1, smart_import, 'services.irc')
	#eventSender.push(event)
	
	#init the brain
	
	if len(sys.argv) > 1:
		brain = sys.argv[1]
	else:
		brain = "scrutator.protocols.identify.brain.GlobalBrainClient"

	mb = MinimalBrainClient()
	context.setBean('minimalbrain',mb)

	ic = smart_load(brain)()
	context.setBean('brain',ic)
	
	
	
	reactor.run()
