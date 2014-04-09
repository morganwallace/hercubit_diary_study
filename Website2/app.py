from flask import Flask, render_template, session, request, make_response, jsonify
from flask.ext.socketio import SocketIO, emit
import time
import os
import sys
import hercubit
import urllib2,json



app = Flask(__name__)
app.debug=True  # Disable this before distributing
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
device_data_generator=[]
DEVICE_CONNECTED=False

# Fusion Tables constants
exerciseTableId = "1OBObNVqy3kHdpdDaGaC1xH5sfmGWb-oGBNfosOMo";
goalTableId = "1R8s9_P6t9IH8DOG3rBieAh05W9_H5C2K4MdQCuRG";
scopes = 'https://www.googleapis.com/auth/fusiontables';
clientId = '755998331131-jsf1f67tj7ojvlc9bai1p6273qidsbn5.apps.googleusercontent.com';
# apiKey = 'AIzaSyD1nrNVFFr6z0_S9vOryX9kF7U-7pVZDBU'; //charles
apiKey = "AIzaSyA8juHC7LiH4pY4HM3XPIUTuFFt6y2jWqU"

########################
# Normal web server stuff

@app.route('/')
def index():
	#show cookie in terminal
	app.logger.debug("Cookie:\n"+str(request.cookies))

	if 'username' in request.cookies:
		username = request.cookies.get('username')
		print username
		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/getAllGoals.php?username="+username
		response = urllib2.urlopen(url)
		goals = json.load(response)
	else: 
		print "else"
		username = ""
		goals = ""

	return render_template('index.html',username=username,month=time.strftime("%B"),goals=goals)


@app.route('/signup', methods=['POST'])
def signup():
	print 'test'
	username = request.form['username']
	# email= request.form['signup-email']
	app.logger.debug("signup completed for username: " + username)
	resp = make_response(jsonify(username=username))
	# This is where we would create a new user in fusion tables
	#
	resp.set_cookie('username', username)
	return resp

@app.route('/logout', methods=['POST'])
def logout():
	if 'username' in request.cookies:  
		resp = make_response(jsonify(success=True, type='logout'))
		resp.set_cookie('username', '')
		return resp
	else:
		resp = make_response(jsonify(success=False, type='logout'))
		return resp 
	# app.logger.debug("Cookie:\n"+str(request.cookies))
	# resp = make_response(jsonify(username="blerg"))
	# resp.delete_cookie("username","blerg",domain=".app.localhost")
	# app.logger.debug(resp)
	# return resp


########################
# connection to the db server
@app.route('/addGoal', methods=['POST'])
def addGoal():
	print 'addGoal'
	if 'username' in request.cookies: 
		username = request.cookies.get('username')

		exerciseType = request.form['exerciseType']
		exerciseCount = request.form['exerciseCount']
		exerciseWeight = request.form['exerciseWeight']
		if exerciseType==0:
			exerciseType = "Bisep curl"
		elif exerciseType==1:
			exerciseType = "Trisep curl"
		else:
			exerciseType = "Shoulder"

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/insertNewGoal.php?username="+username+"&exercise="+exerciseType+"&count="+exerciseCount+"&weight="+exerciseWeight
		response = urllib2.urlopen(url)
		insertStatus = json.load(response)

	resp = make_response(jsonify(username=username))
	return resp

@app.route('/deleteGoal', methods=['POST'])
def deleteGoal():
	print 'deleteGoal'
	if 'username' in request.cookies:
		
		username = request.cookies.get('username')
		print username

		goalId = request.form['id'][5:]
		print goalId

		url = "http://people.ischool.berkeley.edu/~katehsiao/hercubit-db/deleteGoal.php?id="+goalId
		response = urllib2.urlopen(url)
		deleteStatus = json.load(response)

	resp = make_response(jsonify(username=username))
	return resp



########################
# connection with device

@app.route('/debug')
def debug():
    return render_template('web_socket_debug.html')


@socketio.on('bluetooth_conn', namespace='/test')
def bluetooth_conn():
	global device_data_generator, DEVICE_CONNECTED
	print "user requested connection"
	DEVICE_CONNECTED=True
	from hercubit import device
	device_data_generator=device.sensor_stream()#simulate_sample_rate=False
	from hercubit.settings import sampleRate
	emit('connection established',{'sample_rate': sampleRate*1000})


# Retrieve the data from device
@socketio.on('get_sample', namespace='/test')
@app.route('/getsample')
def get_sample():
	global device_data_generator
	from hercubit import rep_tracker
	if DEVICE_CONNECTED==True:
		sample=device_data_generator.next()
		print sample #uncomment to see raw output
		count=rep_tracker.live_peaks(sample)
		if count!=None:
			emit('device response', {'data': count})


@socketio.on('stop', namespace='/test')
def stop():
	global DEVICE_CONNECTED
	DEVICE_CONNECTED=False
	from hercubit.settings import ser
	ser.close()
	print "stopped"
	emit('Bluetooth Connection Stopped')


@socketio.on('web_socket_connected', namespace='/test')
def test_connect():
	print "connected"
	emit('connect', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')



    

if __name__ == '__main__':
    import webbrowser
    if app.debug!=True:
    	webbrowser.open_new_tab('http://localhost:5000')
    socketio.run(app)
    

