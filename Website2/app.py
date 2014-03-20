from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
import time
import os
import sys
#import hercubit module from Python viz directory
hercubit_path=os.path.join(os.path.dirname(os.getcwd()),'Python viz')
sys.path.append(hercubit_path)
import hercubit

app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
device_data_generator=[]
DEVICE_CONNECTED=False


@app.route('/')
def index():
    return render_template('index.html')

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
	if DEVICE_CONNECTED==True:
		global device_data_generator
		try:
			sample=device_data_generator.next()
		except:
			stop()
			return None
		sample=str(sample)
		print sample
		emit('device response', {'data': sample})



@socketio.on('stop', namespace='/test')
def stop():
	global DEVICE_CONNECTED
	DEVICE_CONNECTED=False
	hercubit.settings.ser.close()
	emit('Bluetooth Connection Stopped')


@socketio.on('web_socket_connected', namespace='/test')
def test_connect():
	print "connected"
	emit('connect', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
    

if __name__ == '__main__':
    socketio.run(app)
