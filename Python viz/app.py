from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
import time


app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
device_data_generator=[]


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('bluetooth_conn', namespace='/test')
def bluetooth_conn():
	global device_data_generator
	print "user requested connection"
	from hercubit import device
	device_data_generator=device.acc_data()
	emit('connection established')

def get_data():
	while True:
		sample=device_data_generator.next()
		sample=str(sample)
		print sample
		emit('my response', {'data': sample})
@socketio.on('get_sample', namespace='/test')
def get_sample():
	global device_data_generator
	get_data()	


@socketio.on('stop', namespace='/test')
def test_message():
    # print message
	# session['receive_count'] = session.get('receive_count', 0) + 1
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
