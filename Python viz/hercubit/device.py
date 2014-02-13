import serial
from time import time
from time import sleep
import settings
from settings import ser

t0=time()

# print str(time()-t0)+" seconds for bluetooth to connect"


def acc_data():
    global t0
    # Ensure we don't read too fast
    while t0+settings.sampleRate>time():
        sleep(.005)
    t = time()
    t0=t
    x,y,z=get_data_from_serial()
    sample =(t,x,y,z)
    return sample


def get_data_from_serial():
    s=ser.readline()
    s=s.split(",")
    if len(s)!=3:
        return None
    for i in range(len(s)):
        try: s[i]=float(s[i].strip())
        except: return None
    x,y,z = s[0],s[1],s[2]
    # print str(x,y,z)
    return x,y,z

def run():
    """Use this code as the starting point 
    in scripts that import this module"""

    while True:
        l=acc_data()
        print l

if __name__ == '__main__':
    run()
