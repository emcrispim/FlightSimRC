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

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty
from kivy.graphics.opengl import *
from kivy.graphics import *
from objloader import ObjFile
from kivy.logger import Logger
from kivy.vector import Vector
from kivy.core.image import Image


class Knobs3D(Widget):

	ytrans = NumericProperty(0)
	toffsety = None

#--------------------------------------------------------------------
	def __init__(self, **kwargs):
		super(Knobs3D, self).__init__(**kwargs)
		with self.canvas:
			self.fbo = Fbo(with_depthbuffer = True,compute_normal_mat=True,size = Window.size)
			Rectangle(size=Window.size, texture=self.fbo.texture)
		self.fbo.add_reload_observer(self.test)
		self.fbo.shader.source = resource_find('simple.glsl')
		#self.canvas = RenderContext(compute_normal_mat=True)
		#self.canvas.shader.source = resource_find('simple.glsl')
		self.scene = ObjFile(resource_find("obj/knobs3D.obj"))

	def test(self,fbo):
		print "test"	
#--------------------------------------------------------------------
	def init(self):
		height = self.parent.height
		self.max = height*0.87
		self.min = height*0.20
		with self.fbo:	
			self.cb = Callback(self.setup_gl_context)
			PushMatrix()
			self.setup_scene()
			PopMatrix()
			self.cb = Callback(self.reset_gl_context)
		Clock.schedule_once(self.update_glsl, 0.5)    
		
#--------------------------------------------------------------------
	def setup_gl_context(self, *args):
		glEnable(GL_DEPTH_TEST)
		self.fbo.clear_buffer()
		#glEnable(GL_CULL_FACE)

#--------------------------------------------------------------------
	def reset_gl_context(self, *args):
		glDisable(GL_DEPTH_TEST)
		#glDisable(GL_CULL_FACE)

#--------------------------------------------------------------------
	def update_glsl(self, *largs):
		#asp = glb.root.width/ float (glb.root.height)
		#sp = asp/2
		#trans = asp/2.4
		#proj = Matrix().view_clip(-asp-trans, asp-trans, -asp/2.0, asp/2.0, 1, 100, 1)
		asp = float(Window.width) / Window.height / 2.3
		transx = -asp/1.75
		transy = asp/17.0
		proj = Matrix().view_clip(-asp-transx, asp-transx, -asp/2.0+transy, asp/2.0+transy, 1, 100, 1)
		self.fbo['projection_mat'] = proj

#--------------------------------------------------------------------
	def setup_scene(self):
		def _draw_element(m):
			UpdateNormalMatrix()
			Mesh(
				vertices=m.vertices,
				indices=m.indices,
				fmt=m.vertex_format,
				mode='triangles',
				texture = self.basetexture
			)

		self.basetexture = Image('img/textures3D.png').texture
		self.trans = Translate(0, 0,-1)
		self.scale = Scale(1)

		base = self.scene.objects['Base']
		_draw_element(base)

		PushMatrix()
		self.rot_spdbrk = Rotate(0, 1, 0, 0)
		self.rot_spdbrk.origin = (0,0,-7)
		speedbrake = self.scene.objects['SpeedBrake_SpdBrkLever']
		_draw_element(speedbrake)
		PopMatrix()
		
		PushMatrix()
		self.rot_throttle = Rotate(0, 1, 0, 0)
		self.rot_throttle.origin = (0,0,-20)
		throttle = self.scene.objects['Throttle_LHThrottle']
		_draw_element(throttle)
		PopMatrix()
	

		PushMatrix()
		self.rot_flaps = Rotate(0, 1, 0, 0)
		self.rot_flaps.origin = (0,0,-7)
		flaps = self.scene.objects['Flaps_FlapLever']
		_draw_element(flaps)
		PopMatrix()

		

