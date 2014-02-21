from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
import time


app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
	print "what"
	from hercubit import device
	while True:
		
		# now=time.time()
		sample=device.acc_data()
		# print sample
		session['receive_count'] = session.get('receive_count', 0) + 1
		emit('my response', {'data': sample, 'count': session['receive_count']})
		time.sleep(1)

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    # print message
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response',
	     {'data': message['data'], 'count': session['receive_count']},
	     broadcast=True)



@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
