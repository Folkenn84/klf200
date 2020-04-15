##
## AHM, 2018 
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from connection import *
from time import sleep


def send_request(conn):
    print("Activate Scene with ID = 0")
    conn.write(bytes(ST_GW_ACTIVATE_SCENE_REQ(bSceneID=0)))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())))
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
