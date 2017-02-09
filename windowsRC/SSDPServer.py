#from twisted.internet.protocol import DatagramProtocol
from kivy.clock import Clock
import socket
import sys

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900

class SSDPServer():

	def __init__(self,incomingport,ui):
		self.ui = ui
		self.setmsg(incomingport)
		self.start()
	
	#def datagramReceived(self, datagram, address):
	#	first_line = datagram.rsplit('\r\n')[0]
	#	Logger.debug( "Received %s from %r" % (first_line, address, ) )

	
	def send_msearch(self,dt):	
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(('',0))
		addr = SSDP_ADDR , SSDP_PORT
		try:
			self.ui.ssdpson = True
			print self.msg
			s.sendto(self.msg,addr)
		except socket.error as e:
			self.ui.ssdpson = False
			self.ui.logmsg("ERR","Discover Service:"+str(e))
		except:
			self.ui.ssdpson = False
			self.ui.logmsg("ERR",str(sys.exc_info()[0]))
			
	def setmsg(self,incomingport):
		self.msg = "flightsimrc:%s"%(str(incomingport))
		self.ui.logmsg("OK","Set discover message to:"+self.msg)

	def start(self):
		self.clock = Clock.schedule_interval(self.send_msearch,6)

	def stop(self):
		self.clock.cancel()
		pass