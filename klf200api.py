##
## AHM, 2018 
##

import struct
from slip import *
from toolbox import getIndex, toHex

# ===============================================================================
#
# ===============================================================================

GW_CS_GET_SYSTEMTABLE_DATA_REQ = 0x0100
GW_CS_GET_SYSTEMTABLE_DATA_CFM = 0x0101
GW_CS_GET_SYSTEMTABLE_DATA_NTF = 0x0102

GW_CS_DISCOVER_NODES_REQ = 0x0103
GW_CS_DISCOVER_NODES_CFM = 0x0104
GW_CS_DISCOVER_NODES_NTF = 0x0105

GW_CS_VIRGIN_STATE_REQ = 0x0108
GW_CS_VIRGIN_STATE_CFM = 0x0109

GW_CS_CONTROLLER_COPY_REQ = 0x010A
GW_CS_CONTROLLER_COPY_CFM = 0x010B
GW_CS_CONTROLLER_COPY_NTF = 0x010C
GW_CS_CONTROLLER_COPY_CANCEL = 0x010D

GW_RECORD_SCENE_REQ = 0x0405
GW_RECORD_SCENE_CFM = 0x0406
GW_RECORD_SCENE_NTF = 0x0407

GW_ACTIVATE_SCENE_REQ = 0x0412
GW_ACTIVATE_SCENE_CFM = 0x0413

GW_PASSWORD_ENTER_REQ = 0x3000
GW_PASSWORD_ENTER_CFM = 0x3001

GW_PASSWORD_CHANGE_REQ = 0x3002
GW_PASSWORD_CHANGE_CFM = 0x3003
GW_PASSWORD_CHANGED_NTF = 0x3004

GW_GET_ALL_NODES_INFORMATION_REQ = 0x0202
GW_GET_ALL_NODES_INFORMATION_CFM = 0x0203
GW_GET_ALL_NODES_INFORMATION_NTF = 0x0204
GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF = 0x0205

GW_GET_NODE_INFORMATION_REQ = 0x0200
GW_GET_NODE_INFORMATION_CFM = 0x0201
GW_GET_NODE_INFORMATION_NTF = 0x0210
GW_NODE_STATE_POSITION_CHANGED_NTF = 0x0211

GW_HOUSE_STATUS_MONITOR_ENABLE_REQ = 0x0240
GW_HOUSE_STATUS_MONITOR_ENABLE_CFM = 0x0241
GW_HOUSE_STATUS_MONITOR_DISABLE_REQ = 0x0242
GW_HOUSE_STATUS_MONITOR_DISABLE_CFM = 0x0243

GW_COMMAND_SEND_REQ = 0x0300
GW_COMMAND_SEND_CFM = 0x0301
GW_COMMAND_RUN_STATUS_NTF = 0x0302
GW_COMMAND_REMAINING_TIME_NTF = 0x0303
GW_SESSION_FINISHED_NTF = 0x0304

GW_STATUS_REQUEST_REQ = 0x0305
GW_STATUS_REQUEST_CFM = 0x0306
GW_STATUS_REQUEST_NTF = 0x0307

GW_GET_STATE_REQ = 0x000C
GW_GET_STATE_CFM = 0x000D

# ===============================================================================
#
# ===============================================================================

dictNodeType = {
    0: "NO_TYPE",  # (All nodes except controller)
    1: "Venetian blind",
    2: "Roller shutter",
    3: "Awning",  # (External for windows)
    4: "Window opener",
    5: "Garage opener",
    6: "Light",
    7: "Gate opener",
    8: "Rolling Door Opener",
    9: "Lock",
    10: "Blind",
    11: "SCD",  # (Secure Configuration Device)
    12: "Beacon",
    13: "Dual Shutter",
    14: "Heating Temperature Interface",
    15: "On / Off Switch",
    16: "Horizontal Awning",
    17: "External Venetian Blind",
    18: "Louvre Blind",
    19: "Curtain track",
    20: "Ventilation Point",
    21: "Exterior heating",
    22: "Heat pump",  # (Not currently supported)
    23: "Intrusion alarm",
    24: "Swinging Shutter",
}

dictPriorityLevel = {
    0: 'Human Protection',
    1: 'Environment Protection',
    2: 'User Level 1',
    3: 'User Level 2',
    4: 'Comfort Level 1',
    5: 'Comfort Level 2',
    6: 'Comfort Level 3',
    7: 'Comfort Level 4',
}

dictCommandOriginator = {
    0x00: "LOCAL_USER",  # // User pressing button locally on actuator
    0x01: "USER",  # // User Remote control causing action on actuator
    0x02: "RAIN",  # // Sensor
    0x03: "TIMER",  # // Sensor
    0x04: "SECURITY",  # // SCD controlling actuator
    0x05: "UPS",  # // UPS unit
    0x06: "SFC",  # // Smart Function Controller
    0x07: "LSC",  # // Lifestyle Scenario Controller
    0x08: "SAAC",  # // Stand Alone Automatic Controls
    0x09: "WIND",  # // Wind detection
    0x10: "MYSELF",  # // Used when an actuator decides to move by itself
    0xFE: "AUTOMATIC_CYCLE",  # // Used in context with automatic cycle;
    0xFF: "EMERGENCY"  # // Used in context with emergency or security commands,
    # // -this command originator should never be disabled
}

dictVelocity = {
    0: 'DEFAULT',
    1: 'SILENT',
    2: 'FAST',
    255: 'VELOCITY_NOT_AVAILABLE',  # Only used in status reply
}

dictControllerCopyMode = {
    0: "TransmittingConfigurationMode",
    # Transmitting Configuration Mode (TCM): The gateway gets key and system table from another controller.
    1: "ReceivingConfigurationMode",
    # Receiving Configuration Mode (RCM): The gateway gives key and system table to another controller.
}


# ===============================================================================
#
# ===============================================================================


class ST_GW_FRAME:
    def __init__(self, Command):
        self.DataLength = 0
        self.Command = Command
        self.binary_output = b""

    def __bytes__(self):
        self.binary_output = struct.pack("BB", 0, self.DataLength + 3)
        self.binary_output += struct.pack(">H", self.Command)
        self.binary_output += self.pack_data()
        self.binary_output += struct.pack("B", self.calc_crc())
        return slip_pack(self.binary_output)

    def calc_crc(self):
        crc = 0
        for sym in self.binary_output:
            crc = crc ^ int(sym)
        return crc

    def pack_data(self):
        return b""


class ST_GW_GET_STATE_REQ(ST_GW_FRAME):
    def __init__(self):
        ST_GW_FRAME.__init__(self, GW_GET_STATE_REQ)
        self.DataLength = 0

    def pack_data(self):
        ret = b''
        return ret


class ST_GW_HOUSE_STATUS_MONITOR_ENABLE_REQ(ST_GW_FRAME):
    def __init__(self):
        ST_GW_FRAME.__init__(self, GW_HOUSE_STATUS_MONITOR_ENABLE_REQ)
        self.DataLength = 0

    def pack_data(self):
        ret = b''
        return ret


class ST_GW_HOUSE_STATUS_MONITOR_DISABLE_REQ(ST_GW_FRAME):
    def __init__(self):
        ST_GW_FRAME.__init__(self, GW_HOUSE_STATUS_MONITOR_DISABLE_REQ)
        self.DataLength = 0

    def pack_data(self):
        ret = b''
        return ret


class ST_GW_STATUS_REQUEST_REQ(ST_GW_FRAME):
    def __init__(self, wSessionID=0x0018,
                 node_id=2):
        ST_GW_FRAME.__init__(self, GW_STATUS_REQUEST_REQ)
        self.DataLength = 26
        self.SessionID = wSessionID
        self.StatusType = 1
        self.FPI = 0xffff
        self.IndexArrayCount = 1
        self.IndexArray = node_id

    def pack_data(self):
        ret = struct.pack(">H", self.SessionID)
        ret += bytes([self.IndexArrayCount])
        ret += bytes([self.IndexArray])
        ret += bytes([0])
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += bytes([self.StatusType])
        ret += struct.pack("H", self.FPI)
        return ret


class ST_GW_COMMAND_SEND_REQ(ST_GW_FRAME):
    def __init__(self, wSessionID=0x0012,
                 CommandOriginator='USER',
                 PriorityLevel='User Level 2',
                 NodeID=1,
                 Position=0):
        ST_GW_FRAME.__init__(self, GW_COMMAND_SEND_REQ)
        self.DataLength = 66
        self.SessionID = wSessionID
        self.CommandOriginator = getIndex(dictCommandOriginator, CommandOriginator)
        self.PriorityLevel = getIndex(dictPriorityLevel, PriorityLevel)
        self.ParameterActive = 0
        self.FPI = 0x0000
        self.FPVarray = Position
        self.IndexArrayCount = 1
        self.IndexArray = NodeID
        self.PriorityLevelLock = 0x0000

    def pack_data(self):
        ret = struct.pack(">H", self.SessionID)
        ret += bytes([self.CommandOriginator])
        ret += bytes([self.PriorityLevel])
        ret += bytes([self.ParameterActive])
        ret += struct.pack(">H", self.FPI)
        ret += struct.pack(">H", self.FPVarray)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += struct.pack(">H", 0xD400)
        ret += bytes([self.IndexArrayCount])
        ret += bytes([self.IndexArray])
        ret += bytes([0])
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += struct.pack("H", 0x0000)
        ret += bytes([0])
        ret += bytes([0])
        ret += struct.pack("H", self.PriorityLevelLock)
        ret += struct.pack("H", 0x0000)
        return ret


class ST_GW_GET_NODE_INFORMATION_REQ(ST_GW_FRAME):
    def __init__(self, NodeID):
        ST_GW_FRAME.__init__(self, GW_GET_NODE_INFORMATION_REQ)
        self.DataLength = 1
        self.NodeID = NodeID

    def pack_data(self):
        ret = bytes([self.NodeID])
        return ret


class ST_GW_GET_ALL_NODES_INFORMATION_REQ(ST_GW_FRAME):
    def __init__(self):
        ST_GW_FRAME.__init__(self, GW_GET_ALL_NODES_INFORMATION_REQ)
        self.DataLength = 0

    def pack_data(self):
        ret = b''
        return ret


class ST_GW_CS_GET_SYSTEMTABLE_DATA_REQ(ST_GW_FRAME):
    def __init__(self):
        ST_GW_FRAME.__init__(self, GW_CS_GET_SYSTEMTABLE_DATA_REQ)
        self.DataLength = 0

    def pack_data(self):
        ret = b''
        return ret


class ST_GW_CS_VIRGIN_STATE_REQ(ST_GW_FRAME):
    def __init__(self):
        ST_GW_FRAME.__init__(self, GW_CS_VIRGIN_STATE_REQ)
        self.DataLength = 0

    def pack_data(self):
        ret = b''
        return ret


class ST_GW_CS_DISCOVER_NODES_REQ(ST_GW_FRAME):
    def __init__(self, NodeType='NO_TYPE'):
        ST_GW_FRAME.__init__(self, GW_CS_DISCOVER_NODES_REQ)
        self.DataLength = 1
        self.bNodeType = getIndex(dictNodeType, NodeType)

    def pack_data(self):
        ret = bytes([self.bNodeType])
        return ret


class ST_GW_CS_CONTROLLER_COPY_REQ(ST_GW_FRAME):
    def __init__(self, ControllerCopyMode='TransmittingConfigurationMode'):
        ST_GW_FRAME.__init__(self, GW_CS_CONTROLLER_COPY_REQ)
        self.DataLength = 1
        self.bControllerCopyMode = getIndex(dictControllerCopyMode, ControllerCopyMode)

    def pack_data(self):
        ret = bytes([self.bControllerCopyMode])
        return ret


class ST_GW_ACTIVATE_SCENE_REQ(ST_GW_FRAME):
    def __init__(self,
                 wSessionID=0x1234,
                 CommandOriginator='USER',
                 PriorityLevel='User Level 2',
                 bSceneID=0,
                 Velocity='DEFAULT'):
        ST_GW_FRAME.__init__(self, GW_ACTIVATE_SCENE_REQ)
        self.DataLength = 6
        self.wSessionID = wSessionID
        self.bCommandOriginator = getIndex(dictCommandOriginator, CommandOriginator)
        self.bPriorityLevel = getIndex(dictPriorityLevel, PriorityLevel)
        self.bSceneID = bSceneID
        self.bVelocity = getIndex(dictVelocity, Velocity)

    def pack_data(self):
        ret = struct.pack(">H", self.wSessionID)
        ret += bytes([self.bCommandOriginator])
        ret += bytes([self.bPriorityLevel])
        ret += bytes([self.bSceneID])
        ret += bytes([self.bVelocity])
        return ret


class ST_GW_RECORD_SCENE_REQ(ST_GW_FRAME):
    def __init__(self, SceneName):
        ST_GW_FRAME.__init__(self, GW_RECORD_SCENE_REQ)
        self.DataLength = 64
        self.SceneName = SceneName

    def pack_data(self):
        binary_data = bytes(self.SceneName, encoding='ascii')
        binary_len = len(binary_data)
        ret = binary_data[:self.DataLength if binary_len > self.DataLength else binary_len]
        while binary_len < self.DataLength:
            ret += b'\x00'
            binary_len = binary_len + 1
        return ret


class ST_GW_PASSWORD_ENTER_REQ(ST_GW_FRAME):
    def __init__(self, Password):
        ST_GW_FRAME.__init__(self, GW_PASSWORD_ENTER_REQ)
        self.DataLength = 32
        self.Password = Password

    def pack_data(self):
        binary_data = bytes(self.Password, encoding='ascii')
        binary_len = len(binary_data)
        ret = binary_data[:self.DataLength if binary_len > self.DataLength else binary_len]
        while binary_len < self.DataLength:
            ret += b'\x00'
            binary_len = binary_len + 1
        return ret


class ST_GW_PASSWORD_CHANGE_REQ(ST_GW_FRAME):
    def __init__(self, OldPassword, NewPassword):
        ST_GW_FRAME.__init__(self, GW_PASSWORD_CHANGE_REQ)
        self.DataLength = 64
        self.NewPassword = NewPassword
        self.OldPassword = OldPassword

    def pack_data(self):
        password_length = self.DataLength / 2
        binary_data = bytes(self.OldPassword, encoding='ascii')
        binary_len = len(binary_data)
        ret = binary_data[:password_length if binary_len > password_length else binary_len]
        while binary_len < password_length:
            ret += b'\x00'
            binary_len = binary_len + 1
        binary_data = bytes(self.NewPassword, encoding='ascii')
        binary_len = len(binary_data)
        ret += binary_data[:password_length if binary_len > password_length else binary_len]
        while binary_len < password_length:
            ret += b'\x00'
            binary_len = binary_len + 1
        return ret


if __name__ == "__main__":
    print(toHex(bytes(ST_GW_CS_VIRGIN_STATE_REQ())))
    print(toHex(bytes(ST_GW_CS_DISCOVER_NODES_REQ('NO_TYPE'))))
    print(toHex(bytes(ST_GW_CS_CONTROLLER_COPY_REQ('TransmittingConfigurationMode'))))
    print(toHex(bytes(ST_GW_ACTIVATE_SCENE_REQ(bSceneID=0))))
    print(toHex(bytes(ST_GW_PASSWORD_ENTER_REQ("password"))))
    print(toHex(bytes(ST_GW_PASSWORD_CHANGE_REQ("password", "newpass"))))
