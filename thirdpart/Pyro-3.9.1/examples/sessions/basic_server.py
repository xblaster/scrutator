import Pyro.core
import Pyro.naming


def initTLSfunc(tls):
	print "initializig TLS", repr(tls)
	# we create a counter attribute and set it to 0 initially,
	# so that all worker invocations can just increase the counter.
	tls.counter = 0


class Worker(Pyro.core.ObjBase):
	def process(self, clientThreadName):
		print "got a call from client thread", clientThreadName
		tls = self.getLocalStorage()
		tls.counter += 1
		print "   TLS.counter=%d (tls=%r)" % (tls.counter, tls)
		print "   caller=", tls.caller
		

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)
daemon.setInitTLS(initTLSfunc)

try:
	ns.createGroup(":test")
except Exception:
	pass
try:
	ns.unregister(":test.threadstorage")
except Exception:
	pass

daemon.connect(Worker(), ":test.threadstorage")

print "Server running."
daemon.requestLoop()
