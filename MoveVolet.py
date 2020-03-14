##
## AHM, 2018 
##

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import toHex
from connection import *
from time import sleep


def send_request(conn, position, nodeID):
    print("Move Store = ", nodeID)
    conn.write(bytes(ST_GW_COMMAND_SEND_REQ(NodeID=nodeID, Position=position)))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    # One or more command handler status frames will be recieved.
    # Number depends of scene size and number of actuator movements.    
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    
def main():
    position = (100 - int(sys.argv[1])) * 512
    nodeID = int(sys.argv[2])

    try:
        conn = init()
        send_request(conn, position, nodeID)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()

main()
print("Finished")
