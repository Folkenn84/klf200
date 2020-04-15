##
## AHM, 2018 
##

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import toHex
from connection import *
from CommandSend import send_request as commandSend


def send_request(conn, nodeID):
    print("Stop Store = ", nodeID)
    position = 53760
    commandSend(conn, position, nodeID, nodeID+50)


def main():
    nodeID = int(sys.argv[1])
    try:
        conn = init()
        send_request(conn, nodeID)
    except BaseException as e:
        raise e
    finally:
        conn.close()


# main()
