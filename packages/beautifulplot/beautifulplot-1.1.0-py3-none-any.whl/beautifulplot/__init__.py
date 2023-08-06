'''                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.'''

from .BarChart import BarChart
from .ScatterPlot import ScatterPlot
from .BoxPlot import BoxPlot
import matplotlib.pyplot as plt

def show():
    plt.show()