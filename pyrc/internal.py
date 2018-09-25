import socket, time, select, sys, traceback
from multiprocessing import Process, Queue

def NonblockingGet(queue):
    try:
        return queue.get(block=False)
    except:
        if queue.empty():
            return None
        else:
            raise

# messageHandler : function(client, sentMsg, receivedMsg)
def PyrcSocketHandler(stop_queue, send_msg_queue, server_ip, messageHandler, client, debug=True):
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server_ip, 6667))
    ircsock.setblocking(False)
    stop = False
    while not stop:
        try:
            rlist, wlist, elist = select.select([ircsock], [ircsock], [], 0.001)
            # receive
            if ircsock in rlist:
                raw_msg = ircsock.recv(4096)
                try:
                    msg = raw_msg.decode("utf-8")
                    if len(msg) > 0:
                        if msg.endswith("\n"):
                            msg = msg[:-1]
                        if msg.startswith("PING"):
                            send_msg_queue.put("PONG")
                        messageHandler(client, None, msg)
                except:
                    print("Can't decode message in utf-8", msg)
            # send
            if ircsock in wlist:
                msg = NonblockingGet(send_msg_queue)
                if msg:
                    msgLine = msg + "\n"
                    ircsock.send(msgLine.encode("utf-8"))
                    messageHandler(client, msg, None)
            # stop
            stop = NonblockingGet(stop_queue)
            if not stop:
                stop = False
            # wait
            time.sleep(0.001)
        except KeyboardInterrupt:
            stop = True
        except:
            traceback.print_exc()
