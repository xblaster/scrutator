from twisted.web import xmlrpc, server

class SCRTServices(xmlrpc.XMLRPC):
    """An example object to be published."""

    def xmlrpc_push(self, obj_list, source):
        """Push event"""
        return x

    def xmlrpc_pull(self, source):
        """Pull event to a destination"""
        return a + b

if __name__ == '__main__':
    from twisted.internet import reactor
    r = SCRTServices()
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()
