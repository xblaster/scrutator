# -*- coding: utf-8 -*-
from scrutator.core.network import *
from scrutator.core.factory import *

from scrutator.core.sync.event import *

from scrutator.minidi.tool import *
from scrutator.minidi.injector import *

#from scrutator.protocols.identify.brain import GlobalBrainClient
from scrutator.protocols.common import MinimalBrainClient


from scrutator.core.config import AgentConfig




#import sys

def onReactorInit():
	#init the brain
	
	if len(sys.argv) > 1:
		brain = sys.argv[1]
	else:
		brain = "scrutator.protocols.identify.brain.GlobalBrainClient"

	ic = smart_load(brain)()
	context.setBean('brain',ic)	


if __name__ == '__main__':
	context = Context() 
	context.addConfig(AgentConfig())
	
	eventSender = context.getBean('eventSender')
	define_smart_load_bus(eventSender)
	
	mb = MinimalBrainClient()
	context.setBean('minimalbrain',mb)
	
	reactor.callLater(0.5, onReactorInit)
	
	reactor.run()
	
