##
## AHM, 2018 
##
import ssl, socket, time, struct
from setup import *
from slip import *
from klf200api import *

LoopDelay       = 1

def init():
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(10.0)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = False
    #accept self-signed certificate
    context.verify_mode = ssl.CERT_NONE

    conn = context.wrap_socket(sock, server_hostname=KLF200_ADDRESS)

    conn.connect((KLF200_ADDRESS, PORT))
    conn.settimeout(30.0) # 30 sec

    #status KLF200
    conn.write(bytes(ST_GW_GET_STATE_REQ()))
    print(toHex(slip_unpack(conn.recv())))

    #connection
    #conn.write(bytes(ST_GW_PASSWORD_ENTER_REQ(PASSWORD)))
    #toHex(slip_unpack(conn.recv()))

    time.sleep(LoopDelay)

    return conn
