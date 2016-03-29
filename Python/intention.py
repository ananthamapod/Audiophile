class Intention(object):
    """ Intention class, produced by deliberating on Percepts,
    represents intended action """
    def __init__(self, command="NOTHING", value=0):
        super(Intention, self).__init__()
        self.command = command
        self.value = value

if __name__ == "__main__":
    """ Unit testing for Intention will go below """
    pass
