import Pyro.core
import Pyro.naming
import sys

# server based on using TLS to store session data


print """
This is the storage server that depends on Thread Local Storage to keep track
of what the resource is for that given session. TLS only works for this if
the server runs with real threads (so every connection/session has its own
distinct TLS). If you disable multithreading, TLS will overlap for all
sessions and resources get mixed up. You can check this by looking at the
output on the screen and the contents of the datafiles."""
print """
If running with multithreading you will, after running the storage_client,
end up with a few datafiles: one for every user, and only that user's lines
in it. If not using multithreading things will break: almost all lines
(from all users) end up in a single datafile and errors might occur
because wrong stuff is closed."""
print

Pyro.config.PYRO_MULTITHREADED = raw_input("Enable multithreading y/n? ") in ('y', 'Y')


# The datastore.
# It will store lines of text in a file named after the 'user'.
# The resource that is owned by this user session (the file handle) is stored on the TLS.
class DataStore(Pyro.core.ObjBase):
	def init(self, username):
		tls = self.getLocalStorage()
		tls.datastore = open("datastorage_%s.txt" % username, "w")
		
	def addline(self, textline):
		tls = self.getLocalStorage()
		sys.stdout.write("adding line to " + tls.datastore.name + "\n")
		sys.stdout.flush()
		tls.datastore.write(textline + " | came from " + str(tls.caller) + "\n")
	
	def close(self):
		tls = self.getLocalStorage()
		tls.datastore.close()	
			
		

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

print "Server (TLS version) is running."
daemon.requestLoop()
