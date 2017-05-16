#!/usr/bin/python

import sys, getopt
from comm import CommService
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import uinput


events = (uinput.BTN_JOYSTICK,
		  uinput.BTN_A,
		  uinput.BTN_B,
		  uinput.BTN_C,
		  uinput.BTN_EAST,
		  uinput.BTN_X,
		  uinput.BTN_Y,
		  uinput.BTN_Z,
		  uinput.BTN_START,
		  # uinput.ABS_HAT0X + (0, 100, 0, 0),
		  # uinput.ABS_HAT0Y + (0, 100, 0, 0),
	      uinput.ABS_X + (0, 100, 0, 0), 
	      uinput.ABS_Y + (0, 100, 0, 0),
	      uinput.ABS_Z + (0, 100, 0, 0),
	      uinput.ABS_RX + (0, 100, 0, 0),
	      uinput.ABS_RY + (0, 100, 0, 0),
	      uinput.ABS_RZ + (0, 100, 0, 0),
	      uinput.ABS_BRAKE + (0, 100, 0, 0),
	      # uinput.ABS_TILT_X + (0, 100, 0, 0),
	      # uinput.ABS_TILT_Y + (0, 100, 0, 0),
	      )


events2 = (  uinput.ABS_X + (0, 100, 0, 0), 
	      	 uinput.ABS_Y + (0, 100, 0, 0),
	      	 uinput.ABS_HAT0X + (0, 100, 0, 0),
		     uinput.ABS_HAT0Y + (0, 100, 0, 0)
		  )

DEBUG = True
INCOMINGPORT =7707

try:
	device = uinput.Device(events,name="FlightSimRC_main")
	device2 = uinput.Device(events2,name="FlightSimRC_aux")
except Exception as e:
	print """\nERROR: This aplication requires the uinput module loaded and access to uinput device.
Run application with root privileges or give read/write permissions to /dev/uinput to the current user.

Usage Example: sudo modprobe uinput
               sudo ./mainnogui.py -p <port>\n"""
	exit(0)


class s(CommService):
	def log(self,level,msg):
		print level+":"+msg
		if level=='ERROR':
			sys.exit(2)
	def invert(self,value):
		return 100-int(value)

	def setAxis(self,key,value):
		if key=='X':
			device.emit(uinput.ABS_X, int(value))
		if key=='Y':
			device.emit(uinput.ABS_Y, 100-int(value))
		if key=='Z':
			device.emit(uinput.ABS_Z, int(value))
		if key=='Rx':
			device.emit(uinput.ABS_RX, value)
		if key=='Ry':
			value = self.invert(value)
			device.emit(uinput.ABS_RY, value)
		if key=='Rz':
			value = self.invert(value)
			device.emit(uinput.ABS_RZ, value)
		if key=='sl0':
			value = self.invert(value)
			device.emit(uinput.ABS_BRAKE,value)
		if key=='X1':
			device2.emit(uinput.ABS_X, int(value))
		if key=='Y1':
			device2.emit(uinput.ABS_Y, int(value))
		if key=='B1':
			device.emit(uinput.BTN_JOYSTICK, int(value))
		if key=='B2':
			device.emit(uinput.BTN_A, int(value))
		if key=='B3':
			device.emit(uinput.BTN_B, int(value))
		if key=='B4':
			device.emit(uinput.BTN_C, int(value))
		if key=='B5':
			device.emit(uinput.BTN_X, int(value))
		if key=='B6':
			device.emit(uinput.BTN_Y, int(value))
		if key=='B7':
			device.emit(uinput.BTN_Z, int(value))
		if key=='B8':
			device.emit(uinput.BTN_START, int(value))
		if key=='DPX':
			device2.emit(uinput.ABS_HAT0X, int(value))
		if key=='DPY':
			device2.emit(uinput.ABS_HAT0Y, int(value))


		print "AXIS:"+key+":"+str(value)

def usage():
	print 'mainnogui.py -p <port>'


def startservice(port):
	

	u = s()
	u.start(int(port))
	reactor.run()

def main(argv):
	inport = None
	try:
		opts, args = getopt.getopt(argv,"hp",["port="])
	except:
		usage()
		sys.exit(2)
	if opts:
		opt = opts[0][0]
		if opt == '-h':
			usage()
			sys.exit()
		elif opt =='-p':
			startservice(args[0])
	else:
		usage()
	

if __name__ == "__main__":
   main(sys.argv[1:])