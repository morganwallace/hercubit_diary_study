from __future__ import division
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
from os.path import join
import csv
import time
from hercubit import settings
from hercubit.device import acc_data
# filename=join("labeled_data",raw_input("name this training set: "))
samples=[]

t0=time.time()
    # else: yield data_gen()
# data_gen.t = 0

fig, ax = plt.subplots()
lineX, = ax.plot([], [],"r-", lw=2)
lineY, = ax.plot([], [],"g-", lw=2)
lineZ, = ax.plot([], [],"b-", lw=2)

ax.set_ylim(-50000, 50000)
ax.set_xlim(0, 10)
ax.grid()
ax.set_xlabel('time (s)')
ax.set_ylabel('acceleration (g)')
tdata, xdata, ydata, zdata = [], [],[],[]
def run(data):
    global t0
    # update the data
    t,x,y,z = data
    #override t to be count of seconds
    t=time.time()-t0
    print (t,x,y,z)
    tdata.append(t)
    ydata.append(y)
    xdata.append(x)
    zdata.append(z)
    xmin, xmax = ax.get_xlim()

    if t >= xmax-1: #once the line get's 9 10ths of the way...
        #move the window by 5 seconds forward
        xmin+=5
        xmax+=5 
        ax.set_xlim(xmin, xmax)
        ax.figure.canvas.draw()
    lineX.set_data(tdata, xdata)
    lineY.set_data(tdata, ydata)
    lineZ.set_data(tdata, zdata)
    return lineX,lineY,lineZ



ani = animation.FuncAnimation(fig, run, acc_data, blit=False, interval=100,
    repeat=False)
plt.show()
