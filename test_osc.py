import OSC
from OSCSender import OSCSender
from OSCReceiver import OSCReceiver

import time
def main():
	print "starting this"
	sender = OSCSender(port = 12345)
	for i in range(300):
		sender.defineMessage("/value", i)
		sender.sendMessages()

	receiver = OSCReceiver(time.time(), port = 12346)
	receiver.start()
	
	quit = False
	try:
		while not quit:
			receiver.currentElement
			time.sleep(1.0/30)
		#End program
		receiver.close()
		receiver.join()
	except (KeyboardInterrupt):
		receiver.close()
		receiver.join()
		sender.oscclient.close()

if __name__ == '__main__':
	main()