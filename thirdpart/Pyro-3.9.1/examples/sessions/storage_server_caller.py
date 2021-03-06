import Pyro.core
import Pyro.naming
import sys

# server based on using caller object on the TLS to store session data


print """
This is the storage server that depends on the caller object in the TLS to
keep track of what the resource is for that given session. Because that object
is always equal to the current active client connection, it will work with
or without multithreading enabled. You can check this by looking at the
output on the screen and the contents of the datafiles."""
print

Pyro.config.PYRO_MULTITHREADED = raw_input("Enable multithreading y/n? ") in ('y', 'Y')


# The datastore.
# It will store lines of text in a file named after the 'user'.
# The resource that is owned by this user session (the file handle) is stored
# on the caller object on the TLS.
class DataStore(Pyro.core.ObjBase):
	def init(self, username):
		caller = self.getLocalStorage().caller
		caller.datastore = open("datastorage_%s.txt" % username, "w")
		
	def addline(self, textline):
		caller = self.getLocalStorage().caller
		sys.stdout.write("adding line to " + caller.datastore.name + "\n")
		sys.stdout.flush()
		caller.datastore.write(textline + " | came from " + str(caller) + "\n")
	
	def close(self):
		caller = self.getLocalStorage().caller
		caller.datastore.close()	
			
		

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)

try:
	ns.createGroup(":test")
except Exception:
	pass
try:
	ns.unregister(":test.datastorage")
except Exception:
	pass

daemon.connect(DataStore(), ":test.datastorage")

print "Server (caller version) is running."
daemon.requestLoop()
