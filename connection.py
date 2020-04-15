##
## AHM, 2018 
##

import ssl, socket, time, struct
from setup import *
from slip import *
from klf200api import *

LoopDelay = 1


def init():
    conn = initconn()

    ## status KLF200
    # conn.write(bytes(ST_GW_GET_STATE_REQ()))
    # result = slip_unpack(conn.recv())
    code = 12
    # code = int(toHex(result[2:5]).replace(':', ''), 16)
    ## time.sleep(LoopDelay)

    # connection
    if code == 12:
        ## conn.close()
        ## conn = initconn()
        conn.write(bytes(ST_GW_PASSWORD_ENTER_REQ(PASSWORD)))
        print(toHex(slip_unpack(conn.recv())))
        # time.sleep(LoopDelay)

    return conn


def initconn():
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(None)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = False
    # accept self-signed certificate
    context.verify_mode = ssl.CERT_NONE

    conn = context.wrap_socket(sock) # , server_hostname=KLF200_ADDRESS)

    conn.connect((KLF200_ADDRESS, PORT))
    conn.settimeout(None)  # 30 sec
    return conn
