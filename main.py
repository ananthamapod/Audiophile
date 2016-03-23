import serial
from plotter import Plotter
from agent import Agent
from audio import Audio
from operator import itemgetter
import time

def handshake(ser):
    """ Serial handshake with Arduino to get the connection going """
    if ser.readline():
        print 'arduino connection established'
        print 'responding ...'
        ser.write('B')
        # wait for serial handshake to register
        time.sleep(2)

def act(intention, ser, audio, plotter):
    """ Deciphers intended action from intention, writes to serial,
    records audio, and plots respectively based on action parameters """
    c = intention.command
    v = intention.value
    print c
#    if c = "TURN":
#        ser.write("T: " + str(v))
#    elif c = "MOVETO":
#        ser.write()

def run(ser, audio, agent, plotter):
    """ Running loop """
    inputs = ser.readline()
    try:
        """ Wrap in a try-except block to catch malformed serial communications
        or empty lines """
        inputs = inputs.split(" ")
        l = inputs[0]
        f = inputs[1]
        r = inputs[2]
        encoders = inputs[3:]
        plotter.updatePlot(l, f, r)
        percepts = agent.perceive(l=l,f=f,r=r,encoders=encoders)
        intentions = agent.deliberate(percepts)
        for i in intentions:
            act(i, ser, audio, plotter)
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
    return ser, audio, agent, plotter

def finish(audio):
    """ Takes all the recorded frames and plots them by coordinate """
    frames = audio.getFrames()
    coordinates = sorted(frames.keys(), key=itemgetter(0,1))


if __name__ == "__main__":
    """ Tests entire setup """
    ser, audio, agent, plotter = setup()
    handshake(ser)

    while True:
        try:
            run(ser, audio, agent, plotter)
        except KeyboardInterrupt:
            break

    finish(audio)
