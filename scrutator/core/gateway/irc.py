from twisted.words.protocols import irc

class IrcGate(irc.IRCClient):
	
	def __init__(self, mgr):
		self.eventMgr = mgr
	
	def push(self, event):
		return self.eventMgr.push(event)

	def connectionMade(self):
		pass

	def connectionLost(self, reason):
		pass


	# callbacks for events

	def signedOn(self):
		pass

	def joined(self, channel):
		pass

	def privmsg(self, user, channel, msg):
		pass

	def action(self, user, channel, msg):
		pass

    # irc callbacks

	def irc_NICK(self, prefix, params):
		"""Called when an IRC user changes their nickname."""
		pass
    
	def kickedFrom(self, channel, kicker, message):
		pass
        
	def left(self, channel):
		pass