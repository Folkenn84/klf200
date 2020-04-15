##
## MQTT
##

import struct, threading
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
        while 1:
            result = self.connexion.recv()
            command = parse_command(result)
            if GW_GET_NODE_INFORMATION_NTF == command:
                print("command traité : ", toHex(slip_unpack(result)))
                nodeid = int(parse_command(result, 4, 5))
                position = 100 - int(parse_command(result, 89, 91) / 512)
                self.mqtt.publish("klf200/node_" + str(nodeid), payload=position)
            elif GW_NODE_STATE_POSITION_CHANGED_NTF == command:
                print("command traité : ", toHex(slip_unpack(result)))
                nodeid = int(parse_command(result, 4, 5))
                position = 100 - int(parse_command(result, 6, 8) / 512)
                self.mqtt.publish("klf200/status/" + str(nodeid), payload=position)
            else:
                print("command non traité : ", toHex(slip_unpack(result)))


class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn, mqttComm):
        threading.Thread.__init__(self)
        self.connexion = conn	     # réf. du socket de connexion
        self.mqtt = mqttComm

    def run(self):
        self.mqtt.loop_start()
        self.mqtt.subscribe("klf200/action")
        self.mqtt.connect(MQTT_ADDRESS)
        self.mqtt.on_message = self.on_message


    def on_message(self, client, userdata, message):
        value = str(message.payload.decode("utf-8")).split(" ")
        print("traitement", value)
        if "STATUS" == value[0]:
            position = positionVolet(self.connexion, int(value[1]))
            # client.publish("klf200/status/" + value[1], payload=position)
        elif "MOVE" == value[0]:
            moveVolet(self.connexion, int(value[2]), int(value[1]))
        elif "STOP" == value[0]:
            stopVolet(self.connexion, int(value[1]))
        # print("message received ", str(message.payload.decode("utf-8")))
        # print("message topic=", message.topic)
        # print("message qos=", message.qos)
        # print("message retain flag=", message.retain)

# ===============================================================================
#
# ===============================================================================
def main():

    client = mqtt.Client("KLF200")
    client.connect(MQTT_ADDRESS)
    client.on_message = on_message
    client.loop_start()
    client.subscribe("klf200/action")
    # th_E = ThreadEmission(connklf200, client)
    # th_E.start()
    th_R = ThreadReception(connklf200, client)
    th_R.start()
    print("starting reception")

    client.publish("klf200/action", retain=True)
    # client.publish("maison/klf200", "STATUS 2")

    # client.publish("maison/klf200", "MOVE 2 100")
    # client.publish("maison/klf200", "STOP 2")
    # time.sleep(4)
    # print("pending", connklf200.pending())
    # time.sleep(4)
    client.publish("klf200/action", "POSITION_VOLET 1")
    # client.publish("klf200/action", "MOVE 2 50")
    # client.publish("klf200/action", "STOP 2")
    client.publish("klf200/action", "POSITION_VOLET 2")
    client.publish("klf200/action", "POSITION_VOLET 3")
    client.publish("klf200/action", "POSITION_VOLET 4")
    # client.publish("klf200/action", "STOP 3")
    client.publish("klf200/action", "POSITION_VOLET 5")
    while True:
        try:
            time.sleep(5)
        except BaseException as e:
            client.loop_stop()
            # th_E._stop()
            th_R._delete()


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


connklf200 = init()
# conn2klf200 = init()
main()
connklf200.close()
# conn2klf200.close()
