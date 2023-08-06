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


class BoxPlot:
    
    """A simple class to make beautiful Boxplot"""


    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.axisList = []
        self.width = 0.35
        self.data = []





    def plot(self, data, color = ['b', 'g', 'r', 'c' ,'m', 'y'], label = None, fancy = False):
        """
        Description: plots a beautiful boxplot
        
        :param data: data to plot. 
        :type data: list of lists/numpy arrays
        :param color: color to assign at each bar, specify one element to set the same color for all bars. 
        :type color: list of strings
        :param label: list of labels for each bar. 
        :type label: list of strings
        :param width: width of bars. 
        :type width: float
        :param fancy: plot a fancy boxplot 
        :type width: bool
        """


        self.data = data
        bp = self.ax.boxplot(self.data, labels = label, patch_artist=True)


        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        colorskey = ['b', 'g', 'r', 'c' ,'m', 'y', 'k', 'w']

        for j, i in enumerate(color):
            for k, l in enumerate(colorskey):
                if i == l:
                    color[j] = colors[k]

        if not (fancy): # beautiful boxplot
            plt.setp(bp['whiskers'], color = 'black', linewidth = 4)
            plt.setp(bp['caps'], color = 'black', linewidth = 4)
            plt.setp(bp['fliers'], color='black', marker='o', linewidth = 4)
            plt.setp(bp['medians'], color = 'black', linewidth = 4)
            
            for i, box in enumerate(bp['boxes']):
                box.set(color='black', linewidth = 4)
                if (len(color) == 1):
                    box.set(facecolor = color[0])
                elif (len(color) >= len(data)):
                    box.set(facecolor = color[i])
                else :
                    print("invalide len of color")


        elif (fancy): # fancy boxplot
            if (len(color) == 1):
                for box in bp['boxes']:
                    box.set(color = color[0], linewidth = 4)
                    box.set(facecolor = color[0])

                for whisker in bp['whiskers']:
                    whisker.set(color = color[0], linewidth = 4)

                for cap in bp['caps']:
                    cap.set(color = color[0], linewidth = 4)

                for i, cap in enumerate(bp['medians']):
                    cap.set(color = 'black', linewidth = 4)

            elif (len(color) >= len(data)):
                for i, box in enumerate(bp['boxes']):
                    box.set(color = color[i], linewidth = 4)
                    box.set(facecolor = color[i])

                for i, whisker in enumerate(bp['whiskers']):
                    if i%2 == 0:
                        whisker.set(color = color[int(i*0.5)], linewidth = 4)
                    else:
                        whisker.set(color = color[int(i*0.5)], linewidth = 4)

                for i, cap in enumerate(bp['caps']):
                    if i%2 == 0:
                        cap.set(color = color[int(i*0.5)], linewidth = 4)
                    else:
                        cap.set(color = color[int(i*0.5)], linewidth = 4)

                plt.setp(bp['medians'], color = 'black', linewidth = 4)





    def addLabels(self, xlabel = None, ylabel = None, size = 16):
        """
        Description: add axis label to a beautiful barchart
        
        :param xlabel: label for the horizontal axis.
        :type xlabel: string
        :param ylabel: label for the vertical axis.
        :type ylabel: string
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
        :type title: string
        :param size: size of the font.
        :type size: float
        """



        if title:
            self.ax.set_title(title, fontsize = size)
        else:
            self.ax.set_ylabel('Why you call this method!?', fontsize = size)




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




    def addPvalueBar(self, cat1, cat2, test = None, pvalue = None):
        """
        Description: add pvalue bar on top of a beautiful barchart
        
        :param cat1: index of the first set of data, count beginning at 1.
        :type cat1: int
        :param cat2: index of the second set of data, count beginning at 1.
        :type cat2: int
        :param test: p-test to used to compute the pvalue. Supported test: 'One-sample ttest', 'Wilcoxon', 'Unpaired t test', 'Mann-Whitney', 'Paired t test'.
        :type test: strings
        :param value: value of p-value.
        :type value: float
        
        :return: computed pvalue.
        :rtype: float.
        """

        
        if not pvalue:
            testList = ['Unpaired t test', 'Mann-Whitney', 'Paired t test', 'Wilcoxon test']
            testFunc = [scipy.stats.ttest_ind, scipy.stats.mannwhitneyu, scipy.stats.ttest_rel, scipy.stats.wilcoxon]
            for i, j in enumerate(testList):
                if j == test and (j == 'Unpaired t test' or j == 'Paired t test'):
                    for k in self.data:
                        p = scipy.stats.normaltest(k)
                        if p[1] > 0.05:
                            print('Non normal distribution detected, use non-parametric test instead.')
                            break
                    pvalue = testFunc[i](self.data[cat1 -1], self.data[cat2 - 1])[1]

                if j == test and (j == 'Mann-Whitney' or j == 'Wilcoxon test'):
                    pvalue = testFunc[i](self.data[cat1 -1], self.data[cat2 - 1])[1]
                    

        yMin, yMax = self.ax.get_ylim()
        diff = yMax - yMin

        if abs(cat1 - cat2) == 1: 
            y = max(np.max(self.data[cat1 - 1]), np.max(self.data[cat2 - 1])) + 0.05*diff

        else:
            if cat2 - cat1 > 0:
                offSet = np.max(np.max(self.data[cat1 : cat2 - 1])) - max(np.max(self.data[cat1 - 1]), np.max(self.data[cat2 - 1]))
                if offSet < 0:
                    offSet = 0
            if cat2 - cat1 < 0:
                offSet = np.max(np.max(self.data[cat2 : cat1 - 1]) - max(np.max(self.data[cat1 - 1]), np.max(self.data[cat2 - 1])))
                if offSet < max(np.max(self.data[cat1 - 1], np.max(self.data[cat2 - 1]))):
                    offSet = 0
            y = max(np.max(self.data[cat1 - 1]), np.max(self.data[cat2 - 1])) + 0.1*diff + offSet

        for i, j in enumerate(self.axisList):
            if y > j - 0.1*y and y < j + 0.1*y:
                y = j + 0.1*diff
        
        self.ax.hlines(y, cat1, cat2, linewidth = 3)
        self.ax.vlines(cat1, y - 0.03*diff, y, linewidth = 3)
        self.ax.vlines(cat2, y - 0.03*diff, y, linewidth = 3)
        self.ax.vlines(cat1 + (cat2 - cat1)/2, y, y + 0.02*diff, linewidth = 3)
        self.ax.annotate(str('p = ' + str(round(pvalue, 5))), xy= (cat1 + (cat2 - cat1)/2, y + 0.05*diff),  xycoords='data', horizontalalignment='center', verticalalignment='top', size=12,)
        self.axisList.append(y)

        return pvalue




    def addPvalueMark(self, cat1, cat2, test = None, pvalue = None, marker = '*'):
        """
        Description: add pvalue bar on top of a beautiful barchart

        :param cat1: index of the first set of data, count beginning at 1.
        :type cat1: int
        :param cat2: index of the second set of data, count beginning at 1.
        :type cat2: int
        :param test: p-test to used to compute the pvalue.
        :type test: strings
        :param value: value of p-value.
        :type value: float
        
        :return: computed pvalue.
        :rtype: float.
        """

        if not pvalue:
            testList = ['Unpaired t test', 'Mann-Whitney', 'Paired t test', 'Wilcoxon test']
            testFunc = [scipy.stats.ttest_ind, scipy.stats.mannwhitneyu, scipy.stats.ttest_rel, scipy.stats.wilcoxon]
            for i, j in enumerate(testList):
                if j == test and (j == 'Unpaired t test' or j == 'Paired t test'):
                    for k in self.data:
                        p = scipy.stats.normaltest(k)
                        if p[0] > 0.05:
                            print('Non normal distribution detected, use non-parametric test instead.')
                            break
                    pvalue = testFunc[i](self.data[cat1 -1], self.data[cat2 - 1])[1]

                if j == test and (j == 'Mann-Whitney' or j == 'Wilcoxon test'):
                    pvalue = testFunc[i](self.data[cat1 -1], self.data[cat2 - 1])[1]
        
        y =  np.max(self.data[cat2 -1]) + 0.08*(self.ax.get_ylim()[1] - self.ax.get_ylim()[0])

        for i, j in enumerate(self.axisList):
            if y == j:
                x = cat2 + self.width/5

        
        if pvalue < 0.0001:
            self.ax.annotate(marker*4, xy=(cat2, y + 0.3*y),  xycoords='data', horizontalalignment='center', verticalalignment='top',)
        elif pvalue < 0.001:
            self.ax.annotate(marker*3, xy=(cat2, y + 0.3*y),  xycoords='data', horizontalalignment='center', verticalalignment='top',)
        elif pvalue < 0.01:
            self.ax.annotate(marker*2, xy=(cat2, y + 0.3*y),  xycoords='data', horizontalalignment='center', verticalalignment='top',)
        elif pvalue < 0.05:
            self.ax.annotate(marker, xy=(cat2, y + 0.3*y),  xycoords='data', horizontalalignment='center', verticalalignment='top',)
        else:
            self.ax.annotate('NS', xy=(cat2, y + 0.3*y),  xycoords='data', horizontalalignment='center', verticalalignment='top',)

        return pvalue



    def addN(self, where = None, size = 12):
        """
        Description: add the number of elements for each bar.

        :param where: index of bar to display N, count beginning at 1.
        :type where: list
        :param size: font size.
        :type size: int
        """

        for i, j in enumerate(self.data):
            y = np.max(j) + 0.08*(self.ax.get_ylim()[1] - self.ax.get_ylim()[0])
            if where != None:
                for k, l in enumerate(where):
                    if i == l - 1:
                        self.ax.annotate(str('N = '  + str(len(j))), xy=(l, y),  xycoords='data', horizontalalignment='center', verticalalignment='top', size=size,)
            else:
                self.ax.annotate(str('N = ' + str(len(j))), xy=(i + 1, y),  xycoords='data', horizontalalignment='center', verticalalignment='top', size=size,)



    def plotPoints(self, size = 10):
        """
        Description: plot points distribution inside each bar

        :param size: points size.
        :type size: int
        """


        for i, j in enumerate(self.data):
            x = np.linspace(i + 1 - self.width*0.5 , i + 1 + self.width*0.5, len(j))
            plt.scatter(x, j, s = size, c = "black", alpha=0.5, zorder = 3)
                
