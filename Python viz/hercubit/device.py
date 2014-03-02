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
                sample= [float(i) for i in line.split(",")]
            except:
                yield None
            yield sample
    else:
        while True:
            sample =literal_eval(ser.readline())
            sample = list(sample['accel'])
            sample.insert(0,time())
            yield tuple(sample)



def sensor_stream(sensor="all"):
    """Generator for streaming sensor data.
    If the argument is 'all' then Acceleromater, Gyro, and Magetometer data are
    all returned.
    Otherwise the argument will return just one type"""

    global t0
    # Ensure we don't read too fast
    while t0+sampleRate>time():
        sleep(sampleRate)
    t0=time()
    while True:
        if conn_type =="archive":
            sleep(sampleRate/2) # simulate actual sample rate
            try:
                sample= [float(i) for i in ser.readline().split(",")]
            except:
                ser.close()
                quit()
            yield sample
        else:
            # Read a line from the serial port and convert it to a python dictioary object
            sample =literal_eval(ser.readline())

            # If just one sensor type is requested...
            if sensor !="all": # sensor could be 'accel', 'gyro', or 'magnet'
                sample = list(sample[sensor])
                sample.insert(0,time())
            else:
                sample['time']=time()
            yield sample

        # for i in range(len(sample)):
        #     try: sample[i]=float(sample[i].strip())
        #     except: yield None
        # if len(sample)==3: #From Device, Acc only
        #     t=time()
        # elif len(sample)==4: # from backup file
        #     t=sample.pop(0)
        #     sleep(sampleRate/2) # simulate actual sample rate
        # else:
        #     yield None
        # x,y,z = sample[0], sample[1],sample[2]
        # # print (t,x,y,z)
        # yield t,x,y,z


def run():
    """Use this code as the starting point 
    in scripts that import this module"""
    l=sensor_stream('accel')
    while True:        
        print l.next()

if __name__ == '__main__':
    run()
