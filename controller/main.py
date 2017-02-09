
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

import glb


# Kivy libraries
from kivy.config import Config
from kivy.logger import Logger 
from kivy.app import App 
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  ObjectProperty,NumericProperty
from kivy.config import Config
from kivy.clock import Clock



# App libraries
from Controllers import *
from knobs3d import Knobs3D
from Settings import *
import comm


Config.set('kivy', 'log_level', 'debug')
Config.write()  

#for PC only
Window.size = (960, 540)
#Config.set('graphics', 'width', '200')
#Config.set('graphics', 'height', '200')

	
Builder.load_file('Settings.kv')

'''
	 class MainUI
'''
class MainUI(BoxLayout):#the app ui

	app            		= ObjectProperty(None)
	rudder         		= ObjectProperty(None)
	padctrl		   		= ObjectProperty(None)
	elevatortrim   		= ObjectProperty(None)
	ruddertrim     		= ObjectProperty(None)
	brakes				= ObjectProperty(None)
	knobs 				= ObjectProperty(None)
	throttle 			= ObjectProperty(None)
	flaps 				= ObjectProperty(None)
	speedbrake 			= ObjectProperty(None)
	lights				= ObjectProperty(None)
	buttonspanel 		= ObjectProperty(None)
	dgtpad 				= ObjectProperty(None)
	init5on = False
	glb.comm = commctrl = comm.ctrl()
	send = {}
	lights_act_timer = 0
	lights_ack_timer = 0
	settings = Settings()

#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(MainUI, self).__init__(**kwargs)

#--------------------------------------------------------------------
	def init5(self):
		if not self.init5on:
			self.rudder.docenter()
			self.brakes.do_disable()
			self.init5on = True
			self.knobs.init()
			self.throttle.init('throttle')
			self.flaps.init('flaps')
			self.speedbrake.init('speedbrake')

			p = comm.SSDP()
			p.open()
			Clock.schedule_interval(self.loop,1/20.0)

#--------------------------------------------------------------------
	def startcom(self,ip,port):
		Logger.debug("Start com")
		self.commctrl.start(ip,port)

#--------------------------------------------------------------------
	
	def setmsg(self,key,value):
		self.lights.act = 1
		self.lights_act_timer = 5
		self.send[key]=str(value)
		#print "%s,%s" %(key,str(value))

#--------------------------------------------------------------------

	def loop(self, dt):
		if self.lights_act_timer >1:
			self.lights_act_timer-=1
		elif self.lights_act_timer == 1:
			self.lights_act_timer = 0
			self.lights.act = 0

		if self.lights_ack_timer > 1:
			self.lights_ack_timer -=1
		elif self.lights_ack_timer == 1:
			self.lights_ack_timer = 0
			self.lights.ack = 0

		if self.commctrl.started:
			if len(self.send):
				for key, value in self.send.iteritems():
					msg=key+':'+value+'\n'
					self.commctrl.send(msg)
				self.send={}

#--------------------------------------------------------------------
	def on_ruddertrimBT(self,state):
		if state == "down":
			self.ruddertrim.enpanel()
			self.buttonspanel.dispanel()
		else:
			self.ruddertrim.dispanel()

#--------------------------------------------------------------------
	def on_buttonpanelBT(self,state):
		if state == "down":
			self.ruddertrim.dispanel()
			self.buttonspanel.enpanel()
		else:
			self.buttonspanel.dispanel()

#--------------------------------------------------------------------

	def on_dgtpadBT(self,state):
		if state == "down":
			self.dgtpad.enpanel()
		else:
			self.dgtpad.dispanel()

#--------------------------------------------------------------------

	def on_btpress(self,bt):
		def untoggle(dt):
			self.ids[bt]._do_press()
			print "untoggle"

		if not(glb.app.getSetting(bt)):
			Clock.schedule_once(untoggle, 0.2)
			
		

#--------------------------------------------------------------------

	def openSettings(self):
		self.settings.open()


'''
	 class FlightSimRC
'''
class FlightSimRC(App): #our app
	use_kivy_settings = False
	texture_ruddertrim_wheel 	= ObjectProperty(None)
	texture_elevatortrim_wheel 	= ObjectProperty(None)
	elevatortrim_value 			= NumericProperty(50)
	ruddertrim_value 			= NumericProperty(50)
	rudder 						= NumericProperty(50)

#--------------------------------------------------------------------
	def build(self):

		Window.bind(on_draw=self.ondraw) 
		self.ui = MainUI()
		glb.root = self.ui
		glb.app = self
		self.texture_ruddertrim_wheel =  CoreImage.load('img/ruddertrimwheel.png').texture
		self.texture_ruddertrim_wheel.wrap = 'repeat'
		self.texture_elevatortrim_wheel = CoreImage.load('img/elevatortrimwheel.png').texture
		self.texture_elevatortrim_wheel.wrap = 'repeat'
		return self.ui #show it


#--------------------------------------------------------------------
	def setSettingsAsString(self,setting,value):
		return self.config.set("Settings",setting,value)

#--------------------------------------------------------------------
	def getSettingAsString(self,setting):
		return self.config.get("Settings",setting)

#--------------------------------------------------------------------
	def getSetting(self,setting):
		return self.config.getint("Settings",setting)

#--------------------------------------------------------------------
	def setSetting(self,setting,value):
		return self.config.set("Settings",setting,int(value))

#--------------------------------------------------------------------
	def build_config(self,config):
		config.setdefaults('Settings',{
			'manualip':0,
			'ip':'0.0.0.0',
			'port':0,
			'rudderautocenter':1,
			'smoothrudder':1,
			'padautocenter':1,
			'brakesautodisable':1,
			'ruddertrims':50,
			'elevatortrims':50,
			'btn1_text':'btn1',
			'btn2_text':'btn2',
			'btn3_text':'btn3',
			'btn4_text':'btn4',
			'btn1_toggle':1,
			'btn2_toggle':1,
			'btn3_toggle':1,
			'btn4_toggle':1
			})

#--------------------------------------------------------------------
	def ondraw(self,arg1):
		self.ui.init5()


#--------------------------------------------------------------------
	def open_settings(self, *largs):
		pass


#--------------------------------------------------------------------
	def on_pause(self):
		Logger.debug("FGcontroller entered in pause")
		return True

#--------------------------------------------------------------------
	def on_resume(self):
		Logger.debug("FGcontroller resumed")

		# Here you can check if any data needs replacing (usually nothing)
		pass

if __name__ == '__main__':
	FlightSimRC().run()
