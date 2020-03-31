##
## AHM, 2018 
## This scrip will delete io-homecontrol® nodes and system key from KLF200
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from connection import *


def send_request(conn):
    print("Clear system in KLF200")
    conn.write(bytes(ST_GW_CS_VIRGIN_STATE_REQ()))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")


def main():
    try:
        conn = init()
        send_request(conn)
    except BaseException as e:
        raise e
    finally:
        conn.close()


main()
print("Finished")
