#!/usr/bin/env python
#coding: utf-8

import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "Fhf@4kVksDla1ehd"
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/mynamespace')
def connect():
    emit("response", {'data': 'Connected'})

@socketio.on('disconnect', namespace='/mynamespace')
def disconnect():
    session.clear()
    print "Disconnected"

@socketio.on("request", namespace='/mynamespace')
def request(message):
    emit("response", {'data': message['data'], broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
