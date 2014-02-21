#Settings for Hercubit

import os

####  #Serial Connection
# bluetooth
try: # Mac OSX
	try:
		#Bluetooth
		SERIAL_PORT='/dev/tty.OpenPilot-BT-DevB'

		SERIAL_SPEED=57600
	except:
		# USB
		try:
			SERIAL_PORT='/dev/tty.usbmodem1421'
			SERIAL_SPEED=9600
		except:
			SERIAL_PORT='/dev/tty.usbmodem1422'
			SERIAL_SPEED=9600

except: # Windows * CHARLES- PLEASE FILL THIS IN
	try:
		# Bluetooth
		pass
	except:
		# USB
		pass
print "using serial port:  " + SERIAL_PORT

import serial
ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
####


# Note : Morgan's bluetooth pairing code is '1234'

######  Peak Detection Preference Variables  ######
sampleRate=.1 #this should match the rate from the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3