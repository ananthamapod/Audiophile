import constants
from percept import Percept
from intention import Intention
from collections import deque
import math
import datetime

class Agent(object):
    """Main Agent class, handles all interactions with percepts, intentions,
    and actions, as well as access to outward facing interface
    for sensors and actuators"""
    def __init__(self):
        super(Agent, self).__init__()
        self.states = {'orient','move', 'measure'}
        self.leftStore = deque([None] * 20, maxlen=20)
        self.rightStore = deque([None] * 20, maxlen=20)
        self.frontStore = deque([None] * 20, maxlen=20)
        self.currState = 'orient'
        self.prevTime = datetime.datetime.now()
        self.prevLeft = 0
        self.prevRight = 0
        self.currLeft = None
        self.currRight = None
        self.currPos = 0
        self.currTurn = 0
        self.currAngle = 0
        self.targetSpeed = 0
        self.targetAngle = 0

    def perceive(self, **kwargs):
        """ Interprets sensations as percepts about the agent's world,
        returns list of percepts """
        percepts = []
        def setup():
            if leftStore[0] is None:
                leftStore.append(kwargs.get('l'))
                frontStore.append(kwargs.get('f'))
                rightStore.append(kwargs.get('r'))
                percepts.append(Percept())
                return percepts
            print "Perceiving ..."
            #encoders = kwargs.get('encoders')
            encoders = [self.prevLeft, self.prevRight]
            if encoders:
                print encoders
                left, right = encoders
                if left < right+constants.epsilon and left > right-constants.epsilon:
                    percepts.append(Percept('speed', left))
                else:
                    # Governing turning equation:
                    # d_theta_Tank/d_t = L/2 (R d_theta_left/d_t) - L/2 (R d_theta_right/d_t)
                    percepts.append(Percept('turn', (constants.L*constants.R/2.0)*(left-right)))

        return percepts

    def deliberate(self, percepts):
        """ Deliberates upon percepts, decides on course of actions,
        and generates and returns list of intentions """
        intentions = []
        for p in percepts:
            if p.description is not "Empty":
                if p.description is "speed":
                    if p.value is not self.targetSpeed:
                        speed = round(p.value + (self.targetSpeed-p.value)/2)
                        print "speed is %d\n" % speed
                if p.description is "turn":
                    pass
        if len(intentions) == 0:
            intentions.append(Intention())
        return intentions

if __name__ == "__main__":
    """ Unit testing for Agent will go below """
    pass
