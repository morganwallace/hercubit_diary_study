# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/python
import serial
import time
import json
from wsgiref.handlers import CGIHandler
import flask
from flask import Flask
from flask import render_template
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

app = Flask(__name__)
app.debug = True






@app.route('/')
def index():
    return flask.jsonify({"raw":[(30,40,50)],"reps":4})


if __name__ == "__main__":
     app.run()



