#!python
from pyrc import pyrc
import re, sys, traceback


def messageHandler(client, sentMsg, receivedMsg):
    if sentMsg:
        sys.stdout.write(" - Me  - -\n{} - - - - -\n".format(sentMsg))
    if receivedMsg:
        sys.stdout.write(" - Srv - -\n{} - - - - -\n".format(receivedMsg))


if __name__ == '__main__':
    server_ip = "irc.root-me.org"
    username = "Pell"
    hostname = "Pell"
    servername = "Pell"
    realname = "Pell"
    nick = "Pell"
    password = None

    client = pyrc.PyrcClient()
    client.connect(messageHandler, server_ip, username, hostname, servername, realname, nick, password)
    try:
        while True:
            input_txt = input("")
            cmd_match = re.search(r"^/(\S+)\s*(.*)$", input_txt)
            if cmd_match:
                cmd = cmd_match.group(1)
                cmd_args = cmd_match.group(2).split(" ")

                if cmd == "join" and len(cmd_args) > 0:
                    client.joinChan(cmd_args[0])
                elif cmd == "quit":
                    client.quitChan()
                elif cmd == "whisp" and len(cmd_args) > 1:
                    client.sendMsg(cmd_args[0], " ".join(cmd_args[1:]))
                elif cmd == "raw" and len(cmd_args) > 0:
                    client.sendLine(" ".join(cmd_args))
                else:
                    print("Unkown command")
            else:
                client.sendMsgToChan(input_txt)
    except:
        traceback.print_exc()

    client.disconnect()
    print("IRC client disconnected")
