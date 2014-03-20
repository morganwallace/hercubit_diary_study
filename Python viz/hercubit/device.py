import serial
from time import time
from time import sleep
from settings import *
from ast import literal_eval

t0=time()


def acc_data():
    """yeilds tuple of time, and xyz acceleration

    * Mimics old acc_data generator for legacy functionality"""


    global t0
    while t0+sampleRate>time():
        sleep(sampleRate)
    t0=time()
    if conn_type =="archive":
        for line in ser:
            sleep(sampleRate/2) # simulate actual sample rate
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


def sensor_stream(sensor="all", simulate_sample_rate=True):
    """Generator for streaming sensor data.
    If the argument is 'all' then Acceleromater, Gyro, and Magetometer data are
    all returned.
    Otherwise the argument will return just one type"""

    global t0
    # Ensure we don't read too fast
    while t0+sampleRate>time():
        sleep(sampleRate)
    t0=time()
    print conn_type
    if conn_type =="archive":
        archive_data.readline()
        while True:
            line=archive_data.readline()
            if line is not None:
                if simulate_sample_rate==True: sleep(sampleRate) # simulate actual sample rate
                s= [float(i) for i in line.split(",")[-10:]]
                formatted_sample= {'time':s[0],'accel':(s[1],s[2],s[3]),'gyro':(s[4],s[5],s[6]),'magnet':(s[7],s[8],s[9])}
                yield formatted_sample
            else: break
    else:
        while True:
            # Read a line from the serial port and convert it to a python dictioary object
            try:
                sample =literal_eval(ser.readline())
                sample['time']=time()
            except:
                sample= {'accel':(0,0,0),'gyro':(0,0,0),'magnet':(0,0,0)}            
            # If just one sensor type is requested...
            if sensor !="all": # sensor could be 'accel', 'gyro', or 'magnet'
                yield list(sample[sensor])
            else: 
                yield sample
            


def run():
    """Use this code as the starting point 
    in scripts that import this module"""
    sensor_generator=sensor_stream()
    while True:    
        print sensor_generator.next()

if __name__ == '__main__':
    run()
