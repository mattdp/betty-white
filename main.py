#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from six.moves import zip

#BELOW is step 1, modding example code to see hundreds or
#thousands of data displayed
# code from http://matplotlib.org/1.3.0/examples/pylab_examples/histogram_demo_extended.html

#
# The hist() function now has a lot more options
#

#
# first create a single histogram
#
mu, sigma = 200, 25

x = mu + sigma*P.randn(1000,3)

#250 kinda visible, 500 very wispy
numBars = 318

n, bins, patches = P.hist(x, numBars, normed=1, histtype='bar',
                            color=['crimson', 'burlywood', 'chartreuse'],
                            label=['Crimson', 'Burlywood', 'Chartreuse'],
                            edgecolor='None')

n, bins, patches = P.hist(x, numBars, normed=1, histtype='bar', stacked=True, edgecolor='None')

P.show()