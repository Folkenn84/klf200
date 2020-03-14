##
## AHM, 2018 
##
from klf200api import *
from connection import *
from toolbox import *
from setup import *
from time import sleep

LoopDelay       = 1


def send_request(conn):

    conn.write(bytes(ST_GW_STATUS_REQUEST_REQ(NodeID=2)))
    toHex(slip_unpack(conn.recv()))
    # One or more command handler status frames will be recieved.
    # Number depends of scene size and number of actuator movements.    
    result = slip_unpack(conn.recv())
    print(100- int(int(toHex(result[13:15]).replace(':',''), 16)/512))
    toHex(slip_unpack(conn.recv()))

    sleep(2) # waith 2 sec
    
def main():
    try:
        conn = init()
        send_request(conn)
    except BaseException as e:
        raise(e)
    finally:
        conn.close()

main()
