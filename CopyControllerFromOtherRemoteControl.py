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
from setup import *


PORT            = 51200
LoopDelay       = 1


def process_connection(conn):
    conn.settimeout(100.0)
    
    print("Send valid password")
    conn.write(bytes(ST_GW_PASSWORD_ENTER_REQ(PASSWORD)))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")
    
    time.sleep(LoopDelay)

    print("Copy ststem (Nodes and key) from other remote controller to KLF200")
    conn.write(bytes(ST_GW_CS_CONTROLLER_COPY_REQ('TransmittingConfigurationMode')))
    print("Received: ", toHex(slip_unpack(conn.recv())))
    print("Received: ", toHex(slip_unpack(conn.recv())), "\n")

	
def main():
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(10.0)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = False
    #accept self-signed certificate
    context.verify_mode = ssl.CERT_NONE

    conn = context.wrap_socket(sock, server_hostname=KLF200_ADDRESS)

    try:
        conn.connect((KLF200_ADDRESS, PORT))
        process_connection(conn)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()


main()
print("Finished")
