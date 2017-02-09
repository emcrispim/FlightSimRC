#!/usr/bin/python

import sys, getopt
from comm import CommService
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

DEBUG = True
INCOMINGPORT =7707


class s(CommService):
	def log(self,level,msg):
		print level+":"+msg
		if level=='ERROR':
			sys.exit(2)

	def setAxis(self,key,value):
		print "AXIs:"+key+":"+value

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