#!/usr/bin/python
import serial
import json
from wsgiref.handlers import CGIHandler
import flask
from flask import Flask
from flask import render_template
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from hercubit import peak_detect





app = Flask(__name__)
app.debug = True

r=peak_detect.reps

@app.route('/')
def index():
	global r
	print "whatever"
	while True:
		print "looking for rep now"
		peak_detect.detect_rep()
		if  peak_detect.reps is not None:
		# if peak_detect.reps!=r:
			r= peak_detect.reps
			print r
			return flask.jsonify({"raw":[(30,40,50)],"reps":r})

	

if __name__ == "__main__":
	app.run()


