
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
from inputs.pad import PadCtrl,AcclPopup
from inputs.dgtpad import DgtPadPanel,DgtPadCtrl
from inputs.trim import RudderTrim,ElevatorTrim
from inputs.button import LButtonsPanel,RButtonsPanel
from inputs.knobs import BrakesKnob,RudderKnob
from inputs.knobs3d import Knobs3D,Knobs3DCtrl
from Settings import *
import comm


Config.set('kivy', 'log_level', 'debug')
Config.write()  

#for PC only
#Window.size = (960, 540)
#Window.size = (1280, 720)

	
Builder.load_file('ui/settings.kv')
Builder.load_file('ui/dgtpad.kv')
Builder.load_file('ui/custom.kv')

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
	lbuttonspanel 		= ObjectProperty(None)
	rbuttonspanel 		= ObjectProperty(None)
	dgtpadpanel 		= ObjectProperty(None)
	DgtPadCtrl        	= ObjectProperty(None)
	init5on = False
	commctrl = comm.ctrl()
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
			self.commctrl.init(glb.app.getSetting('manualip'),glb.app.getSettingAsString('ip'),glb.app.getSetting('port'))
			Clock.schedule_interval(self.loop,1/20.0)



#--------------------------------------------------------------------
	def setmsg(self,key,value):
		self.lights.act = 1
		self.lights_act_timer = 5
		self.commctrl.queue(key,value)

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

		self.commctrl.process()
		self.padctrl.process()
		
#--------------------------------------------------------------------
	def on_ruddertrimBT(self,state):
		if state == "down":
			self.ruddertrim.enpanel()
			self.rudder.disable()
			self.lbuttonspanel.dispanel()
			self.rbuttonspanel.dispanel()
		else:
			self.ruddertrim.dispanel()
			self.rudder.enable()

#--------------------------------------------------------------------
	def on_buttonpanelBT(self,state):
		if state == "down":
			self.ruddertrim.dispanel()
			self.lbuttonspanel.enpanel()
			self.rbuttonspanel.enpanel()
		else:
			self.lbuttonspanel.dispanel()
			self.rbuttonspanel.dispanel()

#--------------------------------------------------------------------

	def on_dgtpadBT(self,state):
		if state == "down":
			self.dgtpadpanel.enpanel()
		else:
			self.dgtpadpanel.dispanel()

#--------------------------------------------------------------------

	def on_btpress(self,bt):
		statemap={"down":1,"normal":0}
	
		self.setmsg('B'+bt[3:4],statemap[self.ids[bt].state])
	
		def untoggle(dt):
			self.ids[bt]._do_press()
			self.setmsg('B'+bt[3:4],0)

		Logger.debug("MAIN: button:"+bt+" state:"+self.ids[bt].state)
		if not(glb.app.getSetting(bt)):
			Clock.schedule_once(untoggle, 0.2)
			
#--------------------------------------------------------------------
	def on_accelerometer(self,state):
		if state =="down":
			AcclPopup().open()
		else:
			self.padctrl.PadMode()
			# print "up"

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
			'acclelevators':50,
			'acclailerons':50,
			'btn1_text':'btn1',
			'btn2_text':'btn2',
			'btn3_text':'btn3',
			'btn4_text':'btn4',
			'btn5_text':'btn5',
			'btn6_text':'btn6',
			'btn7_text':'btn7',
			'btn8_text':'btn8',
			'btn1_toggle':1,
			'btn2_toggle':1,
			'btn3_toggle':1,
			'btn4_toggle':1,
			'btn5_toggle':1,
			'btn6_toggle':1,
			'btn7_toggle':1,
			'btn8_toggle':1
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

