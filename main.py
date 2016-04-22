from flask import Flask, redirect, request, render_template

### APP INTERNALS ###
app = Flask(__name__, static_url_path="")

### GLOBALS ###
project = None
numPoints = 0
tSeries = {}
fSeries = {}


# main route for dashboard
@app.route('/')
def home():
	return app.send_static_file('index.html')


# create new project for measurements
@app.route('/new', methods=["POST"])
def new():
	if request.form.get("name"):
		project = request.form.get("name")
		numPoint = 0
		tSeries.clear()
		fSeries.clear()
		return 'Success'
	return redirect('/')


# login for the robot
@app.route('/login', methods=["GET","POST"])
def login():
	if request.form.get("id"):
		return "Welcome"
	
	return redirect("/")


# route for the robot to add data for the project
@app.route('/addFrames', methods=["POST"])
def frames():
	pass


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
