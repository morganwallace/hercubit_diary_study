from hercubit import peak_detect
from time import sleep


print "hi"

r=peak_detect.reps
while True:
	peak_detect.detect_rep()
	if  peak_detect.reps is not None:
	# if peak_detect.reps!=r:
		r= peak_detect.reps
		print r
	# if peak_detect.reps!=r:
	# 	r=peak_detect.reps
	# 	print r