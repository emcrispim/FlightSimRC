#!/usr/bin/python

import sys, getopt
from comm import CommService
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import uinput


events = (uinput.BTN_JOYSTICK, 
	      uinput.ABS_X + (0, 100, 0, 0), 
	      uinput.ABS_Y + (0, 100, 0, 0),
	      uinput.ABS_Z + (0, 100, 0, 0),
	      uinput.ABS_RX + (0, 100, 0, 0),
	      uinput.ABS_RY + (0, 100, 0, 0),
	      uinput.ABS_RZ + (0, 100, 0, 0),
	      uinput.ABS_BRAKE + (0, 100, 0, 0),
	      uinput.ABS_TILT_X + (0, 100, 0, 0),
	      uinput.ABS_TILT_Y + (0, 100, 0, 0)
	      )
device = uinput.Device(events)

DEBUG = True
INCOMINGPORT =7707


class s(CommService):
	def log(self,level,msg):
		print level+":"+msg
		if level=='ERROR':
			sys.exit(2)

	def setAxis(self,key,value):
		if key=='X':
			device.emit(uinput.ABS_X, int(value))
		if key=='Y':
			device.emit(uinput.ABS_Y, 100-int(value))
		if key=='Z':
			device.emit(uinput.ABS_Z, int(value))
		if key=='Rx':
			device.emit(uinput.ABS_RX, int(value))
		if key=='Ry':
			device.emit(uinput.ABS_RY, int(value))
		if key=='Rz':
			device.emit(uinput.ABS_RZ, int(value))
		if key=='sl0':
			device.emit(uinput.ABS_BRAKE, int(value))
		if key=='X1':
			device.emit(uinput.ABS_TILT_X, int(value))
		if key=='Y1':
			device.emit(uinput.ABS_TILT_Y, int(value))

		print "AXIS:"+key+":"+value

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