from collections import deque
import matplotlib.pyplot as plt
import numpy as np

class Plotter(object):
    def __init__(self, plot_size=100):
        self.PLOTSIZE = 100
        self.ldata = deque([None] * plot_size, maxlen=plot_size)
        self.fdata = deque([None] * plot_size, maxlen=plot_size)
        self.rdata = deque([None] * plot_size, maxlen=plot_size)
        self.fig = None
        self.lplot = None
        self.fplot = None
        self.rplot = None

    def configurePlots(self):
        """ Sets up the figure for plotting 3 graphs """
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)

        x = np.arange(self.PLOTSIZE)

        self.lplot, self.fplot, self.rplot = ax.plot(
            x,
            self.ldata,
            'g-',
            x,
            self.fdata,
            'b-',
            x,
            self.rdata,
            'r-')

        plt.axis([0, self.PLOTSIZE, 0, 100])
        plt.grid(True)

        self.fig.canvas.show()
        plt.show(block=False)

    def updatePlot(self, l, f, r):
        """ Updates plot based on new sensor values from Arduino """

        # push new sensor values onto capped value arrays
        self.ldata.append(float(l))
        self.fdata.append(float(f))
        self.rdata.append(float(r))

        # set the data onto the plot
        self.lplot.set_ydata(self.ldata)
        self.fplot.set_ydata(self.fdata)
        self.rplot.set_ydata(self.rdata)

        """# print for posterity
        print "Left: %s" % l
        print "Front: %s" % f
        print "Right: %s" % r"""

        self.fig.canvas.show()

if __name__ == "__main__":
    """ Unit testing for Plotter will go below """
    pass
