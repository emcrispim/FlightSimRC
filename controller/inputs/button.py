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
from kivy.properties import NumericProperty
from kivy.animation import Animation



'''
   class ButtonsPanel
'''
class ButtonsPanel(Widget):
  panel_active = False

#--------------------------------------------------------------------
  def showanim(self):
    def complete(animation,widget):
      glb.root.rudder.rudder_active = False
      self.panel_active = True
    Animation.cancel_all(self)
    anim = Animation(y=0,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

#--------------------------------------------------------------------
  def hideanim(self,height):
    def complete(animation,widget):
      glb.root.rudder.rudder_active = True
      self.panel_active = False
      
    Animation.cancel_all(self)
    anim = Animation(y=-height,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

#--------------------------------------------------------------------
  def dispanel(self):
    self.hideanim(self.height)


'''
   class LButtonsPanel
'''

class LButtonsPanel(ButtonsPanel):
  def enpanel(self):
    glb.root.ids.btn1_toggle.text = glb.app.getSettingAsString('btn1_text')[0:10]
    glb.root.ids.btn2_toggle.text = glb.app.getSettingAsString('btn2_text')[0:10]
    glb.root.ids.btn3_toggle.text = glb.app.getSettingAsString('btn3_text')[0:10]
    glb.root.ids.btn4_toggle.text = glb.app.getSettingAsString('btn4_text')[0:10]
    self.showanim()
#--------------------------------------------------------------------


'''
   class RButtonsPanel
'''
class RButtonsPanel(ButtonsPanel):
#--------------------------------------------------------------------
  def enpanel(self):
    glb.root.ids.btn5_toggle.text = glb.app.getSettingAsString('btn5_text')[0:10]
    glb.root.ids.btn6_toggle.text = glb.app.getSettingAsString('btn6_text')[0:10]
    glb.root.ids.btn7_toggle.text = glb.app.getSettingAsString('btn7_text')[0:10]
    glb.root.ids.btn8_toggle.text = glb.app.getSettingAsString('btn8_text')[0:10]
    self.showanim()

#--------------------------------------------------------------------
  def dispanel(self):
    self.hideanim(self.height/5)




