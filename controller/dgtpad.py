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
   class DgtPadPanel
'''
class DgtPadPanel(Widget):
  padpanel_active = False


#--------------------------------------------------------------------
  def enpanel(self):
    def complete(animation,widget):
      self.padpanel_active = True

    glb.root.speedbrake.knob_active = False
    glb.root.throttle.knob_active = False
    glb.root.flaps.knob_active = False
    Animation.cancel_all(self)
    anim = Animation(y=self.parent.height-self.height*1.02,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

#--------------------------------------------------------------------
  def dispanel(self):
    def complete(animation,widget):
      self.padpanel_active = False
      glb.root.speedbrake.knob_active = True
      glb.root.throttle.knob_active = True
      glb.root.flaps.knob_active = True
      
    Animation.cancel_all(self)
    anim = Animation(y=self.parent.height,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)


'''
   class DgtPadCtrl
'''
class DgtPadCtrl(Widget):
  pad_active = False

#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(DgtPadCtrl, self).__init__(**kwargs)

#--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos) and self.pad_active:
      tx,ty = touch.pos
      self.toffsetx = self.center_x - tx
      self.toffsety = self.center_y - ty
      touch.grab(self)
