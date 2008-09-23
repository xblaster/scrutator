import pprint
 
import xml.dom.minidom
from xml.dom.minidom import Node

import xmlrpclib
import re
import sys
import getopt

class Channel:
    def __init__(self):
        self.name = "unknown"
        self.verbose = 0
        self.canTalk = 0
        self.canLearn = 0
        self.status = "offline"

class Server:
    def __init__(self):
        self.name = "unknown"
        self.host = "127.0.0.1"
        self.channels = dict()
        self.nickname = "red_abzeu"

    def addChannel(self, channel):
        if self.channels.has_key(channel.name):
            raise "this server already exist"
        
        self.channels[str(channel.name)] = channel

class ConnectionManager:
	def __init__(self):
		self.servers = dict() 	
		
	def addServer(self,server):
		if self.servers.has_key(server.name):
			raise "this server already exist"
		
		self.servers[str(server.name)] = server
	
	def addChannel(self, servername, channel):
		if not self.servers.has_key(servername):
			raise "this server does not exist"
		
		self.servers[str(servername)].addChannel(channel)
        
class XmlAdapter:
    def __init(self):
        pass
    
    def createConnectionManager(self):
        result = ConnectionManager()
        doc = xml.dom.minidom.parse(sys.argv[1])
        for node in doc.getElementsByTagName("server"):
          serv = self.createServer(node)
          for nickname in doc.getElementsByTagName("nickname"):
            serv.nickname = str(nickname.childNodes[0].data)
          result.addServer(serv)
          

        
        return result
    
    def createChannel(self,node):
        c = Channel()
        c.name = node.getAttribute("name")
        
        for verbose in node.getElementsByTagName("verbose"):
            c.verbose = int(verbose.childNodes[0].data)
            #print "verbose"
            #print c.verbose
        
        for canTalk in node.getElementsByTagName("canTalk"):
            c.canTalk = int(canTalk.childNodes[0].data)
        
        for canLearn in node.getElementsByTagName("canLearn"):
            c.canLearn = int(canLearn.childNodes[0].data)
        
        return c
    
    def createServer(self, node):
        s = Server()
        s.host = node.getAttribute("host")
        s.name = node.getAttribute("name")
        
        for childnode in node.childNodes:
            if childnode.nodeType != Node.TEXT_NODE:
                s.addChannel(self.createChannel(childnode))
        
        return s

def addLink(url, author, channel, desc, network):
    """    $param1 = new XML_RPC_Value(htmlentities($url),'string');
    $param2 = new XML_RPC_Value($author,'string');
    $param3 = new XML_RPC_Value($channel,'string');
    $param4 = new XML_RPC_Value(htmlentities($desc),'string');
    param5 = new XML_RPC_Value($_GET['__network'],'string');
    $param6 = new XML_RPC_Value($_GET['__name'],'string');
    $param7 = new XML_RPC_Value($_GET['__pwd'],'string');
    $msg = new XML_RPC_Message('lo2k.add_link', array($param1,$param2,$param3,$param4,$param5,$param6,$param7));
    $cli = new XML_RPC_Client('/index.php?ctrl=API&action=index', 'scrutator.lo2k.net');
    
    """     
    server = xmlrpclib.ServerProxy("http://scrutator.lo2k.net/index.php?ctrl=API&action=index")
    lo2kObj = server.lo2k
    return lo2kObj.add_link(url, author, channel, desc, network, 'scrutator2', 'coincoin')

def detectLink(message):
    p = re.compile('(http://|www\.)[^ ]*', re.IGNORECASE)
    m = p.search(message)
    
    if not m:
        return m
    
    else:
        return m.group()

def learn(message):        
    server = xmlrpclib.ServerProxy("http://srv.lo2k.net:2217")
    return server.learn(message)
    
def doreply(message):
    server = xmlrpclib.ServerProxy("http://srv.lo2k.net:2217")
    return server.doreply(message)

def get_comment(message):
    separator = ['<=','=>','<-','->','<','>']
    for sep in separator:
        if sep in message:
            comm, comm2 = message.split(sep,1)
            if not 'http' in comm2:
                return comm2.strip()
            return comm.strip()
    return ''
     
        
    
def main():
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere
    """
    c = XmlAdapter()
    
    #print detectlink("retgeruinei")
    #print detectlink("ntroeuntotu e http://www.scrutator.lo2k.net")
    #server = xmlrpclib.ServerProxy("http://srv.lo2k.net:2217")
    #print server.doreply("arf trop fort :)")
    
    #d = c.createConnectionManager()
    #server = xmlrpclib.ServerProxy("http://scrutator.lo2k.net/index.php?ctrl=API&action=index")
    #lo2kObj = server.lo2k
    #d = dict()
    #s = dict()
    #st = dict()
    #st['status'] = 'online'
    #s['#scrutator'] = st
    #d['worldnet'] = s
    #try:
    #try:
    #    print lo2kObj.update_channels('test', d)
    #except xml.parsers.expat.ExpatError, e:
    #    pprint.pprint(e)
    print get_comment('http://scrutator.lo2k.net < trop lol')
    #print addLink('http://www.lo2k.net','X-Blaster','#scrutator','test','Worldnet')
    #print d.servers['worldnet'].channels['#scrutator'].name
            
if __name__ == "__main__":
    main()

