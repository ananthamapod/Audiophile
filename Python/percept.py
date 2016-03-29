class Percept(object):
    """Percept class, for all perceptions determined from sensor inputs"""
    def __init__(self, desc="Empty", value=None):
        super(Percept, self).__init__()
        self.description = desc
        self.value = value

if __name__ == "__main__":
    """ Unit testing for Percept will go below """
    pass
