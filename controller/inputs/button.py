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
  def enpanel(self):
    def complete(animation,widget):
      glb.root.rudder.rudder_active = False
      self.panel_active = True

    print "open buttons panel"
    glb.root.ids.btn1_toggle.text = glb.app.getSettingAsString('btn1_text')[0:10]
    glb.root.ids.btn2_toggle.text = glb.app.getSettingAsString('btn2_text')[0:10]
    glb.root.ids.btn3_toggle.text = glb.app.getSettingAsString('btn3_text')[0:10]
    glb.root.ids.btn4_toggle.text = glb.app.getSettingAsString('btn4_text')[0:10]
    Animation.cancel_all(self)
    anim = Animation(y=0,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

#--------------------------------------------------------------------
  def dispanel(self):
    def complete(animation,widget):
      glb.root.rudder.rudder_active = True
      self.panel_active = False
      
    Animation.cancel_all(self)
    anim = Animation(y=-self.height,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)