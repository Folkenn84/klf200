##
## AHM, 2018 
##
import sys
from klf200api import *
from connection import *
from toolbox import *
from setup import *
from time import sleep

LoopDelay = 1


def send_request(conn):
    conn.write(bytes(ST_GW_GET_STATE_REQ()))


def main():
    node_id = int(sys.argv[1])
    try:
        conn = init()
        send_request(conn, node_id)
    except BaseException as e:
        raise e
    finally:
        conn.close()


# main()
