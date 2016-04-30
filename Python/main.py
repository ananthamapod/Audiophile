from flask import Flask, redirect, request, render_template, session
from flask.ext.session import Session
import secrets
from datetime import datetime
import os
import json
from audio import FFT

### APP INTERNALS ###
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, static_url_path="", template_folder=tmpl_dir)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

### GLOBALS ###
project = None
numPoints = 0
tSeries = {}
fSeries = {}
startTime = None


# main route for dashboard
@app.route('/')
def home():
	print numPoints
	return render_template('home.html',pName='Rutgers Day Demo',numPoints=numPoints, start=startTime, fData=fSeries)


# create new project for measurements
@app.route('/new', methods=["POST"])
def new():
	global startTime
	if session.get('robot'):
		if request.form.get("name"):
			project = request.form.get("name")
			numPoint = 0
			tSeries.clear()
			fSeries.clear()
			startTime = datetime.now()
			return 'Success'
	return 'Failure'


# login for the robot
@app.route('/login', methods=["GET","POST"])
def login():
	if request.form.get("id"):
		# very simple single key based authentication scheme
		print request.form.get("id")
		if str(request.form.get("id")) == secrets.robot_id:
			session['robot'] = True
			return "Welcome"
	return redirect("/")


# route for the robot to add data for the project
@app.route('/add', methods=["POST"])
def frames():
	global numPoints
	global tSeries
	if session.get('robot'):
		coords = request.form.get('coords')
		frames = request.form.get('tSeries')
		if coords and frames:
			if not tSeries.get(coords):
				numPoints += 1
			tSeries[coords], fSeries[coords] = FFT(frames)
			return "Success"
	return "Failure"


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
