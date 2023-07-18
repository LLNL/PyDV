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


"""
A python interface for PyDV functionality.

.. module: pydvpy
.. moduleauthor:: Edward Rusu <rusu1@llnl.gov>

>>> import pydvpy as pydvif
"""

import json
import os
import string
import traceback
import sys
import re
import random as sysrand

from distutils.version import LooseVersion

import numpy as np
import scipy
import scipy.integrate
import scipy.special
import scipy.signal
import scipy.misc

import matplotlib.pyplot as plt

try:
    from matplotlib import style
    stylesLoaded = True
except:
    stylesLoaded = False

try:
    from . import curve
except ImportError:
    import curve

try:
    import pact.pdb as pdb
    pdbLoaded = True
except:
    pdbLoaded = False

def span(xmin, xmax, numpts=100):
    """
    Generates a straight line of slope 1 and y intercept 0 in the specified domain with an optional number
    of points.

    >>> c = pydvif.span(1, 10)

    :param xmin: The minimum x value
    :type xmin: float
    :param xmax: The maximum x value
    :type xmax: float
    :param numpts: The number of points used to plot the line
    :type numpts: int
    :returns: curve -- the curve object representing the straight line.
    """
    spacing = (float(xmax) - float(xmin)) / (float(numpts) - 1.0)
    fxmin = float(xmin)
    x = []
    for i in range(numpts):
        x.append(fxmin)
        fxmin += spacing
    x = np.array(x)
    y = np.array(x)
    c = makecurve(x, y, 'Straight Line')

    return c


def makecurve(x, y, name='Curve', fname='', xlabel='', ylabel='', title='', record_id=''):
    """
    Generate a curve from two lists of numbers.

    >>> c1 = pydvif.makecurve([1, 2, 3, 4], [5, 10, 15, 20])

    >>> c2 = pydvif.makecurve([1, 2, 3, 4], [7, 8, 9, 10], 'Line')

    :param x: list of x values
    :type x: list
    :param y: list of y values
    :type y: list
    :param name: the name of the new curve
    :type name: str
    :param fname: the name of the file containing this curves data.
    :type fname: str
    :returns: curve -- the curve generated from the x and y list of values.
    """
    if len(x) != len(y):
        print(f"Curve {name} doesn't have the same length: len(x)={len(x)} and len(y)={len(y)} ")
        name += " !!!ERROR:len(x)!=len(y)!!!"            
    c = curve.Curve(fname, name, record_id, xlabel, ylabel, title)
    c.x = np.array(x, dtype=float)
    c.y = np.array(y, dtype=float)

    return c


def get_styles():
    """
    Get the list of available plot styles.

    :return: list -- the list of available style names or an empty list if no styles exist.
    """
    if stylesLoaded:
        return plt.style.available

    return list()


def create_plot(curvelist, **kwargs):
    """
    Create a plot from of the curves in curvelist. The available keyword arguments are:
    * Filename: fname='myFile'
    * Save Format: ftype='pdf'
    * Plot Title: title='My Title'
    * X-Axis Label: xlabel='X'
    * Y-Axis Label: ylabel='Y'
    * Show/Hide Plot Legend: legend=True
    * Plot Style: stylename='ggplot'
    * Show X-Axis in log scale: xls=True
    * Show Y-Axis in log scale: yls=True
    * Set the width of the figure in inches: fwidth=1.2
    * Set the height of the figure in inches: fheight=2.1

    >>> curves = pydvif.read('testData.txt')

    >>> plot1 = pydvif.create_plot(curves, fname='myPlot1')

    >>> plot2 = pydvif.create_plot(curves, fname='myPlot2', ftype='pdf', fwidth=10.1, fheight=11.3, title='My Plot', xlabel='X', ylabel='Y', legend=True, stylename='ggplot')

    :param curvelist: The curve or list of curves to plot
    :type curvelist: list
    :param kwargs: The keyword arguments to modify the plot.
    :type kwargs: dict
    :return: matplotlib.pyplot -- the plot of the curves
    """
    fname = None
    ftype = 'png'
    title = ''
    xlabel = ''
    ylabel = ''
    legend = False
    stylename = 'ggplot'
    xls = False
    yls = False
    fwidth = None
    fheight = None

    # Process kwargs
    for key, val in list(kwargs.items()):
        if key == 'fname':
            fname = val
        elif key == 'ftype':
            ftype = val
        elif key == 'title':
            title = val
        elif key == 'xlabel':
            xlabel = val
        elif key == 'ylabel':
            ylabel = val
        elif key == 'legend':
            legend = val 
        elif key == 'stylename':
            stylename = val
        elif key == 'xls':
            xls = val
        elif key == 'yls':
            yls = val
        elif key == 'fwidth':
            fwidth = val
        elif key == 'fheight':
            fheight = val

    if stylesLoaded:
        styles = get_styles()

        try:
            idx = styles.index(stylename)
            style.use(styles[idx])
        except:
            if len(styles) > 0:
                style.use(styles[0])

    plt.clf()
    plt.cla()
    axis = plt.gca()

    if(xls):
        axis.set_xscale('log', nonposx='clip')
    if(yls):
        axis.set_yscale('log', nonposy='clip')

    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        if not curve.hidden:
            xdat = np.array(curve.x)
            ydat = np.array(curve.y)

            if(yls):
                for i in range(len(ydat)):
                    if(ydat[i] < 0):
                        ydat[i] = 1e-301    #custom ydata clipping
            if(xls):
                for i in range(len(xdat)):
                    if(xdat[i] < 0):
                        xdat[i] = 1e-301    #custom xdata clipping

            if curve.ebar is not None:
                c = plt.errorbar(xdat, ydat, yerr=[curve.ebar[0], curve.ebar[1]], xerr=[curve.ebar[2], curve.ebar[3]], fmt='-')
            elif curve.erange is not None:
                c = plt.plot(xdat, ydat)
                plt.fill_between(xdat, ydat - curve.erange[0], ydat + curve.erange[1], alpha=0.4, color=c[0].get_color())
            else:
                c = plt.plot(xdat, ydat)

            if curve.linespoints:
                plt.setp(c[0], marker=curve.marker, markersize=curve.markersize, linestyle=curve.linestyle)
            elif curve.scatter:
                plt.setp(c[0], marker=curve.marker, markersize=curve.markersize, linestyle=' ')
            else:
                plt.setp(c[0], linestyle=curve.linestyle)

            if curve.linewidth:
                plt.setp(c[0], lw=curve.linewidth)
                plt.setp(c[0], mew=curve.linewidth)

            plt.setp(c[0], label=curve.name)

            if curve.color != '':
                plt.setp(c, color=curve.color)
            else:
                curve.color = c[0].get_color()

            if curve.dashes is not None:
                c[0].set_dashes(curve.dashes)

    if legend:
        plt.legend(fancybox=True, numpoints=1, loc=1, ncol=1).get_frame().set_alpha(0.5)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # Change figure size
    figure = plt.gcf()
    if fwidth is not None:
        figure.set_figwidth(float(fwidth), True)
    if fheight is not None:
        figure.set_figheight(float(fheight), True)

    if fname is not None:
        try:
            plt.savefig(fname + '.' + ftype, format=ftype)
        except:
            print('Error: Could not save image to ' + fname + ' of type ' + ftype)

    return plt


def save(fname, curvelist, verbose=False):
    """
    Saves the given Curve or list of Curves to a file named fname.

    >>> curves = list()

    >>> curves.append(pydvif.makecurve([1, 2, 3, 4], [5, 10, 15, 20]))

    >>> pydvif.save('myfile.txt', curves) OR

    >>> pydvif.save('myfile.txt', curves[0])

    :param fname: ULTRA filename
    :type fname: str
    :param curvelist: The curve or list of curves to save
    :type curvelist: Curve or list
    :param verbose: prints the error stacktrace when True
    :type verbose: bool
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    try:
        f = open(fname, 'w')
        for curve in curves:
            f.write('# ' + curve.name + '\n')
            for dex in range(len(curve.x)):
                f.write(' ' + str(curve.x[dex]) + ' ' + str(curve.y[dex]) + '\n')
    except:
        print('Error: Can not write to: ' + fname)
        if verbose:
            traceback.print_exc(file=sys.stdout)
    finally:
        if f:
            f.close()


def savecsv(fname, curvelist, verbose=False):
    """
    Saves the Curve or list of Curves to file in comma separated values (csv) format. Assumes
    all curves have the same x basis.

    >>> curves = list()

    >>> curves.append(pydvif.makecurve([1, 2, 3, 4], [5, 10, 15, 20]))

    >>> pydvif.savecsv('myfile.csv', curves)

    :param fname: ULTRA filename
    :type fname: str
    :param curvelist: The Curve or list of Curves to save
    :type curvelist: list
    :param verbose: prints the error stacktrace when True
    :type verbose: bool
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    try:
        f = open(fname, 'w')
        s = '# time'
        for curve in curves:
            s += ', ' + curve.name
        s += '\n'
        f.write(s)
        for i in range(len(curvelist[0].x)):
            s = str(curvelist[0].x[i])
            for j in range(len(curvelist)):
                s += ', ' + str(curvelist[j].y[i])
            s += '\n'
            f.write(s)
    except:
        print('Error: Can not write to: ' + fname)
        if verbose:
            traceback.print_exc(file=sys.stdout)
    finally:
        if f:
            f.close()


def read(fname, gnu=False, xcol=0, verbose=False, pattern=None, matches=None):
    """
    Read the file and add parsed curves to a curvelist

    >>> curves = pydvif.read('testData.txt')

    >>> curves = pydvif.read('testData.txt', False, 0, False, '*_name', 20)

    :param fname: ULTRA filename
    :type fname: str
    :param gnu: optional, flag to determine if the file is a column oriented (.gnu) file.
    :type gnu: bool
    :param xcol: optional, x-column number for column oriented (.gnu) files
    :type xcol: int
    :param verbose: optional, prints the error stacktrace when True
    :type verbose: bool
    :param pattern: optional, the regular expression pattern
    :type pattern: str
    :param matches: optional, maximum number of times to match pattern, if specified
    :type matches: int
    :returns: list -- the list of curves from the file matching pattern, if specified
    
    """
    def bundle_curve(_curve, build_x, build_y):
        if len(build_x) != len(build_y):
            build_y.append(build_y[-1])

            _curve.x = np.array(build_x, dtype=float).repeat(2)[1:]
            _curve.y = np.array(build_y, dtype=float).repeat(2)[:-1]
            _curve.step = True
        else:
            _curve.x = np.array(build_x, dtype=float)
            _curve.y = np.array(build_y, dtype=float)
            _curve.step = False

        return _curve

    curve_list = list()
    regex = None

    if pattern:
        regex = re.compile(r"%s" % pattern)
    fname = os.path.expanduser(fname)
    _, ext = os.path.splitext(fname)
    try:
        if gnu or ext == '.gnu':
            return __loadcolumns(fname, xcol)

        if pdbLoaded:
            try:
                fpdb = pdb.open(fname, 'r')
                return __loadpdb(fname, fpdb)
            except:
                pass

        match_count = 0
        build_list_x = list()
        build_list_y = list()
        current = None
        new_curve = True
        potential_curve_name = ""
        with open(fname, 'r') as f:
            for line in f:
                split_line = re.split(r'[ _\t]+', str.strip(line))
                if not split_line or not split_line[0]:
                    continue
                elif split_line[0] in {'##', 'end', 'End', 'END'}:
                    continue
                elif split_line[0] == '#':
                    # We may have just finished buiding a curve, so we need to
                    # add it to the list of curves.
                    # If this is the first curve, then current will be None, so
                    # we won't add anything.
                    # If there is a sequence of lines that start with # before
                    # getting to the actual data, then the new_curve flag will
                    # keep us from adding all those comments as curves.
                    if current and not new_curve: 

                        # Need this since it will add last match below and outside loop
                        if matches and match_count >= matches:
                            break

                        curve_list.append(bundle_curve(current, build_list_x, build_list_y))
                        build_list_x = list()
                        build_list_y = list()

                    # Begin setup of new curve
                    new_curve = True
                    potential_curve_name = ' '.join(split_line[1:])
                else:
                    if new_curve:
                        curve_name = potential_curve_name
                        new_curve = False
                        if regex:
                            if regex.search(curve_name):
                                match_count += 1
                                current = curve.Curve(fname, curve_name)
                                build_list_x += split_line[::2]
                                build_list_y += split_line[1::2]
                            else:
                                current = None
                        else:
                            current = curve.Curve(fname, curve_name)
                            build_list_x += split_line[::2]
                            build_list_y += split_line[1::2]

                    elif current and not new_curve: # add data to current curve
                        build_list_x += split_line[::2]
                        build_list_y += split_line[1::2]

        # Append the last curve that we built
        if current:
            curve_list.append(bundle_curve(current, build_list_x, build_list_y))

    except IOError:
        print('could not load file: {}'.format(fname))
        if verbose:
            traceback.print_exc(file=sys.stdout)
    except ValueError:
        print('invalid pydv file: {}'.format(fname))
        if verbose:
            traceback.print_exc(file=sys.stdout)

    return curve_list


def filtercurves(curvelist, pattern):
    """
    Filters the list of curves based on the regular expression pattern.

    >>> curves = pydvif.filtercurves(curves, "*_name")

    :param curvelist: the list of curves
    :type curvelist: Curve
    :param pattern: the regular expression pattern
    :type pattern: str
    :return: list -- The list of filtered curves from curvelist based on the regular expression pattern
    """
    results = list()
    regex = re.compile(r"%s" % pattern)

    for c in curvelist:
        if regex.search(c.name) is not None:
            results.append(c)

    return results


def readcsv(fname, xcol=0, verbose=False):
    """
    Load a csv (comma separated values) data file, add parsed curves to
    a curvelist. '#' is the comment character.  First uncommented line must
    be the column labels.  We assume the first column is the x-data, every
    other column is y-data.  We also assume all columns are the same length.

    >>> curves = readcsv('testData.csv')

    :param fname: csv filename
    :type fname: str
    :param xcol: x-column number for column oriented (.gnu) files
    :type xcol: int
    :param verbose: prints the error stacktrace when True
    :type verbose: bool
    :returns: list -- the list of curves from the csv file
    """

    curvelist = list()

    try:
        f = open(fname, 'r')
    except IOError:
        print('readcsv: could not load file: ' + fname)
        if verbose:
            traceback.print_exc(file=sys.stdout)
        return curvelist

    try:
        lines = f.readlines()
        iLine = 0
        for l in lines:
            if l[0] != '#':
                break;
            iLine += 1
        if iLine == 0 and False: # FIXME make condition to catch no labels
            print('WARNING: columns have no labels, labels will be assigned...someday')
        alllabels = lines[iLine] # this line has the labels on it.
        colLabels = alllabels.split(',')
        colLabels = [w.strip() for w in colLabels]
        for w in colLabels:  # if someone made labels with quotes, kill the quotes
            if '"' in w: w.replace('"','')
        # check that we have a label for every column
        if len(colLabels) != len(lines[iLine].split(',')) and iLine > 0:
            raise RuntimeError('Sorry, right now PDV requires you to have a label for every column.')
        # We assume some column is the x-data, every other column
        # is y-data
        iLine += 1 # go to next line after header labels
        numcurves = len(lines[iLine].split(',')) - 1

        # Make the curves, append them to self.curvelist.
        # First, get data into lists of numbers
        numDataLines = len(lines) - iLine
        localCurves = []
        for i in range(numcurves+1):
            localCurves.append([]) # FIGURE OUT COOL WAY TO DO THIS LATER: localCurves = (numcurves+1)*[[]]
        # turn the strings into numbers
        for l in lines[iLine:]:
            nums = [float(n) for n in l.split(',')]
            # print 'nums = ', nums, 'numcurves = ', numcurves
            assert len(nums) == numcurves + 1
            if xcol >= numcurves:
                print('xcolumn is %d, larger than the number of curves in the file, use "setxcolumn" to fix that' % xcol)
            for colID in range(numcurves + 1):
                localCurves[colID].append(nums[colID])
        # convert lists to numpy arrays
        for colID in range(numcurves):
            localCurves[colID] = np.array(localCurves[colID])
        # Make Curve objects, add to self.curvelist
        for colID in range(numcurves + 1):
            if colID != xcol:
                c = makecurve(localCurves[xcol], localCurves[colID], colLabels[colID], fname)
                print("Appended curve: ", colLabels[colID], len(c.x), len(c.y))
                curvelist.append(c)
        # tidy up
        f.close()
    # anticipate failure!
    except ValueError as e:
        print(e.message)
        print('readcsv: invalid pydv file: ' + fname)
        if verbose:
            traceback.print_exc(file=sys.stdout)

    return curvelist

def readsina(fname, verbose=False):
    """
    Load a Sina JSON data file, add parsed curves to a curvelist.

    We assume JSON conforming to the Sina schema, with each curve defined in a curve_set. We assume
    there is only one record, and if there are more then we only read the first one. We also assume
    only one independent variable per curve_set; if there are more than one, then PyDV may exhibit
    undefined behavior. Can also read curve_sets within libraries in library_data.
    
    >>> curves = readsina('testData.json')

    :param fname: Sina JSON filename
    :type fname: str
    :param verbose: prints the error stacktrace when True
    :type verbose: bool
    :returns: list: the list of curves from the sina file
    """
    curves = {}
    listed_order = []
    try:
        # Load the curve data from the curve_sets
        with open(fname, 'r') as fp:
            try:
                sina_file = json.load(fp)
                record_id = sina_file['records'][0]['id']
                curve_sets = sina_file['records'][0]['curve_sets']
                library_data = sina_file['records'][0]['library_data']

                def add_curve_set(curve_sets, curves, listed_order, library=''):
                    for curve_set_name, curve_set in curve_sets.items():
                        independent_dict = next(iter(curve_set['independent'].items()))
                        independent_name = independent_dict[0]
                        independent_value = independent_dict[1]['value']
                        for name, v in curve_set['dependent'].items():
                            # TODO: Save the name x and y names with the curves
                            dependent_variable_name = name
                            full_name = curve_set_name + '__SINA_DEP__' + dependent_variable_name
                            dependent_variable_value = v['value']
                            curve_name = dependent_variable_name + ' vs ' + independent_name + " (" + \
                                curve_set_name + ")"
                            if library != '':
                                curve_name += ' ' + library
                                full_name += '__LIBRARY__' + library
                            c = makecurve(x=independent_value, y=dependent_variable_value,
                                name=curve_name, fname=fname, xlabel=independent_name,
                                ylabel=dependent_variable_name, title=curve_name, record_id=record_id)
                            c.step = False
                            print("Appended curve: {}, len x,y: {},{}"
                                .format(dependent_variable_name, len(c.x), len(c.y)))
                            curves[full_name] = c
                            listed_order.append(full_name)
                    return curves, listed_order

                curves, listed_order = add_curve_set(curve_sets, curves, listed_order)

                for library in library_data:
                    if 'curve_sets' in library_data[library]:
                        curve_sets = library_data[library]['curve_sets']
                        curves, listed_order = add_curve_set(curve_sets, curves, listed_order, library=library)
            except KeyError:
                print('readsina: Sina file {} is malformed'.format(fname))
                if verbose:
                    traceback.print_exc(file=sys.stdout)
                return []

        # Try to load the order in which the user wants to load the curves into PyDV
        with open(fname, 'r') as fp:
            try:
                order_options = json.load(fp)['records'][0]['data']['SINA_timeplot_order']['value']
            except:
                order_options = listed_order

    except IOError:
        print('readsina: could not load file: {}'.format(fname))
        if verbose:
            traceback.print_exc(file=sys.stdout)
        return []
    
    try:
        curves_lst = [curves[name] for name in order_options]
    except KeyError:
        print('readsina: mismatch between dependent variable names in the curve_sets and the ' + \
            'ordering specified in SINA_timeplot_order. Using default ordering instead.')
        if verbose:
            traceback.print_exc(File=sys.stdout)
        curves_lst = [curves[name] for name in listed_order]
    return curves_lst



########################################################
################## Math Functions  #####################
########################################################

def cos(curvelist):
    """
    Take the cosine of y values of a Curve or list of Curves.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.cos(curves) OR

     >>> pydvif.cos(curves[0])

    :param curvelist: The Curve or list of Curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.cos(curve.y)


def cosx(curvelist):
    """
    Take the cosine of x values of a Curve or list of Curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.cosx(curves) OR

    >>> pydvif.cosx(curves[0])

    :param curvelist: The Curve or list of Curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.cos(curve.x)

def cosh(curvelist):
    """
    Take the hyperbolic cosine of y values of a Curve or list of Curves.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.cosh(curves) OR

     >>> pydvif.cosh(curves[0])

    :param curvelist: The Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.cosh(curve.y)


def coshx(curvelist):
    """
    Take the hyperbolic cosine of x values of a Curve or list of Curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.coshx(curves) OR

    >>> pydvif.coshx(curves[0])

    :param curvelist: The Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.cosh(curve.x)


def acosh(curvelist):
    """
    Take the hyperbolic arccosine of y values of a Curve or list of Curves.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.acosh(curves) OR

     >>> pydvif.acosh(curves[0])

    :param curvelist: The Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.arccosh(curve.y)


def acoshx(curvelist):
    """
    Take the hyperbolic arccosine of x values of a Curve or list of Curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.acoshx(curves) OR

    >>> pydvif.acoshx(curves[0])

    :param curvelist: The Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.arccosh(curve.x)


def acos(curvelist):
    """
    Take the arccosine of y values of a Curve or list of Curves

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.acos(curves) OR

     >>> pydvif.acos(curves[0])

    :param curvelist: The Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.arccos(curve.y)


def acosx(curvelist):
    """
    Take the arccosine of x values of a Curve or list of Curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.acosx(curves) OR

    >>> pydvif.acosx(curves[0])

    :param curvelist: The Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.arccos(curve.x)


def sin(curvelist):
    """
    Take the sine of y values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.sin(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """
    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.sin(c.y)
    else:
        curvelist.y = np.sin(curvelist.y)


def sinx(curvelist):
    """
    Take the sine of x values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.sinx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.sin(c.x)
    else:
        curvelist.x = np.sin(curvelist.x)


def sinh(curvelist):
    """
    Take the hyperbolic sine of y values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.sinh(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.sinh(c.y)
    else:
        curvelist.y = np.sinh(curvelist.y)


def sinhx(curvelist):
    """
    Take the hyperbolic sine of x values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.sinhx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.sinh(c.x)
    else:
        curvelist.x = np.sinh(curvelist.x)


def asinh(curvelist):
    """
    Take the hyperbolic arcsine of y values of a single curve or curves in a list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.asinh(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.asinh(c.y)
    else:
        curvelist.y = np.asinh(curvelist.y)


def asinhx(curvelist):
    """
    Take the hyperbolic arcsine of x values of a single curve or curves in a list.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.asinhx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.asinh(c.x)
    else:
        curvelist.x = np.asinh(curvelist.x)


def asin(curvelist):
    """
    Take the arcsine of y values of a single curve or curves in a list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.asin(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """
    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.asin(c.y)
    else:
        curvelist.y = np.asin(curvelist.y)


def asinx(curvelist):
    """
    Take the arcsine of x values of a single curve or curves in a list.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.asinx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.asin(c.x)
    else:
        curvelist.x = np.asin(curvelist.x)


def tan(curvelist):
    """
    Take the tangent of y values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.tan(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.tan(c.y)
    else:
        curvelist.y = np.tan(curvelist.y)


def tanx(curvelist):
    """
    Take the tangent of x values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.tanx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.tan(c.x)
    else:
        curvelist.x = np.tan(curvelist.x)


def tanh(curvelist):
    """
    Take the hyperbolic tangent of y values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.tanh(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.tanh(c.y)
    else:
        curvelist.y = np.tanh(curvelist.y)


def tanhx(curvelist):
    """
    Take the hyperbolic tangent of x values of a single curve or multiple curves in list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.tanhx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.tanh(c.x)
    else:
        curvelist.x = np.tanh(curvelist.x)


def atan(curvelist):
    """
    Take the arctangent of y values of a single curve or curves in a list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.atan(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.atan(c.y)
    else:
        curvelist.y = np.atan(curvelist.y)


def atanx(curvelist):
    """
    Take the arctangent of x values of a single curve or curves in a list.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.atanx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.atan(c.x)
    else:
        curvelist.x = np.atan(curvelist.x)


def atanh(curvelist):
    """
    Take the hyperbolic arctangent of y values of a single curve or curves in a list.

     >>> curves = pydvif.read('testData.txt')

     >>> pydvif.atanh(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.atanh(c.y)
    else:
        curvelist.y = np.atanh(curvelist.y)


def atanhx(curvelist):
    """
    Take the hyperbolic arctangent of x values of a single curve or curves in a list.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.atanhx(curves)

    :param curvelist: A single curve or a list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.atanh(c.x)
    else:
        curvelist.x = np.atanh(curvelist.x)


def atan2(c1, c2, t=None):
    """
    Perform the atan2 method for a pair of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.atan2(curves[0], curves[1])   OR

    >>> pydvif.atan2(curves[0], curves[1], tuple(['A', 'B']))

    :param c1: the first curve
    :type c1: curve
    :param c2: the second curve
    :type c2: curve
    :param t: A tuple containing exactly two values to insert into the name string for the new curve
    :type t: tuple
    :return: curve -- a new curve with the results from this operation
    """
    if t is None:
        t = tuple([c1.name, c2.name])

    c = curve.Curve('', 'atan2(%s,%s)' % t)
    c.x = np.array(c1.x)
    c.y = np.arctan2(c1.y, c2.y)

    return c


def add(curvelist):
    """
    Add one or more curves.

    >>> curves = pydvif.read('testData.txt')

    >>> c = pydvif.add(curves)

    :param curvelist: The list of curves
    :type curvelist: list
    :returns: curve -- the curve containing the sum of the curves in curvelist
    """

    numcurves = len(curvelist)
    if numcurves > 1:
        name = curvelist[0].name
        sendline = 'curvelist[' + str(0) + ']'
        for i in range(1, numcurves):
            name += ' + ' + curvelist[i].name
            sendline += '+ curvelist[' + str(i) + ']'

        c = eval(sendline)
        c.name = name

        if c.x is None or len(c.x) < 2:
            print('Error: curve overlap is insufficient')
            return 0

        return c
    elif numcurves == 1:
        return curvelist[0]
    else:
        return curvelist


def subtract(curvelist):
    """
    Take difference of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> c = pydvif.subtract(curves)

    :param curvelist: The list of curves
    :type curvelist: list
    :returns: curve -- the curve containing the difference of the curves
    """

    numcurves = len(curvelist)
    if numcurves > 1:
        name = curvelist[0].name
        sendline = 'curvelist[' + str(0) + ']'
        for i in range(1, numcurves):
            name += ' - ' + curvelist[i].name
            sendline += '- curvelist[' + str(i) + ']'

        c = eval(sendline)
        c.name = name

        if c.x is None or len(c.x) < 2:
            print('Error: curve overlap is insufficient')
            return 0

        return c
    elif numcurves == 1:
        return curvelist[0]
    else:
        return curvelist


def multiply(curvelist):
    """
    Take product of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> c = pydvif.multiply(curves)

    :param curvelist: The list of curves
    :type curvelist: list
    :returns: Curve -- the curve containing the product of the curves
    """
    numcurves = len(curvelist)
    if numcurves > 1:
        name = __toCurveString(curvelist[0])
        sendline = 'curvelist[' + str(0) + ']'
        for i in range(1, numcurves):
            name += ' * ' + __toCurveString(curvelist[i])
            sendline += '* curvelist[' + str(i) + ']'

        c = eval(sendline)
        c.name = name

        if c.x is None or len(c.x) < 2:
            print('Error: curve overlap is insufficient')
            return 0

        return c
    elif numcurves == 1:
        return curvelist[0]
    else:
        return curvelist


def divide(curvelist):
    """
    Take quotient of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> c = pydvif.divide(curves)

    :param curvelist: The list of curves
    :type curvelist: list
    :returns: curve -- the curve containing the quotient of the curves
    """
    numcurves = len(curvelist)
    if numcurves > 1:
        name = __toCurveString(curvelist[0])
        sendline = 'curvelist[' + str(0) + ']'
        for i in range(1, numcurves):
            name += ' / ' + __toCurveString(curvelist[i])
            sendline += '/ curvelist[' + str(i) + ']'

        c = eval(sendline)
        c.name = name

        if c.x is None or len(c.x) < 2:
            print('Error: curve overlap is insufficient')
            return 0

        return c
    elif numcurves == 1:
        return curvelist[0]
    else:
        return curvelist


def divx(curvelist, value):
    """
    Divide x values of the curve(s) by a constant value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.divx(curves, 4)

    :param curvelist: The curve or curvelist
    :type curvelist: Curve or list
    :param value: The divisor
    :type value: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if float(value) == 0:
            value = 1.e-10
        c.x /= float(value)


def divy(curvelist, value):
    """
    Divide y values of the curve(s) by a constant value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.divy(curves, 4)

    :param curvelist: The curve or curvelist
    :type curvelist: Curve or list
    :param value: The divisor
    :type value: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if float(value) == 0:
            value = 1.e-10
        c.y /= float(value)


def dx(curvelist, value):
    """
    Shift x values of a curve or list of curves by a constant value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.dx(curves, 4) OR

    >>> pydvif.dx(curves[0], 4)


    :param curvelist: A curve or curvelist
    :type curvelist: Curve or list
    :param value: The amount to shift the x values by
    :type value: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x += float(value)


def dy(curvelist, value):
    """
    Shift y values of a curve or list of curves by a constant value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.dy(curves, 4) OR

    >>> pydvif.dy(curves[0], 4)


    :param curvelist: A curve or curvelist
    :type curvelist: Curve or list
    :param value: The amount to shift the y values by
    :type value: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y += float(value)


def mx(curvelist, value):
    """
    Scale x values of a curve or list of curves by a constant value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.mx(curves, 4) OR

    >>> pydvif.mx(curves[0], 4)


    :param curvelist: A curve or curvelist
    :type curvelist: Curve or list
    :param value: The amount to scale the x values by
    :type value: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x *= float(value)


def my(curvelist, value):
    """
    Scale y values of a curve or list of curves by a constant value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.my(curves, 4) OR

    >>> pydvif.my(curves[0], 4)


    :param curvelist: A curve or curvelist
    :type curvelist: Curve or list
    :param value: The amount to scale the y values by
    :type value: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y *= float(value)

def l1(c1, c2, xmin=None, xmax=None):
    """
    Make a new curve that is the L1 norm of curve c1 and  curve c2.
    The L1-norm is the integral(\|c1 - c2\|) over the interval [xmin, xmax].

    >>> c = pydvif.l1(curve1, curve2)

    >>> c2 = pydvif.l1(curve1, curve2, 1.1, 10.9)

    :param c1: The first curve
    :type c1: Curve
    :param c2: The second curve
    :type c2: Curve
    :param xmin: the minimum x value to perform the L1 norm
    :type xmin: float
    :param xmax: the maximum x value to perform the L1 norm
    :type xmax: float
    :returns Curve: A new curve that is the L1 norm of c1 and c2
    """
    c = c1 - c2
    c.y = np.abs(c.y)

    if xmin is not None and xmax is not None:
        if xmax <= xmin:
            raise RuntimeError("xmin > xmax or xmin == xmax in l1")
    else:
        xmin = np.min(c.x)
        xmax = np.max(c.x)

    d = integrate(c, xmin, xmax)
    d[0].name = "L1 of " + __toCurveString(c1) + " and " + __toCurveString(c2)

    return d[0]


def l2(c1, c2, xmin=None, xmax=None):
    """
    Make a new curve that is the L2 norm of curve c1 and curve c2.
    The L2-norm is (integral((c1 - c2)**2)**(1/2) over the interval [xmin, xmax].

    >>> c = pydvif.l2(curve1, curve2)

    >>> c2 = pydvif.l2(curve1, curve2, 3.1, 30.9)

    :param c1: The first curve
    :type c1: Curve
    :param c2: The second curve
    :type c2: Curve
    :param xmin: the minimum x value to perform the L2 norm
    :type xmin: float
    :param xmax: the maximum x value to perform the L2 norm
    :type xmax: float
    :returns Curve: A new curve that is the L2 norm of c1 and c2
    """
    c = c1 - c2
    c.y = np.abs(c.y)
    c = c**2.0

    if xmin is not None and xmax is not None:
        if xmax <= xmin:
            raise RuntimeError("xmin > xmax or xmin == xmax in l2")
    else:
        xmin = np.min(c.x)
        xmax = np.max(c.x)

    d = integrate(c, xmin, xmax)
    d[0] = d[0]**(0.5)
    d[0].name = "L2 of " + __toCurveString(c1) + " and " + __toCurveString(c2)

    return d[0]


def norm(c1, c2, p, xmin=None, xmax=None):
    """
    Make a new curve that is the p-norm of curve c1 and curve c2.

    >>> curves = pydvif.read('testData.txt')

    >>> c = pydvif.norm(curves[0], curves[1], 'inf')

    >>> curves.append(c)

    :param c1: The first curve
    :type c1: Curve
    :param c2: The second curve
    :type c2: Curve
    :param p: the order (e.g., 'inf', '3', '5')
    :type p: str
    :param xmin: the minimum x value to perform the p-norm
    :type xmin: float
    :param xmax: the maximum x value to perform the p-norm
    :type xmax: float
    :returns Curve: A new curve that is the p-norm of c1 and c2
    """
    c = c1 - c2
    c.y = np.abs(c.y)

    if p.lower() != "inf":
        N = int(p)
        c = c**N

    if xmin is not None and xmax is not None:
        if xmax <= xmin:
            raise RuntimeError("xmin > xmax or xmin == xmax in norm")
    else:
        xmin = np.min(c.x)
        xmax = np.max(c.x)

    if p.lower() == "inf":
        Linf = 0.0
        for xi, yi in zip(c.x, c.y):
            if xmin <= xi <= xmax:
                Linf = max(Linf, yi)
        d = c
        d.y = np.array([Linf] * c.y.shape[0])
        d.name = "Linf of " + __toCurveString(c1) + " and " + __toCurveString(c2)

        return d
    else:
        d = integrate(c, xmin, xmax)
        d[0] = d[0]**(1.0/N)
        d[0].name = "L%d of " % N + __toCurveString(c1) + " and " + __toCurveString(c2)

        return d[0]


def abs(curvelist):
    """
    Take the absolute value of the y values of the Curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.abs(curves) OR

    >>> pydvif.abs(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.abs(curve.y)

def absx(curvelist):
    """
    Take the absolute value of the x values of the Curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.absx(curves) OR

    >>> pydvif.absx(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.abs(curve.x)


def log(curvelist, keep=True):
    """
    Take the natural logarithm of y values of the Curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.log(curves) OR

    >>> pydvif.log(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    :param keep: flag to determine whether or not to discard zero or negative y-values before taking the log.
                 keep is True by default.
    :type keep: optional, boolean
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if not keep:
            skiplist = np.where(c.y <= 0)[0]
            if len(skiplist) > 0:
                c.y = np.delete(c.y, skiplist)
                c.x = np.delete(c.x, skiplist)

        c.y = np.log(c.y)
        if c.name[:3] == 'exp':
            c.name = c.name[4:-1] # Pop off the exp( from the front and the ) from the back
        else:
            c.name = 'log(' + c.name + ')'

def logx(curvelist, keep=True):
    """
    Take the natural logarithm of x values of the Curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.logx(curves) OR

    >>> pydvif.logx(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    :param keep: flag to determine whether or not to discard zero or negative x-values before taking the log.
                 keep is True by default.
    :type keep: optional, boolean
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if not keep:
            skiplist = np.where(c.x <= 0)[0]
            if len(skiplist) > 0:
                c.y = np.delete(c.y, skiplist)
                c.x = np.delete(c.x, skiplist)

        c.x = np.log(c.x)
        if c.name[:4] == 'expx':
            c.name = c.name[5:-1] # Pop off the expx( from the front and the ) from the back
        else:
            c.name = 'logx(' + c.name + ')'

def log10(curvelist, keep=True):
    """
    Take the base 10 logarithm of y values of a Curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.log10(curves) OR

    >>> pydvif.log10(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    :param keep: flag to determine whether or not to discard zero or negative y-values before taking the base 10 logarithm.
                 keep is True by default.
    :type keep: optional, boolean
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if not keep:
            skiplist = np.where(c.y <= 0)[0]
            if len(skiplist) > 0:
                c.y = np.delete(c.y, skiplist)
                c.x = np.delete(c.x, skiplist)

        c.y = np.log10(c.y)
        c.name = 'log10(' + c.name + ')'


def log10x(curvelist, keep=True):
    """
    Take the base 10 logarithm of x values of a Curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.log10x(curves) OR

    >>> pydvif.log10x(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    :param keep: flag to determine whether or not to discard zero or negative y-values before taking the base 10 logarithm.
                 keep is True by default.
    :type keep: optional, boolean
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if not keep:
            skiplist = np.where(c.x <= 0)[0]
            if len(skiplist) > 0:
                c.y = np.delete(c.y, skiplist)
                c.x = np.delete(c.x, skiplist)

        c.x = np.log10(c.x)
        c.name = 'log10x(' + c.name + ')'


def exp(curvelist):
    """
    Exponentiate y values of the Curve or list of curves (e**y).

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.exp(curves) OR

    >>> pydvif.exp(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.exp(curve.y)


def expx(curvelist):
    """
    Exponentiate x values of the Curve or list of curves (e**x).

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.expx(curves) OR

    >>> pydvif.expx(curves[0])

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.exp(curve.x)


def powa(curvelist, a):
    """
    Raise a fixed value, a, to the power of the y values of the Curve or list of curves. y = a^y

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.powa(curves, 2) OR

    >>> pydvif.powa(curves[0], 2)

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    :param a: the fixed value
    :type a: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.y = np.power(float(a), curve.y)


def powax(curvelist, a):
    """
    Raise a fixed value, a, to the power of the x values of the Curve or curves. x = a^x

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.powax(curves, 4.2) OR

    >>> pydvif.powax(curves[0], 4.2)

    :param curvelist: the Curve or list of curves
    :type curvelist: Curve or list
    :param a: the fixed value
    :type a: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for curve in curves:
        curve.x = np.power(float(a), curve.x)


def powr(curvelist, a):
    """
    Raise a the y values of a curve or list of curves to a fixed power, y = y^a.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.powr(curves, 4.2) OR

    >>> pydvif.powr(curves[0], 4.2)

    :param curvelist: the curve or list of curves
    :type curvelist: curve or list
    :param a: the fixed value
    :type a: float
    """
    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.power(c.y, float(a))
    else:
        curvelist.y = np.power(curvelist.y, float(a))


def powrx(curvelist, a):
    """
    Raise a the x values of a curve or list of curves to a fixed power, x = x^a.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.powrx(curves, 4.2) OR

    >>> pydvif.powrx(curves[0], 4.2)

    :param curvelist: the curve or list of curves
    :type curvelist: curve or list
    :param a: the fixed value
    :type a: float
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.power(c.x, float(a))
    else:
        curvelist.x = np.power(curvelist.x, float(a))


def sqr(curvelist):
    """
    Take the square of the y values in a curve or list of curves.

    :param curvelist: the curve or list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.square(c.y)
    else:
        curvelist.y = np.square(curvelist.y)


def sqrx(curvelist):
    """
    Take the square of the x values in a curve or list of curves.

    :param curvelist: the curve or list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.square(c.x)
    else:
        curvelist.x = np.square(curvelist.x)


def sqrt(curvelist):
    """
    Take the square root of the y values in a curve or list of curves.

    :param curvelist: the curve or list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.y = np.sqrt(c.y)
    else:
        curvelist.y = np.sqrt(curvelist.y)


def sqrtx(curvelist):
    """
    Take the square root of the x values in a curve or list of curves.

    :param curvelist: the curve or list of curves
    :type curvelist: curve or list
    """

    if isinstance(curvelist, list):
        for c in curvelist:
            c.x = np.sqrt(c.x)
    else:
        curvelist.x = np.sqrt(curvelist.x)


def xmax(curvelist, limit):
    """
    Filter out points in the curve or list of curves whose x values are greater than limit.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param limit: The maximum value
    :type limit: float
    """

    curves = list()

    if isinstance(curvelist, list):
        curves = curvelist
    else:
        curves.append(curvelist)

    for c in curves:
        nx = []
        ny = []

        for i in range(len(c.x)):
            if c.x[i] <= float(limit):
                nx.append(c.x[i])
                ny.append(c.y[i])

        c.x = np.array(nx)
        c.y = np.array(ny)


def xmin(curvelist, min):
    """
    Filter out points in the curve or list of curves whose x values are less than min.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param min: The minimum value
    :type min: float
    """

    curves = list()

    if isinstance(curvelist, list):
        curves = curvelist
    else:
        curves.append(curvelist)

    for c in curves:
        nx = []
        ny = []

        for i in range(len(c.x)):
            if c.x[i] >= float(min):
                nx.append(c.x[i])
                ny.append(c.y[i])

        c.x = np.array(nx)
        c.y = np.array(ny)


def xminmax(curvelist, min, max):
    """
    Filter out points in the curve or list of curves whose x values are
    less than min or greater than max.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param min: The minimum value
    :type  min: float
    :param max: The maximum value
    :type max: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves = curvelist
    else:
        curves.append(curvelist)

    for c in curves:
        nx = []
        ny = []

        for i in range(len(c.x)):
            if float(min) <= c.x[i] <= float(max):
                nx.append(c.x[i])
                ny.append(c.y[i])

        c.x = np.array(nx)
        c.y = np.array(ny)


def ymax(curvelist, max):
    """
    Filter out points in the curve or list of curves whose y values are greater than limit.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param max: The maximum value
    :type max: float
    """

    curves = list()

    if isinstance(curvelist, list):
        curves = curvelist
    else:
        curves.append(curvelist)

    for c in curves:
        nx = []
        ny = []

        for i in range(len(c.y)):
            if c.y[i] <= float(max):
                nx.append(c.x[i])
                ny.append(c.y[i])

        c.x = np.array(nx)
        c.y = np.array(ny)


def ymin(curvelist, min):
    """
    Filter out points in the curve or list of curves whose y values are less than min.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param min: The minimum value
    :type min: float
    """

    curves = list()

    if isinstance(curvelist, list):
        curves = curvelist
    else:
        curves.append(curvelist)

    for c in curves:
        nx = []
        ny = []

        for i in range(len(c.y)):
            if c.y[i] >= float(min):
                nx.append(c.x[i])
                ny.append(c.y[i])

        c.x = np.array(nx)
        c.y = np.array(ny)


def yminmax(curvelist, min, max):
    """
    Filter out points in the curve or list of curves whose y values are
    less than min or greater than max.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param min: The minimum value
    :type  min: float
    :param max: The maximum value
    :type max: float
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        nx = []
        ny = []

        for i in range(len(c.y)):
            if float(min) <= c.y[i] <= float(max):
                nx.append(c.x[i])
                ny.append(c.y[i])

        c.x = np.array(nx)
        c.y = np.array(ny)


def yn(curvelist, n):
    """
    Take the Bessel function of the second kind of order n for the y values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param n: The order
    :type n: int
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = scipy.special.yn(int(n), c.y)


def ynx(curvelist, n):
    """
    Take the Bessel function of the second kind of order n for the x values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param n: The order
    :type n: int
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = scipy.special.yn(int(n), c.x)


def y0(curvelist):
    """
    Take the Bessel function of the second kind of the zeroth order for the y values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = scipy.special.y0(c.y)


def y0x(curvelist):
    """
    Take the Bessel function of the second kind of the zeroth order for the x values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = scipy.special.y0(c.x)


def y1(curvelist):
    """
    Take the Bessel function of the second kind of the first order for the y values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = scipy.special.y1(c.y)


def y1x(curvelist):
    """
    Take the Bessel function of the second kind of the first order for the x values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = scipy.special.y1(c.x)


def jn(curvelist, n):
    """
    Take the Bessel function of the first kind of the nth order for the y values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param n: The order
    :type n: float
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = scipy.special.jn(float(n), c.y)


def jnx(curvelist, n):
    """
    Take the Bessel function of the first kind of the nth order for the x values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    :param n: The order
    :type n: float
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = scipy.special.jn(int(n), c.x)


def j0(curvelist):
    """
    Take the Bessel function of the first kind of the zeroth order for the y values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = scipy.special.j0(c.y)


def j0x(curvelist):
    """
    Take the Bessel function of the first kind of the zeroth order for the x values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = scipy.special.j0(c.x)


def j1(curvelist):
    """
    Take the Bessel function of the first kind of the first order for the y values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = scipy.special.j1(c.y)


def j1x(curvelist):
    """
    Take the Bessel function of the first kind of the first order for the x values of
    curves in curvelist.

    :param curvelist: The curve or list of curves
    :type curvelist: curve or list
    """
    # scipy.special.errprint(1)
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = scipy.special.j1(c.x)


def recip(curvelist):
    """
    Take the reciprocal of the y values of the curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.recip(curves[1])

    >>> pydvif.create_plot(curves, legend=True, stylename='ggplot')

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = np.reciprocal(c.y)


def recipx(curvelist):
    """
    Take the reciprocal of the x values of the curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.dx(curves, 2)

    >>> pydvif.recipx(curves)

    >>> pydvif.create_plot(curves, legend=True, stylename='ggplot')

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    :return:
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.x = np.reciprocal(c.x)


def integrate(curvelist, low=None, high=None):
    """
     Take the integral of the curve or curves in curvelist.

    :param curvelist: A curve or list of curves
    :type curvelist: curve or list
    :param low: The lower limit
    :type low: float
    :param high: The maximum limit
    :type high: float
    :return: list -- the list of integrated curves
    """
    curves = list()
    ncurves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        nc = c.copy()
        nc.plotname = ''
        nc.color = ''

        if low is None:
            nc.name = 'Integrate ' + c.plotname
        else:
            nc.name = 'Integrate %s [%.1f,%.1f]' % (c.plotname, low, high)

        if low is None:
            low = min(nc.x)

        if high is None:
            high = max(nc.x)

        r = __get_sub_range(nc.x, low, high)
        nc.x = nc.x[r[0]:r[1]+1]
        nc.y = nc.y[r[0]:r[1]+1]
        nc.y = np.array(scipy.integrate.cumtrapz(nc.y, nc.x, initial=0.0))

        ncurves.append(nc)

    return ncurves


def alpha(ac, ig, res, npts=-1):
    if npts == -1:
        npts = len(ac.y)

    ai = curve.Curve.__mul__(ac, ig)
    num = convolveb(ai, res, npts)
    denom = convolveb(ig, res, npts)
    alpha_measured = curve.Curve.__div__(num, denom)

    alpha_measured.name = "Measured alpha"
    alpha_measured.plotname = ''
    return alpha_measured


def gaussian(amp, wid, center, num=100, nsd=3):
    """
    Generate a gaussian function.

    >>> curve = pydvif.gaussian(5, 10, 0)

    >>> pydvif.create_plot(curve, legend=True, stylename='ggplot')

    :param amp: amplitude
    :type amp: float
    :param wid: width
    :type wid: float
    :param center: center
    :type center: float
    :param num: optional, number of points
    :type num: int
    :param nsd: optional, number of half-widths
    :type nsd: float
    :return: Curve -- representing the gaussian function
    """
    crv_min = center - (nsd * wid)
    crv_max = center + (nsd * wid)
    cc = span(crv_min, crv_max, num)

    dd = cc.y - center
    cc.y = dd * dd * -1
    cc.y = np.exp(cc.y / (wid * wid))
    cc.y = cc.y * amp

    cc.name = "Gaussian"
    return cc


def getymax(c, xmin=None, xmax=None):
    """
    Get the maximum y-value for the curve within the specified domain.

    :param c: the curve
    :type Curve:
    :param xmin: the minimum x-value for the sub-domain
    :type xmin: float, optional
    :param xmax: the maximum x-value for the sub-domain
    :type xmax: float, optional
    :return: str -- curve name
             list -- a list of tuples where each tuple contains the x-value and
                the max y-value.
    """
    if xmin is not None:
        r = __get_sub_range(c.x, xmin, xmax)
        ymax = max(c.y[r[0]:r[1]+1])
    else:
        ymax = max(c.y)
    xy_pairs_at_max = getx(c, ymax, xmin, xmax)

    return __toCurveString(c), xy_pairs_at_max


def getymin(c, xmin=None, xmax=None):
    """
    Get the minimum y-value for the curve within the specified domain.

    :param c: the curve
    :type Curve:
    :param xmin: the minimum x-value for the sub-domain
    :type xmin: float, optional
    :param xmax: the maximum x-value for the sub-domain
    :type xmax: float, optional
    :return: str -- curve name
             list -- a list of tuples where each tuple contains the x-value and
                the min y-value.
    """
    if xmin is not None:
        r = __get_sub_range(c.x, xmin, xmax)
        ymin = min(c.y[r[0]:r[1]+1])
    else:
        ymin = min(c.y)
    xy_pairs_at_min = getx(c, ymin, xmin, xmax)

    return __toCurveString(c), xy_pairs_at_min


def correlate(c1, c2, mode='valid'):
    """
    Computes the cross-correlation of two 1D sequences (c1.y and c2.y) as defined by numpy.correlate.

    :param c1: The first curve with 1D input sequence c1.y
    :type c1: Curve
    :param c2: The second curve with 1D input sequence c2.y
    :type c2: Curve
    :param mode:
        full:
          By default, mode is 'full'.  This returns the convolution
          at each point of overlap, with an output shape of (N+M-1,). At
          the end-points of the convolution, the signals do not overlap
          completely, and boundary effects may be seen.

        same:
          Mode 'same' returns output of length ``max(M, N)``.  Boundary
          effects are still visible.

        valid:
          Mode 'valid' returns output of length
          ``max(M, N) - min(M, N) + 1``.  The convolution product is only given
          for points where the signals overlap completely.  Values outside
          the signal boundary have no effect.
    :type mode: 'full'(default), 'same' or 'valid' 
    :return: Curve -- the cross-correlation of c1.y and c2.y
    """
    nc = curve.Curve('', 'correlate(' + __toCurveString(c1) + ', ' + __toCurveString(c2) + ')')

    ic1, step = curve.interp1d(c1, len(c1.x), True)
    c2npts = (max(c2.x) - min(c2.x)) / step
    ic2 = curve.interp1d(c2, c2npts)

    y = np.correlate(ic1.y, ic2.y, mode)
    start = min([min(ic1.x), min(ic2.x)])
    stop = max([max(ic1.x), max(ic2.x)])
    nc.x = np.linspace(start, stop, num=len(y))
    nc.y = np.array(y)

    return nc


def convolve(c1, c2, npts=100):
    """
    Compute and return the convolution of two real curves:
    -
    -   ``(g*h)(x) = Int(-inf, inf, dt, g(t)*h(x-t))``
    -
    The Fourier Transform is used to perform the convolution.

    >>> curves = pydvif.read('testData.txt')

    >>> newcurve = pydvif.convolve(curves[0], curves[1])

    :param c1: (N,) The first curve
    :type c1: Curve
    :param c2: (M,) The second curve
    :type c2: Curve
    :param npts: the number of points used to create a uniform temporal spacing
    :type npts: int
    :return: Curve -- the convolution of the two curves c1 and c2
    """

    # Create uniform temporal spacing
    ic1, step = curve.interp1d(c1, npts, True)

    c2npts = (max(c2.x) - min(c2.x)) / step
    ic2 = curve.interp1d(c2, c2npts)

    y = np.array(scipy.signal.convolve(ic1.y, ic2.y, mode='full', method='fft'))
    delx = (max(c1.x) - min(c1.x)) / npts
    y *= delx

    xstart = min(min(c1.x), min(c2.x))
    xstop = xstart + (len(y) * delx)
    x = np.linspace(xstart, xstop, num=len(y))

    namestr = 'Conv ' + __toCurveString(c1) + '*' + __toCurveString(c2) + ' (FFT) ' + str(npts)
    nc = makecurve(x, y, namestr)

    return nc


def convolveb(c1, c2, npts=100):
    """
    Computes the convolution of the two given curves:
    -
    -   ``(g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) / Int(-inf, inf, dt*h(t))``
    -
    This computes the integrals directly which avoid padding and aliasing
    problems associated with FFT methods (it is however slower).

    :param c1: (N,) The first curve
    :type c1: Curve
    :param c2: (M,) The second curve
    :type c2: Curve
    :param npts: the number of points
    :type npts: int
    :return: Curve -- the convolution of the two curves c1 and c2 using integration and normalizing c2
    """

    return convolve_int(c1, c2, True, npts)


def convolvec(c1, c2, npts=100):
    """
    Computes the convolution of the two given curves:
    -
    -   ``(g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) / Int(-inf, inf, dt*h(t))``
    -
    This computes the integrals directly which avoid padding and aliasing
    problems associated with FFT methods (it is however slower).

    :param c1: (N,) The first curve
    :type c1: Curve
    :param c2: (M,) The second curve
    :type c2: Curve
    :param npts: the number of points
    :type npts: int
    :return: Curve -- the convolution of the two curves c1 and c2 using integration and no normalization
    """

    return convolve_int(c1, c2, False, npts)


def convolve_int(c1, c2, norm=True, npts=100):
    """
    Computes the convolution of the two curves (c1, c2). The integrals are computed directly which avoid padding
    and aliasing problems associated with FFT methods (it is however slower).

    :param c1: (N,) The first curve
    :type c1: Curve
    :param c2: (M,) The second curve
    :type c2: Curve
    :param norm: if true then the result is normalized to unit area.
    :type norm: bool
    :param npts: the number of points
    :type npts: int
    :return: nc: Curve -- the convolution of the two curves c1 and c2
    """

    # Create uniform temporal spacing
    ic1, step = curve.interp1d(c1, npts, True)
    c2npts = (max(c2.x) - min(c2.x)) / step
    ic2 = curve.interp1d(c2, c2npts)

    # normalize c2 to unit area in its domain
    if norm:
        area = np.trapz(ic2.y, ic2.x)
        if area == 0:
            area = 0.0000009
        ic2.y = ic2.y / area

    y = np.array(scipy.signal.convolve(ic1.y, ic2.y, mode='full', method='direct'))
    delx = (max(c1.x) - min(c1.x)) / npts
    y *= delx

    xstart = min(min(c1.x), min(c2.x))
    xstop = xstart + (len(y) * delx)
    x = np.linspace(xstart, xstop, num=len(y))
    namestr = 'Conv ' + __toCurveString(c1) + '*' + __toCurveString(c2) + ' (Int) ' + str(npts)
    nc = makecurve(x, y, namestr)

    return nc


def fft(c, n=None, axis=-1, norm=None):
    """
    Compute the one-dimensional discrete Fourier Transform for the x- or y-values of c.

    This function computes the one-dimensional *n*-point discrete Fourier
    Transform (DFT) with the efficient Fast Fourier Transform (FFT)
    algorithm [CT].

    Raises IndexError: if `axes` is larger than the last axis of `a`.

    Notes: FFT (Fast Fourier Transform) refers to a way the discrete Fourier
    Transform (DFT) can be calculated efficiently, by using symmetries in the
    calculated terms.  The symmetry is highest when `n` is a power of 2, and
    the transform is therefore most efficient for these sizes.

    The DFT is defined, with the conventions used in this implementation, in
    the documentation for the `numpy.fft` module.

    Citation: Cooley, James W., and John W. Tukey, 1965, "An algorithm for the
            machine calculation of complex Fourier series," *Math. Comput.*
            19: 297-301.

    >>> curves = pydvif.read('testData.txt')

    >>> realcurve, imagcurve = pydvif.fft(curves[0])

    :param c: Curve with x- or y-values as input array, can be complex.
    :type c: Curve
    :param n: Length of the transformed axis of the output. If `n` is smaller than the length of the input, the input is cropped. If it is larger, the input is padded with zeros.  If `n` is not given, the length of the input along the axis specified by `axis` is used.
    :type n: int, optional
    :param axis: Axis over which to compute the FFT.  If not given, the last axis is used.
    :type axis: int, optional
    :param norm: Normalization mode (see `numpy.fft`). Default is None.
    :type norm: None, "ortho", optional
    :return: Curve tuple -- Two curves with the real and imaginary parts.
    """

    nc1 = curve.Curve('', 'Real part FFT ' + __toCurveString(c))
    nc2 = curve.Curve('', 'Imaginary part FFT ' + __toCurveString(c))

    numpy1_10 = LooseVersion(np.__version__) >= LooseVersion("1.10.0")
    cnorm = c.normalize()
    clen = len(c.x)

    if numpy1_10:
        complex_array = np.fft.fft(cnorm.y, n, axis, norm)
        complex_array = np.fft.fftshift(complex_array)
    else:
        complex_array = np.fft.fft(cnorm.y, n, axis)
        complex_array = np.fft.fftshift(complex_array)

    val = 1.0 / (float(max(cnorm.x) - min(cnorm.x)) / 2.0)
    nc1.x = np.fft.fftfreq(clen, d=val)
    nc1.x = np.fft.fftshift(nc1.x)
    nc1.y = complex_array.real

    nc2.x = np.array(nc1.x)
    nc2.y = complex_array.imag

    my(nc2, -1)

    return nc1, nc2


def derivative(c, eo=1):
    """
    Take the derivative of the curve.

    >>> curves = pydvif.read('testData.txt')

    >>> newCurve = pydvif.derivative(curves[0])

    :param c: The curve
    :type c: Curve
    :param eo: edge_order, gradient is calculated using N-th order accurate differences at the boundaries.
               Default: 1.
    :type eo: int, optional
    :return: A new curve representing the derivate of c
    """
    nc = curve.Curve('', 'Derivative ' + __toCurveString(c))

    nc.x = c.x
    nc.y = np.gradient(c.y, c.x, edge_order=eo)

    return nc


def diffMeasure(c1, c2, tol=1e-8):
    """
    Compare two curves. For the given curves a fractional difference measure and its average are computed.

    >>> curves = pydvif.read('testData.txt')

    >>> c1, c2  = pydvif.diffMeasure(curves[0], curves[1])

    >>> curves.append(c1)

    >>> curves.append(c2)

    >>> pydvif.create_plot(curves, legend=True)

    :param c1: The first curve
    :type c1: Curve
    :param c2: The second curve
    :type c2: Curve
    :param tol: The tolerance
    :type tol: float
    :return: tuple -- Two curves representing the fractional difference measure and its average
    """
    cdiff = curve.Curve('', 'FD = $|$' + __toCurveString(c1) + ' - ' + __toCurveString(c2) + '$|$/($|$' + __toCurveString(c1) + '$|$ + $|$' + __toCurveString(c2) + '$|$)')
    ic1, ic2 = curve.getinterp(c1, c2)
    f1 = tol * (np.max(ic1.y) - np.min(ic1.y))
    f2 = tol * (np.max(ic2.y) - np.min(ic2.y))
    ydiff = np.abs(ic1.y - ic2.y)
    yden = (np.abs(ic1.y)+f1) + (np.abs(ic2.y)+f2)
    dx = np.max(ic1.x) - np.min(ic1.x)
    cdiff.x = np.array(ic1.x)
    cdiff.y = np.array(ydiff/yden)

    cint = curve.Curve('', 'Integral(FD)/dX')
    yint = scipy.integrate.cumtrapz(cdiff.y, cdiff.x, initial=0.0)
    cint.x = np.array(ic1.x)
    cint.y = np.array(yint/dx)

    return cdiff, cint


########################################################
##################  Curve Related  #####################
########################################################

def vs(c1, c2):
    """
    Create a new curve that will plot as the range of the first curve against
    the range of the second curve.

    >>> curves = pydvif.read('testData.txt')

    >>> c1 = pydvif.vs(curves[0], curves[1])

    >>> curves.append(c1)

    >>> pydvif.create_plot(curves, legend=True)

    :param c1: The first curve
    :type c1: Curve
    :param c2: The second curve
    :type c2: Curve
    :return: Curve -- the new curve
    """
    newfilename = ''
    newrecord_id = ''
    if c1.filename == c2.filename:
        newfilename = c1.filename 
        if c1.record_id == c2.record_id:
            newrecord_id = c1.record_id
    nc = curve.Curve(newfilename, __toCurveString(c1) + ' vs ' + __toCurveString(c2), newrecord_id, c2.ylabel, c1.ylabel)
    ic1, ic2 = curve.getinterp(c1, c2)
    nc.x = np.array(ic2.y)
    nc.y = np.array(ic1.y)
    return nc


def subsample(curvelist, stride=2, verbose=False):
    """
    Subsample the curve or list of curves, i.e., reduce to every nth value.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.subsample(curves, 4)

    >>> pydvif.create_plot(curves, legend=True)

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    :param stride: The step size through the array
    :type stride: int
    :param verbose: If True additional information will be printed to stdout
    :type verbose: bool
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        n = len(c.x)
        xss = c.x[0:n:int(stride)]
        yss = c.y[0:n:int(stride)]
        c.x = xss
        c.y = yss

        if verbose:
            print("Reduced %s from %i -> %i values." % (c.name, n, len(c.x)))


def smooth(curvelist, factor=1):
    """
    Smooth the curve to the given degree.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.smooth(curves, 4)

    >>> pydvif.create_plot(curves, legend=True)

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    :param factor: The smooth factor
    :type factor: int
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        if len(c.x) < 2:
            return 0

        x = list()
        y = list()

        for i in range(len(c.x)):
            tfactor = factor

            if i-factor < 0 and i < (len(c.x)-1)/2:
                tfactor = i
            elif i+factor >= len(c.x):
                tfactor = len(c.x) - 1 - i

            xsum = 0
            ysum = 0

            for j in range(-tfactor, tfactor+1):
                xsum += c.x[i+j]
            for j in range(-factor, factor+1):
                if 0 <= i+j < len(c.x):
                    ysum += c.y[i+j]
                elif i+j < 0:
                    ysum += c.y[0]
                else:
                    ysum += c.y[-1]

            x.append(xsum/(2*tfactor+1))
            y.append(ysum/(2*factor+1))

        c.x = np.array(x)
        c.y = np.array(y)


def errorbar(scur, cury1, cury2, curx1=None, curx2=None, mod=1):
    """
    Plot error bars on the given curve.

    >>> curves = list()

    >>> curves.append(pydvif.span(1,10))

    >>> curves.append(pydvif.span(1,10))

    >>> curves.append(pydvif.span(1,10))

    >>> pydvif.dy(curves[0], 0.25)

    >>> pydvif.dy(curves[2], -0.25)

    >>> pydvif.errorbar(curves[1], curves[0], curves[2])

    >>> pydvif.create_plot(curves, legend=True)

    :param scur: The given curve
    :type scur: Curve
    :param cury1: y-error-curve
    :type cury1: Curve
    :param cury2: y+error-curve
    :type cury2: Curve
    :param curx1: x-error-curve
    :type curx1: Curve
    :param curx2: x+error-curve
    :type curx2: Curve
    :param mod: point-skip
    :type mod: int
    """
    ebar = [np.zeros(len(scur.x)), np.zeros(len(scur.x)), np.zeros(len(scur.x)), np.zeros(len(scur.x))]
    lowy = list()
    for i in range(len(scur.x)):
        y = np.interp(scur.x[i], cury1.x, cury1.y)
        if scur.y[i] - y <= 0:
            lowy.append(y)
        else:
            lowy.append(scur.y[i])

    ebar[0] = np.array(lowy)
    ebar[1] = np.interp(scur.x, cury2.x, cury2.y)

    if curx1 is not None and curx2 is not None:
        ebar[2] = np.interp(scur.x, curx1.x, curx1.y)
        ebar[3] = np.interp(scur.x, curx2.x, curx2.y)

    for i in range(len(ebar[0])):
        if (i % int(mod) != 0) and (i != len(ebar[0]) - 1):
            ebar[0][i] = None
            ebar[1][i] = None
            ebar[2][i] = None
            ebar[3][i] = None

    scur.ebar = ebar
    scur.erange = None


def errorrange(scur, cury1, cury2):
    """
    Plot shaded error region on given curve.

    >>> curves = list()

    >>> curves.append(pydvif.span(1,10))

    >>> curves.append(pydvif.span(1,10))

    >>> curves.append(pydvif.span(1,10))

    >>> pydvif.dy(curves[0], 0.25)

    >>> pydvif.dy(curves[2], -0.25)

    >>> pydvif.errorrange(curves[1], curves[0], curves[2])

    >>> pydvif.create_plot(curves, legend=True)

    :param scur: The given curve
    :type scur: Curve
    :param cury1: y-error-curve
    :type cury1: Curve
    :param cury2: y+error-curve
    :type cury2: Curve
    """

    errorbar(scur, cury1, cury2)
    scur.erange = [scur.ebar[0], scur.ebar[1]]
    scur.ebar = None


def fit(c, n=1, logx=False, logy=False):
    """
    Make a new curve that is a polynomial fit to curve c.

    >>> curves = list()

    >>> curves.append(pydvif.span(1,10))

    >>> pydvif.sin(curves)

    >>> curves.append(pydvif.fit(curves[0], 2))

    >>> pydvif.create_plot(curves, legend=True)

    :param c: The curve to fit
    :type c: Curve
    :param n: Degree of the fitting polynomial
    :type n: int
    :param logx: Take the log(x-values) before fitting if True
    :type logx: bool
    :param logy: Take the log(y-values) before fitting if True
    :type logy: bool
    :return: Curve -- The fitting polynomial
    """
    x = c.x
    y = c.y

    if logx:
        x = np.log10(x)

    if logy:
        y = np.log10(y)

    coeffs = scipy.polyfit(x, y, n)
    if len(coeffs) == 2:
        print("slope = ", coeffs[0], " intercept = ", coeffs[1])
    else:
        print("coefficients are: ", coeffs)

    if n==1:
        oString = "1st "
    elif n == 2:
        oString = "2nd "
    elif n == 3:
        oString = "3rd "
    else:
        oString = "%dth " % n

    nc = curve.Curve('', oString + 'order fit to ' + __toCurveString(c))
    nc.x = np.array(x)
    nc.y = scipy.polyval(coeffs, x)

    if logx:
        nc.x = 10.0**nc.x

    if logy:
        nc.y = 10.0**nc.y

    return nc


def getdomain(curvelist):
    """
    Get domain of the curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> domains = pydvif.getdomain(curves)

    >>> plotname, minx, maxx = domains[0]

    :param curvelist: The given curve or list of curves
    :type curvelist: Curve or list
    :return: list -- A list of tuples where each tuple contains the curve name, minimum x, and maximum x
    """
    domains = list()
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        domains.append((__toCurveString(c), min(c.x), max(c.x)))

    return domains


def disp(c, domain=True):
    """
    Create a string formatted list of the curve's x-values if domain is True, otherwise y-values.

    >>> c = pydvif.span(1, 10)

    >>> yvalues = pydvif.disp(c, False)

    :param c: The given curve
    :type curvelist: Curve
    :param domain: if True, display the x-values of the curve. Otherwise, display the y-values of the curve
    :type domain: bool, optional
    :return: list -- The list of x- or y-values as strings
    """
    ss = list()

    for i in range(len(c.x)):
        if domain:
            ss.append('x[%d]: %.4f' % (i, c.x[i]))
        else:
            ss.append('y[%d]: %.4f' % (i, c.y[i]))

    return ss


def getnumpoints(curve):
    """
    Return the given curve's number of points.

    :param curve: The given curve
    :return: int -- the number of points in curve
    """
    return len(curve.x)


def getrange(curvelist):
    """
    Get the range of the curve or list of curves.

    >>> curves = pydvif.read('testData.txt')

    >>> ranges = pydvif.getrange(curves)

    >>> plotname, miny, maxy = ranges[0]

    :param curvelist: The given curve or list of curves
    :type curvelist: Curve or list
    :return: list -- A list of tuples where each tuple contains the curve name, minimum y, and maximum y
    """
    ranges = list()
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        ranges.append((__toCurveString(c), min(c.y), max(c.y)))

    return ranges


def getx(c, value, xmin=None, xmax=None):
    """
    Get the x values of the curve for a given y.

    >>> curves = pydvif.read('testData.txt')

    >>> vals = pydvif.getx(curves[0], 4)

    >>> x, y = vals[0]

    :param c: The curve
    :type c: Curve
    :param value: y value
    :type value: float
    :return: list -- A list of tuples where each tuple contains the x value, and the given y
    """
    xypairs = list()
    r = __get_sub_range(c.x, xmin, xmax)

    if float(value) < np.amin(c.y) or float(value) > np.amax(c.y):
        raise ValueError('y-value out of range')

    for i in range(r[0], r[1] + 1):
        if c.y[i] == float(value):
            xypairs.append((c.x[i], float(value)))
        else:
            ymax = c.y[i]
            if i+1 < len(c.y):
                ymax = c.y[i+1]

            if c.y[i] < float(value) < ymax:
                x = np.interp(float(value), [c.y[i], ymax], [c.x[i], c.x[i+1]])
                if x <= r[1]:
                    xypairs.append((x, float(value)))
            elif ymax < float(value) < c.y[i]:
                x = np.interp(float(value), [ymax, c.y[i]], [c.x[i+1], c.x[i]])
                if x <= r[1]:
                    xypairs.append((x, float(value)))

    return xypairs


def gety(c, value):
    """
    Get the y values of the curve for a given x.

    >>> curves = pydvif.read('testData.txt')

    >>> vals = pydvif.gety(curves[0], 2)

    >>> x, y = vals[0]

    :param c: The curve
    :type c: Curve
    :param value: x value
    :type value: float
    :return: list -- A list of tuples where each tuple contains the y value, and the given x
    """
    xypairs = list()

    #if float(value) < np.amin(c.x) or float(value) > np.amax(c.x):
        #raise ValueError, 'x-value out of range'

    for i in range(len(c.x)):
        if float(value) < np.amin(c.x):
            xypairs.append((float(value), 0))   # c.y[0]))
        elif float(value) > np.amax(c.x):
            xypairs.append((float(value), 0))   # c.y[-1]))
        elif c.x[i] == float(value):
            xypairs.append((float(value), c.y[i]))
        else:
            xmax = c.x[i]
            if i+1 < len(c.x):
                xmax = c.x[i+1]

            if c.x[i] < float(value) < xmax:
                y = np.interp(float(value), [c.x[i], xmax], [c.y[i], c.y[i+1]])
                xypairs.append((float(value), y))
            elif xmax < float(value) < c.x[i]:
                y = np.interp(float(value), [xmax, c.x[i]], [c.y[i+1], c.y[i]])
                xypairs.append((float(value), y))

    return xypairs


def line(m, b, xmin, xmax, numpts=100):
    """
    Generate a line with y = mx + b and an optional number of points.

    >>> curves = list()

    >>> curves.append(pydvif.line(2, 5, 0, 10))

    >>> pydvif.create_plot(curves, legend=True, stylename='ggplot')

    :param m: The slope
    :type m: float
    :param b: The y-intercept
    :type b: float
    :param xmin: The minimum x value
    :type xmin: float
    :param xmax: The maximum x value
    :type xmax: float
    :param numpts: The number of points to use for the new line
    :type numpts: int
    :return: Curve -- The curve representing the newly created line
    """
    m = float(m)
    b = float(b)
    xmin = float(xmin)
    xmax = float(xmax)
    numpts = int(numpts)

    spacing = (xmax - xmin) / (numpts - 1)
    x = list()
    y = list()

    for i in range(numpts):
        x.append(xmin)
        y.append(xmin * m + b)
        xmin += spacing

    x = np.array(x)
    y = np.array(y)
    c = curve.Curve('', 'Straight Line')
    c.x = x
    c.y = y

    return c

def makeextensive(curvelist):
    """
    Set the y-values such that ``y[i] *= (x[i+1] - x[i])``

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.makeextensive(curves)

    >>> pydvif.create_plot(curves, legend=True)

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        for i in range(1, len(c.y)):
            c.y[i] *= (c.x[i] - c.x[i-1])

        c.y[0] = c.y[1]
        c.name = 'mkext(' + c.name + ')'

def makeintensive(curvelist):
    """
    Set the y-values such that y[i] /= (x[i+1] - x[i]).

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.makeintensive(curves)

    >>> pydvif.create_plot(curves, legend=True)

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        for i in range(1, len(c.y)):
            d = c.x[i] - c.x[i-1] if (c.x[i] - c.x[i-1]) != 0 else 0.000000001
            c.y[i] /= d

        c.y[0] = c.y[1]
        c.name = 'mkint(' + c.name + ')'

def dupx(curvelist):
    """
    Duplicate the x-values such that y = x for each of the given curves.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.dupx(curves)

    >>> pydvif.create_plot(curves, legend=True)

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        c.y = np.copy(c.x)

def sort(curve):
    """
    Sort the specified curve so that their points are plotted in order of ascending x values.

     >>> c = pydvif.span(1, 10)

     >>> pydvif.sort(c)

    :param curve: The curve to sort
    :type curve: Curve
    """
    index_array = np.argsort(curve.x)
    x = list()
    y = list()

    for index in index_array:
        x.append(curve.x[index])
        y.append(curve.y[index])

    curve.x = np.array(x)
    curve.y = np.array(y)

def rev(curve):
    """
    Swap x and y values for the specified curves. You may want to sort after this one.

     >>> c = pydvif.span(1, 10)

     >>> pydvif.rev(c)

    :param curve: The curve to sort
    :type curve: Curve
    """
    x = np.copy(curve.y)
    y = np.copy(curve.x)

    curve.x = x
    curve.y = y

def random(curve):
    """
    Generate random y values between -1 and 1 for the specified curves.

     >>> c = pydvif.span(1, 10)

     >>> pydvif.random(c)

    :param curve: The curve to sort
    :type curve: Curve
    """
    for i in range(len(curve.y)):
        curve.y[i] = sysrand.uniform(-1, 1)

def xindex(curvelist):
    """
    Create curves with y-values vs. integer index values.

    >>> curves = pydvif.read('testData.txt')

    >>> pydvif.xindex(curves)

    >>> pydvif.create_plot(curves, legend=True)

    :param curvelist: The curve or list of curves
    :type curvelist: Curve or list
    """
    curves = list()

    if isinstance(curvelist, list):
        curves.extend(curvelist)
    else:
        curves.append(curvelist)

    for c in curves:
        stop = len(c.y)
        c.x = np.linspace(1, stop, num=stop)


def appendcurves(curvelist):
    """
    Merge two or more curves over the union of their domains. Where domains overlap, take the
    average of the curve's y-values.

    >>> curves = pydvif.read('testData.txt')

    >>> newcurve = pydvif.appendcurve(curves)

    :param curvelist: the specified curves
    :type curvelist: list
    :return: Curve -- the merging of the two curves c1 and c2
    """
    if len(curvelist) < 2:
        if len(curvelist) == 1:
            return curvelist[0]
        else:
            return
    else:
        nc = curve.append(curvelist[0], curvelist[1])

        for i in range(2, len(curvelist)):
            nc = curve.append(nc, curvelist[i])

    suffix = ''
    for c in curvelist:
         suffix += "%s" % c.plotname

    nc.name = 'Append(' + suffix + ')'

    return nc


def max_curve(curvelist):
    """
    Construct a curve from the maximum y values of the intersection of the curves domain.

    :param curvelist: the specified curves
    :return: Curve -- a new curve with the maximum y-values over the intersection of the domains of the specified curves.
    """
    # Get union of domains
    if len(curvelist) <= 1:
        return None
    else:
        ux = set(curvelist[0].x).union(set(curvelist[1].x))
        for i in range(2, len(curvelist)):
            ux = set(curvelist[i].x).union(ux)

    ux = list(ux)
    ux.sort()

    # Create curve label suffix
    name_suffix = ''
    for i in range(len(curvelist)):
        name_suffix += "%s" % curvelist[i].plotname

    # Calculate max
    x = np.array(ux)
    y = np.zeros(len(x))

    for i in range(len(x)):
        y[i] = float(-sys.maxsize - 1)
        for j in range(len(curvelist)):
            try:
                vals = gety(curvelist[j], x[i])
                for val in vals:
                    if y[i] < val[1]:
                        y[i] = val[1]
            except:
                pass

    nc = curve.Curve('','Max(' + name_suffix + ')')
    nc.x = np.array(x)
    nc.y = y

    return nc


def min_curve(curvelist):
    """
    Construct a curve from the minimum y values of the intersection of the curves domain.

    :param curvelist: the specified curves
    :return: Curve -- a new curve with the minimum y-values over the intersection of the domains of the specified curves.
    """
    # Get union of domains
    if len(curvelist) <= 1:
        return None
    else:
        ux = set(curvelist[0].x).union(set(curvelist[1].x))
        for i in range(2, len(curvelist)):
            ux = set(curvelist[i].x).union(ux)

    ux = list(ux)
    ux.sort()

    # Create curve label suffix
    name_suffix = ''
    for i in range(len(curvelist)):
        name_suffix += "%s" % curvelist[i].plotname

    # Calculate min
    x = np.array(ux)
    y = np.zeros(len(x))

    for i in range(len(x)):
        y[i] = float(sys.maxsize)
        for j in range(len(curvelist)):
            try:
                vals = gety(curvelist[j], x[i])
                for val in vals:
                    if y[i] > val[1]:
                        y[i] = val[1]
            except:
                pass

    nc = curve.Curve('','Min(' + name_suffix + ')')
    nc.x = np.array(x)
    nc.y = y

    return nc

def average_curve(curvelist):
    """
    Average the specified curves over the intersection of their domains.

    :param curvelist: the specified curves
    :return: Curve -- a new curve with the average values over the intersection of the domains of the specified curves.
    """
    # Get union of domains
    if len(curvelist) <= 1:
        return None
    else:
        ux = set(curvelist[0].x).union(set(curvelist[1].x))
        for i in range(2, len(curvelist)):
            ux = set(curvelist[i].x).union(ux)

    ux = list(ux)
    ux.sort()

    # Create curve label suffix
    name_suffix = ''
    for i in range(len(curvelist)):
        name_suffix += "%s" % curvelist[i].plotname

    # Calculate average
    x = np.array(ux)
    y = np.zeros(len(x))

    for i in range(len(x)):
        cnt = 0
        for j in range(len(curvelist)):
            try:
                vals = gety(curvelist[j], x[i])
                for val in vals:
                    y[i] += val[1]
                    cnt += 1
            except:
                pass

        y[i] /= cnt

    nc = curve.Curve('','Average(' + name_suffix + ')')
    nc.x = np.array(x)
    nc.y = y

    return nc


########################################################
################## Private Methods #####################
########################################################

def __fft(c):
    """
    Compute the Fast Fourier Transform of a real curve.

    :param c: The curve
    :type c: Curve
    :return: tuple - two curves, one with the real part and the other with the imaginary part for their y-values.
    """
    nc1 = curve.Curve('', 'Real part FFT ' + __toCurveString(c))
    nc2 = curve.Curve('', 'Imaginary part FFT ' + __toCurveString(c))

    cnorm = c.normalize()
    clen = len(c.x)

    complex_array = np.fft.fft(cnorm.y)

    nc1.y = complex_array.real
    nc1.x = np.linspace(min(cnorm.x), max(cnorm.x), len(nc1.y))

    nc2.y = complex_array.imag
    nc2.x = np.linspace(min(cnorm.x), max(cnorm.x), clen)

    my(nc2, -1)

    return nc1, nc2


def __ifft(cr, ci):
    """
    Compute the 1D inverse discrete Fourier Transform.

    :param cr: Curve containing the real part of a complex number as it's y-values.
    :type c: Curve
    :param ci: Curve containing the imaginary part of a complex number as it's y-values
    :type c: Curve
    :return: tuple - two curves, one with the real part and the other with the imaginary part for their y-values.
    """
    nc1 = curve.Curve('', 'Real part iFFT ' + __toCurveString(cr))
    nc2 = curve.Curve('', 'Imaginary part iFFT ' + __toCurveString(ci))

    carray = np.zeros(len(cr.y), dtype=complex)

    for i in range(len(cr.y)):
       carray[i] = complex(cr.y[i], ci.y[i])

    numpy1_10 = LooseVersion(np.__version__) >= LooseVersion("1.10.0")

    if numpy1_10:
        complex_array = np.fft.ifft(carray)
    else:
        complex_array = np.fft.ifft(carray)

    # nc1.x = np.array(cr.x)
    nc1.y = complex_array.real
    nc1.x = np.linspace(min(cr.x), max(cr.x), len(nc1.y))

    # nc2.x = np.array(ci.x)
    nc2.y = complex_array.imag
    nc2.x = np.linspace(min(ci.x), max(ci.x), len(nc2.y))

    return nc1, nc2


def __complex_times(ra, ia, rb, ib):
    """
    Perform the complex product of the given pairs of curves representing the real and imaginary components.

    :param ra: Curve containing the real part
    :type ra: Curve
    :param ia: Curve containing the imaginary part
    :type ia: Curve
    :param rb: Curve containing the real part
    :type rb: Curve
    :param ib: Curve containing the imaginary part
    :type ib: Curve
    :return: tuple - pair of curves representing the complex conjugate
    """
    rs1 = ra * rb
    rs2 = ia * ib
    is1 = ra * ib
    is2 = ia * rb
    sa = rs1 - rs2
    sb = is1 + is2

    return sa, sb


def __get_sub_range(x, low, high):
    """
    Returns a tuple with the index of the first value in x greater than low and
    the index of the first value in x less than high.

    :param x: The array of x-values
    :type x: array
    :param low: The lower definite integral interval value
    :type low: float
    :param high: The upper definite integral interval value
    :type high: float
    :return: tuple -- a tuple with the indices of the first value in x that is
                      greater than low and the first value in x less than high.
                      If low or high is not specified, the corresponding return
                      will be None.
    """
    min_idx = np.where(x >= low)[0][0] if low is not None else 0
    max_idx = np.where(x <= high)[0][-1] if high is not None else len(x) - 1
    return min_idx, max_idx


def __toCurveString(c):
    """
    Returns the string description of the curve.

    :param c: The curve
    :type c: Curve
    :return: str -- The curve's name if not empty, otherwise, the curve's plotname
    """
    if c.name:
        return c.name

    return c.plotname


def __loadcolumns(fname, xcol):
    """
     Load a column oriented text data file, add parsed curves to the curvelist.
     '#' is the comment character.  The last comment line must be the column
     labels.  We assume the first column is the x-data, every other column is y-data.
     We also assume all columns are the same length.

    :param fname: The column oriented (.gnu) file
    :type fname: str
    :param xcol: x-column number for column oriented (.gnu) files
    :type xcol: int
    :returns: list -- the list of curves from the file
    """
    curvelist = []

    try:
        f = open(fname, 'r')
        lines = f.readlines()
        iLine = 0
        for l in lines:
            if l.strip()[0] != '#':
                break;
            iLine += 1
        if iLine == 0:
            print('WARNING: columns have no labels, labels will be assigned...someday')
        alllabels = lines[iLine - 1][1:] # drop leading '#' character
        if '"' in alllabels:
            colLabels = [x for x in alllabels.split('"')[1:-1] if len(x.replace(" ", "")) > 0]
        else:
            colLabels = alllabels.split()
        # check that we have a label for every column
        if len(colLabels) != len(lines[iLine].split()) and iLine > 0:
            raise RuntimeError('Sorry, right now PyDV requires you to have a label for every column.')
        # We assume some column is the x-data, every other column
        # is y-data
        numcurves = len(lines[iLine].split()) - 1

        # Make the curves, append them to self.curvelist.
        # First, get data into lists of numbers
        numDataLines = len(lines) - iLine
        localCurves = []
        for i in range(numcurves+1):
            localCurves.append([])
        # FIGURE OUT COOL WAY TO DO THIS LATER: localCurves = (numcurves+1)*[[]]
        for l in lines[iLine:]:
            nums = [float(n) for n in l.split()]
            assert len(nums) == numcurves + 1
            for colID in range(numcurves + 1):
                localCurves[colID].append(nums[colID])
        # convert lists to numpy arrays
        for colID in range(numcurves):
            localCurves[colID] = np.array(localCurves[colID])
        # Make Curve objects, add to curvelist
        for colID in range(numcurves + 1):
             if colID != xcol:
                c = curve.Curve(fname, colLabels[colID])
                c.x = localCurves[xcol]
                c.y = localCurves[colID]
                print("Appended curve: ", colLabels[colID], len(c.x), len(c.y))
                curvelist.append(c)
        # tidy up
        f.close()
    # anticipate failure!
    except IOError:
        traceback.print_exc(file=sys.stdout)
        print('could not load file: ' + fname)
    except ValueError:
        print('invalid pydv file: ' + fname)

    return curvelist

def __loadpdb(fname, fpdb):
    curvelist = []

    try:
        curveList = fpdb.ls('curve*')
        if (len(curveList) == 0):
            raise ValueError
        for cname in curveList:
            curveid = fpdb.read(cname).strip('\x00').split('|')
            if (len(curveid) != 8):
                raise IOError
            current = curve.Curve( fname, fpdb.read(curveid[1]).strip('\x00') )
            current.x = np.array( fpdb.read( curveid[3] ) )
            current.y = np.array( fpdb.read( curveid[4] ) )
            curvelist.append(current)

            fpdb.close()
    except IOError:
        print('could not load file: ' + fname)
    except ValueError:
        print('invalid pydv file: ' + fname)

    return curvelist
