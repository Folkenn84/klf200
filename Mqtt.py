##
## MQTT
##

import struct, threading
from ssl import SSLSocket

import paho.mqtt.client as mqtt
import time

from setup import *
from connection import *
from PositionVolet import send_request as positionVolet
from MoveVolet import send_request as moveVolet
from StopVolet import send_request as stopVolet
from slip import *
from toolbox import *


class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn, mqttComm):
        threading.Thread.__init__(self)
        self.connexion = conn	     # réf. du socket de connexion
        self.mqtt = mqttComm

    def run(self):
        try:
            while 1:
                result = self.connexion.recv()
                command = parse_command(result)
                if GW_GET_NODE_INFORMATION_NTF == command:
                    print("command traité : ", toHex(slip_unpack(result)), flush=True)
                    nodeid = int(parse_command(result, 4, 5))
                    if nodeid == 0:
                        self.mqtt.publish("klf200/status/" + str(nodeid), payload=toHex(slip_unpack(result)))
                    else:
                        position = 100 - int(parse_command(result, 89, 91) / 512)
                        self.mqtt.publish("klf200/status/" + str(nodeid), payload=position)
                elif GW_NODE_STATE_POSITION_CHANGED_NTF == command:
                    print("command traité : ", toHex(slip_unpack(result)), flush=True)
                    nodeid = int(parse_command(result, 4, 5))
                    if nodeid == 0:
                        self.mqtt.publish("klf200/status/" + str(nodeid), payload=toHex(slip_unpack(result)))
                    else:
                        position = 100 - int(parse_command(result, 6, 8) / 512)
                        self.mqtt.publish("klf200/status/" + str(nodeid), payload=position)
                elif GW_GET_STATE_CFM == command:
                    print("command traité : ", toHex(slip_unpack(result)), flush=True)
                    position = int(parse_command(result, 4, 5))
                    self.mqtt.publish("klf200/status/gateway", payload=position)
                else:
                    print("command non traité : %s", toHex(slip_unpack(result)))
        except BaseException as e:
            print(e, flush=True)


# ===============================================================================
#
# ===============================================================================
def main():
    initconnKlf200()
    client = mqtt.Client("KLF200")
    client.connect(MQTT_ADDRESS)
    client.on_message = on_message
    client.loop_start()
    client.subscribe("klf200/action")
    th_R = ThreadReception(connklf200, client)
    th_R.start()
    print("starting reception", flush=True)

    client.publish("klf200/action", retain=True)
    client.publish("klf200/action", "POSITION_VOLET 0")
    client.publish("klf200/action", "POSITION_VOLET 1")
    client.publish("klf200/action", "POSITION_VOLET 2")
    client.publish("klf200/action", "POSITION_VOLET 3")
    client.publish("klf200/action", "POSITION_VOLET 4")
    client.publish("klf200/action", "POSITION_VOLET 5")
    while True:
        try:
            time.sleep(5)
        except BaseException as e:
            print("plantage de la boucle : %s", e)
            client.loop_stop()
            # th_E._stop()
            th_R._delete()
            connklf200.close()
            exit("ERROR")
    exit("OK")


def on_message(client, userdata, message):
    value = str(message.payload.decode("utf-8")).split(" ")
    time.sleep(1)
    print("traitement", value)
    if "POSITION_VOLET" == value[0]:
        positionVolet(connklf200, int(value[1]))
        # client.publish("klf200/status/" + value[1], payload=position)
    elif "MOVE_VOLET" == value[0]:
        moveVolet(connklf200, int(value[2]), int(value[1]))
    elif "STOP_VOLET" == value[0]:
        stopVolet(connklf200, int(value[1]))
    # print("message received ", str(message.payload.decode("utf-8")))
    # print("message topic=", message.topic)
    # print("message qos=", message.qos)
    # print("message retain flag=", message.retain)


def initconnKlf200():
    global connklf200
    connklf200 = init()


connklf200 = None
# main()
