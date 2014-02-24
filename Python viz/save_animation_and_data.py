from __future__ import division
import time
# import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
import matplotlib.animation as animation
import pickle
import os
import csv
from hercubit.settings import *
from hercubit.device import acc_data
device_sample_generator = acc_data()


### ADJUST THESE VARIALBES ###
#
exerciseType="curls"
runningTime=1 #seconds
movingWindow=False
#
###

now = time.strftime("%Y-%m-%d__%H-%M-%S")
dirname=os.path.join("saved_animations_and_data",now+"_"+exerciseType)
filename=now+"_"+exerciseType

#Initialized variables
samples=[]

fig,ax = plt.subplots()

# fig = matplotlib..figure.Figure(figsize=(8,6))
tdata, xdata, ydata, zdata = [], [],[],[]

    #Vizualization parameters
lineX, = ax.plot([], [],"r-", lw=2,label="X")
lineY, = ax.plot([], [],"g-", lw=2,label="Y")
lineZ, = ax.plot([], [],"b-", lw=2,label="Z")
legend=plt.legend()
ax.set_ylim(-1.0, 1.0)
ax.set_xlim(0, runningTime)
if movingWindow==True: ax.set_xlim(0, 20)
ax.grid()
ax.set_xlabel('time (s)')
ax.set_ylabel('acceleration (g)')
ax.set_title(exerciseType)

xs=[]
ys=[]
zs=[]


def save(samples):
    '''Save csv and png of sampled data
    '''
    global dirname
    global filename
    os.mkdir(dirname)
    picpath=os.path.join(dirname,exerciseType+".png")
    plt.savefig(picpath)
    pickle.dump(samples,open(dirname+"/"+filename+".p","wb"))
    with open(dirname+"/"+filename+".csv","wb") as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(["t (sec)","x","y","z"]) #header
        for i in samples:
            writer.writerow((i))


t0=time.time()
def run(data):
    # update the data
    global movingWindow
    global t0

    # EXIT sceanario 
    if t0+runningTime<=time.time():
        ser.close()
        save(samples)

    t,x,y,z = data
    t=t-t0
    tdata.append(t)
    ydata.append(y)
    xdata.append(x)
    zdata.append(z)
    xmin, xmax = ax.get_xlim()
    if movingWindow==True:
        if t >= xmax-1: #once the line get's halfway...
            #move the window by 1/20th of a second forward
            xmin+=5
            xmax+=5 
            ax.set_xlim(xmin, xmax)
            ax.figure.canvas.draw()
    lineX.set_data(tdata, xdata)
    lineY.set_data(tdata, ydata)
    lineZ.set_data(tdata, zdata)
    return lineX,lineY,lineZ



ani = animation.FuncAnimation(fig, run, acc_data, blit=False, interval=10,
    repeat=False)


# save a video of this animation
# ani.save("test.mp4")
plt.show()


