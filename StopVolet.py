##
## AHM, 2018 
##

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import toHex
from setup import *
from time import sleep

PORT            = 51200
LoopDelay       = 1


def process_connection(conn, position, nodeID):
    conn.settimeout(60.0) # 60 sec
    
    print("Send valid password")
    conn.write(bytes(ST_GW_PASSWORD_ENTER_REQ(PASSWORD)))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    
    time.sleep(LoopDelay)

    print("Stop Store = ", nodeID)
    conn.write(bytes(ST_GW_COMMAND_SEND_REQ(NodeID=nodeID, Position=position)))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))

    sleep(2) # waith 2 sec
    
def main():
    position = 53760
    nodeID = int(sys.argv[1])
        
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(10.0)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = False
    #accept self-signed certificate
    context.verify_mode = ssl.CERT_NONE

    conn = context.wrap_socket(sock, server_hostname=KLF200_ADDRESS)

    try:
        conn.connect((KLF200_ADDRESS, PORT))
        process_connection(conn, position, nodeID)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()

main()
print("Finished")
