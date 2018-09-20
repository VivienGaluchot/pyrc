from pyrc import pyrc

if __name__ == '__main__':
    username = "Pell"
    hostname = "Pell"
    servername = "Pell"
    realname = "Pellgrain"
    nick = "Pell"
    password = None
    char = "#root-me_challenge"

    pyrcCl = pyrc.PyrcClient()
    pyrcCl.connect("irc.root-me.org", username, hostname, servername, realname, nick, password)
    pyrcCl.joinChan(char)
    try:
        while(1):
            to_send = input("")
            pyrcCl.sendRaw(to_send + "\n")
    except:
        pyrcCl.disconnect()
        raise
