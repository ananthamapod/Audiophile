import constants
from percept import Percept
from intention import Intention
from collections import deque

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
                return
            print "Perceiving ..."
            encoders = kwargs.get('encoders')
            if encoders:
                print encoders
                left, right = encoders
                if left < right+constants.epsilon and left > right-constants.epsilon:
                    percepts.append(Percept('speed', left))
                else:
                    # Governing turning equation:
                    # d_theta_Tank = L/2 (R d_theta_left) - L/2 (R d_theta_right)
                    percepts.append(Percept('angle', (constants.L*constants.R/2.0)*(left-right)))

        return percepts

    def deliberate(self, percepts):
        """ Deliberates upon percepts, decides on course of actions,
        and generates and returns list of intentions """
        intentions = []
        for p in percepts:
            if p.description is not "Empty":
                print p.description + ": " + str(p.value)
        if len(intentions) == 0:
            intentions.append(Intention())
        return intentions

if __name__ == "__main__":
    """ Unit testing for Agent will go below """
    pass
