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
    glb.root.dgtpadctrl.enpanel()
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
    glb.root.dgtpadctrl.dispanel()
    anim = Animation(y=self.parent.height,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)


'''
   class DgtPadCtrl
'''
class DgtPadCtrl(Widget):
  padactive = False

  btmap = [
        




    #   ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27']

        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #00
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #01
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #02
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #03
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #04
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #05
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #06
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #07
        ['NW','NW','NW','NW','NW','NW','NW','NW','NW','NW','N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'N' ,'NE','NE','NE','NE','NE','NE','NE','NE','NE','NE','NE'], #08
        ['W' ,'W' ,'NW','NW','NW','NW','NW','NW','NW','NW','XX','XX','XX','XX','XX','XX','XX','NE','NE','NE','NE','NE','NE','NE','NE','NE','NE','E' ], #09
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'NW','NW','NW','XX','XX','XX','XX','XX','XX','XX','XX','NE','NE','NE','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #10
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #11
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #12
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #13
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #14
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #15   
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ,'E' ], #16  
        ['W' ,'W' ,'W' ,'W' ,'W' ,'W' ,'SW','SW','SW','XX','XX','XX','XX','XX','XX','XX','XX','XX','XX','SE','SE','SE','SE','E' ,'E' ,'E' ,'E' ,'E' ], #17
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','XX','XX','XX','XX','XX','XX','XX','XX','SE','SE','SE','SE','SE','SE','SE','SE','SE','E' ], #18
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'XX','XX','XX','XX','XX','SE','SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #19   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #20
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S', 'S' ,'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #21   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S' ,'S', 'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #22   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #23   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #24   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #25   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S', 'S', 'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #26   
        ['SW','SW','SW','SW','SW','SW','SW','SW','SW','S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'S' ,'SE','SE','SE','SE','SE','SE','SE','SE','SE','SE'], #27
    #   ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27']
       ]
          
#--------------------------------------------------------------------
  def __init__(self,**kwargs):
    super(DgtPadCtrl, self).__init__(**kwargs)


#--------------------------------------------------------------------
  def enpanel(self):
    def complete(animation,widget):
      self.padactive = True

    Animation.cancel_all(self)
    anim = Animation(center_y=self.parent.parent.height-self.parent.height*1.04/2,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

#--------------------------------------------------------------------
  def dispanel(self):
    def complete(animation,widget):
      self.padactive = False
      
    Animation.cancel_all(self)
    anim = Animation(y=self.parent.height*2,t='out_expo',duration=0.3) 
    anim.bind(on_complete=complete)
    anim.start(self)

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
        self.update()

      maxy = self.parent.center_y+self.parent.height/2-self.height/2
      miny = self.parent.center_y-self.parent.height/2+self.height/2
      if (ofy>=miny) and (ofy<maxy):
        self.center_y = ofy
        self.update()

#--------------------------------------------------------------------
  def on_touch_up(self,touch):
    if (touch.grab_current is self) and self.padactive:
      self.do_center()
      touch.ungrab(self)

#--------------------------------------------------------------------
  def update(self):
    scale=self.parent.width/27
    ygrid = (self.parent.height-(self.center_y-self.parent.y))/scale
    xgrid = self.center_x/scale
    print "x:%d,y:%d"%(xgrid,ygrid)
    print self.btmap[int(ygrid)][int(xgrid)]




  def do_center(self):
    self.center_y = self.parent.center_y
    self.center_x = self.parent.center_x