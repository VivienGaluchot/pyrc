#!python
from pyrc import pyrc
from threading import Thread
import time, re
import traceback


class InputHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        try:
            while True:
                input_txt = input("")
                cmd_match = re.search(r"^/(\S+)\s*(.*)$", input_txt)
                if cmd_match:
                    cmd = cmd_match.group(1)
                    cmd_args = cmd_match.group(2).split(" ")

                    if cmd == "join" and len(cmd_args) > 0:
                        self.client.joinChan(cmd_args[0])
                    elif cmd == "quit":
                        self.client.quitChan()
                    if cmd == "whisp" and len(cmd_args) > 2:
                        self.client.sendMsg(cmd_args[0], cmd_args[1:].join(" "))
                else:
                    self.client.sendMsgToChan(input_txt)
        except:
            traceback.print_exc()
        print ("Quit InputHandler")


if __name__ == '__main__':
    username = "Pell"
    hostname = "Pell"
    servername = "Pell"
    realname = "Pell"
    nick = "Pell"
    password = None

    client = pyrc.PyrcClient()
    client.connect("irc.root-me.org", username, hostname, servername, realname, nick, password)

    # client.joinChan("#root-me_challenge")
    try:
        inputHandler = InputHandler(client)
        inputHandler.start()
        inputHandler.join()
    except:
        traceback.print_exc()

    client.disconnect()
    print("IRC client disconnected")
