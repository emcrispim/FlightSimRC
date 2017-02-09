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



'''
   class SSDP
''' 

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900

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
		if msg == "flightsimrc":
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


	def int_to_ip(self,ipnum):
		oc1 = int(ipnum / 16777216) % 256
		oc2 = int(ipnum / 65536) % 256
		oc3 = int(ipnum / 256) % 256
		oc4 = int(ipnum) % 256
		return '%d.%d.%d.%d' %(oc4,oc3,oc2,oc1)

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
			Logger.debug("Not running android ip set:192.168.1.86")
			ip = '192.168.1.86'
		return ip

	def on_dismiss(self):
		Logger.debug("dismiss popup")



class EchoProtocol(DatagramProtocol):
	def datagramReceived(self, data, (host, port)):

		if data == 'ACK':
			glb.root.lights.ack = 1
			glb.root.lights_ack_timer = 5
				