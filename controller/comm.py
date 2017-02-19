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





'''
   class SSDP
''' 

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900
SSDP_MSG = "flightsimrc"

class Client(DatagramProtocol):
	def __init__(self, iface,bind):
		self.iface = iface
		self.bind = bind
		self.ssdp = reactor.listenMulticast(SSDP_PORT, self, listenMultiple=True)
		self.ssdp.setLoopbackMode(1)
		self.ssdp.joinGroup(SSDP_ADDR, interface=iface)

	def datagramReceived(self, datagram, (host,port)):
		Logger.debug("Datagram:%s ip:%s" %(datagram,host))
		msg=''
		try:	
			msg,port = datagram.rsplit(':')
		except:
			Logger.debug("Cannot handle SSDP message")
		if msg == SSDP_MSG:
			self.bind.ids.msg.text = "Discovered Receiver at %s:%s" % (host,port)
			self.bind.ids.bt1.text = "Continue"
			glb.root.startcom(host,int(port))
			self.stop()

	def stop(self):
		self.ssdp.leaveGroup(SSDP_ADDR, interface=self.iface)
		self.ssdp.stopListening()



class SSDP(Popup):

#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(SSDP, self).__init__(**kwargs)

#--------------------------------------------------------------------
	def on_open(self):
		self.ip = self.getIP()
		self.ids.msg.text = "Searching..."
		self.dp = Client(self.ip,self)

#--------------------------------------------------------------------
	def int_to_ip(self,ipnum):
		oc1 = int(ipnum / 16777216) % 256
		oc2 = int(ipnum / 65536) % 256
		oc3 = int(ipnum / 256) % 256
		oc4 = int(ipnum) % 256
		return '%d.%d.%d.%d' %(oc4,oc3,oc2,oc1)

#--------------------------------------------------------------------
	def getIP(self):
		
		try:
			from jnius import autoclass
			PythonActivity = autoclass('org.renpy.android.PythonActivity')
			SystemProperties = autoclass('android.os.SystemProperties')
			Context = autoclass('android.content.Context')
			wifi_manager = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
			ip = wifi_manager.getConnectionInfo()
			ip = ip.getIpAddress()
			ip = self.int_to_ip(int(ip))
		except:
			Logger.debug("Not running android ip trying via socket")
			s = socket(AF_INET,SOCK_DGRAM)
			s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
			s.connect(("<broadcast>",0))
			Logger.debug("Get ip:%s"%s.getsockname()[0])
			ip = s.getsockname()[0]
		return ip

#--------------------------------------------------------------------
	def on_dismiss(self):
		Logger.debug("dismiss popup")


class CommPopup(Popup):

#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(CommPopup, self).__init__(**kwargs)

#--------------------------------------------------------------------
	def connected(self):
		self.ids.msg.text = "Connected"
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
	controllerPortNumber = False
	controllerPortInterface = False
	connected = False
	msgQueue={}

#--------------------------------------------------------------------
	def datagramReceived(self, data, (host, port)):
		Logger.debug("DataReceive:"+data)
		if data == 'CONNECT ACK':
			self.connected = True
			self.popup.connected()

		if data == 'ACK':
			glb.root.lights.ack = 1
			glb.root.lights_ack_timer = 5

#--------------------------------------------------------------------
	def init(self,manual,ip,port):
		self.connected = False

		if manual:
			self.popup=CommPopup()
			self.popup.setMsg('Connecting...')
			self.popup.open()
			Logger.debug("manual ip configuration")
			self.init_ReceiverConnection(ip,port) 
			self.init_ControllerPort(port+1)
			#manual mode keep sending until receiver response
		else:
			Logger.debug("autodiscover configuration")
			#start discover

#--------------------------------------------------------------------
	def init_ControllerPort(self,port):
		self.controllerPortNumber = port  

		self.UDPSock_out = socket(AF_INET,SOCK_DGRAM)
		if self.controllerPortInterface:
			self.controllerPortInterface.stopListening()
		try:
			self.controllerPortInterface = reactor.listenUDP(self.controllerPortNumber,self)
		except:
			Logger.error("port %d already in use "%(port+1))

#--------------------------------------------------------------------
	def init_ReceiverConnection(self,ip,port):
		self.UDPSock_out = socket(AF_INET,SOCK_DGRAM)
		self.receiverIp = ip
		self.receiverPort = port


#--------------------------------------------------------------------
	def process(self):
		if not self.connected:
			self.send("CONNECT:%d\n"%self.controllerPortNumber)
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
	def start(self,ip,port):
		self.ip = ip
		self.outport = port
		Logger.debug("init UDP socket")
		self.UDPSock_out = socket(AF_INET,SOCK_DGRAM)
		if self.outgoingport:
			self.outgoingport.stopListening()
		try:
			self.outgoingport = reactor.listenUDP(self.port+1,DataReceive())
		except:
			Logger.error("port %d already in use "%(port+1))
		self.send("CONNECT:%d\n"%(port+1))

#--------------------------------------------------------------------
	def send(self,msg):
		try:
			#Logger.debug("SEND: %s"%msg.replace(':',';'))
			self.UDPSock_out.sendto(msg,(self.receiverIp,self.receiverPort))
		except:
			Logger.error("SEND")




