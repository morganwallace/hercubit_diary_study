import serial
from time import time
from time import sleep
from settings import *

t0=time()

def acc_data():
    global t0
    # Ensure we don't read too fast
    # while t0+sampleRate>time():
    #     sleep(sampleRate)
    # t0=time()
    while True:
        sample =ser.readline()
        if not sample: break
        sample=sample.split(",")
        for i in range(len(sample)):
            try: sample[i]=float(sample[i].strip())
            except: yield None
        if len(sample)==3: #From Device, Acc only
            t=time()
        elif len(sample)==4: # from backup file
            t=sample.pop(0)
            sleep(sampleRate/2) # simulate actual sample rate
        else:
            yield None
        x,y,z = sample[0], sample[1],sample[2]
        print (t,x,y,z)
        yield t,x,y,z


def run():
    """Use this code as the starting point 
    in scripts that import this module"""
    l=acc_data()
    while True:        
        print l.next()

if __name__ == '__main__':
    run()
