##
## AHM, 2018 
##
## Precondition: KLF200 must be empty, for example by running Virgin.py script. 
##	Other controler must contain a valid system and must be in ReceivingConfigurationMode
##	for example if you have a KLR200 remote controller with at least one node in its system table.
## 	then on KLR200 you navigate to menu\New products\Copy control pad
## 	and press -> button on Send copy page before execute this script.
## 

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from slip import *
from connection import *


def send_request(conn):
    print("Copy ststem (Nodes and key) from other remote controller to KLF200")
    conn.write(bytes(ST_GW_CS_CONTROLLER_COPY_REQ('TransmittingConfigurationMode')))
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
