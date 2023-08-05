#!/usr/bin/env python3.4
# coding: latin-1

# (c) Massachusetts Institute of Technology 2015-2017
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
cytoflow.utility.matplotlib_widgets
-----------------------------------

Additional widgets to be used with matplotlib
'''

import time
from matplotlib.lines import Line2D
from matplotlib.widgets import AxesWidget

class PolygonSelector(AxesWidget):
    """Selection polygon.
    
    The selected path can be used in conjunction with
    :func:`~matplotlib.path.Path.contains_point` to select data points
    from an image.
    
    Parameters
    ----------
    
    ax : :class:`~matplotlib.axes.Axes`
        The parent axes for the widget.
        
    callback : callable
        When the user double-clicks, the polygon closes and the ``callback`` 
        function is called and passed the vertices of the selected path.
    """

    def __init__(self, ax, callback=None, useblit=True):
        AxesWidget.__init__(self, ax)

        self.useblit = useblit and self.canvas.supports_blit
        self.verts = []
        self.drawing = False
        self.line = None
        self.callback = callback
        self.last_click_time = time.time()
        self.connect_event('button_press_event', self.onpress)
        self.connect_event('motion_notify_event', self.onmove)

    def onpress(self, event):
        if self.ignore(event):
            return

        if not self.drawing:
            # start over
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
            self.verts = [(event.xdata, event.ydata)]
            self.line = Line2D([event.xdata], [event.ydata], linestyle='-', color='black', lw=1)
            self.ax.add_line(self.line)
            self.drawing = True
        else:
            self.verts.append((event.xdata, event.ydata))
            self.line.set_data(list(zip(*self.verts)))
                
        if event.dblclick or (time.time() - self.last_click_time < 0.3):
            self.callback(self.verts)
            self.ax.lines.remove(self.line)
            self.drawing = False

        self.last_click_time = time.time()    

    def onmove(self, event):
        if self.ignore(event):
            return
        if not self.drawing:
            return
        if event.inaxes != self.ax:
            return

        self.line.set_data(list(zip(*(self.verts + [(event.xdata, event.ydata)]))))

        if self.useblit:
            self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.line)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()