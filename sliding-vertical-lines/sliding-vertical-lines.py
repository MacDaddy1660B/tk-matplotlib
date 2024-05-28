#!/usr/bin/env python3

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy
import tkinter


## This is a little experiment to use the matplotlib TKAgg backend.
## It uses a sliding scale to adjust the positioning of the center
## of two vertical lines on a plot window.
## TODO: update the plot with new data streaming in from somewhere
## else, such as from a random number generator, or a time-dependent
## wavefunction, or something.

class PlotWdg(tkinter.Canvas):
    """
    This is the custom plot widget. It controls the plot area and
    sets the positioning of the vertical lines through the 
    updateVerticalBars() callback.
    """

    def __init__(self, *args, **kwargs):
        
        kwargs.setdefault('vCenter', 0)
        vCenter = kwargs.pop('vCenter')
        kwargs.setdefault('vWidth', 1)
        self.vWidth = kwargs.pop('vWidth')
        
        super().__init__(*args, **kwargs)
        
        kwargs.setdefault('master',self.master)
        self.master = kwargs.get('master')
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.plotLine = self.ax.plot(
                numpy.linspace(0,10,11),
                numpy.linspace(0,10,11)**2,
                'b--',
                )
        self.ax.set_title('$y=x^2$')
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y$')
        self.ax.set_xlim(self.ax.get_xlim() + numpy.array([-self.vWidth, self.vWidth]))
        self.drawVlines(vCenter)
        self.figCanvas = FigureCanvasTkAgg(
                self.fig,
                master=self.master
                )
        self.figCanvas.draw()
        self.figCanvas.get_tk_widget().pack()

    def drawVlines(self, vCenter):
        self.vlinesCollection = self.ax.vlines(
                [vCenter-self.vWidth,vCenter+self.vWidth],
                numpy.array( [line.get_ydata().min() for line in self.plotLine] ).min(),
                numpy.array( [line.get_ydata().max() for line in self.plotLine] ).max(),
                #*self.ax.get_ybound(),
                color='red',
                linestyles='dotted',
                )

    def updateVerticalBars(self, vCenter):
        self.vlinesCollection.remove()
        self.drawVlines(vCenter)
        self.figCanvas.draw()


if __name__=='__main__':
    """
    Since the Scale widget doesn't need to do anything special,
    we just use it. The PlotWdg is custom and its class is
    defined above. The state variable of scaleWdg is send to
    the PlotWdg.updateVerticalBars callback upon a motion
    event with the scale.
    """
    
    root = tkinter.Tk()

    sliderWdg = tkinter.Scale(
            root,
            label='Center',
            from_=0,
            to=10,
            tickinterval=2,
            length=200,
            orient=tkinter.HORIZONTAL,
            )
    plotWdg = PlotWdg(
            master=root,
            vCenter=sliderWdg.get(),
            vWidth=1.5
            )
    sliderWdg.bind("<Motion>", lambda e: plotWdg.updateVerticalBars(sliderWdg.get()))
    
    for wdg in (sliderWdg, plotWdg):
        wdg.pack()
        #pass

    root.mainloop()
