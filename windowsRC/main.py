
##########################################################################
# Author:               Eduardo Crispim, emcrispim@gmail.com
# Date:                 July, 2016
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
#########################################################################


__version__ = '1.0.0' #declare the app version. Will be used by buildozer

from kivy.support import install_twisted_reactor

install_twisted_reactor()

import sys
import socket
import platform
from kivy.logger import Logger
from kivy.app import App 
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import  ObjectProperty,BooleanProperty,NumericProperty
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.widget import Widget

from twisted.internet import reactor, task, error
from UDPServer import *
from SSDPServer import *


Config.set('kivy', 'log_level', 'debug')
Config.write() 

class Status(Widget):
	r = NumericProperty(0)
	g = NumericProperty(0)

	def set_on(self,value):
		if value:
			self.g = 1
			self.r = 0
		else:
			self.r = 1
			self.g = 0


Window.size = (960, 540)

def getNetworkIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.connect(('<broadcast>', 0))
	return s.getsockname()[0]

 

'''
	 class MainUI
'''
class MainUI(BoxLayout):#the app ui

	app            = ObjectProperty(None)
	ssdpsview      = Status()
	udpserviceview = Status()
	vjoyview 	   = Status()
	controllerview = Status()

	settings = {}

	ssdpson 	   = BooleanProperty(True)
	vjoyon 		   = BooleanProperty(True)
	udpserviceon   = BooleanProperty(True)
	controlleron   = BooleanProperty(True) 


#--------------------------------------------------------------------

	def on_controlleron(self,instance,value):
		self.controllerview.set_on(value)
#--------------------------------------------------------------------

	def on_vjoyon(self,instance,value):
		self.vjoyview.set_on(value)

#--------------------------------------------------------------------

	def on_ssdpson(self,instance,value):
		self.ssdpsview.set_on(value)

#--------------------------------------------------------------------

	def on_udpserviceon(self,instance,value):
		self.udpserviceview.set_on(value)

#--------------------------------------------------------------------

	def __init__(self, **kwargs):
		super(MainUI, self).__init__(**kwargs)

#--------------------------------------------------------------------
		
	def init5(self):
		p = platform
		system = p.system()
		if p.architecture()[0]=='32bit':
			self.logmsg("OK",'Detected 32-bit architecture')
		else:
			self.logmsg("OK",'Detected 64-bit architecture')
		self.controlleron = False
		self.ssdpson = False
		self.vjoyon = False
		self.udpserviceon = False
		self.loadconfig()
		manualip = bool(self.settings["MANUALIP"])
		ip = self.settings['IP']
		if not manualip:
			self.getautoip(ip)
		else:
			self.logmsg("OK","Using manual ip %s"%ip)
		self.initssdps()
		self.startUDPService()
		if system =='Windows':
			self.logmsg("OK",'%s OS'%system)
			self.startVjoyDriver()
		elif system=='Linux':
			self.logmsg("OK",'%s OS'%system)
		else:
			self.logmsg("ERROR","Incompatible OS:"+system)
			



		

#--------------------------------------------------------------------
	
	def startVjoyDriver(self):
		self.vjoyon = True
		try:
			from vjoy.vjoy import *
			vjoy = VJoy(1)
		except VirtualJoystickException as msg:
			self.logmsg("ERR",str(msg))
			self.vjoyon = False
		except:
			self.vjoyon = False
			self.logmsg("ERR","Cannot start vjoy driver:"+str(sys.exc_info()[0]))

		if self.vjoyon:
			self.logmsg("OK","Connected" + vjoy.productString())
			self.vjoy = vjoy

#--------------------------------------------------------------------
	def startUDPService(self):
		
		ip = self.settings['IP']
		incomingport = self.settings['INCOMINGPORT']
		try:
			self.udpserviceon = True
			self.udpport = reactor.listenUDP(incomingport,UDPUIServer(self))
		except error.CannotListenError as e:
			self.udpserviceon = False
			self.logmsg("ERR","Cannot start UDP service reason:%s"%e)
		except:
			self.udpserviceon = False
			self.logmsg("ERR","Cannot start UDP service:"+str(sys.exc_info()[0]))
		if self.udpserviceon:
			self.logmsg("OK","Start listening with ip:%s port:%d"%(ip,incomingport))

#--------------------------------------------------------------------

	def restartUDPService(self):
		def dfbstop(ignored):
			self.logmsg("OK","Stopping UDP Service")
			self.controlleron = False
			return self.udpport.stopListening()
		def clbstop(ignored):
			self.udpserviceon = False
			self.logmsg("OK","UDP Service Stopped")
			self.startUDPService()
		if self.udpserviceon:
			d = dfbstop("")
			d.addCallback(clbstop)
		else:
			self.startUDPService()

#--------------------------------------------------------------------
	
	def initssdps(self):
		try:
			self.ssdpson = True
			self.ssdps = SSDPServer(self.settings['INCOMINGPORT'],self)
		except:
			self.ssdpson = False
			self.logmsg("ERR","Cannot init discover service:"+str(sys.exc_info()[0]))
		
		if self.ssdpson:
			self.logmsg("OK","Discover service started")

#--------------------------------------------------------------------

	def getautoip(self,currentip):
		ok = True
		try: 
			ip = getNetworkIp()
		except:
			ok = False
			self.logmsg("ERR","Cannot get network IP")
		if ok:
			self.logmsg("OK","Found network ip interface %s"%ip)
			self.settings['IP'] = ip
			self.app.config.set("Settings","IP",ip)
			self.app.config.write()
			self.ids.ip.text=ip
		return ok

#--------------------------------------------------------------------

	def onmanualip(self,active):
		self.ids.ip.disabled = not active
		if not active:
			self.getautoip(self.settings['IP'])
		self.app.config.set("Settings","MANUALIP",int(active))
		self.app.config.write()
		self.loadconfig()
		


#--------------------------------------------------------------------

	def onportfocus(self,focus,text):
		if not focus:
			self.app.config.set("Settings","INCOMINGPORT",text)
			self.app.config.write()
			self.loadconfig()

#--------------------------------------------------------------------

	def onipfocus(self,focus,text):
		if not focus:
			self.app.config.set("Settings","IP",text)
			self.app.config.write()
			self.loadconfig()

#--------------------------------------------------------------------

	def setAxis(self,sliderid,value):
		if self.vjoyon:
			self.vjoy.setAxis(sliderid,int(value))

#--------------------------------------------------------------------

	def logmsg(self,level,msg):
		if level =="OK":
			header = '[color=00ff00][OK][/color]'
		elif level == "ERR":
			header = '[color=ff0000][ERR][/color]'
		elif level == "WARN":
			header = '[color=888800][WARN][/color]'
		self.ids.loglabel.text += header+':[color=000000]'+msg.decode('utf-8')+'[/color]\n'
		self.ids.scroll.scroll_y=0

#--------------------------------------------------------------------

	def loadconfig(self):
		ip = self.settings['IP'] = self.app.config.get("Settings","IP")
		incomingport =  self.settings['INCOMINGPORT'] = self.app.config.getint("Settings","INCOMINGPORT")
		self.settings['MANUALIP'] = self.app.config.getint("Settings","MANUALIP")
		self.ids.manualip.active = bool(self.settings['MANUALIP'])
		self.ids.ip.text = ip 
		self.ids.ip.disabled = not bool(self.settings['MANUALIP'])
		self.ids.incomingport.text = str(incomingport)
#--------------------------------------------------------------------

	def restartServices(self):
		self.logmsg("OK","Restarting services...")
		if self.ssdpson:
			incomingport =  self.settings['INCOMINGPORT']
			self.ssdps.setmsg(incomingport)
		self.restartUDPService()




'''
	 class FlightSimRCServer
'''
class FlightSimRCServer(App): #our app
	use_kivy_settings = False

#--------------------------------------------------------------------
	
	def build(self):
		self.ui = MainUI(app=self)# create the UI
		self.ui.loadconfig()
		self.ui.init5()
		return self.ui #show it

#--------------------------------------------------------------------
	def build_config(self,config):
		config.setdefaults('Settings',{
			'IP':'127.0.0.1',
			'INCOMINGPORT':7707,
			'MANUALIP':0
		})


if __name__ == '__main__':
	FlightSimRCServer().run() #start our app