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
from kivy.uix.popup import Popup
from kivy.properties import  ObjectProperty


'''
   class Settings
'''
class Settings(Popup):

	#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(Settings, self).__init__(**kwargs)

	#--------------------------------------------------------------------
	def on_open(self):
		self.ids.elevatortrims.value = glb.app.getSetting('elevatortrims')
		self.ids.ruddertrims.value = glb.app.getSetting('ruddertrims')
		self.ids.rudderautocenter.active = glb.app.getSetting('rudderautocenter')
		self.ids.brakesautodisable.active = glb.app.getSetting('brakesautodisable')
		self.ids.padautocenter.active = glb.app.getSetting('padautocenter')
		self.ids.btn1_text.text = glb.app.getSettingAsString('btn1_text')
		self.ids.btn2_text.text = glb.app.getSettingAsString('btn2_text')
		self.ids.btn2_text.text = glb.app.getSettingAsString('btn2_text')
		self.ids.btn3_text.text = glb.app.getSettingAsString('btn3_text')
		self.ids.btn4_text.text = glb.app.getSettingAsString('btn4_text')
		self.ids.btn1_toggle.active = glb.app.getSetting('btn1_toggle')
		self.ids.btn2_toggle.active = glb.app.getSetting('btn2_toggle')
		self.ids.btn3_toggle.active = glb.app.getSetting('btn3_toggle')
		self.ids.btn4_toggle.active = glb.app.getSetting('btn4_toggle')

	#--------------------------------------------------------------------
	def save(self):
		glb.app.setSetting('elevatortrims',self.ids.elevatortrims.value)
		glb.app.setSetting('ruddertrims',self.ids.ruddertrims.value)
		glb.app.setSetting('rudderautocenter',int(self.ids.rudderautocenter.active))
		glb.app.setSetting('brakesautodisable',int(self.ids.brakesautodisable.active))
		glb.app.setSetting('padautocenter',int(self.ids.padautocenter.active))
		glb.app.setSettingsAsString('btn1_text',self.ids.btn1_text.text)
		glb.app.setSettingsAsString('btn2_text',self.ids.btn2_text.text)
		glb.app.setSettingsAsString('btn3_text',self.ids.btn3_text.text)
		glb.app.setSettingsAsString('btn4_text',self.ids.btn4_text.text)
		glb.app.setSetting('btn1_toggle',int(self.ids.btn1_toggle.active))
		glb.app.setSetting('btn2_toggle',int(self.ids.btn2_toggle.active))
		glb.app.setSetting('btn3_toggle',int(self.ids.btn3_toggle.active))
		glb.app.setSetting('btn4_toggle',int(self.ids.btn4_toggle.active))
		glb.app.config.write()
		self.dismiss()
