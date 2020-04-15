##
## AHM, 2018 
##

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import toHex
from connection import *
from setup import *


def send_request(conn, nodeID):
    print("Get Node Info with ID = ", nodeID)
    conn.write(bytes(ST_GW_GET_NODE_INFORMATION_REQ(NodeID=nodeID)))
    # print("Received: ", toHex(slip_unpack(conn.recv())))
    # return conn.recv()


def main():
    nodeid = int(sys.argv[1])
    try:
        conn = init()
        result = send_request(conn, nodeid)
        print("Received: ", toHex(slip_unpack(result)))
    except BaseException as e:
        raise e
    finally:
        conn.close()


# main()
# print("Finished")
