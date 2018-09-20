#!python
from pyrc import pyrc
import time

if __name__ == '__main__':
    username = "Pell"
    hostname = "Pell"
    servername = "Pell"
    realname = "Pell"
    nick = "Pell"
    password = None
    chan = "#root-me_challenge"

    client = pyrc.PyrcClient()
    client.connect("irc.root-me.org", username, hostname, servername, realname, nick, password)
    time.sleep(4)
    client.joinChan(chan)
    try:
        while(1):
            to_send = input("")
            client.sendRaw(to_send + "\n")
    except:
        client.disconnect()
        raise
