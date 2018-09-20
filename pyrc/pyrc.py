#!python3
import socket, time, select, sys
from multiprocessing import Process, Queue
from pyrc import internal

class PyrcClient:
    def __init__(self):
        # Socket
        self.connected = False
        # Process
        self.stop_queue = Queue()
        self.send_msg_queue = Queue()
        self.process = None

    def connect(self, server_ip, username, hostname, servername, realname, nick, password):
        assert(not self.connected)
        self.process = Process(target=internal.PyrcSocketHandler, args=(self.stop_queue, self.send_msg_queue, server_ip))
        self.process.start()
        self.connected = True
        time.sleep(1)
        if password:
            self.sendRaw("PASS {}\n".format(password))
        self.sendRaw("NICK {}\n".format(nick))
        self.sendRaw("USER {} {} {} :{}\n".format(username, hostname, servername, realname))

    def disconnect(self):
        assert(self.connected)
        self.stop_queue.put(True)
        self.process.join(1)
        if self.process.exitcode != None:
            print("kill with signal", self.process.exitcode)
        else:
            self.process.terminate()
        self.process = None
        self.connected = False

    def sendRaw(self, msg):
        assert(self.connected)
        self.send_msg_queue.put(msg)

    def ping(self, ):
        self.sendRaw("PONG :pingis\n")

    def sendMsg(self, dest, msg):
        self.sendRaw("PRIVMSG "+ dest +" :"+ msg +"\n")

    def joinChan(self, chan):
        self.sendRaw("JOIN "+ chan +"\n")

    def quitChan(self, chan):
        self.sendRaw("PART " + channel + "\r\n")
