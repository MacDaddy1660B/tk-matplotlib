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
    updateVerticalBars() callback. We use matplotlib-like
    keyword arguments and pass the rest to tkinter.
    """

    def __init__(self, *args, **kwargs):
        
        kwargs.setdefault('vCenter', 0)
        kwargs.setdefault('vWidth', 1)
        kwargs.setdefault('xdata', [0])
        kwargs.setdefault('ydata', [0])
        kwargs.setdefault('plotLineFmt', 'k-')
        kwargs.setdefault('title', None)
        kwargs.setdefault('xlabel', None)
        kwargs.setdefault('ylabel', None)
        kwargs.setdefault('vLineColors', None)
        kwargs.setdefault('vLineStyles', 'solid')
        vCenter = kwargs.pop('vCenter')
        self.vWidth = kwargs.pop('vWidth')
        self.xdata = kwargs.pop('xdata')
        self.ydata = kwargs.pop('ydata')
        self.plotLineFmt = kwargs.pop('plotLineFmt')
        title = kwargs.pop('title')
        xlabel = kwargs.pop('xlabel')
        ylabel = kwargs.pop('ylabel')
        self.vLineColors = kwargs.pop('vLineColors')
        self.vLineStyle = kwargs.pop('vLineStyles')
        
        super().__init__(*args, **kwargs)
        
        kwargs.setdefault('master',self.master)
        self.master = kwargs.get('master')
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.plotLine = self.ax.plot(
                self.xdata,
                self.ydata,
                self.plotLineFmt,
                )
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlim(self.ax.get_xlim() + numpy.array([-self.vWidth, self.vWidth]))
        self.drawVlines(vCenter)
        self.figCanvas = FigureCanvasTkAgg(
                self.fig,
                master=self.master
                )
        self.figCanvas.draw()
        self.Wdg = self.figCanvas.get_tk_widget()

    def drawVlines(self, vCenter):
        self.vlinesCollection = self.ax.vlines(
                [vCenter-self.vWidth,vCenter+self.vWidth],
                numpy.array( [line.get_ydata().min() for line in self.plotLine] ).min(),
                numpy.array( [line.get_ydata().max() for line in self.plotLine] ).max(),
                colors=self.vLineColors,
                linestyles=self.vLineStyle,
                )

    def updateVLines(self, vCenter):
        self.vlinesCollection.remove()
        self.drawVlines(vCenter)
        self.figCanvas.draw()


def main():
    """
    Since the Scale widget doesn't need to do anything special,
    we just use it. The scale is moved by motion of the slider,
    left/right/up/down arrows, and button-1 release.
    
    The PlotWdg is custom and its class is
    defined above. The state variable of scaleWdg is sent to
    the PlotWdg.updateVerticalBars callback upon a motion
    event with the scale.

    A Reset button resets everything to its initial state.
    The Return key is bound to this button.
    """

    SLIDER_DEFAULT_VALUE = 5
    SCALE_BIND_LIST = ["<ButtonRelease-1>","<Motion>","<Up>","<Down>","<Left>","<Right>"]
    
    root = tkinter.Tk()
    root.title('Tk-Matplotlib vLine Slider')

    sliderWdg = tkinter.Scale(
            root,
            label='Center',
            from_=0,
            to=10,
            resolution=0.1,
            tickinterval=2,
            length=200,
            orient=tkinter.HORIZONTAL,
            )
    wdgList = [sliderWdg]
    sliderWdg.set(SLIDER_DEFAULT_VALUE)
    resetButtonWdg = tkinter.Button(
            root,
            text="Reset",
            command= lambda : [
                sliderWdg.set(SLIDER_DEFAULT_VALUE), 
                plotWdg.updateVLines(sliderWdg.get())
                ],
            )
    wdgList.append(resetButtonWdg)
    plotWdg = PlotWdg(
            master=root,
            xdata=numpy.linspace(0,10,11),
            ydata=numpy.linspace(0,10,11)**2,
            plotLineFmt='b--',
            title='$y=x^2$',
            xlabel='$x$',
            ylabel='$y$',
            vCenter=sliderWdg.get(),
            vWidth=0.5,
            vLineColors='red',
            vLineStyles='dotted',
            )
    wdgList.append(plotWdg.Wdg)
    
    for BIND in SCALE_BIND_LIST:
        sliderWdg.bind(BIND, lambda e: plotWdg.updateVLines(sliderWdg.get()))
    resetButtonWdg.bind("<Return>", resetButtonWdg.cget("command"))
    
    for wdg in wdgList:
        wdg.grid(padx=10,pady=10)

    root.mainloop()



if __name__=='__main__':
    main()

