##
## AHM, 2018 
## Discover.py will add io-homecontrol® nodes, that is open for configutation, to KLF200's systemtable. 
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from slip import *
from setup import *
from connection import *


def send_request(conn):
    print("Discover all node types")
    conn.write(bytes(ST_GW_CS_DISCOVER_NODES_REQ()))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")


def main():
    try:
        conn = init()
        send_request(conn)
    except BaseException as e:
        raise (e)
    finally:
        conn.close()


main()
print("Finished")
