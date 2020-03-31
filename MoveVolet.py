#
# AHM, 2018
#

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import toHex
from connection import *
from time import sleep
from CommandSend import send_request as commandSend


def send_request(conn, position, nodeID):
    print("Move Store = ", nodeID, "POS = ", position)
    commandSend(conn, (100 - position) * 512, nodeID)


def main():
    position = int(sys.argv[1])
    nodeID = int(sys.argv[2])

    try:
        conn = init()
        send_request(conn, position, nodeID)
    except BaseException as e:
        raise (e)
    finally:
        conn.close()

main()
print("Finished")
