#!/usr/bin/env python
import numpy as np
import pylab as P

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
x = mu + sigma*P.randn(10000)

# the histogram of the data with histtype='step'
n, bins, patches = P.hist(x, 1000, normed=1, histtype='stepfilled')
P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

# add a line showing the expected distribution
y = P.normpdf( bins, mu, sigma)
l = P.plot(bins, y, 'k--', linewidth=1.5)

P.figure()

x = mu + sigma*P.randn(1000,3)

n, bins, patches = P.hist(x, 250, normed=1, histtype='bar',
                            color=['crimson', 'burlywood', 'chartreuse'],
                            label=['Crimson', 'Burlywood', 'Chartreuse'])

n, bins, patches = P.hist(x, 250, normed=1, histtype='bar', stacked=True)

P.show()