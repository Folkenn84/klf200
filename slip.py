##
## AHM, 2018 
##

import struct

END     = b"\xC0"    # SLIP escape character as per RFC 1055
ESC     = b"\xDB"    # SLIP escape character as per RFC 1055
ESC_END = b"\xDC"    # SLIP escape character as per RFC 1055
ESC_ESC = b"\xDD"    # SLIP escape character as per RFC 1055


def slip_pack(inputFrame):    
    data = inputFrame
    data = data.replace(ESC, ESC + ESC_ESC)
    data = data.replace(END, ESC + ESC_END)
    return END + data + END

def slip_unpack(inputFrame):
    data = inputFrame
    if(data[0:1]==END and data[-1:]==END):
        data = data.replace(ESC + ESC_END, END)
        data = data.replace(ESC + ESC_ESC, ESC)
        return data[1:-1]
    else:
        print("Error: No SLIP frame!\n")
        return inputFrame # error -> return input

