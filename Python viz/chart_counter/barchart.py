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
######  Preferences Variables  ######
sampleRate=.1 #this is set by the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3

# ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
ser = serial.Serial('/dev/tty.OpenPilot-BT-DevB', 57600)

def get_data_from_serial():
    global ser
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

def data_gen():
    global reps
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
        if  peak_range>.6:
            if (prev_slope>0 and y_slope<0) or (prev_slope<0 and y_slope>0):
                print "peak with range: %f" % peak_range
                peaks+=1
                # print peaks
                if peaks==2:
                    if peak_range>1.20: 
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
        data.append(get_data_from_serial())
        # print data
        if data:
            # last_read=time.time()
            detect_rep()
            # print str(time.time()-last_read)
        yield all_reps
        


# # rects = plt.bar(index, sets, bar_width,
# #                  alpha=opacity,
# #                  color='r',
# #                  error_kw=error_config,
# #                  label='Curls')
# rect=plt.bar(1,1,bar_width)
# # rect2, = ax.plot([], [],"g-", lw=2,label="Y")
# # rect3, = ax.plot([], [],"b-", lw=2,label="Z")
# # legend=plt.legend()
# ax.set_ylim(0, 20.0)
# ax.set_xlim(0, 1)
# ax.set_xlabel('Sets')
# ax.set_ylabel('Reps')
# tick_labels = tuple(["Set"+ str(i+1) for i in range(1)])
# # plt.xticks(index + bar_width, tick_labels)
# ax.set_title("Daily workout - Curls")

# last_rep=0
# def run(reps):
#     # global rect.
#     # # global sets, opacity, error_config,bar_width,index
#     # global last_rep
#     # # update the data
#     # # print "running"
#     # # if sets[0]!=reps:
#     # #     sets[0]=reps
#     # #     rects = plt.bar(index, sets, bar_width,
#     # #                  alpha=opacity,
#     # #                  color='b',
#     # #                  error_kw=error_config,
#     # #                  label=reps)

#     # if last_rep!=reps:
#     #     last_rep=reps
#     return plt.bar(1,reps,bar_width)
#         # return rects
# ani = animation.FuncAnimation(fig, run, main, blit=False, interval=10, repeat=False)
# plt.show()
# if __name__ == '__main__':
#     main()


fig,ax = plt.subplots()

sets=[0,0]
n_groups = 2

#goal line
goal=10
plt.plot([0, n_groups], [goal, goal], color='g', linestyle='--', linewidth=2)

index = np.arange(n_groups)
bar_width = 0.5
error_config = {'ecolor': '0.3'}
opacity = 1
rects = plt.bar(index, sets, bar_width,
                 color='r',
                 error_kw=error_config,
                 label='Curls')
# rect=plt.bar(1,0,bar_width)
# rect2, = ax.plot([], [],"g-", lw=2,label="Y")
# rect3, = ax.plot([], [],"b-", lw=2,label="Z")
# legend=plt.legend()
ax.set_ylim(0, 15.0)
ax.set_xlim(0, n_groups)
ax.set_xlabel('Sets')
ax.set_ylabel('Reps')
plt.xticks(index + bar_width, ('Bicep Curl', 'Lateral Raise', 'C', 'D', 'E'))
ax.set_title("Daily workout - Curls")
sets=[]
last_rep=[0,0]
def run(reps):
    global sets, error_config,bar_width, last_rep
    # update the data
    # sets[0]=reps
    if all_reps['curls']>last_rep[0]:
        last_rep[0]=all_reps['curls']
        rects = plt.bar(index+.25, [all_reps['curls'],all_reps['latRaise']], bar_width,
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


