import serial
from time import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from settings import  *

def data_gen():
    while True:
        sample=get_data_from_serial()
        if sample!= None: 
            t=time()
            return t, sample


ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
def get_data_from_serial():
    s=ser.readline()
    # print s
    s=s.split(",")
    if len(s)!=3:
        return None
    for i in range(len(s)):
        try: s[i]=float(s[i].strip())
        except: return None
    # print s
    x,y,z = s[0],s[1],s[2]
    return x, y, z

# while True:
#     print serial.Serial('/dev/tty.usbmodem1421', 9600).readline()
data=[]
start_time=time()
while start_time+2>time():
    if len(data)*sampleRate>=max_rep_window: 
        del data[0]
        sample = data_gen()
        data.append(sample)
        print data
