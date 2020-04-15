##
## AHM, 2018 
##

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import *
from connection import *
from setup import *
from GetNodeInfo import send_request as getNodeInfo


def send_request(conn, nodeID):
    print("Get position with ID = ", nodeID)
    result = getNodeInfo(conn, nodeID)
    # print(toHex(slip_unpack(result)))
    # position = 100 - int(parse_command(result, 89, 91) / 512)
    # print(position)
    # return position


def main():
    nodeid = int(sys.argv[1])
    try:
        conn = init()
        send_request(conn, nodeid)
    except BaseException as e:
        raise e
    finally:
        conn.close()


#main()
#print("Finished")
