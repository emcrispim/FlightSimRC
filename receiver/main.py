
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
from comm import CommService


Config.set('kivy', 'log_level', 'debug')
Config.write() 


'''
	 class UCommService
'''
class UCommService(CommService):

	def __init__(self,ui):
		self.ui = ui


	def log(self,level,message):
		self.ui.logmsg(level,message)

	def ctrl_status(self,value):
		self.ui.controlleron = value

	def setAxis(self,key,value):
		self.ui.ids[key].value = int(value)

	def start_success(self):
		self.ui.commserviceson = True

Window.size = (960, 540)


'''
	 class MainUI
'''
class MainUI(BoxLayout):#the app ui

	app            = ObjectProperty(None)
	vjoyon 		   = BooleanProperty(True)
	commserviceson = BooleanProperty(True)
	controlleron   = BooleanProperty(True) 


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
		self.vjoyon = False
		self.commserviceson = False
		self.commservice = UCommService(self)
		incomingport = self.app.config.getint("Settings","INCOMINGPORT")
		self.ids.incomingport.text = str(incomingport)
		self.commservice.start(incomingport)
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

	def onportfocus(self,focus,text):
		if not focus:
			print "not focus"
			self.setconfig()

#--------------------------------------------------------------------
	def setconfig(self):
		value = self.ids.incomingport.text
		self.app.config.set("Settings","INCOMINGPORT",value)
		self.app.config.write()


#--------------------------------------------------------------------

	def setAxis(self,sliderid,value):
		if self.vjoyon:
			self.vjoy.setAxis(sliderid,int(value))

#--------------------------------------------------------------------

	def logmsg(self,level,msg):
		if level =="OK" or level == "INFO":
			header = '[color=00ff00][OK][/color]'
		elif level == "ERR" or level == "ERROR":
			header = '[color=ff0000][ERR][/color]'
		elif level == "WARN":
			header = '[color=888800][WARN][/color]'
		if level !="DEBUG":
			self.ids.loglabel.text += header+':[color=000000]'+msg.decode('utf-8')+'[/color]\n'
			self.ids.scroll.scroll_y=0

#--------------------------------------------------------------------

	def restartServices(self):
		self.commserviceson = False
		self.logmsg("OK","Restarting services...")
		self.setconfig()
		self.commservice.restart(self.app.config.getint("Settings","INCOMINGPORT"))
	




'''
	 class FlightSimRCServer
'''
class FlightSimRCServer(App): #our app
	use_kivy_settings = False

#--------------------------------------------------------------------
	
	def build(self):
		self.ui = MainUI(app=self)# create the UI
		self.ui.init5()
		return self.ui #show it

#--------------------------------------------------------------------
	def build_config(self,config):
		config.setdefaults('Settings',{
			'INCOMINGPORT':7707
		})


if __name__ == '__main__':
	FlightSimRCServer().run() #start our app