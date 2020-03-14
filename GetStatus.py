##
## AHM, 2018 
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import toHex
from setup import *
from time import sleep

PORT            = 51200
LoopDelay       = 1


def process_connection(conn):
    conn.settimeout(30.0) # 10 sec
    
    conn.write(bytes(ST_GW_PASSWORD_ENTER_REQ(PASSWORD)))
    toHex(slip_unpack(conn.recv()))
    
    time.sleep(LoopDelay)

    conn.write(bytes(ST_GW_STATUS_REQUEST_REQ(NodeID=2)))
    toHex(slip_unpack(conn.recv()))
    # One or more command handler status frames will be recieved.
    # Number depends of scene size and number of actuator movements.    
    result = slip_unpack(conn.recv())
    print(100- int(int(toHex(result[13:15]).replace(':',''), 16)/512))
    toHex(slip_unpack(conn.recv()))
##    print("Received: ", toHex(slip_unpack(conn.recv())))
##    print("Received: ", toHex(slip_unpack(conn.recv())))
##    print("Received: ", toHex(slip_unpack(conn.recv())))    
##    print("Received: ", toHex(slip_unpack(conn.recv())))
##    print("Received: ", toHex(slip_unpack(conn.recv())))
##    print("Received: ", toHex(slip_unpack(conn.recv())))       
##    print("Received: ", toHex(slip_unpack(conn.recv())))
##    print("Received: ", toHex(slip_unpack(conn.recv())))    

    sleep(2) # waith 2 sec
    
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
