#Settings for Hercubit

MICRO_CONTROLLER="Arduino Micro"

####  #Serial Connection
# bluetooth
SERIAL_PORT='/dev/tty.OpenPilot-BT-DevB'
SERIAL_SPEED=57600
#
# usb
#SERIAL_PORT='/dev/tty.usbmodem1421'
#SERIAL_SPEED=9600
#
import serial
from time import time
start_time=time()
ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
print str(time()-start_time)+" seconds for bluetooth to connect"
####


# Note : bluetooth pairing code is '1234'

######  Preferences Variables  ######
sampleRate=.1 #this should match the rate from the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3