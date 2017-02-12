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
   class RudderTrim
'''
class RudderTrim(Widget):

  ruddertrim_active = False
  ofx = None
  xtrans = NumericProperty(0)

  #--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(RudderTrim, self).__init__(**kwargs)

  #--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos) and self.ruddertrim_active:
      tx,ty = touch.pos
      self.ofx = tx
      touch.grab(self)

  #-------------------------------------------------------------------- 
  def on_touch_move(self,touch):
    if touch.grab_current is self:
      tx,ty = touch.pos
      delta = self.ofx-tx
      st = -0.9*glb.app.getSetting('ruddertrims') + 100
      if 0 < glb.app.ruddertrim_value-delta/st <100:
        self.xtrans+=(delta/self.width)
        glb.app.ruddertrim_value-=delta/st
        glb.root.setmsg('X1',int(glb.app.ruddertrim_value))
      self.ofx = tx


  #--------------------------------------------------------------------
  def on_touch_up(self,touch):
    if touch.grab_current is self:
      touch.ungrab(self)

  #--------------------------------------------------------------------
  def enpanel(self):
    print self.pos
    def complete(animation,widget):
      print "anim complete"
      print "set panel enable"
      print "set rudder disabled"
      glb.root.rudder.rudder_active = False
      self.ruddertrim_active = True


    Animation.cancel_all(self)
    anim = Animation(y=0,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

  #--------------------------------------------------------------------
  def dispanel(self):
    def complete(animation,widget):
      glb.root.rudder.rudder_active = True
      self.ruddertrim_active = False
      
    Animation.cancel_all(self)
    anim = Animation(y=-self.height,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)


'''
   class ElevatorTrim
'''
class ElevatorTrim(Widget):

  ofy = None
  ytrans = NumericProperty(0)

#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(ElevatorTrim, self).__init__(**kwargs)


#--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos):
      tx,ty = touch.pos
      self.ofy = ty
      touch.grab(self)

#-------------------------------------------------------------------- 
  def on_touch_move(self,touch):
    if touch.grab_current is self:
      tx,ty = touch.pos
      delta = self.ofy-ty
      st = -0.9*glb.app.getSetting('elevatortrims') + 100
      if 0 < glb.app.elevatortrim_value-delta/st <100:
        self.ytrans+= (delta/self.height) 
        glb.app.elevatortrim_value-=delta/st
        glb.root.setmsg('Y1',int(glb.app.elevatortrim_value))
      self.ofy = ty

#--------------------------------------------------------------------
  def on_touch_up(self,touch):
    if touch.grab_current is self:
      touch.ungrab(self)