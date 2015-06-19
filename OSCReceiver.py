import OSC
from threading import Thread

class OSCReceiver(OSC.OSCServer, Thread):
	def __init__(self, basetime, host="localhost", port=12345):
		self.connection = (host, port)

		OSC.OSCServer.__init__(self, self.connection)
		Thread.__init__(self)

		self.addMsgHandler('default', self.msgReceive)
		self.basetime = basetime
		self.messages = {} # address: value

		#GUI values
		self.currentElement = ""
		self.currentFeature = "POSITION"
		self.currentFilter = 2
		self.log = 1

	def msgReceive(self, addr, tags, data, sender):
		#mocap Element
		if "mocapElement" in addr:
			self.messages[addr] = data
		elif addr == "/GUI/currentElement":
			self.currentElement = "/mocapElement/" + data[0]
		elif addr == "/GUI/currentFeature":
			self.currentFeature = data[0]
		elif addr == "/GUI/filter":
			self.currentFilter = data[0]
		elif addr == "/GUI/log":
			self.log = data[0]
		elif addr == "/value":
			print data[0]

	def run(self):
		c = self.connection
		print "Receiving OSC messages in {}:{}\n".format(c[0], c[1])
		self.serve_forever()

	def close(self):
		OSC.OSCServer.close(self)
