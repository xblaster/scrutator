from scrutator.core.server import *

if __name__ == '__main__':
    from twisted.internet import reactor
    r = SCRTServices()
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()