##
## AHM, 2018 
## This scrip will delete io-homecontrol® nodes and system key from KLF200
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from setup import *

PORT            = 51200
LoopDelay       = 1


def process_connection(conn):
    conn.settimeout(100.0)
    
    print("Send valid password")
    conn.write(bytes(ST_GW_PASSWORD_ENTER_REQ(PASSWORD)))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    
    time.sleep(LoopDelay)

    print("Clear system in KLF200")
    conn.write(bytes(ST_GW_CS_VIRGIN_STATE_REQ()))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")

	
def main():
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(10.0)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = False
    #accept self-signed certificate
    context.verify_mode = ssl.CERT_NONE

    conn = context.wrap_socket(sock, server_hostname=KLF200_ADDRESS)

    try:
        conn.connect((KLF200_ADDRESS, PORT))
        process_connection(conn)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()


main()
print("Finished")
