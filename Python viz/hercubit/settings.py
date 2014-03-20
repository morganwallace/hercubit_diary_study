#Settings for Hercubit

import os
import serial
from platform import system
conn_type=""
####  #Serial Connection
# bluetooth
global ser
# print serial.tools.list_ports()
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
			SERIAL_PORTS=['/dev/tty.HC-06-DevB-1','/dev/tty.OpenPilot-BT-DevB','/dev/tty.HC-06-DevB']
			SERIAL_SPEED=57600
			for port in SERIAL_PORTS:
				try:
					ser = serial.Serial(port, SERIAL_SPEED)
					print"\nBluetooth Connected!"
					conn_type="bluetooth"
					SERIAL_PORT=port
					break
				except:
					pass
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
	backup_path=os.path.join('Python viz','saved_animations_and_data','backup','2014-03-14__15-36-14_bicep curl.csv')
	if os.getcwd()[os.getcwd().rfind('/'):]=='/Website2':	
		archive=os.path.join(os.path.dirname(os.getcwd()),backup_path)
		archive_data=open(archive)
	else:
		archive=os.getcwd()
		while archive[archive.rfind('/'):] != '/Fitness-Tracking':
			archive=os.path.dirname(archive)
			
		archive=os.path.join(archive,backup_path)
		archive_data=open(archive)
	print archive



# Note : bluetooth pairing code is '1234'

######  Peak Detection Preference Variables  ######
sampleRate=.100 #this should match the rate from the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second
dominant_axis=3