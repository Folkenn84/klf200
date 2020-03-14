##
## AHM, 2018 
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from connection import *
from setup import *

def send_request(conn):
    print("Get Node Info with ID = ")
    conn.write(bytes(ST_GW_GET_NODE_INFORMATION_REQ(NodeID=2)))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    
def main():
    try:
        conn = init()
        send_request(conn)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()

main()
print("Finished")
