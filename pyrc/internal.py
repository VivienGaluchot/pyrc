import socket, time, select, sys
from multiprocessing import Process, Queue

def NonblockingGet(queue):
    try:
        return queue.get(block=False)
    except:
        if queue.empty():
            return None
        else:
            raise

def PyrcSocketHandler(stop_queue, send_msg_queue, server_ip):
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server_ip, 6667))
    ircsock.setblocking(False)
    stop = False
    while not stop:
        rlist, wlist, elist = select.select([ircsock], [ircsock], [], 0.001)
        # receive
        if ircsock in rlist:
            raw_msg = ircsock.recv(2048)
            try:
                msg = raw_msg.decode("utf-8")
            except:
                msg = raw_msg
            if len(msg) > 0:
                if not msg.endswith("\n"):
                    msg = msg + "\n"
                sys.stdout.write(" - Srv - -\n{} - - - - -\n".format(msg))
        # send
        if ircsock in wlist:
            msg = NonblockingGet(send_msg_queue)
            if msg:
                ircsock.send(msg.encode("utf-8"))
                sys.stdout.write(" - Me  - -\n{} - - - - -\n".format(msg))
        # stop
        stop = NonblockingGet(stop_queue)
        if not stop:
            stop = False
        # wait
        time.sleep(0.001)
