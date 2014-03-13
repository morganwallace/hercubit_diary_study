#Settings for Hercubit

import os
import serial
from platform import system
conn_type=""
####  #Serial Connection
# bluetooth
global ser
if system()== 'Darwin': # Mac OSX
	
	### FIRST TRY USB
	# USB
	possible_USBs=["/dev/tty.usbmodem1421","/dev/tty.usbmodem1411","/dev/tty.usbmodem1422","/dev/tty.usbmodemfd121","/dev/tty.usbmodemfd111","/dev/tty.usbmodemfd122"]
	for usb_path in possible_USBs:
		if os.path.exists(usb_path):
			print "Attempting to connect to "+usb_path+"...\n"
			SERIAL_PORT=usb_path
			SERIAL_SPEED=9600
			ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
			conn_type="usb"
	if conn_type=="":
		print "No USB connection"
		try:
			#Bluetooth
			print "Attempting to connect to bluetooth...\n"
			SERIAL_PORT='/dev/tty.OpenPilot-BT-DevB'

			SERIAL_SPEED=57600
			ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
			print"\nBluetooth Connected!"
			conn_type="bluetooth"
		except:
			pass


elif system() =="Windows": # Windows * CHARLES- PLEASE FILL THIS IN
	try:
		# Bluetooth
		pass
	except:
		# USB
		pass


	
# print type(ser)
	
try:
	ser
	print "using serial port:  " + SERIAL_PORT
except:
 #if no serial connection available simulate with old file
	# import pickle
	print "\nNo serial connection available. Falling back on archived data..."
	conn_type="archive"
	from time import sleep
	# sleep(1)
	if os.getcwd()[os.getcwd().rfind("/"):] == "/hercubit":
		archive=os.path.join("..","saved_animations_and_data","backup")
	else:
		archive=os.path.join("saved_animations_and_data")
	for arch_folder in os.listdir(archive):
		if arch_folder[0] != ".":
			selected_archive=os.path.join(archive, arch_folder)
			for arch_file in os.listdir(selected_archive):
				if arch_file[-4:]==".csv": # if you find a python pickle file
					pickled_file=os.path.join(selected_archive,arch_file)
					print "using archive file: "+pickled_file+"\n"
					# sleep(1)
					ser = open(pickled_file)
					ser.readline()
					
					#break out of for loops, just getting the first csv file
					break
			break
	# type(ser)
####


# Note : Morgan's bluetooth pairing code is '1234'

######  Peak Detection Preference Variables  ######
sampleRate=.100 #this should match the rate from the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3