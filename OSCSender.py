import OSC

class OSCSender():
    def __init__(self, host="localhost", port = 12346):
        print "Sending OSC messages to {}:{}".format(host, port)

        self.oscclient = OSC.OSCClient()
        self.connection = (host, port)
        self.oscclient.connect(self.connection)
        self.messages = []
        self.currentElement = ""
        self.currentFeature = ""

    def defineMessage(self, address, value):
        message = OSC.OSCMessage(address)
        message.append(value)
        self.messages.append(message)

    def sendMessages(self):
        bundle = OSC.OSCBundle()
        for m in self.messages:
            bundle.append(m)
        try:            
            self.oscclient.send(bundle)
        except OSC.OSCClientError:
            print "Error sending to {}:{}, maybe closed port?".format(self.oscclient.address()[0], self.oscclient.address()[1])
        self.messages = []

    def close(self):
        self.sending = False