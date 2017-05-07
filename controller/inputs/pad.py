##########################################################################
# Author:               Eduardo Crispim, emcrispim@gmail.com
# Date:                 July, 2016
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
#########################################################################

import glb

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ObjectProperty
from kivy.uix.popup import Popup
from plyer import accelerometer
from kivy.clock import Clock




'''
	 class PadCtrl
'''
class PadCtrl(Widget):

	angle = NumericProperty(0)
	padactive=1
	threshold = None
	toffsetx = None
	toffsety = None
	accloffsety = None
	alpha = 0.5
	fx = 0
	fy = 0
	fz = 0

#--------------------------------------------------------------------
	def __init__(self,**kwargs):
		super(PadCtrl, self).__init__(**kwargs)

#--------------------------------------------------------------------
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos) and self.padactive:
			tx,ty = touch.pos
			self.toffsetx = self.center_x - tx
			self.toffsety = self.center_y - ty
			touch.grab(self)

#--------------------------------------------------------------------
	def on_touch_move(self,touch):
		if (touch.grab_current is self) and self.padactive:
			tx,ty=touch.pos
			ofx = tx + self.toffsetx
			ofy = ty + self.toffsety
			if (ofx>=self.width/2) and ofx<=(self.parent.width-self.width/2):
				self.center_x = ofx
				self.update_x()

			if (ofy>=self.height/2) and (ofy<self.parent.height-self.height/2):
				self.center_y = ofy
				self.update_y()

#--------------------------------------------------------------------
	def on_touch_up(self,touch):
		if (touch.grab_current is self) and self.padactive:
			self.do_center()
			touch.ungrab(self)

#--------------------------------------------------------------------
	def do_center(self):
		if glb.app.getSetting('padautocenter'):
			self.center=self.parent.width/2,self.parent.height/2
			self.update_x()
			self.update_y()

#--------------------------------------------------------------------
	def setposition(self,x,y):
		self.center=(x,y)

#--------------------------------------------------------------------
	def  AcclMode(self):
		self.padactive=0
		self.showpad = False
		accelerometer.enable()
		self.accloffsety = accelerometer.acceleration[0]

#--------------------------------------------------------------------
	def PadMode(self):
		self.padactive=1
		self.showpad = True

#--------------------------------------------------------------------
	def update_x(self):
		xref = self.parent.width-self.width
		y = (self.center_x-self.width/2.0)/xref * 100
		glb.root.setmsg('X',int(y))

#--------------------------------------------------------------------
	def update_y(self):
		yref = self.parent.height-self.height
		y = (self.center_y-self.height/2.0)/yref * 100
		glb.root.setmsg('Y',int(y))

#--------------------------------------------------------------------
# NOT TESTED
	def process(self):
		if self.padactive==0:
			try:
				x = accelerometer.acceleration[0]-self.accloffsety #read the X value
				y = accelerometer.acceleration[1]  # Y
				z = accelerometer.acceleration[2] # Z
			
				self.fx = x * self.alpha + (self.fx * (1.0 - self.alpha))
				self.fy = y * self.alpha + (self.fy * (1.0 - self.alpha))
				self.fz = z * self.alpha + (self.fz * (1.0 - self.alpha))
			except:
				x = 1
				y = 1
				z = 1

			#Roll & Pitch Equations
			aileron  = atan2(self.fy, self.fz)*57.3
			elevator = atan2(-self.fx, sqrt(self.fy*self.fy + self.fz*self.fz))*57.3
			
			elevator = elevator / 45.0
			aileron = aileron / 60.0
			
			if elevator>1:
				elevator=1
			elif elevator<-1:
				elevator=-1
			if aileron>1:
				aileron=1
			elif aileron<-1:
				aileron=-1

	 		# NOT FINISHED NOT WORKING CHANGE THIS 
-------self.padctrl.FGToControllerCoordinates(aileron,elevator)
			self.padctrl.ControllerToFGCoordinates()



'''
	 class AcclPopup
'''   
class AcclPopup(Popup):
	
	timer = 3
	has_accl = True

#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(AcclPopup, self).__init__(**kwargs)

#--------------------------------------------------------------------
	def on_open(self):
		try:
			accelerometer._get_acceleration()
		 	accelerometer.enable()
		except:
		 	self.has_accl = False

		if self.has_accl:
			Clock.schedule_interval(self.loop,1)
			self.ids.timer_label.text = "Calibrate in %s s" % str(self.timer)
		else:
			self.ids.timer_label.text = "Accelerometer not available"

#--------------------------------------------------------------------
	def loop(self,dt):
		if self.timer>0:
			self.timer-=1
			self.ids.timer_label.text = "Calibrate in %s s" % str(self.timer)
		else:
			Clock.unschedule(self.loop)
			self.dismiss()

#--------------------------------------------------------------------
	def on_dismiss(self):
		if self.has_accl:
			glb.root.padctrl.AcclMode()