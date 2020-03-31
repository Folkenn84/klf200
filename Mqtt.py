##
## MQTT
##

import struct
import paho.mqtt.client as mqtt
import time
from setup import *
from connection import *
from GetStatus import send_request as getStatus
from MoveVolet import send_request as moveVolet
from StopVolet import send_request as stopVolet
from slip import *
from toolbox import getIndex, toHex


# ===============================================================================
#
# ===============================================================================
def main():
    client = mqtt.Client("KLF200")
    client.connect(MQTT_ADDRESS)
    client.on_message = on_message
    client.loop_start()
    client.subscribe("maison/klf200")
    print("pending", connklf200.pending())
    client.publish("maison/klf200", retain=True)
    #client.publish("maison/klf200", "STATUS 2")

    client.publish("maison/klf200", "MOVE 2 100")
    client.publish("maison/klf200", "STOP 2")
    time.sleep(4)
    # print("pending", connklf200.pending())
    # time.sleep(4)
    client.publish("maison/klf200", "STATUS 2")
    client.publish("maison/klf200", "STATUS 2")
    time.sleep(20)
    client.loop_stop()


def on_message(client, userdata, message):
    value = str(message.payload.decode("utf-8")).split(" ")
    print("traitement", value)
    if "STATUS" == value[0]:
        getStatus(connklf200, int(value[1]))
    elif "MOVE" == value[0]:
        moveVolet(connklf200, int(value[2]), int(value[1]))
    elif "STOP" == value[0]:
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
