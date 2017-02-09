from twisted.internet.protocol import DatagramProtocol
from twisted.internet import defer
from socket import socket,AF_INET,SOCK_DGRAM

class UDPServer(DatagramProtocol):

	controller_ip = ''
	controller_port = 0	

	def datagramReceived(self, data, (host, port)):
		key=''
		value=''
		try:
			key,value = data.split(":")
		except:
			self.log('WARN','Received a malformed message discarding')
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
			print key,value
			self.UDPSock_out.sendto('ACK',(self.controller_ip,self.controller_port)) 
			self.setAxis(key,value)



	def log(self,level,message):
		pass

	def setAxis(self,key,value):
		pass

	def ctrl_status(self,value):
		pass


class UDPUIServer(UDPServer):

	def __init__(self,ui):
		self.ui = ui


	def log(self,level,message):
		self.ui.logmsg(level,message)

	def ctrl_status(self,value):
		self.ui.controlleron = True

	def setAxis(self,key,value):
		self.ui.ids[key].value = int(value)
