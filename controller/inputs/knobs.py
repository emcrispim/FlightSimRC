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
   class BrakesKnob
'''
class BrakesKnob(Widget):

  toffsety = None

  ymax = 0.90
  ymin = 0.10

#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(BrakesKnob, self).__init__(**kwargs)

#--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos):
      tx,ty = touch.pos
      self.toffsety = self.center_y - ty
      touch.grab(self)

#--------------------------------------------------------------------
  def on_touch_move(self,touch):
    if touch.grab_current is self:
      yref = self.parent.height
      tx,ty=touch.pos
      ofy = ty + self.toffsety
      if (ofy>=yref*self.ymin) and (ofy<=yref*self.ymax):
        self.center_y=ofy
        self.update()
      elif (ofy < yref*self.ymin):
        self.center_y=yref*self.ymin
        self.update()

#--------------------------------------------------------------------
  def on_touch_up(self, touch):
    if touch.grab_current is self:
      if glb.app.getSetting('brakesautodisable'):
        self.do_disable()
        self.update()
      touch.ungrab(self)

#--------------------------------------------------------------------
  def update(self):
    yref = self.parent.height
    ymax = yref*self.ymax*0.885
    yoffset = yref*self.ymin
    y = (self.center_y-yoffset)/ymax
    glb.root.setmsg('sl0',int(y*100))  

#--------------------------------------------------------------------
  def do_disable(self):
    yref = self.parent.height
    self.center_y = yref*self.ymax
    self.update()


'''
   class RudderKnob
'''
class RudderKnob(Widget):

  toffsetx = None
  xmax = 0.925
  xmin = 0.07
  enabled = True

#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(RudderKnob, self).__init__(**kwargs)

#--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if (self.collide_point(*touch.pos) and self.enabled):
      tx,ty = touch.pos
      self.toffsetx = self.center_x - tx
      touch.grab(self)

#--------------------------------------------------------------------
  def on_touch_move(self,touch):
    if touch.grab_current is self :
      xref = self.parent.width
      tx,ty=touch.pos
      ofx = tx + self.toffsetx
      if (ofx>=xref*self.xmin) and (ofx<=xref*self.xmax):
        self.center_x=ofx
        self.update()

#--------------------------------------------------------------------
  def on_touch_up(self, touch):
    if touch.grab_current is self :
      if glb.app.getSetting('rudderautocenter'):
        self.docenter()
        self.update()
      elif abs(self.center_x-self.parent.width*0.5)<23:
        self.docenter()
        self.update()
      touch.ungrab(self)

#--------------------------------------------------------------------
  def update(self):
    xref = self.parent.width
    xmin = self.xmin*xref
    xrange = xref * (self.xmax-self.xmin)
    y = ((self.center_x-xmin)/xrange)*100
    glb.root.setmsg('Z',int(y))

#--------------------------------------------------------------------
  def docenter(self):
    self.center_x=self.parent.width*0.5

#--------------------------------------------------------------------
  def disable(self):
    self.enabled = False

#--------------------------------------------------------------------
  def enable(self):
    self.enabled = True