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

"""
cytoflow.views.kde_2d
---------------------
"""

from traits.api import provides, Constant

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.nonparametric.api as smnp

import cytoflow.utility as util

from .i_view import IView
from .base_views import Base2DView

@provides(IView)
class Kde2DView(Base2DView):
    """
    Plots a 2-d kernel-density estimate.  Sort of like a smoothed histogram.
    The density is visualized with a set of isolines.
    
    .. warning:: :class:`Kde2DView` is currently **VERY SLOW.**  
    
    Attributes
    ----------

    Examples
    --------
    
    Make a little data set.
    
    .. plot::
        :context: close-figs
            
        >>> import cytoflow as flow
        >>> import_op = flow.ImportOp()
        >>> import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
        ...                              conditions = {'Dox' : 10.0}),
        ...                    flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
        ...                              conditions = {'Dox' : 1.0})]
        >>> import_op.conditions = {'Dox' : 'float'}
        >>> ex = import_op.apply()
        
    Plot a density plot
    
    .. plot::
        :context: close-figs
    
        >>> flow.Kde2DView(xchannel = 'V2-A',
        ...                xscale = 'log',
        ...                ychannel = 'Y2-A',
        ...                yscale = 'log',
        ...                huefacet = 'Dox').plot(ex)
    """
    
    id = Constant('edu.mit.synbio.cytoflow.view.kde2d')
    friend_id = Constant("2D Kernel Density Estimate")
    
    def plot(self, experiment, **kwargs):
        """
        Plot a faceted 2d kernel density estimate
        
        Parameters
        ----------
        shade : bool
            Shade the interior of the isoplot?  (default = `False`)
            
        min_alpha, max_alpha : float
            The minimum and maximum alpha blending values of the isolines,
            between 0 (transparent) and 1 (opaque).
            
        n_levels : int
            How many isolines to draw? (default = 10)
            
        kernel : str
            The kernel to use for the kernel density estimate. Choices are:
                - ``gau`` for Gaussian (the default)
                - ``biw`` for biweight
                - ``cos`` for cosine
                - ``epa`` for Epanechnikov
                - ``tri`` for triangular
                - ``triw`` for triweight
                - ``uni`` for uniform
            
        bw : str or float
            The bandwidth for the kernel, controls how lumpy or smooth the
            kernel estimate is.  Choices are:
            
                - ``scott`` (the default) - ``1.059 * A * nobs ** (-1/5.)``, where ``A`` is ``min(std(X),IQR/1.34)``
                
                - ``silverman`` - ``.9 * A * nobs ** (-1/5.)``, where ``A`` is ``min(std(X),IQR/1.34)``
                
                - ``normal_reference`` - ``C * A * nobs ** (-1/5.)``, where ``C`` is calculated from the kernel. Equivalent (up to 2 dp) to the ``scott`` bandwidth for gaussian kernels. See bandwidths.py

            If a float is given, it is used as the bandwidth.
            
        gridsize : int
            How many times to compute the kernel on each axis?  (default: 100)
        
        Notes
        -----
        Other ``kwargs`` are passed to `matplotlib.axes.Axes.contour <https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.contour.html>`_

        """
        
        super().plot(experiment, **kwargs)
        
    def _grid_plot(self, experiment, grid, xlim, ylim, xscale, yscale, **kwargs):

        
        kwargs.setdefault('shade', False)
        kwargs.setdefault('min_alpha', 0.2)
        kwargs.setdefault('max_alpha', 0.9)
        kwargs.setdefault('n_levels', 10)

        grid.map(_bivariate_kdeplot, 
                 self.xchannel, 
                 self.ychannel, 
                 xscale = xscale, 
                 yscale = yscale, 
                 **kwargs)
        
        return {}
        
# yoinked from seaborn/distributions.py, with modifications for scaling.
def _bivariate_kdeplot(x, y, xscale=None, yscale=None, shade=False, kernel="gau",
                       bw="scott", gridsize=100, cut=3, clip=None, legend=True, **kwargs):
    
    ax = plt.gca()
    
    # Determine the clipping
    clip = [(-np.inf, np.inf), (-np.inf, np.inf)]
        
    x = xscale(x)
    y = yscale(y)

    x_nan = np.isnan(x)
    y_nan = np.isnan(y)
    
    x = x[~(x_nan | y_nan)]
    y = y[~(x_nan | y_nan)]

    # Compute a bivariate kde using statsmodels.
    if isinstance(bw, str):
        bw_func = getattr(smnp.bandwidths, "bw_" + bw)
        x_bw = bw_func(x)
        y_bw = bw_func(y)
        bw = [x_bw, y_bw]
    elif np.isscalar(bw):
        bw = [bw, bw]

    kde = smnp.KDEMultivariate([x, y], "cc", bw)
    x_support = _kde_support(x, kde.bw[0], gridsize, cut, clip[0])
    y_support = _kde_support(y, kde.bw[1], gridsize, cut, clip[1])
    xx, yy = np.meshgrid(x_support, y_support)
    z = kde.pdf([xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    n_levels = kwargs.pop("n_levels", 10)
    color = kwargs.pop("color")
    kwargs['colors'] = (color, )
    
    x_support = xscale.inverse(x_support)
    y_support = yscale.inverse(y_support)
    xx, yy = np.meshgrid(x_support, y_support)    
    
    contour_func = ax.contourf if shade else ax.contour
    cset = contour_func(xx, yy, z, n_levels, **kwargs)
    num_collections = len(cset.collections)
    
    min_alpha = kwargs.pop("min_alpha", 0.2)
    if shade:
        min_alpha = 0
        
    max_alpha = kwargs.pop("max_alpha", 0.9)
    
    alpha = np.linspace(min_alpha, max_alpha, num = num_collections)
    for el in range(num_collections):
        cset.collections[el].set_alpha(alpha[el])

    # Label the axes
    if hasattr(x, "name") and legend:
        ax.set_xlabel(x.name)
    if hasattr(y, "name") and legend:
        ax.set_ylabel(y.name)

    return ax        

def _kde_support(data, bw, gridsize, cut, clip):
    """Establish support for a kernel density estimate."""
    support_min = max(data.min() - bw * cut, clip[0])
    support_max = min(data.max() + bw * cut, clip[1])
    return np.linspace(support_min, support_max, gridsize)

util.expand_class_attributes(Kde2DView)
util.expand_method_parameters(Kde2DView, Kde2DView.plot)


if __name__ == '__main__':
    import cytoflow as flow
    tube1 = flow.Tube(file = '../../cytoflow/tests/data/Plate01/RFP_Well_A3.fcs',
                      conditions = {"Dox" : 10.0})
    
    tube2 = flow.Tube(file = '../../cytoflow/tests/data/Plate01/CFP_Well_A4.fcs',
                      conditions = {"Dox" : 1.0})                      

    ex = flow.ImportOp(conditions = {"Dox" : "float"}, tubes = [tube1, tube2])
    
    thresh = flow.ThresholdOp()
    thresh.name = "Y2-A+"
    thresh.channel = 'Y2-A'
    thresh.threshold = 200.0

    ex2 = thresh.apply(ex)
    
    scatter = flow.ScatterplotView()
    scatter.name = "Scatter"
    scatter.xchannel = "FSC-A"
    scatter.ychannel = "SSC-A"
    scatter.xscale = "logicle"
    scatter.yscale = "logicle"
    scatter.huefacet = 'Dox'
    
    plt.ioff()
    scatter.plot(ex2)
    plt.show()
    
