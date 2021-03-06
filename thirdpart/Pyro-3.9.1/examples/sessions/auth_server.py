import Pyro.core
import Pyro.naming
import Pyro.protocol
import sys

# Server based on using TLS to store session data.
# It uses client authentication to get the user name for the session.


print """
This is the storage server that depends on TLS and multithreading.
It uses client connection authentication to identify the client that
belongs to the connection, instead of simply storing a client identifier
that is passed in via a remote method call."""


# The datastore.
# It will store lines of text in a file named after the 'user'.
# The resource that is owned by this user session (the file handle) is stored on the TLS.
class DataStoreAuth(Pyro.core.ObjBase):
	def init(self):
		# use the username set on the connection object (by the ConnValidator)
		tls = self.getLocalStorage()
		tls.username = tls.caller.username
		tls.datastore = open("datastorage_%s.txt" % tls.username, "w")
	
	def addline(self, textline):
		tls = self.getLocalStorage()
		sys.stdout.write("adding line to " + tls.datastore.name + "\n")
		sys.stdout.flush()
		tls.datastore.write(textline + " | user=" + tls.username + " | came from " + str(tls.caller) + "\n")
	
	def close(self):
		tls = self.getLocalStorage()
		tls.datastore.close()	


# The Connection Validator, server side
# This is only an example, don't use it like this in your own code!
class SimpleServersideConnValidator(Pyro.protocol.DefaultConnValidator):
	def acceptIdentification(self, daemon, connection, token, challenge):
		# The token will be the username:password string, received from the client.
		login, password = token.split(':', 1)
		if password != "secretpassw0rd":
			return (0, Pyro.constants.DENIED_SECURITY)
		# We store the login name on the connection object to refer to it later.
		connection.username = login
		return (1, 0)
		

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)
daemon.setNewConnectionValidator(SimpleServersideConnValidator())

try:
	ns.createGroup(":test")
except Exception:
	pass
try:
	ns.unregister(":test.datastorage_auth")
except Exception:
	pass

daemon.connect(DataStoreAuth(), ":test.datastorage_auth")

print "Server (auth) is running."
daemon.requestLoop()
