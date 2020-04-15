#
# AHM, 2018
#

import ssl, socket, time, struct, sys
from klf200api import *
from toolbox import *
from connection import *
from time import sleep


def send_request(conn, position, nodeID, sessionid):
    conn.write(bytes(ST_GW_COMMAND_SEND_REQ(NodeID=nodeID, wSessionID=sessionid, Position=position)))
    #result = conn.recv()
    #command = parse_command(result)
    #status = parse_command(result, 6, 7)
    #if GW_COMMAND_SEND_CFM == command and status == 1:
    #    while True:
    #        result = conn.recv()
    #        print(toHex(slip_unpack(result)))
    #        command = parse_command(result)
    #        if command == GW_SESSION_FINISHED_NTF:
    #            break