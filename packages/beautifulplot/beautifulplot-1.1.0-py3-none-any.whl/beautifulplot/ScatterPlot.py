'''                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.'''

import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
mpl.style.use('fivethirtyeight')
import numpy as np
import scipy.stats



class ScatterPlot:
    
    """A simple class to make beautiful scatter plot"""


    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.data = []
        self.pointColor = []
        self.pointFit = []




    def plot(self, data, size = 30, color = None, marker = 'o', legend = None):
        """
        Description: plots a beautiful scatter plot
        
        :param data: data to plot. 
        :type data: list of lists/numpy arrays
        :param color: color of point.
        :type color: list of string
        :param size: size of a point.
        :type size: int

        """
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        colorskey = ['b', 'g', 'r', 'c' ,'m', 'y', 'k', 'w']

        for k, l in enumerate(colorskey):
            if color == l:
                color = colors[k]

        self.data = data
        
        if color == None:
            for i, j in enumerate(colorskey):
                for k, l in enumerate(self.pointColor):
                    if j != l:
                        color = colors[k]
                        self.pointColor.append(j)
                        break

        self.ax.scatter(data[0], data[1], c= color, s = size, marker = marker, label = legend)

        if legend:
            self.ax.legend()




    def addLabels(self, xlabel = None, ylabel = None, size = 16):
        """
        Description: add axis label to a beautiful barchart
        
        :param xlabel: label for the horinzontal axis.
        :type xlabel: strings
        :param ylabel: label for the vertical axis.
        :type ylabel: strings
        :param size: size of the font.
        :type size: float
        """



        if xlabel:
            self.ax.set_xlabel(xlabel, fontsize = size)
        if ylabel:
            self.ax.set_ylabel(ylabel, fontsize = size)




    def addTitle(self, title = None, size = 16):
        """
        Description: add title to a beautiful barchart
        
        :param title: title the the beautiful plot.
        :type title: strings
        :param size: size of the font.
        :type size: float
        """



        if title:
            self.ax.set_title(title, fontsize = size)
        else:
            self.ax.set_ylabel('Why call this method!?', fontsize = size)




    def limits(self, xlim = None, ylim = None):
        """
        Description: change axis limits to a beautiful barchart
        
        :param xlim: limits for the horizontal axis.
        :type xlim: list[xmin, xmax].
        :param ylim: limits for the vertical axis.
        :type ylim: list[ymin ymax].
        """

        if xlim:
            self.ax.set_xlim(xlim)
        if ylim:
            self.ax.set_ylim(ylim)

        

    def fitting(self, data, equation = 'linear', color = None, custom = None, size = 10):
        """
        Description: fit data of a beautiful scatter plot
        
        :param equation: fitting equation. Available: 'linear', 'polynomial2', 'polynomial3', 'custom'
        :type string: list[xmin, xmax].
        :param custom: custom equation for fitting, def f(x, *[parameters]): return equation.
        :type custom: function 
        """

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        colorskey = ['b', 'g', 'r', 'c' ,'m', 'y', 'k', 'w']

        for k, l in enumerate(colorskey):
            if color == l:
                color = colors[k]

        if not color:
            for i, j in enumerate(colorskey):
                for k, l in enumerate(self.pointFit):
                    if j != l:
                        color = colors[k]
                        self.pointFit.append(j)
                        break

        if equation == 'linear':
            def f(x, a, b): return a*x+b 
            [popt, pcov] = scipy.optimize.curve_fit(f, data[0], data[1])
            perr = np.sqrt(np.diag(pcov))
            equationStr = "y = (" + str(round(popt[0],3)) + '$\pm$' + str(round(perr[0],3)) + ')x + ' + str(round(popt[1],3)) + '$\pm$' + str(round(perr[1],3))

        if equation == 'polynomial2':
            def f(x, a, b, c): return a*x**2+b*x+c 
            [popt, pcov] = scipy.optimize.curve_fit(f, data[0], data[1])
            perr = np.sqrt(np.diag(pcov))
            equationStr = "y = " + str(round(popt[0],3)) + '$x^{2}$ + ' + str(round(popt[1],3)) + 'x +' + str(round(popt[2],3))

        if equation == 'polynomial3':
            def f(x, a, b, c, d): return a*x**3+b*x**2+c*x+d 
            [popt, pcov] = scipy.optimize.curve_fit(f, data[0], data[1])
            perr = np.sqrt(np.diag(pcov))
            equationStr = 'y = ' + str(round(popt[0],3)) + '$x^{3}$ + ' + str(round(popt[1],3)) + '$x^{2}$ + ' + str(round(popt[2],3)) + 'x + ' + str(round(popt[3],3))

        if custom:
            [popt, pcov] = scipy.optimize.curve_fit(custom, data[0], data[1])
            equationStr = ''

        
        xMin, xMax = self.ax.get_xlim()
        yMin, yMax = self.ax.get_ylim()
        x = np.linspace(xMin, xMax, 10000)

        self.ax.plot(x, f(x, *popt), zorder = 0, color = color)
        self.ax.annotate(equationStr, xy=(xMax, yMax),  xycoords='data', horizontalalignment='right', verticalalignment='top', size = size)




        


        




