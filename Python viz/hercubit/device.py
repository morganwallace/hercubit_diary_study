from __future__ import division
"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
import matplotlib.animation as animation
import serial
import time
import os
import pickle
from settings import *


data=[]
slopes=[]
start_time=time.time()


def get_data_from_serial():
    serialOutput=ser.readline()
    serialTuple=serialOutput.split(",")
    if len(serialTuple)!=3:
        return None
    for i in range(len(serialTuple)):
        try:serialTuple[i]=float(serialTuple[i].strip())
        except: return None
    x, y, z = serialTuple[0],serialTuple[1],serialTuple[2]
    t=time.time()
    return t,x,y,z


def get_slope(axis, samples=2):
    """returns the slope of the axis from the 
    second to last point to the current point"""
    global data
    rise=data[-1][axis] - data[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
    run=data[-1][0] - data[-samples][0] #time change
    return rise/run

reps=0
def rep_event(exer, root_times=(0,0)):
        """This is triggered when we have detected a rep.
        This function increments the rep count which is saved
        in a file accessible to our game running in Processing"""
        global data
        global reps
        del data[:-1]
        reps+=1
        print reps
        yield reps

peaks=0
prev_slope=0
peak,dip,peak_range=0,0,0
all_reps={"curls":0,"latRaise":0}
def detect_rep():
    """Use changes in slope to find peaks. 
    After a second peak is detected, trigger the rep_event function

    """
    global data,peak,dip,peak_range
    global prev_slope
    global peaks
    global reps
    #data  looks like [(.2,,5,-1.1,.4),(.4,,5,-1.1,.4),...]
    sample=data[-1]
    # initialize the data for the first sample
    if len(data)==1:
        peak,dip,peak_range=sample[dominant_axis],sample[dominant_axis],0

    else:
        if sample[dominant_axis]>peak:  
            peak=sample[dominant_axis]
            peak_range=peak - dip
        # dips
        if sample[dominant_axis]<dip:  
            dip=sample[dominant_axis]
            peak_range=peak - dip

    if len(data)>3:
        y_slope=get_slope(dominant_axis)
        # print str(y_slope)
        d_slope=prev_slope- y_slope
        if  peak_range>.8:
            if (prev_slope>0 and y_slope<0) or (prev_slope<0 and y_slope>0):
                print "peak with range: %f" % peak_range
                peaks+=1
                # print peaks
                if peaks==2:
                    if peak_range>.6: 
                        exercise="curl"
                        # print exercise
                        all_reps["curls"]+=1
                        print exercise + str(all_reps["curls"])
                    else: 
                        exercise="latRaise"
                        all_reps["latRaise"]+=1
                        print exercise + str(all_reps["curls"])
                    # print exercise
            # rep_event(exercise)
                    del data[:-1]
                    reps+=1
                    print reps
                    # print "test"
                    peaks=0
                    peak, dip,range_z=sample[dominant_axis],sample[dominant_axis], 0
        prev_slope=y_slope
        
print peaks
def main():
    global data
    global sampleRate
    global max_rep_window
    global reps
    global all_reps
    print 'test'
    #loops forever
    while True:
        #limit time for rep detection to 5 seconds
        if len(data)*sampleRate>=max_rep_window: 
            del data[0]
            
        #Get time, x, y, and z from serial port
        data.append(get_data_from_serial())
        print data
        if data:
            # last_read=time.time()
            detect_rep()
            # print str(time.time()-last_read)
        yield all_reps


if __name__ == '__main__':
    main()
    
