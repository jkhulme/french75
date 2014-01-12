from pylab import *
from matplotlib.collections import LineCollection

# In order to efficiently plot many lines in a single set of axes,
# Matplotlib has the ability to add the lines all at once. Here is a
# simple example showing how it is done.

ys = [(1,2, None, None, None, None), (None, None, 3,4, None, None), (None, None, None, None, 5,6)]
# Here are many sets of y to plot vs x
x = [1,2,3,4,5,6]

# We need to set the plot limits, they will not autoscale
ax = axes()
ax.set_xlim(1,6)
ax.set_ylim(1,6)

# colors is sequence of rgba tuples
# linestyle is a string or dash tuple. Legal string values are
#          solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
#          where onoffseq is an even length tuple of on and off ink in points.
#          If linestyle is omitted, 'solid' is used
# See matplotlib.collections.LineCollection for more information
line_segments = LineCollection([list(zip(x,y)) for y in ys], # Make a sequence of x,y pairs
                                linewidths    = 1)
ax.add_collection(line_segments)
fig = gcf()
ax.set_title('Line Collection with mapped colors')
sci(line_segments) # This allows interactive changing of the colormap.
show()
