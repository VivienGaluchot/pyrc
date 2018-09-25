import time
from multiprocessing import Process, Queue
from pyrc import internal

class PyrcClient:
    def __init__(self):
        # Irc
        self.chan = None
        # Socket
        self.connected = False
        # Process
        self.stop_queue = Queue()
        self.send_msg_queue = Queue()
        self.process = None

    def connect(self, messageHandler, server_ip, username, hostname, servername, realname, nick, password):
        assert(not self.connected)
        self.connected = True
        self.process = Process(target=internal.PyrcSocketHandler, args=(self.stop_queue, self.send_msg_queue, server_ip, messageHandler, self))
        self.process.start()
        time.sleep(1)
        if password:
            self.sendLine("PASS {}".format(password))
        self.sendLine("NICK {}".format(nick))
        self.sendLine("USER {} {} {} :{}".format(username, hostname, servername, realname))

    def disconnect(self):
        assert(self.connected)
        self.stop_queue.put(True)
        self.process.join(1)
        if self.process.exitcode != None:
            print("Pyrc process stopped with signal", self.process.exitcode)
        else:
            self.process.terminate()
        self.process = None
        self.connected = False

    def sendLine(self, msg):
        assert(self.connected)
        self.send_msg_queue.put(msg + "\n")

    def sendMsg(self, dest, msg):
        self.sendLine("PRIVMSG " + dest + " :" + msg)

    def sendMsgToChan(self, msg):
        if self.chan != None:
            self.sendLine("PRIVMSG " + self.chan + " :" + msg)
        else:
            print("No chan joined")

    def joinChan(self, chan):
        self.chan = chan
        self.sendLine("JOIN " + chan)

    def quitChan(self):
        self.sendLine("PART " + self.chan)
        self.chan = None
