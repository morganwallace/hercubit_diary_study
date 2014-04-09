import serial
from time import time
from time import sleep
import settings
from ast import literal_eval

t0=time()


def acc_data():
    """yeilds tuple of time, and xyz acceleration

    * Mimics old acc_data generator for legacy functionality"""


    global t0
    while t0+settings.sampleRate>time():
        sleep(settings.sampleRate)
    t0=time()
    if conn_type =="archive":
        for line in ser:
            sleep(settings.sampleRate/2) # simulate actual sample rate
            try:
                s= [float(i) for i in line.split(",")]
                formatted_sample= {'accel':(0,0,0),'gyro':(0,0,0),'magnet':(0,0,0)}  
            except:
                yield None
            yield sample
    else:
        while True:
            sample =literal_eval(ser.readline())
            sample = list(sample['accel'])
            sample.insert(0,time())
            yield tuple(sample)