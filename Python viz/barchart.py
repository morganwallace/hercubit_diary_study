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
import hercubit.settings as settings
import hercubit.device as device

'''
#################################################

1. Process the buffer in the Serial port from the
accelerometer to find peaks.

2. Send peak data (timing) to another Serial port
so that Processing can read it in real-time
#################################################
'''
data=[]
slopes=[]
start_time=time.time()

# ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
# bluetooth pairing code is '1234'


sampleRate=.1 #this should match the rate from the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3


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
        

def main():
    global data
    global sampleRate
    global max_rep_window
    global reps
    global all_reps

    #loops forever
    while True:
        #limit time for rep detection to 5 seconds
        if len(data)*sampleRate>=max_rep_window: 
            del data[0]
            
        #Get time, x, y, and z from serial port
        data.append(device.acc_data())
        # print data
        if data:
            # last_read=time.time()
            detect_rep()
            # print str(time.time()-last_read)
        yield all_reps
        


fig,ax = plt.subplots()

sets=[0]
n_groups = 1

#goal line
goal=10
plt.plot([0, n_groups], [goal, goal], color='g', linestyle='--', linewidth=2)

index = np.arange(n_groups)
bar_width = 0.5
error_config = {'ecolor': '0.3'}
opacity = 1
rects = plt.bar(index, sets, bar_width,
                 color='r',
                 error_kw=error_config)
# rect=plt.bar(1,0,bar_width)
# rect2, = ax.plot([], [],"g-", lw=2,label="Y")
# rect3, = ax.plot([], [],"b-", lw=2,label="Z")
# legend=plt.legend()
ax.set_ylim(0, 15.0)
ax.set_xlim(0, n_groups)
ax.set_xlabel('Sets')
ax.set_ylabel('Reps')
plt.xticks(index + bar_width, ('Bicep Curl'))
ax.set_title("Daily workout - Curls")
sets=[]
last_rep=[0,0]
def run(reps):
    global sets, error_config,bar_width, last_rep
    # update the data
    # sets[0]=reps
    if all_reps['curls']>last_rep[0]:
        last_rep[0]=all_reps['curls']
        rects = plt.bar(index+.25, [all_reps['curls']], bar_width,
                     color='r',
                     error_kw=error_config,
                     label=reps)
        # return plt.bar(1,reps,bar_width)
        return rects
    elif all_reps['latRaise']>last_rep[1]:
        last_rep[1]=all_reps['latRaise']
        rects = plt.bar(index+.25, [all_reps['curls'],all_reps['latRaise']], bar_width,
                     color='r',
                     error_kw=error_config,
                     label=reps)
        # return plt.bar(1,reps,bar_width)
        return rects

ani = animation.FuncAnimation(fig, run, main, blit=False, interval=10,
repeat=True)
plt.show()

if __name__ == '__main__':
    main()


