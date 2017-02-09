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
   class touchKnob
'''
class touchKnob(Widget):
  toffsety = None
  name = None
  knob_active = True

#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(touchKnob,self).__init__(**kwargs)

#--------------------------------------------------------------------
  def init(self,name):
    self.name = name
    if name == 'throttle':
      self.move_throttle(0)
    elif name == 'flaps':
      self.move_flaps(self.parent.height)
    elif name =='speedbrake':
      self.move_speedbrake(self.parent.height)

#--------------------------------------------------------------------
  def move_throttle(self,ofy):
    max = self.parent.height-self.height/2.0
    min = self.height/2
    if min < ofy < max:
      self.center_y = ofy
    elif ofy <= min:
      self.center_y = min
    elif ofy >= max:
      self.center_y = max
    rot = max/2.0 - self.center_y + self.height/3
    glb.root.knobs.rot_throttle.angle = rot / self.height*2.4
    self.setmsg('Ry',self.center_y,min,max)


#--------------------------------------------------------------------
  def move_speedbrake(self,ofy):
    max = self.parent.height/1.2
    min = self.parent.height/8
    if min < ofy < max:
      self.center_y = ofy
    elif ofy <= min:
      self.center_y = min
    elif ofy >= max:
      self.center_y = max
    rot = max/2.0 - self.center_y + self.height/1.8
    glb.root.knobs.rot_spdbrk.angle = rot / self.height*10
    self.setmsg('Rx',self.center_y,min,max)

#--------------------------------------------------------------------
  def move_flaps(self,ofy):
    max = self.parent.height/1.28
    min = self.parent.height/5
    if min < ofy < max:
      self.center_y = ofy
    elif ofy <= min:
      self.center_y = min
    elif ofy >= max:
      self.center_y = max
    rot = max/2.0 - self.center_y + self.height/1.5
    glb.root.knobs.rot_flaps.angle = rot / self.height*14
    self.setmsg('Rz',self.center_y,min,max)

#--------------------------------------------------------------------
  def setmsg(self,key,value,min,max):
    m = 100/(max-min)
    y = m * (value - min)
    glb.root.setmsg(key,int(y))

#--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos) and self.knob_active:
      tx,ty = touch.pos
      self.toffsety = self.center_y - ty
      touch.grab(self)

#--------------------------------------------------------------------
  def on_touch_move(self,touch):
    if touch.grab_current is self:
      tx,ty = touch.pos
      ofy = ty + self.toffsety
      if self.name == 'throttle':
        self.move_throttle(ofy)
      elif self.name == 'flaps':
        self.move_flaps(ofy)
      elif self.name == 'speedbrake':
        self.move_speedbrake(ofy)

#--------------------------------------------------------------------
  def on_touch_up(self,touch):
    if touch.grab_current is self:
      touch.ungrab(self)

'''
   class RudderKnob
'''
class RudderKnob(Widget):

  toffsetx = None
  xmax = 0.925
  xmin = 0.07
  rudder_active = True

#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(RudderKnob, self).__init__(**kwargs)

#--------------------------------------------------------------------
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos) and self.rudder_active:
      tx,ty = touch.pos
      self.toffsetx = self.center_x - tx
      touch.grab(self)

#--------------------------------------------------------------------
  def on_touch_move(self,touch):
    if touch.grab_current is self:
      xref = self.parent.width
      tx,ty=touch.pos
      ofx = tx + self.toffsetx
      if (ofx>=xref*self.xmin) and (ofx<=xref*self.xmax):
        self.center_x=ofx
        self.update()

#--------------------------------------------------------------------
  def on_touch_up(self, touch):
    if touch.grab_current is self:
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



'''
   class PadCtrl
'''
class PadCtrl(Widget):

  angle = NumericProperty(0)
  padactive=1
  threshold = None
  toffsetx = None
  toffsety = None

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


'''
   class DgtPad
'''
class DgtPad(Widget):
  dgtpad_active = False

#--------------------------------------------------------------------
  def enpanel(self):
    def complete(animation,widget):
      self.dgtpad_active = True

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
      self.dgtpad_active = False
      glb.root.speedbrake.knob_active = True
      glb.root.throttle.knob_active = True
      glb.root.flaps.knob_active = True
      
    Animation.cancel_all(self)
    anim = Animation(y=self.parent.height,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)



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