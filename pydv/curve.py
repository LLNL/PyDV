# Copyright (c) 2011-2023, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory  
# Written by Mason Kwiat, Douglas S. Miller, and Kevin Griffin, Edward Rusu
# e-mail: rusu1@llnl.gov
# LLNL-CODE-507071
# All rights reserved.  
  
# This file is part of PDV.  For details, see <URL describing code and
# how to download source>. Please also read "Additional BSD Notice".
  
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
  
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the disclaimer below.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the disclaimer (as noted below)
# in the documentation and/or other materials provided with the
# distribution.  Neither the name of the LLNS/LLNL nor the names of
# its contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL LAWRENCE
# LIVERMORE NATIONAL SECURITY, LLC, THE U.S. DEPARTMENT OF ENERGY OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
    
# Additional BSD Notice  
  
# 1. This notice is required to be provided under our contract with
# the U.S.  Department of Energy (DOE).  This work was produced at
# Lawrence Livermore National Laboratory under Contract
# No. DE-AC52-07NA27344 with the DOE.
  
# 2. Neither the United States Government nor Lawrence Livermore
# National Security, LLC nor any of their employees, makes any
# warranty, express or implied, or assumes any liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents
# that its use would not infringe privately-owned rights.
  
# 3.  Also, reference herein to any specific commercial products,
# process, or services by trade name, trademark, manufacturer or
# otherwise does not necessarily constitute or imply its endorsement,
# recommendation, or favoring by the United States Government or
# Lawrence Livermore National Security, LLC.  The views and opinions
# of authors expressed herein do not necessarily state or reflect
# those of the United States Government or Lawrence Livermore National
# Security, LLC, and shall not be used for advertising or product
# endorsement purposes.

import sys
import numpy as np
from scipy import interpolate

class Curve(object):

    name = ''
    filename = ''
    record_id = ''
    xlabel = ''
    ylabel = ''
    title = ''
    plotname = ''
    color = ''
    edited = False
    scatter = False
    linespoints = False
    linewidth = None
    linestyle = '-'
    drawstyle = 'default'
    dashes = None
    hidden = False
    x = np.empty(0)
    y = np.empty(0)
    ebar = None     #errorbar
    erange = None   #errorrange
    marker = '.'    # Use matplotlib markers when setting directly
    markerstyle = None
    markersize = 3
    markerfacecolor = None
    markeredgecolor = None
    plotprecedence = 0
    legend_show = True
    
    def __init__(self, filename='', name='', record_id='', xlabel='', ylabel='', title=''):
        self.filename = filename
        self.name = name
        self.record_id = record_id
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
    
    
    def __add__(a, b):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str(a.plotname + ' + ' + b.plotname + ' ').strip('  ')
        ia, ib = getinterp(a, b)
        if ia.x is not None and ib.x is not None:
            c.x = ia.x
            c.y = ia.y + ib.y
        return c

    
    def __sub__(a, b):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str(a.plotname + ' - ' + b.plotname + ' ').strip('  ')
        ia, ib = getinterp(a, b)
        if ia.x is not None and ib.x is not None:
            c.x = ia.x
            c.y = ia.y - ib.y
        return c
    
    
    def __mul__(a, b):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str(a.plotname + ' * ' + b.plotname + ' ').strip('  ')
        ia, ib = getinterp(a, b)
        if ia.x is not None and ib.x is not None:
            c.x = ia.x
            c.y = ia.y * ib.y
        return c

    def __div__(a, b):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str(a.plotname + ' / ' + b.plotname + ' ').strip('  ')
        ia, ib = getinterp(a, b)
        if ia.x is not None and ib.x is not None:
            c.x = ia.x

            zero_indices = np.where(ib.y == 0)
            for idx in zero_indices:
                ib.y[idx] = 0.000000001

            c.y = ia.y / ib.y
            for idx in zero_indices:
                c.y[idx] = float(sys.maxsize)

        return c

    def __truediv__(a,b):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str(a.plotname + ' / ' + b.plotname + ' ').strip('  ')
        ia, ib = getinterp(a, b)
        if ia.x is not None and ib.x is not None:
            c.x = ia.x

            zero_indices = np.where(ib.y == 0)
            for idx in zero_indices:
                ib.y[idx] = 0.000000001

            c.y = ia.y / ib.y
            for idx in zero_indices:
                c.y[idx] = float(sys.maxsize)

        return c
    
    def __pow__(a, b):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str(a.plotname + '^' + str(b)).strip('  ')
        c.x = np.array(a.x)
        c.y = np.power(a.y, b)
        nans = np.isnan(c.y)    #remove NaNs
        c.x = c.x[~nans]
        c.y = c.y[~nans]
        return c
        
    def __neg__(a):
        c = Curve('', '')
        c.drawstyle = a.drawstyle
        c.plotname = str('-' + a.plotname)
        c.x = np.array(a.x)
        c.y = np.array(-a.y)
        return c
   
    
    ##return a new copy of the curve object##
    def copy(self):
        c = Curve(self.filename, self.name, self.record_id, self.xlabel, self.ylabel, self.title)
        c.plotname = self.plotname
        c.x = np.array(self.x)
        c.y = np.array(self.y)
        c.color = self.color
        c.edited = self.edited
        c.scatter = self.scatter
        c.linespoints = self.linespoints
        c.linewidth = self.linewidth
        c.linestyle = self.linestyle
        c.drawstyle = self.drawstyle
        c.dashes = self.dashes
        c.hidden = self.hidden
        c.marker = self.marker
        c.markerstyle = self.markerstyle
        c.markersize = self.markersize
        c.markeredgecolor = self.markeredgecolor
        c.markerfacecolor = self.markerfacecolor
        c.ebar = self.ebar
        c.erange = self.erange
        c.plotprecedence = self.plotprecedence
        
        return c

    ##return a new normalized copy of the curve object##
    def normalize(self):
        c = self.copy()

        norm = np.linalg.norm(c.y)
        if norm == 0:
            return c

        c.y /= float(norm)
        c.name = "Normalized %s" % self.plotname
        return c


def getinterp(a, b, left=None, right=None, samples=100, match='domain'):
    """
    Gets the interpolated and domain matched versions of the two curves.

    :param a: Curve A
    :type a: curve
    :param b: Curve B
    :type b: curve
    :param left: Value to return for `x < a.x[0]`, default is `a.y[0]`.
    :type left: float, optional
    :param right: Value to return for `x > a.x[-1]`, default is `a.y[-1]`.
    :type: right: float, optional
    :param match {'domain','step'},optional: A string indicating how to interpolate the two curves
    :type match: str
    :returns: curve pair -- the interpolated and domain matched versions of a and b
    """
    if match == 'domain':
        ux = list(set(a.x).union(set(b.x)))  #get union of xvals
        ux.sort()

        ia = a.copy()
        ia.x = np.array(ux)
        ia.y = np.interp(ux, a.x, a.y, left, right) # interpolate y vals

        ib = Curve('', '')
        ib.x = np.array(ux)
        ib.y = np.interp(ux, b.x, b.y, left, right) # interpolate y vals

        return ia, ib
    elif match == 'step':
        ax, step = np.linspace(min(a.x), max(a.x), num=samples, retstep=True)

        bxsamples = int((max(b.x) - min(b.x)) / step)
        if bxsamples < 1:
            bxsamples = 1

        bx = np.linspace(min(b.x), max(b.x), bxsamples)

        ia = a.copy()
        ia.x = ax
        ia.y = np.interp(ax, a.x, a.y, left, right)  # interpolate y vals

        ib = Curve('', '')
        ib.x = bx
        ib.y = np.interp(bx, b.x, b.y, left, right)  # interpolate y vals

        return ia, ib
    else:
        raise ValueError("{} is not a supported option for match".format(match))


def interp1d(a, num=100, retstep=False):
    """
    Gets the interpolated values of the curve with the specified number of samples.

    :param a: Curve A
    :type a: curve
    :param num: Number of samples to generate. Default is 100. Must be non-negative.
    :type: num: int, optional
    :param retstep: return the spacing between samples
    :type: retstep: bool, optional
    :returns: ia: curve -- the interpolated and dimensions matched version of a
              step: float, optional -- only returned if retstep is True. Size of the spacing between samples
    """
    num = int(num)
    f = interpolate.interp1d(a.x, a.y, kind='linear', bounds_error=False, fill_value=0)

    ia = a.copy()

    if retstep:
        ia.x, step = np.linspace(min(a.x), max(a.x), num=num, retstep=True)
        ia.y = f(ia.x)
        return ia, step
    else:
        ia.x = np.linspace(min(a.x), max(a.x), num=num, retstep=False)
        ia.y = f(ia.x)
        return ia


def append(a, b):
    """
    Merge curve a and curve b over the union of their domains. Where domains overlap, take
    the average of the curve's y-values.

    :param a: Curve A
    :type a: curve
    :param b: Curve B
    :type b: curve
    :return: a new curve resulting from the merging of curve a and curve b
    """
    ux = list(set(a.x).union(set(b.x)))  #get union of xvals
    ux.sort()

    aub = Curve('','')
    aub.x = np.array(ux)
    aub.y = np.zeros(len(aub.x))

    for i in range(len(aub.x)):
        xval = aub.x[i]

        aidx = np.where(a.x == xval)[0]
        bidx = np.where(b.x == xval)[0]

        has_a = len(aidx) != 0
        has_b = len(bidx) != 0

        sum = float(0)
        tot = 0

        if has_a:
            for idx in aidx:
                sum += float(a.y[idx])
                tot += 1

        if has_b:
            for idx in bidx:
                sum += float(b.y[idx])
                tot += 1

        aub.y[i] = sum / float(tot)

    return aub

