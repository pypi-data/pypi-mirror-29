# Beautiful Plot

Beautiful Plot is a library based on Matplotlib that allow beautiful and easy plot. Create beautiful bar chart, scatter plot etc... Choose the best statistical test then compute and display it in your plot in just one user friendly command.

Beautiful Plot is under active development and no stable version is released yet. To test it, clone the repository and install the package:
```python
python setup.py install
```




See the documentation at http://benjamin-gallois.fr/BeautifulPlot/index.html or in the documentations folder.

![A beautiful Bar Chart](https://benjamin-gallois.fr/BeautifulPlot/bpChart.png)

# For example:

Produce a beautiful bar chart with p-values, points visualization effortless:

```python
import beautifulplot as bp
import numpy as np

# Generate random data 
data = []
for i in range(5):
    data.append(np.random.normal(np.random.normal(1, 0.1,1), np.random.random(1)/10, np.random.randint(500)))

# Plot
fig = bp.BarChart() # Initialize bar chart
fig.plot(data, color = ['b', 'r', 'y', 'g', 'm'], label = ['dat1', 'dat2', 'dat3', 'dat4', 'dat5']) # Plot bar chart
fig.addLabels(ylabel = 'Intensity') # Add ylabel
fig.addTitle('A beautiful Bar Chart', size = 20) # Add title
fig.addN(size = 12) # Add number of elements in each bar
for i in range(2, 6): # Add p-values
    fig.addPvalueBar(1, i, test = 'Unpaired t test')
fig.plotPoints(size = 2) # Plot points inside each bar

plt.show()
```
![A beautiful Bar Chart](https://benjamin-gallois.fr/BeautifulPlot/bpChart1.png)
