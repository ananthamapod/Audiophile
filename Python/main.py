import serial
from analysis.plotter import Plotter
from agent import Agent
from analysis.audio import Audio
from client import Audiophile_Client
from operator import itemgetter
import time
import math

def handshake(ser):
    """ Serial handshake with Arduino to get the connection going """
    if ser.readline():
        print 'arduino connection established'
        print 'responding ...'
        ser.write('B')
        # wait for serial handshake to register
        time.sleep(2)

def act(intention, ser, audio, plotter, client):
	""" Deciphers intended action from intention, writes to serial,
    records audio, and plots respectively based on action parameters """
	c = intention.command
	v = intention.value
	if c == "RECORD":
		print("3")
		time.sleep(0.5)
		print("2")
		time.sleep(0.5)
		print("1")
		time.sleep(0.5)
		audio.record(v)
		r = client.send_data(audio.get_frames(v), v)
		if r == "Failure":
			client.connect()
			client.send_data(audio.get_frames(v), v)
#    if c == "TURN":
#        ser.write("T: " + str(v))
#    elif c = "MOVETO":
#        ser.write()

def run(ser, audio, agent, plotter, client):
    """ Running loop """
    inputs = ser.readline()
    try:
        """ Wrap in a try-except block to catch malformed serial communications
        or empty lines """
        inputs = inputs.split(" ")
        l = inputs[0]
        f = inputs[1]
        r = inputs[2]
#        encoders = inputs[3:]
        plotter.updatePlot(l, f, r)
        percepts = agent.perceive(l=l,f=f,r=r)#encoders=encoders)
        intentions = agent.deliberate(percepts)
        for i in intentions:
            act(i, ser, audio, plotter, client)
    except:
        print inputs

def setup():
	""" Overall setting up - setting up serial connnection, set up
    audio, agent, plotter, and other essentials """
	ser = serial.Serial('/dev/ttyACM0', 9600)
	handshake(ser)
	audio = Audio()
	agent = Agent()
	plotter = Plotter()
	plotter.configurePlots()
	client = Audiophile_Client()
	return ser, audio, agent, plotter, client

def finish(audio):
    """ Takes all the recorded frames and plots them by coordinate """
    #frames = audio.getFrames()
    #coordinates = sorted(frames.keys(), key=itemgetter(0,1))
    pass


def robot_stop(currSpeed, ser):
	while currSpeed is not 0:
		currSpeed = int(math.floor(currSpeed - (currSpeed)/3.))
		if currSpeed < 40:
			currSpeed = 0
		ser.write("FORWARD " + str(currSpeed))
		print "s" + str(currSpeed)
		time.sleep(2)
	ser.write("STOP")
	return currSpeed

def robot_go(currSpeed, ser):
	if currSpeed is not 100:
		currSpeed = max(currSpeed, 40)
	while currSpeed is not 100:
		currSpeed = int(math.ceil(currSpeed + (100-currSpeed)/3.))
		ser.write("FORWARD " + str(currSpeed))
		print "g" + str(currSpeed)
		time.sleep(2)
	return currSpeed

def robot_turn(angle, ser):
	if angle > 0:
		ser.write("RIGHT 60")
	else:
		ser.write("LEFT 60")
	time.sleep(1)
	return

if __name__ == "__main__":
	""" Tests entire setup """
	ser, audio, agent, plotter, client = setup()
	handshake(ser)
	audio.open_mic()
	client.connect()

	# real loop for doing things the right way
	"""
	while True:
        try:
            run(ser, audio, agent, plotter, client)
        except KeyboardInterrupt:
            break
	"""
	currSpeed = 0
	"""
	while True:
		inputs = ser.readline()
		op = raw_input("command: ")
		if op.lower() == "w":
			currSpeed = robot_go(currSpeed, ser)
		elif op.lower() == "a":
			robot_turn(-90, ser)
		elif op.lower() == "s":
			currSpeed = robot_stop(currSpeed, ser)
		elif op.lower() == "d":
			robot_turn(90, ser)
		else:
			robot_stop(currSpeed, ser)
			break
	"""
	#for j in range(2):
	for i in range(4):
		currSpeed = robot_go(currSpeed, ser)
		currSpeed = robot_stop(currSpeed, ser)
		print("3")
		time.sleep(0.5)
		print("2")
		time.sleep(0.5)
		print("1")
		time.sleep(0.5)
		#coords = (j, i)
		coords = i
		audio.record(coords)
		r = client.send_data(audio.get_frames(coords), coords)
		if r == "Failure":
			client.connect()
			client.send_data(audio.get_frames(coords), coords)

	finish(audio)
