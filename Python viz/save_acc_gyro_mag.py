from __future__ import division
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cPickle as pickle
from os.path import join
import os
import csv
import time
from hercubit import settings
from hercubit.device import sensor_stream
# filename=join("labeled_data",raw_input("name this training set: "))
samples=[]


    # else: yield data_gen()
# data_gen.t = 0



userName="Lazar"
# userName= raw_input("userName: ")
exerciseType="shoulder"



fig, ax = plt.subplots(3, sharex=True)
# fig.set_size_inches(10.5,10.5)
fig.subplots_adjust(hspace=.10)
plots={'accel':ax[0],'gyro':ax[1],'magnet':ax[2]}

#Setup lines in graph
sensors=('accel','gyro','magnet')
axes=('x','y','z')
colors=('-r','-g','-b')
lines={}
for sensor in sensors:
    lines[sensor]={}
    for axis in axes:
        i=axes.index(axis)
        # print sensor+"("+axis+") : "+colors[i]
        lines[sensor][axis]=ax[sensors.index(sensor)].plot([], [],colors[i], lw=1)

#set up maximum allowed time for exercise 
max_time=25

for i in range(len(axes)):
    ax[i].grid()
    ax[i].set_xlim(0, max_time)

ax[0].set_ylim(-2, 2)
ax[1].set_ylim(-30000, 30000)
ax[2].set_ylim(-2000, 2000)


ax[0].set_ylabel('acceleration (g)')
ax[1].set_ylabel('gyro (degrees/sec)')
ax[2].set_ylabel('magnetometer')
ax[2].set_xlabel('time (s)')

tdata=[]
all_data={}
for sensor in sensors:
    all_data[sensor]={'x':[],'y':[],'z':[]}




# variables for saving
now = time.strftime("%Y-%m-%d__%H-%M-%S")
dirname=join("saved_animations_and_data",now+"_"+exerciseType+"_"+userName)
filename=now+"_"+exerciseType
os.mkdir(dirname)
def save(all_data,tdata):
    '''Save csv and png of sampled data
    '''
    global dirname, sensors, axes, userName
    global filename

    #samples should equal list of tuples of the data
    samples=[]
    for i in range(len(tdata)):
        row = [userName,exerciseType,0]
        row.append(tdata[i])
        for sensor in sensors:
            for axis in axes:
                row.append(all_data[sensor][axis][i])
        samples.append(row)

    # try:
        
    # except:
    #     pass
    picpath=join(dirname,exerciseType+".png")
    plt.savefig(picpath,dpi=200)
    pickle.dump(samples,open(os.path.join(dirname,filename+".p"),"wb"))
    with open(join(dirname,filename+".csv"),"wb") as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(['User','exerciseType','rep_count',"t (sec)","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z","magnet_x","magnet_y","magnet_z"]) #header
        for i in samples:
            writer.writerow((i))
    settings.ser.close()
    quit()

t0=0
def run(data):
    global t0, lines, test
    if t0==0: t0=time.time()
    # print data
    #override t to be count of seconds
    t=time.time()-t0
    tdata.append(t)

    for sensor in all_data:
        for axis in all_data[sensor]:
            if axis=="x":i=0
            if axis=="y":i=1
            if axis=="z":i=2
            # if test==0: print sensor+" ("+axis+")"
            all_data[sensor][axis].append(data[sensor][i])
            lines[sensor][axis][0].set_data(tdata, all_data[sensor][axis])
    # all_lines=[[axis for axis in sensor.values()] for sensor in lines.values()]
    # test=1
    #MOVING WINDOW
    xmin, xmax = ax[0].get_xlim()
    if t>=max_time:
        save(all_data,tdata)


    return None
# print list(plt.xticks()[0]) 
# new_ticks=range(max_time*2)
# for i in range(len(new_ticks)):
#     new_ticks[i]= new_ticks[i]/2
# plt.xticks(list(plt.xticks()[0]) + new_ticks)
ani = animation.FuncAnimation(fig, run, sensor_stream, blit=False, interval=100,
    repeat=False)

plt.show()
