from scrutator.core.server import *

if __name__ == '__main__':
	SCRTXMLRPC(SCRTServices(), 7080)
	reactor.run()