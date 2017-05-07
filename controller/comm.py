##########################################################################
# Author:               Eduardo Crispim, emcrispim@gmail.com
# Date:                 July, 2016
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
#########################################################################

from kivy.support import install_twisted_reactor

install_twisted_reactor()

import glb
from kivy.uix.popup import Popup
from kivy.logger import Logger
from twisted.internet import reactor, task
from twisted.internet.protocol import DatagramProtocol
from kivy.properties import  ObjectProperty
from socket import socket,AF_INET,SOCK_DGRAM,SOL_SOCKET,SO_BROADCAST

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900
SSDP_MSG = "flightsimrc"



#### CODE NOT NEDEED
# #--------------------------------------------------------------------
# def int_to_ip(ipnum):
# 	oc1 = int(ipnum / 16777216) % 256
# 	oc2 = int(ipnum / 65536) % 256
# 	oc3 = int(ipnum / 256) % 256
# 	oc4 = int(ipnum) % 256
# 	return '%d.%d.%d.%d' %(oc4,oc3,oc2,oc1)

# #--------------------------------------------------------------------
# def getIP():
		
# 		try:
# 			from jnius import autoclass
# 			PythonActivity = autoclass('org.renpy.android.PythonActivity')
# 			SystemProperties = autoclass('android.os.SystemProperties')
# 			Context = autoclass('android.content.Context')
# 			wifi_manager = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
# 			ip = wifi_manager.getConnectionInfo()
# 			ip = ip.getIpAddress()
# 			ip = int_to_ip(int(ip))
# 		except:
# 			Logger.debug("Not running android ip trying via socket")
# 			s = socket(AF_INET,SOCK_DGRAM)
# 			s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# 			s.connect(("<broadcast>",0))
# 			Logger.debug("Get ip:%s"%s.getsockname()[0])
# 			ip = s.getsockname()[0]
# 		return ip



'''
	 class SSDP
'''
class SSDP(DatagramProtocol):

#--------------------------------------------------------------------	
	def __init__(self,ctrl):
		self.ctrl=ctrl
		self.ssdp = reactor.listenMulticast(SSDP_PORT, self, listenMultiple=True)
		self.ssdp.setLoopbackMode(1)

		#TEST on ANDROID ip or interface not required no tested on android!!!!
		# self.ssdp.joinGroup(SSDP_ADDR, interface=self.iface)
		self.ssdp.joinGroup(SSDP_ADDR)
		Logger.debug("COMM:SSDP Service started")

#--------------------------------------------------------------------

	def datagramReceived(self, datagram, (host,port)):
		Logger.debug("COMM:Datagram:%s ip:%s" %(datagram,host))
		msg=''
		try:	
			msg,port = datagram.rsplit(':')
		except:
			Logger.debug("COMM:Cannot handle SSDP message")
		if msg == SSDP_MSG:
			Logger.debug("COMM:Discovered Receiver at %s:%s" % (host,port))
			self.ctrl.receiverIp = host
			self.ctrl.receiverPort = int(port)
			self.ctrl.controllerPort = int(port)+1 
			self.ctrl.init_ReceiverConnection()
			self.ctrl.init_ControllerPort()
			self.ctrl.send("CONNECT:%d\n"%self.ctrl.controllerPort)

			self.stop()

#--------------------------------------------------------------------

	def stop(self):
		self.ssdp.leaveGroup(SSDP_ADDR)
		# self.ssdp.leaveGroup(SSDP_ADDR, interface=self.iface)
		self.ssdp.stopListening()


'''
	 class CommPopup
'''
class CommPopup(Popup):

#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(CommPopup, self).__init__(**kwargs)
		Logger.debug("COMM:open popup")

#--------------------------------------------------------------------
	def connected(self):
		self.ids.msg.text = "Connected, your good to go!"
		self.ids.bt1.text = "Close"
#--------------------------------------------------------------------
	def setMsg(self,msg):
		self.ids.msg.text = msg


				

'''
	 class ctrl
'''
class ctrl(DatagramProtocol):
	receiverIp = ''
	receiverPort = 0
	controllerPort = False
	UDPSock_in = False
	ctrlconnected = False
	msgQueue={}


#--------------------------------------------------------------------
	def init(self,manual,ip,port):
		self.ctrlconnected = False
		self.manual=manual

		if manual:
			self.popup=CommPopup()
			self.popup.setMsg('Connecting to receiver...')
			self.popup.open()
			Logger.debug("COMM:manual ip configuration")
			self.receiverIp = ip
			self.receiverPort = port
			self.controllerPort = port+1 
			self.init_ReceiverConnection()
			self.init_ControllerPort()

			#manual mode keep sending until receiver response
		else:
			Logger.debug("COMM:autodiscover configuration")
			self.popup=CommPopup()
			self.popup.setMsg('Waiting for receiver...')
			self.popup.open()
			self.ssdp = SSDP(self)


#--------------------------------------------------------------------
	def datagramReceived(self, data, (host, port)):
		Logger.debug("COMM:Datagram:%s ip:%s" %(data,host))
		if data == 'CONNECT ACK':
			self.ctrlconnected = True
			self.popup.connected()
		elif data == 'ACK':
			glb.root.lights.ack = 1
			glb.root.lights_ack_timer = 5

#--------------------------------------------------------------------
	def init_ControllerPort(self):

		if self.UDPSock_in:
			self.UDPSock_in.stopListening()
		try:
			self.UDPSock_in = reactor.listenUDP(self.controllerPort,self)
		except:
			Logger.error("COMM:port %d already in use "%(self.controllerPort))

#--------------------------------------------------------------------
	def init_ReceiverConnection(self):
		self.UDPSock_out = socket(AF_INET,SOCK_DGRAM)


#--------------------------------------------------------------------
	def process(self):
		#this will be in main loop
		if not self.ctrlconnected:
			if self.manual:
				self.send("CONNECT:%d\n"%self.controllerPort)
		else:
			if len(self.msgQueue):
				for key, value in self.msgQueue.iteritems():
					msg=str(key)+':'+str(value)+'\n'
					self.send(msg)
				self.msgQueue={}

#--------------------------------------------------------------------
	def queue(self,key,value):
		self.msgQueue[key]=value

#--------------------------------------------------------------------
	def send(self,msg):
		try:
			#Logger.debug("SEND: %s"%msg.replace(':',';'))
			self.UDPSock_out.sendto(msg,(self.receiverIp,self.receiverPort))
		except:
			Logger.error("COMM:SEND")




