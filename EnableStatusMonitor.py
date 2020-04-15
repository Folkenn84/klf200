##
## AHM, 2018 
## This scrip will delete io-homecontrol® nodes and system key from KLF200
##

import ssl, socket, time, struct
from klf200api import *
from toolbox import *
from connection import *


def send_request(conn):
    print("Enable status monitor in KLF200")
    conn.write(bytes(ST_GW_HOUSE_STATUS_MONITOR_ENABLE_REQ()))
    result = conn.recv()
    command = parse_command(result)
    if GW_HOUSE_STATUS_MONITOR_ENABLE_CFM == command:
        print("OK: ", toHex(slip_unpack(result)))
    else:
        print("ERROR: ", toHex(slip_unpack(result)))


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
