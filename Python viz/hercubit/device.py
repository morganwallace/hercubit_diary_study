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
        sleep(.10001)
    t0=time()
    # print "this prints"
    t,x,y,z=get_data_from_serial()
    sample =get_data_from_serial()
    print sample
    return sample


def get_data_from_serial():
    s=ser.readline()
    s=s.split(",")
    for i in range(len(s)):
        try: s[i]=float(s[i].strip())
        except: return None
    if len(s)>3:
        t=time()
        if len(s)==4:
            s=s[1:]
        x,y,z = s[0], s[1],s[2]
    # elif len(s)==4:
    #     t,x,y,z = s[0], s[1],s[2],s[3]
    else:
        return None
    return t,x,y,z

def run():
    """Use this code as the starting point 
    in scripts that import this module"""

    while True:
        l=acc_data()
        # print l

if __name__ == '__main__':
    run()
