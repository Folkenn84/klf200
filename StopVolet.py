##
## AHM, 2018 
##

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import toHex
from connection import *


def send_request(conn, position, nodeID):
    print("Stop Store = ", nodeID)
    conn.write(bytes(ST_GW_COMMAND_SEND_REQ(NodeID=nodeID, Position=position)))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    
def main():
    position = 53760
    nodeID = int(sys.argv[1])

    try:
        conn = init()
        send_request(conn, position, nodeID)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()

main()
print("Finished")
