from flask import Flask, redirect, request, render_template, session
from flask.ext.session import Session
import secrets

### APP INTERNALS ###
app = Flask(__name__, static_url_path="")
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
	
Session(app)

### GLOBALS ###
project = None
numPoints = 0
tSeries = {}
fSeries = {}


# main route for dashboard
@app.route('/')
def home():
	print numPoints
	print tSeries
	return app.send_static_file('index.html')


# create new project for measurements
@app.route('/new', methods=["POST"])
def new():
	if session.get('robot'):
		if request.form.get("name"):
			project = request.form.get("name")
			numPoint = 0
			tSeries.clear()
			fSeries.clear()
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
			tSeries[coords] = frames
			return "Success"
	return "Failure"


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
