from vJoyInterface import *

class VirtualJoystickException(Exception):
    pass

class VJoy(object):

	axis= {'X':{'id':48,'min':0,'max':0,'m':0},
		   'Y':{'id':49,'min':0,'max':0,'m':0},
		   'Z':{'id':50,'min':0,'max':0,'m':0},
		   'Rx':{'id':51,'min':0,'max':0,'m':0},
		   'Ry':{'id':52,'min':0,'max':0,'m':0},
		   'Rz':{'id':53,'min':0,'max':0,'m':0},
		   'sl0':{'id':54,'min':0,'max':0,'m':0},
		   'sl1':{'id':55,'min':0,'max':0,'m':0}		
	}

	
	def __init__(self, vjoyId):
		if not vJoyInterface.vJoyEnabled():
			raise VirtualJoystickException("vJoy doesn't seem to be enabled on this system. Please download and install vJoy from http://vjoystick.sourceforge.net/")
		elif vJoyInterface.GetVJDStatus(vjoyId) != VjdStat.VJD_STAT_FREE:
			raise VirtualJoystickException("vJoy id %d doesn't seem to be available" % (vjoyId,))
		elif not vJoyInterface.AcquireVJD(vjoyId):
			raise VirtualJoystickException("Unable to acquire vjoyId %d" % (vjoyId,))
		else:
			self.vjoyId = vjoyId
			for key, axe in self.axis.iteritems():
				if vJoyInterface.GetVJDAxisExist(self.vjoyId,axe['id']):
					min = ctypes.c_ulong()
					max = ctypes.c_ulong()
					vJoyInterface.GetVJDAxisMin(self.vjoyId,axe['id'], ctypes.byref(min))
					vJoyInterface.GetVJDAxisMax(self.vjoyId,axe['id'], ctypes.byref(max))
					axe['min'] = min.value
					axe['max'] = max.value
					axe['m'] = (max.value-min.value)/100.0

	# normalized value beetween 0-100
	def setAxis(self,id,value):
		if  0 <= value <= 100:
			axe = self.axis[id]
			vJoyInterface.SetAxis(int(axe['m']*value),self.vjoyId,axe['id'])	
	
	def productString(self):
		ps = '%s (%s)' %(vJoyInterface.GetvJoyProductString(self.vjoyId),vJoyInterface.GetvJoySerialNumberString(self.vjoyId))
		return ps