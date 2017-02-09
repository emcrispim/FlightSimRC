from twisted.internet.protocol import DatagramProtocol
from twisted.internet import defer,error,reactor
from twisted.internet.task import LoopingCall

from socket import socket,AF_INET,SOCK_DGRAM
import sys

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900
SSDP_MSG ='flightsimrc'

class CommService(DatagramProtocol):

	controller_ip = None
	controller_port = None
	receiver_port = None
	started = False

#--------------------------------------------------------------------
	def datagramReceived(self, data, (host, port)):
		key=''
		value=''
		try:
			key,value = data.split(":")
		except:
			self.log('WARN','Received a malformed message discarding')
			self.log("DEBUG",'Mailformed message:'+data)
			return

		if key == 'CONNECT':
			self.controller_ip = host
			self.controller_port = int(value)
			self.log('OK','Controller connected from ip %s at port %s'%(host,(int(value))))
			self.ctrl_status(True)
			self.UDPSock_out = socket(AF_INET,SOCK_DGRAM)
			self.UDPSock_out.sendto('CONNECT ACK',(self.controller_ip,self.controller_port)) 
			return

		if self.controller_ip == host:
			self.UDPSock_out.sendto('ACK',(self.controller_ip,self.controller_port)) 

			self.setAxis(key,value)

#--------------------------------------------------------------------
	def send_msearch(self):
		s = socket(AF_INET, SOCK_DGRAM)
		s.bind(('',0))
		addr = SSDP_ADDR , SSDP_PORT
		msg = SSDP_MSG+":"+str(self.receiver_port)
		try:
			send = True
			s.sendto(msg,addr)
			self.log("DEBUG","Broadcast message:%s"%msg)
		except socket.error as e:
			send = False
			self.log("ERROR","Discover Service:"+str(e))
		except:
			send = False
			self.log("ERROR",str(sys.exc_info()[0]))

		return send 

#--------------------------------------------------------------------
	def start(self,port):
		self.receiver_port = port
		lc = LoopingCall(self.send_msearch)
		lc.start(6)

		try:
			self.started = True
			self.udpport = reactor.listenUDP(port,self)
		except error.CannotListenError as e:
			self.started = False
			self.log("ERROR","Cannot start UDP service reason:%s"%e)
		except:
			self.started = False
			self.log("ERROR","Cannot start UDP service:"+str(sys.exc_info()[0]))
		if self.started:
			self.log("INFO","UDP service Started at port:%d"%(port))
		if self.started:
			self.start_success()
			self.ctrl_status(False)
			self.controller_ip = None
			self.controller_port = None

#--------------------------------------------------------------------
	def restart(self,port):
		def dfbstop(ignored):
			self.log("INFO","Stopping UDP Service")
			self.started = False
			return self.udpport.stopListening()
		def clbstop(ignored):
			self.started = False
			self.log("OK","UDP Service Stopped")
			self.start(port)
		if self.started:
			d = dfbstop("")
			d.addCallback(clbstop)
		else:
			self.start(port)

#--------------------------------------------------------------------
	def log(self,level,message):
		pass

#--------------------------------------------------------------------
	def setAxis(self,key,value):
		pass

#--------------------------------------------------------------------
	def ctrl_status(self,value):
		pass

#--------------------------------------------------------------------
	def start_success(self):
		pass


