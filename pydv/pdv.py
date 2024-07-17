# Copyright (c) 2011-2024, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by Mason Kwiat, Douglas S. Miller, and Kevin Griffin, Ephraim Rusu, Sarah El-Jurf, Jorge Moreno
# e-mail: eljurf1@llnl.gov, moreno45@llnl.gov
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

import cmd
import sys
import os
import re
import warnings
warnings.filterwarnings("ignore", category=Warning)

from threading import Thread

import numpy

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mclr

from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE2
if use_pyside:
    from PySide2.QtCore import (qInstallMessageHandler, QtDebugMsg, QtWarningMsg,
                                QtCriticalMsg, QtFatalMsg, QtSystemMsg, QtInfoMsg)
    # from PySide2.QtGui import *
    from PySide2.QtWidgets import QApplication
else:
    from PyQt5.QtCore import (qInstallMessageHandler, QtDebugMsg, QtWarningMsg,
                              QtCriticalMsg, QtFatalMsg, QtSystemMsg, QtInfoMsg)
    # from PyQt5.QtGui import *
    from PyQt5.QtWidgets import QApplication

import scipy
import traceback
import readline
import code
from numbers import Number
import types  # noqaf401 used for do_custom()
import csv
from itertools import zip_longest
import copy

# HPC Import
try:
    import pydvpy as pydvif
    import curve
    import pdvplot
    import pdvutil

# Package Import
except ImportError:
    from pydv import pydvpy as pydvif
    from pydv import curve
    from pydv import pdvplot
    from pydv import pdvutil

try:
    from matplotlib import style
    stylesLoaded = True
except:
    stylesLoaded = False

from enum import Enum

PYDV_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    version_file = os.path.join(PYDV_DIR, '../scripts/version.txt')
    with open(version_file, 'r') as fp:
        pydv_version = fp.read()

    date_file = os.path.join(PYDV_DIR, '../scripts/date.txt')
    with open(date_file, 'r') as fp:
        pydv_date = fp.read()
except:
    version_file = os.path.join(PYDV_DIR, 'scripts/version.txt')
    with open(version_file, 'r') as fp:
        pydv_version = fp.read()

    date_file = os.path.join(PYDV_DIR, 'scripts/date.txt')
    with open(date_file, 'r') as fp:
        pydv_date = fp.read()


class LogEnum(Enum):
    LOG = 1
    LOGX = 2
    LOG10 = 3
    LOG10X = 4


class Command(cmd.Cmd, object):

    prompt = '[PyDV]: '
    undoc_header = 'Command Shortcuts:'
    ruler = '='

    curvelist = list()
    filelist = []
    plotlist = []
    plotfirst = []
    oldlist = []
    usertexts = []

    history = []
    histptr = -1
    plotedit = False

    plotter = None  # pdvplot.Plotter()
    app = None

    ########################################################################################################
    # state variables #
    ########################################################################################################

    xlabel = ''
    ylabel = ''
    filename = ''
    record_id = ''
    title = ''
    xlabel_set_from_curve = True
    ylabel_set_from_curve = True
    filename_set_from_curve = True
    record_id_set_from_curve = True
    title_set_from_curve = True
    bordercolor = None
    figcolor = None
    plotcolor = None
    xtickcolor = None
    ytickcolor = None
    titlecolor = None
    xlabelcolor = None
    ylabelcolor = None
    xlabelweight = 'normal'
    ylabelweight = 'normal'
    xlabelstyle = 'normal'
    ylabelstyle = 'normal'
    xlim = None
    ylim = None
    showkey = True
    handlelength = None
    key_loc = 1
    key_ncol = 1
    showgrid = True
    showaxis = 'on'
    showplot = 'on'
    showminorticks = False
    gridcolor = 'white'
    gridstyle = 'solid'
    gridwidth = 1.0
    showletters = True
    showcurveinlegend = False
    showrecordidinlegend = False
    showfilenameinlegend = False
    xlogscale = False
    ylogscale = False
    titlefont = 'large'
    xlabelfont = 'medium'
    ylabelfont = 'medium'
    axistickfont = 'medium'
    keyfont = 'small'
    keycolor = 'black'
    curvelabelfont = 'medium'
    annotationfont = 'medium'
    initrun = None
    update = True
    guilims = False
    geometry = 'de'
    xticks = 'de'
    yticks = 'de'
    xCol = 0    # column to use for x-axis, if doing column format reads
    debug = False
    redraw = True
    xmajortickcolor = 'black'
    xminortickcolor = 'black'
    ymajortickcolor = 'black'
    yminortickcolor = 'black'
    xtickformat = 'de'
    ytickformat = 'de'
    xticklength = 4
    xminorticklength = 2
    yticklength = 4
    yminorticklength = 2
    xtickwidth = 1
    xminortickwidth = 0.5
    ytickwidth = 1
    yminortickwidth = 0.5
    menulength = 50
    namewidth = 40
    xlabelwidth = 10
    ylabelwidth = 10
    filenamewidth = 30
    recordidwidth = 10
    updatestyle = False
    linewidth = None
    xtick_labels = {}
    xtickrotation = 0
    ytickrotation = 0

    # Users wanted support for automatically loading some plot attributes. The
    # following commands handle the situations where there are multiple plots or
    # where the user specifies the attributes via the direct commands.
    def set_xlabel(self, label, from_curve=False):
        if 'bold' in label:
            if self.xlabelweight == 'bold':
                self.xlabelweight = 'normal'
            else:
                self.xlabelweight = 'bold'
            label = label.replace('bold', '')
        if 'italic' in label:
            if self.xlabelstyle == 'italic':
                self.xlabelstyle = 'normal'
            else:
                self.xlabelstyle = 'italic'
            label = label.replace('italic', '')
        if label.strip() == '':
            return

        if not from_curve:
            self.xlabel = label
            self.xlabel_set_from_curve = from_curve if label != "" else True
        else:
            if self.xlabel_set_from_curve:
                not_blank = 0
                for cur in self.plotlist:
                    if cur.xlabel != '':
                        not_blank += 1
                if len(self.plotlist) > 1 and self.xlabel == '' and not_blank == 1 and label != '':
                    self.xlabel = label
                elif len(self.plotlist) > 1 and label != self.xlabel:
                    self.xlabel = ''
                else:
                    self.xlabel = label
                    self.xlabel_set_from_curve = from_curve

    def set_ylabel(self, label, from_curve=False):
        if 'bold' in label:
            if self.ylabelweight == 'bold':
                self.ylabelweight = 'normal'
            else:
                self.ylabelweight = 'bold'
            label = label.replace('bold', '')
        if 'italic' in label:
            if self.ylabelstyle == 'italic':
                self.ylabelstyle = 'normal'
            else:
                self.ylabelstyle = 'italic'
            label = label.replace('italic', '')
        if label.strip() == '':
            return

        if not from_curve:
            self.ylabel = label
            self.ylabel_set_from_curve = from_curve if label != "" else True
        else:
            if self.ylabel_set_from_curve:
                not_blank = 0
                for cur in self.plotlist:
                    if cur.ylabel != '':
                        not_blank += 1
                if len(self.plotlist) > 1 and self.ylabel == '' and not_blank == 1 and label != '':
                    self.ylabel = label
                elif len(self.plotlist) > 1 and label != self.ylabel:
                    self.ylabel = ''
                else:
                    self.ylabel = label
                    self.ylabel_set_from_curve = from_curve

    def set_title(self, title, from_curve=False):
        if not from_curve:
            self.title = title
            self.title_set_from_curve = from_curve if title != "" else True
        else:
            if self.title_set_from_curve:
                if len(self.plotlist) > 1 and title != self.title:
                    self.title = ''
                else:
                    self.title = title
                    self.title_set_from_curve = from_curve

    def set_filename(self, filename, from_curve=False):
        if not from_curve:
            self.filename = filename
            self.filename_set_from_curve = from_curve if filename != "" else True
        else:
            if self.filename_set_from_curve:
                if len(self.plotlist) > 1 and filename != self.filename:
                    self.filename = ''
                else:
                    self.filename = filename
                    self.filename_set_from_curve = from_curve

    def set_record_id(self, record_id, from_curve=False):
        if not from_curve:
            self.record_id = record_id
            self.record_id_set_from_curve = from_curve if record_id != "" else True
        else:
            if self.record_id_set_from_curve:
                if len(self.plotlist) > 1 and record_id != self.title:
                    self.record_id = ''
                else:
                    self.record_id = record_id
                    self.record_id_set_from_curve = from_curve

    def precmd(self, line):
        """
        Check for special character/operator commands
        """

        pl = []
        for i in range(len(self.plotlist)):
            pl.append(self.plotlist[i].copy())
        self.oldlist = pl

        if not line or not line.split():
            return line

        line = line.split()

        check = line.pop(0)
        need_join_line = False
        if check == '+':
            line = 'add ' + ' '.join(line)
        elif check == '-':
            line = 'subtract ' + ' '.join(line)
        elif check == '/':
            line = 'divide ' + ' '.join(line)
        elif check == '*':
            line = 'multiply ' + ' '.join(line)
        else:
            line.insert(0, check)
            need_join_line = True

        if need_join_line and len(line) > 2:
            need_join_line = False
            check2 = line.pop(1)

            if check2 == '+':
                line = 'add ' + ' '.join(line)
            elif check2 == '-':
                line = 'subtract ' + ' '.join(line)
            elif check2 == '/':
                line = 'divide ' + ' '.join(line)
            elif check2 == '*':
                line = 'multiply ' + ' '.join(line)
            elif check2 == '**':
                line = 'powr ' + ' '.join(line)
            else:
                line.insert(1, check2)
                need_join_line = True

        if need_join_line:
            line = ' '.join(line)

        line = line.replace('re-id', 'reid')
        line = line.replace('data-id', 'dataid')
        line = line.replace('x-log-scale', 'xlogscale')
        line = line.replace('y-log-scale', 'ylogscale')
        line = line.replace('make-curve', 'makecurve')
        line = line.replace('error-bar', 'errorbar')
        line = line.replace('error-range', 'errorrange')
        line = line.replace('get-range', 'getrange')
        line = line.replace('get-domain', 'getdomain')
        line = line.replace('diff-measure', 'diffMeasure')

        line = line.replace('integrate(', 'commander.integrate(').replace('int(', 'commander.integrate(')
        line = line.replace('derivative(', 'commander.derivative(').replace('der(', 'commander.derivative(')
        # print line

        if self.showkey:
            if plt.gca().get_legend() is not None:
                self.key_loc = plt.gca().get_legend()._loc

        if self.plotter is not None:
            if self.plotter.plotChanged:
                self.apply_uichanges()

        return line

    def default(self, line):
        """
        Check for arithmetic calculation
        """

        try:
            pdvutil.parsemath(line, self.plotlist, self, (plt.axis()[0], plt.axis()[1]))
            self.plotedit = True
        except:
            self.redraw = False
            print('error - unknown syntax: ' + line)
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def postcmd(self, stop, line):
        """
        Save current state for undo/redo
        """

        if self.plotedit:
            # self.history.pop(-1)
            # pl = []
            # for i in range(len(self.plotlist)):
            #    pl.append(self.plotlist[i].copy())

            # print self.history
            # print pl

            if len(self.history) > self.histptr + 1:
                self.history = self.history[:self.histptr + 1]

            self.histptr += 1
            self.history.append(self.oldlist)  # (self.histptr, self.oldlist)

            if len(self.history) > 15:
                self.history.pop(0)
                self.histptr -= 1

            # print self.history
            # print self.histptr

            self.plotedit = False
        if self.update:
            if self.redraw:
                self.updateplot
        self.redraw = True
        return stop

    def emptyline(self):
        """
        Override cmd empty line function to not repeat last command
        """
        self.redraw = False

    ########################################################################################################
    # normal shortcut commands #
    ########################################################################################################

    def do_q(self, line):
        self.do_quit(line)

    def do_ran(self, line):
        self.do_range(line)

    def do_dom(self, line):
        self.do_domain(line)

    def do_rd(self, line):
        self.do_read(line)

    def do_rdcsv(self, line):
        self.do_readcsv(line)

    def do_rdsina(self, line):
        self.do_readsina(line)

    def do_cur(self, line):
        self.do_curve(line)

    def do_era(self, line):
        self.do_erase(line)

    def do_del(self, line):
        self.do_delete(line)

    def do_lst(self, line):
        self.do_list(line)

    def do_lstr(self, line):
        self.do_listr(line)

    def do_sub(self, line):
        self.do_subtract(line)

    def do_div(self, line):
        self.do_divide(line)

    def do_mult(self, line):
        self.do_multiply(line)

    def do_xls(self, line):
        self.do_xlogscale(line)

    def do_yls(self, line):
        self.do_ylogscale(line)

    def do_der(self, line):
        self.do_derivative(line)

    def do_pow(self, line):
        self.do_powr(line)

    def do_power(self, line):
        self.do_powr(line)

    def do_powx(self, line):
        self.do_powrx(line)

    def do_powerx(self, line):
        self.do_powrx(line)

    def do_square(self, line):
        self.do_sqr(line)

    def do_squarex(self, line):
        self.do_sqrx(line)

    def do_convol(self, line):
        self.do_convolve(line)

    def do_convolb(self, line):
        self.do_convolveb(line)

    def do_convolc(self, line):
        self.do_convolvec(line)

    def do_int(self, line):
        self.do_integrate(line)

    def do_geom(self, line):
        self.do_geometry(line)

    def do_xmm(self, line):
        self.do_xminmax(line)

    def do_ymm(self, line):
        self.do_yminmax(line)

    def do_key(self, line):
        self.do_legend(line)

    def do_leg(self, line):
        self.do_legend(line)

    def do_ln(self, line):
        self.do_log(line)

    def do_lnx(self, line):
        self.do_logx(line)

    def do_nc(self, line):
        self.do_newcurve(line)

    def do_mkext(self, line):
        self.do_makeextensive(line)

    def do_mkint(self, line):
        self.do_makeintensive(line)

    def do_system(self, line):
        self.do_shell(line)

    def do_pl(self, line):
        self.do_plotlayout(line)

    def do_help(self, arg):
        """
        Override help function to check for shortcuts
        """

        if (arg == '+'):
            arg = 'add'
        elif (arg == '-' or arg == 'sub'):
            arg = 'subtract'
        elif (arg == '*' or arg == 'mult'):
            arg = 'multiply'
        elif (arg == '/' or arg == 'div'):
            arg = 'divide'
        elif (arg == 'rd'):
            arg = 'read'
        elif (arg == 'rdcsv'):
            arg = 'readcsv'
        elif (arg == 'rdsina'):
            arg = 'readsina'
        elif (arg == 'convol'):
            arg = 'convolve'
        elif (arg == 'convolb'):
            arg = 'convolveb'
        elif (arg == 'convolc'):
            arg = 'convolvec'
        elif (arg == 'cur'):
            arg = 'curve'
        elif (arg == 'era'):
            arg = 'erase'
        elif (arg == 'del'):
            arg = 'delete'
        elif (arg == 'ran'):
            arg = 'range'
        elif (arg == 'dom'):
            arg = 'domain'
        elif (arg == 'lst'):
            arg = 'list'
        elif (arg == 'lstr'):
            arg = 'listr'
        elif (arg == 'q'):
            arg = 'quit'
        elif (arg == 'data-id'):
            arg = 'dataid'
        elif (arg == 're-id'):
            arg = 'reid'
        elif (arg == 'x-log-scale' or arg == 'xls'):
            arg = 'xlogscale'
        elif (arg == 'y-log-scale' or arg == 'yls'):
            arg = 'ylogscale'
        elif (arg == 'der'):
            arg = 'derivative'
        elif (arg == 'pow' or arg == 'power'):
            arg = 'powr'
        elif (arg == 'powx' or arg == 'powerx'):
            arg = 'powrx'
        elif (arg == 'make-curve'):
            arg = 'makecurve'
        elif (arg == 'error-bar'):
            arg = 'errorbar'
        elif (arg == 'int'):
            arg = 'integrate'
        elif (arg == 'geom'):
            arg = 'geometry'
        elif (arg == 'key'):
            arg = 'legend'
        elif (arg == 'leg'):
            arg = 'legend'
        elif (arg == 'error-range'):
            arg = 'errorrange'
        elif (arg == 'get-domain'):
            arg = 'getdomain'
        elif (arg == 'get-range'):
            arg = 'getrange'
        elif (arg == 'xmm'):
            arg = 'xminmax'
        elif (arg == 'ymm'):
            arg = 'yminmax'
        elif (arg == 'ln'):
            arg = 'log'
        elif (arg == 'lnx'):
            arg = 'logx'
        elif (arg == 'nc'):
            arg = 'newcurve'
        elif (arg == 'mkext'):
            arg = 'makeextensive'
        elif (arg == 'mkint'):
            arg = 'makeintensive'
        elif (arg == 'system'):
            arg = 'shell'
        elif (arg == 'pl'):
            arg = 'plotlayout'

        self.redraw = False  # never need to redraw after a 'help'
        return super(Command, self).do_help(arg)

    def do_shell(self, line):
        """
        Execute shell commands
        """

        os.system(line)

    def help_shell(self):
        print("\n   Procedure: Execute shell commands. The symbol \'!\' is a synonym for \'shell\'."
              "\n   Usage: <shell | system> <command>\n")

    ########################################################################################################
    # command functions #
    ########################################################################################################

    def do_newcurve(self, line):
        """
        Evaluate a line of mathematical operations
        """

        try:
            # check for obvious input errors
            if not line:
                return 0
            if len(line.split(':')) > 1:
                print('error - NOT HANDLING RANGES YET, not even sure what that would mean yet')
                return 0
            else:  # ok, got through input error checking, let's get to work
                newline = line  # copy the original line, we need the original for labeling

                # replace all the *.x and *.y entries in the line with
                # their actual data arrays in the plotlist.
                import re  # we are going to need regex!
                arrayMarkers = ['.x', '.y']
                for arrayMarker in arrayMarkers:
                    arrayInsts = re.findall(r"\w\%s" % arrayMarker, line)  # finds [a-z].x then [a-z].y
                    for aInst in arrayInsts:
                        plotname = aInst[0]  # BLAGO!! hard wired for single-letter labels
                        cID = pdvutil.getCurveIndex(plotname, self.plotlist)
                        newline = re.sub(r"%s\%s" % (plotname, arrayMarker),
                                         "self.plotlist[%d]%s" % (cID, arrayMarker), newline)

                # now newline holds a string that can be evaluated by Python
                newYArray = eval(newline)  # line returns a new numpy.array

                # make newYArray into a legitimate curve
                c = curve.Curve(filename='', name=line)  # we name the curve with the input 'line'
                c.plotname = self.getcurvename()  # get the next available data ID label
                c.y = newYArray
                # get the x-values from one of the curves used in the expression
                c.x = self.plotlist[cID].x
                self.addtoplot(c)

            self.plotedit = True
        except:
            print('error - usage: newcurve <expression>')
            print('try "help newcurve" for much more info')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_newcurve(self):
        print('\n   newcurve creats a new curve from an expression\n   Usage: newcurve <numpy expression>\n')
        print('For convenience, both math and numpy modules have been imported into the namespace.')
        print('Just FYI, this feature is way outside the ULTRA syntax PDV is mostly based on.')
        print('EXAMPLE:')
        print()
        print('[PDV]: newcurve sin(a.x*2*pi)/(h.y**2)')
        print()
        print('This creates a new curve according to the complicated expression.')
        print('You can abbreviate newcurve as nc.')
        print()
        print('WARNINGS:')
        print('* Currently, newcurve is hard-wired to only handle single-letter labels.')
        print('  Curve names used in the expression cannot be the @N type we use after')
        print('  we run out of letters. Sorry (April 2015).')
        print('* A common error is to forget the .x or .y on the curve label name.')
        print('* All the arrays in your expression have to span the same domain! Currently (4/2015), newcurve')
        print('  will generate a curve from different domains (with no error message), and that curve')
        print('  will almost certainly not be what you intended.')
        print()

    def do_eval(self, line):
        """
        Evaluate a line of mathematical operations
        """

        try:
            line = line.replace('integrate', 'commander.integrate').replace('int', 'commander.integrate')
            line = line.replace('derivative', 'commander.derivative').replace('der', 'commander.derivative')

            pdvutil.parsemath(line, self.plotlist, self, (plt.axis()[0], plt.axis()[1]))
            self.plotedit = True
        except:
            print('error - usage: eval <curve-operations>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_eval(self):
        print('\n   Procedure: Evaluate mathematical operations on curves\n   Usage: eval <curve-operations>\n')

    def do_debug(self, line):
        """
        Turn on debug tracebacks for commands
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.debug = False
            elif line == '1' or line.upper() == 'ON':
                self.debug = True
            else:
                print('invalid input: requires on or off as argument')
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_debug(self):
        print('\n   Variable: Show debug tracebacks if True\n   Usage: debug on | off\n')

    def do_undo(self, line):
        """
        Undo last operation on a curve
        """

        try:
            if self.histptr > 0:
                if self.histptr == len(self.history) - 1:
                    pl = []
                    for i in range(len(self.plotlist)):
                        pl.append(self.plotlist[i].copy())
                    self.history.append(pl)
                self.plotlist = self.history[self.histptr]
                # self.history = self.history[:self.histptr]
                self.histptr -= 1

                # print self.history
                # print self.histptr
            else:
                print('error - cannot undo further')
        except:
            print('error - usage: undo')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_undo(self):
        print('\n   Procedure: Undo the last operation on plotted curves'
              '\n   Usage: undo\n')

    def do_redo(self, line):
        """
        Redo last curve operation undo
        """

        try:
            if self.histptr < len(self.history) - 2:
                self.histptr += 1
                self.plotlist = self.history[self.histptr + 1]

                # print self.history
                # print self.histptr
            else:
                print('error - cannot redo further')
        except:
            print('error - usage: redo')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_redo(self):
        print('\n   Procedure: Redo the last undone curve operation'
              '\n   Usage: redo\n')

    def do_add(self, line):
        """
        Add one or more curves and plot resulting curve
        """

        try:
            # If adding a number then send to dy
            if any(char.isdigit() for char in line) and not any(char == '@' for char in line):
                # value = float(line.split().pop(-1))
                self.do_dy(line)
            else:
                if len(line.split(':')) > 1:
                    self.do_add(pdvutil.getletterargs(line))
                    return 0
                else:
                    line = line.split()
                    line = ' + '.join(line)
                    pdvutil.parsemath(line, self.plotlist, self, (plt.axis()[0], plt.axis()[1]))
                self.plotedit = True

        except:
            print('error - usage: add <curve-list> [value]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_add(self):
        print('\n   Procedure: Take sum of curves. If the optional value is specified it will add'
              '\n              the y-values of the curves by value (equivalent to using the dy command).'
              '\n              Note: Adding curves by a number modifies the curve. If you want to create'
              '\n              a new curve then copy the original curve first using the copy command.'
              '\n   Usage: add <curve-list> [value]'
              '\n   Shortcuts: +\n')

    def do_subtract(self, line):
        """
        Subtract one or more curves
        """

        try:
            try:
                nline = line.split()
                value = -1.0 * float(nline.pop(-1))
                nline = ' '.join(nline)
                nline = nline + ' ' + str(value)
                self.do_dy(nline)
            except:
                if len(line.split(':')) > 1:
                    self.do_subtract(pdvutil.getletterargs(line))
                    return 0
                else:
                    line = line.split()
                    if len(line) == 1:
                        line = '-' + line[0]
                    else:
                        line = ' - '.join(line)
                    pdvutil.parsemath(line, self.plotlist, self, (plt.axis()[0], plt.axis()[1]))
                self.plotedit = True
        except:
            print('error - usage: subtract <curve-list> [value]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_subtract(self):
        print('\n   Procedure: Take difference of curves. A single curve can be specified, resulting in '
              '\n              the negating of its y-values. If the optional value is specified it will subtract'
              '\n              the y-values of the curves by value (similar to using the dy command).'
              '\n              Note: Subtracting curves by a number modifies the curve. If you want to create'
              '\n              a new curve then copy the original curve first using the copy command.'
              '\n   Usage: subtract <curve-list> [value]'
              '\n   Shortcuts: - , sub\n')

    def do_multiply(self, line):
        """
        Multiply one or more curves
        """

        try:
            # If multiplying by a number then send to my
            if any(char.isdigit() for char in line) and not any(char == '@' for char in line):
                # value = float(line.split().pop(-1))
                self.do_my(line)
            else:
                if len(line.split(':')) > 1:
                    self.do_multiply(pdvutil.getletterargs(line))
                    return 0
                else:
                    line = line.split()
                    line = ' * '.join(line)
                    pdvutil.parsemath(line, self.plotlist, self, (plt.axis()[0], plt.axis()[1]))
                self.plotedit = True
        except:
            print('error - usage: mult <curve-list> [value]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_multiply(self):
        print('\n   Procedure: Take product of curves. If the optional value is specified it will multiply'
              '\n              the y-values of the curves by value (equivalent to using the my command).'
              '\n              Note: Multiplying curves by a number modifies the curve. If you want to create'
              '\n              a new curve then copy the original curve first using the copy command.'
              '\n   Usage: multiply <curve-list> [value]'
              '\n   Shortcuts: * , mult\n')

    def do_divide(self, line):
        """
        Divide one or more curves
        """
        try:
            # If dividing by a number then send to divy
            if any(char.isdigit() for char in line) and not any(char == '@' for char in line):
                # value = float(line.split().pop(-1))
                self.do_divy(line)
            else:
                if len(line.split(':')) > 1:
                    self.do_divide(pdvutil.getletterargs(line))
                    return 0
                else:
                    line = line.split()
                    line = ' / '.join(line)
                    pdvutil.parsemath(line, self.plotlist, self, (plt.axis()[0], plt.axis()[1]))
                self.plotedit = True
        except:
            print('error - usage: divide <curve-list> [value]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_divide(self):
        print('\n   Procedure: Take quotient of curves. If the optional value is specified it will divide'
              '\n              the y-values of the curves by value (equivalent to using the divy command).'
              '\n              Note: Dividing curves by a number modifies the curve. If you want to create'
              '\n              a new curve then copy the original curve first using the copy command.'
              '\n   Usage: divide <curve-list> [value]'
              '\n   Shortcuts: / , div\n')

    def do_read(self, line):
        """
        Read in an ultra file
        """

        try:
            line = line.split()
            n = len(line)

            if n == 1:
                self.load(line[0])
            elif n == 2:
                if line[0].isdigit():
                    self.xCol = int(line[0])
                    self.load(line[1], True)
                else:
                    raise RuntimeError('expecting an x-column number.')
            elif n == 3:
                line[0] = line[0].strip().strip('()')
                matches = int(line[1])
                if matches < 0:
                    matches = None
                self.load(line[2], False, line[0], matches)
            elif n == 4:
                line[0] = line[0].strip().strip('()')
                matches = int(line[1])
                if matches < 0:
                    matches = None
                self.xCol = int(line[2])
                self.load(line[3], True, line[0], matches)
            else:
                print('error - Usage: read [(regex) matches] [x-col] <file-name>')
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False
            self.plotter.updateDialogs()

    def help_read(self):
        print('\n    Macro: Read curve data file'
              '\n    Usage: read [(regex) matches] [x-col] <file-name>'
              '\n    Shortcuts: rd\n'
              '\n    If using regex, set matches equal to a negative number for unlimited matches.'
              '\n    For column oriented (.gnu) files optionally specify the x-column number before the file name.\n')

    def do_readcsv(self, line):
        """
        Read in a csv file
        """

        try:
            line = line.split()

            if len(line) == 2:
                col = line.pop(-1)
            else:
                col = 0

            self.load_csv(line[0], col)
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False
            self.plotter.updateDialogs()

    def help_readcsv(self):
        print('\n   Macro: Read csv data file. For column oriented (.gnu) files optionally specify the x-column'
              '\n          number (e.g., readcsv file.csv 1).'
              '\n   Usage: readcsv <file-name> [xcol]'
              '\n   Shortcuts: rdcsv\n')

    def do_readsina(self, line):
        """
        Read in a Sina file
        """

        try:
            line = line.split()
            self.load_sina(line[0])
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False
            self.plotter.updateDialogs()

    def help_readsina(self):
        print('\n   Macro: Read all curves from sina data file.'
              '\n   Usage: readsina <file-name>'
              '\n   Shortcuts: rdsina\n')

    def do_setxcolumn(self, line):
        """
        Set x-column for cxv or gnu files explicitly
        """

        try:
            line = line.split()

            if len(line) == 1:
                self.xCol = int(line[0])
            else:
                raise RuntimeError("Expecting 1 argument but received {}".format(len(line)))
        except:
            print("error - usage: setxcolumn <n>")
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_setxcolumn(self):
        print("\n    Variable: set x column for reading column formatted data files (.gnu or .csv)."
              "\n    Usage: setxcolumn <n>, where n is an integer.")

    def __menu_curve_math(self, operation, line):
        if len(line.split(':')) > 1:  # check for list notation
            return self.__menu_curve_math(operation, pdvutil.getnumberargs(line, self.filelist))
        else:
            line = line.split()
            curvelist = list()
            for i in range(len(line)):
                curvedex = 0
                if ord('A') <= ord(line[i][0].upper()) <= ord('Z'):  # check for a.% b.% file index notation
                    filedex = ord(line[i][0].upper()) - ord('A')  # file index we want
                    prevfile = ''  # set prevfile to impossible value
                    filecounter = 0
                    while filecounter <= filedex:  # count files up to the one we want
                        if self.curvelist[curvedex].filename != prevfile:  # inc count if name changes
                            prevfile = self.curvelist[curvedex].filename
                            filecounter += 1
                        curvedex += 1  # this will end up being one past what we want
                        if curvedex >= len(self.curvelist):
                            raise RuntimeError("error: in curve list did not find matching file for %s" % line[i])
                    curvedex -= 1  # back curvedex up to point to start of file's curves
                    curvedex += int(line[i].split('.')[-1]) - 1
                elif 0 < int(line[i]) <= len(self.curvelist):
                    curvedex = int(line[i]) - 1
                else:
                    raise RuntimeError("error: curve index out of bounds: " + line[i])

                curvelist.append(self.curvelist[curvedex].copy())

        if len(curvelist) > 1:
            if operation == "add":
                return pydvif.add(curvelist)
            elif operation == "subtract":
                return pydvif.subtract(curvelist)
            elif operation == "multiply":
                return pydvif.multiply(curvelist)
            elif operation == "divide":
                return pydvif.divide(curvelist)
            else:
                raise ValueError("error: Unknown operation: {}".format(operation))
        else:
            raise RuntimeError("error: Expecting more than 1 curve")

    def do_add_h(self, line):
        """
        Add menu curves
        """

        if not line:
            return 0

        try:
            c = self.__menu_curve_math("add", line)

            if len(c.name) > 20:
                c.name = c.name[:20] + '...'
            c.plotname = ''
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: add_h <list-of-menu-numbers>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_add_h(self):
        print('\n   Procedure: Adds curves that have been read from a file but not yet plotted. list-of-menu-numbers '
              '\n              are the index values displayed in the first column of the menu command.'
              '\n   Usage: add_h <list-of-menu-numbers>')

    def do_subtract_h(self, line):
        """
        Subtract menu curves
        """

        if not line:
            return 0

        try:
            c = self.__menu_curve_math("subtract", line)

            if len(c.name) > 20:
                c.name = c.name[:20] + '...'
            c.plotname = ''
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: subtract_h <list-of-menu-numbers>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_subtract_h(self):
        print('\n   Procedure: Subtracts curves that have been read from a file but not yet plotted.  '
              '\n              list-of-menu-numbers are the index values displayed in the first column of the menu '
              '\n              command.'
              '\n   Usage: subtract_h <list-of-menu-numbers>')

    def do_multiply_h(self, line):
        """
        Multiply menu curves
        """

        if not line:
            return 0

        try:
            c = self.__menu_curve_math("multiply", line)

            if len(c.name) > 20:
                c.name = c.name[:20] + '...'
            c.plotname = ''
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: multiply_h <list-of-menu-numbers>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_multiply_h(self):
        print('\n   Procedure: Multiplies curves that have been read from a file but not yet plotted.  '
              '\n              list-of-menu-numbers are the index values displayed in the first column of the menu '
              '\n              command.'
              '\n   Usage: multiply_h <list-of-menu-numbers>')

    def do_divide_h(self, line):
        """
        Divide menu curves
        """

        if not line:
            return 0

        try:
            c = self.__menu_curve_math("divide", line)

            if len(c.name) > 20:
                c.name = c.name[:20] + '...'
            c.plotname = ''
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: divide_h <list-of-menu-numbers>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_divide_h(self):
        print('\n   Procedure: Divides curves that have been read from a file but not yet plotted.  '
              '\n              list-of-menu-numbers are the index values displayed in the first column of the menu '
              '\n              command.'
              '\n   Usage: divide_h <list-of-menu-numbers>')

    def do_curve(self, line):
        """
        Graph the given curves
        """

        if not line:
            return 0
        try:
            if len(line.split(')')) > 1:  # check for regular expression
                line = line.strip().split(')')
                reg = re.compile(r"")
                for i in range(len(line)):
                    line[i] = line[i].strip().strip('(')
                if line[0].split()[0] == 'menu':
                    line[0] = ' '.join(line[0].split()[1:])
                try:
                    reg = re.compile(r"%s" % line[0])
                except:
                    print('error: invalid expression')
                    return 0
                self.do_menu(line[0])
                regline = ''
                for i in range(len(self.curvelist)):
                    searchline = self.curvelist[i].name + ' ' + self.curvelist[i].filename
                    if reg.search(searchline):
                        regline += str(i + 1) + ' '
                line[0] = regline
                line = ' '.join(line)
                self.do_curve(line)  # call curve again but with regexp results
                self.redraw = True
                return 0
            if len(line.split(':')) > 1:  # check for list notation
                # call curve again with list expanded
                self.do_curve(pdvutil.getnumberargs(line, self.filelist))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    curvedex = 0
                    skip = False
                    if ord('A') <= ord(line[i][0].upper()) <= ord('Z'):  # check for a.% b.% file index notation
                        filedex = ord(line[i][0].upper()) - ord('A')  # file index we want
                        prevfile = ''  # set prevfile to impossible value
                        filecounter = 0
                        while filecounter <= filedex:  # count files up to the one we want
                            if self.curvelist[curvedex].filename != prevfile:  # inc count if name changes
                                prevfile = self.curvelist[curvedex].filename
                                filecounter += 1
                            curvedex += 1  # this will end up being one past what we want
                            if curvedex >= len(self.curvelist):
                                print("error: in curve list did not find matching file for %s" % line[i])
                        curvedex -= 1  # back curvedex up to point to start of file's curves
                        curvedex += int(line[i].split('.')[-1]) - 1
                    elif 0 < int(line[i]) <= len(self.curvelist):
                        curvedex = int(line[i]) - 1
                    else:
                        print('error: curve index out of bounds: ' + line[i])
                        skip = True
                    if not skip:
                        # Deep copy
                        current = copy.deepcopy(self.curvelist[curvedex])
                        try:
                            current.step = self.curvelist[curvedex].step
                        except:
                            current.step = False
                        try:
                            current.xticks_labels = self.curvelist[curvedex].xticks_labels
                        except:
                            current.xticks_labels = None
                        self.addtoplot(current)
                        if (len(current.x) == 1 and len(current.y) == 1):
                            current.markerstyle = 'o'
                            current.linestyle = 'None'
                self.plotedit = True
        except:
            print('error - usage: curve <(<regex>) | list-of-menu-numbers>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_curve(self):
        print('\n   Procedure: Select curves from the menu for plotting'
              '\n   Usage: curve <(<regex>) | list-of-menu-numbers>\n   Shortcuts: cur\n')

    def do_erase(self, line):
        """
        Remove all curves from the graph
        """

        self.plotlist = []
        self.usertexts = []

        self.plotedit = True

    def help_erase(self):
        print('\n   Macro: Erases all curves on the screen but leaves the limits untouched\n   Usage: erase'
              '\n   Shortcuts: era\n')

    def do_delete(self, line):
        """
        Remove a curve from the graph
        """

        try:
            if not line:
                return 0
            if len(line.split(':')) > 1:
                self.do_delete(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        self.plotlist.pop(idx)
                    except pdvutil.CurveIndexError:
                        pass

                self.reset_xticks_labels()

                self.plotedit = True

        except:
            print('error - usage: del <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_delete(self):
        print('\n   Procedure: Delete curves from list\n   Usage: delete <curve-list>\n   Shortcuts: del\n')

    def do_color(self, line):
        """
        Set a specific color for a list of curves
        """

        if not line:
            return 0
        try:
            line = line.split()
            color = line.pop(-1)
            line = ' '.join(line)
            if len(line.split(':')) > 1:
                self.do_color(pdvutil.getletterargs(line) + color)
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    for j in range(len(self.plotlist)):
                        name = self.plotlist[j].plotname
                        if name == line[i].upper():
                            if mclr.is_color_like(color):
                                self.plotlist[j].color = color
                                self.plotlist[j].markeredgecolor = color
                                self.plotlist[j].markerfacecolor = color
                            else:
                                print('error: invalid color ' + color)
                                return 0
                            break
            self.plotedit = True
        except:
            print('error - usage: color <curve-list> <color-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_color(self):
        print('\n   Procedure: Set the color of curves\n   Usage: color <curve-list> <color-name>\n   '
              'Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set\n   of hexadecimal red-green-blue '
              'values (RRGGBB).\n   The entire set of HTML-standard color names is available.\n   Try "showcolormap" '
              'to see the available named colors!')

    def do_stats(self, line):
        """
        Return a curves mean and standard deviation
        """

        def find_mode(array):

            mode = scipy.stats.mode(array, keepdims=True)
            if mode.count[0] == 1 and len(array) != 1:
                return numpy.nan, numpy.nan
            else:
                return mode.mode[0], mode.count[0]

        if not line:
            return 0

        if len(line.split(':')) > 1:
            self.do_stats(pdvutil.getletterargs(line))
            return 0
        else:
            try:
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        numx, countx = find_mode(cur.x)
                        numy, county = find_mode(cur.y)

                        print('\nCurve ' + cur.plotname)
                        print('\n\t         X:\t              Y:')
                        print(f'\n\tlength:    {len(cur.x):<15.10g}\t{len(cur.y):<15.10g}')
                        print(f'\tmean:      {numpy.mean(cur.x):<15.10g}\t{numpy.mean(cur.y):<15.10g}')
                        print(f'\tmedian:    {numpy.median(cur.x):<15.10g}\t{numpy.median(cur.y):<15.10g}')
                        print(f'\tmode:      {numx:<15.10g}\t{numy:<15.10g}')
                        print(f'\t    count: {countx:<15.10g}\t{county:<15.10g}')
                        print(f'\tstd:       {numpy.std(cur.x):<15.10g}\t{numpy.std(cur.y):<15.10g}')
                        print(f'\tskew:      {scipy.stats.skew(cur.x):<15.10g}\t{scipy.stats.skew(cur.y):<15.10g}')
                        print(f'\tkurtosis:  {scipy.stats.kurtosis(cur.x):<15.10g}\t{scipy.stats.kurtosis(cur.y):<15.10g}')  # noqae501
                        print(f'\tmin:       {numpy.min(cur.x):<15.10g}\t{numpy.min(cur.y):<15.10g}')
                        print(f'\t25%:       {numpy.quantile(cur.x,.25):<15.10g}\t{numpy.quantile(cur.y,.25):<15.10g}')
                        print(f'\t50%:       {numpy.quantile(cur.x,.50):<15.10g}\t{numpy.quantile(cur.y,.50):<15.10g}')
                        print(f'\t75%:       {numpy.quantile(cur.x,.75):<15.10g}\t{numpy.quantile(cur.y,.75):<15.10g}')
                        print(f'\tmax:       {numpy.max(cur.x):<15.10g}\t{numpy.max(cur.y):<15.10g}')
                        print(f'\tsum:       {numpy.sum(cur.x):<15.10g}\t{numpy.sum(cur.y):<15.10g}')

                    except pdvutil.CurveIndexError:
                        pass

                print('\n')
            except:
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            finally:
                self.redraw = False

    def help_stats(self):
        print('\n   Display the mean and standard deviation for the given curves.'
              '\n   usage: stats <curve-list>\n')

    def do_getattributes(self, line):
        """
        Return a curve's attributes
        """
        if len(line.split(':')) > 1:
            self.do_getattributes(pdvutil.getletterargs(line))
            return 0
        else:
            if not line:
                return 0
            try:
                line = line.split()
                for c in line:
                    idx = pdvutil.getCurveIndex(c, self.plotlist)
                    cur = self.plotlist[idx]
                    try:
                        cur.step = self.curvelist[idx].step
                    except:
                        cur.step = False
                    try:
                        cur.xticks_labels = self.curvelist[idx].xticks_labels
                    except:
                        cur.xticks_labels = None
                    print('\n')
                    print('    Plot name = {}'.format(cur.plotname))
                    print('    Color = {}'.format(cur.color))
                    if cur.linestyle == '-':
                        pp_linestyle = 'solid'
                    elif cur.linestyle == ':':
                        pp_linestyle = 'dot'
                    elif cur.linestyle == '--':
                        pp_linestyle = 'dash'
                    elif cur.linestyle == '-.':
                        pp_linestyle = 'dashdot'
                    print('    Style = {}'.format(pp_linestyle))
                    print('    Curve width = {} '.format(cur.linewidth))
                    print('    Edited = {}'.format(cur.edited))
                    print('    Scatter = {}'.format(cur.scatter))
                    print('    Linespoints = {}'.format(cur.linespoints))
                    print('    Drawstyle = {}'.format(cur.drawstyle))
                    print('    Dashes = {}'.format(cur.dashes))
                    print('    Hidden = {}'.format(cur.hidden))
                    print('    Marker = {}'.format(cur.marker))
                    print('    Markersize = {}'.format(cur.markersize))
                    print('    Markeredgecolor = {}'.format(cur.markeredgecolor))
                    print('    Markerfacecolor = {}'.format(cur.markerfacecolor))
                    print('    Ebar = {}'.format(cur.ebar))
                    print('    Erange = {}'.format(cur.erange))
                    print('    Plotprecedence = {}'.format(cur.plotprecedence))
                    print('    Step Function = {}'.format(cur.step))
                    print('    X-ticks Labels = {}'.format(cur.xticks_labels))
                    print('\n')
            except:
                print('\n   usage: getattributes <curves>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            finally:
                self.redraw = False

    def help_getattributes(self):
        print('\n   Display the given curve\'s attributes, such as: color, style, and width.'
              '\n   usage: getattributes <curves>')

    def do_markerfacecolor(self, line):
        """
        Set the markerface color for a list of curves
        """

        try:
            if not line:
                return 0
            line = line.split()
            color = line.pop(-1)
            line = ' '.join(line)
            if len(line.split(':')) > 1:
                self.do_markerfacecolor(pdvutil.getletterargs(line) + color)
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        if mclr.is_color_like(color):
                            cur.markerfacecolor = color
                        else:
                            print('error: invalid marker face color ' + color)
                            return 0
                    except pdvutil.CurveIndexError:
                        pass

            self.plotedit = True

        except:
            print('error - usage: markerfacecolor <curve-list> <color-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_markerfacecolor(self):
        print('\n   Procedure: Set the markerface color of curves'
              '\n   Usage: markerfacecolor <curve-list> <color-name>'
              '\n          Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set'
              '\n          of hexadecimal red-green-blue values (RRGGBB).'
              '\n          The entire set of HTML-standard color names is available.'
              '\n          Try "showcolormap" to see the available named colors!')

    def do_markeredgecolor(self, line):
        """
        Set the markeredge color for a list of curves
        """

        try:
            if not line:
                return 0
            line = line.split()
            color = line.pop(-1)
            line = ' '.join(line)
            if len(line.split(':')) > 1:
                self.do_markeredgecolor(pdvutil.getletterargs(line) + color)
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        if mclr.is_color_like(color):
                            cur.markeredgecolor = color
                        else:
                            print('error: invalid marker edge color ' + color)
                            return 0
                    except pdvutil.CurveIndexError:
                        pass

            self.plotedit = True

        except:
            print('error - usage: markeredgecolor <curve-list> <color-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_markeredgecolor(self):
        print("\n   Procedure: Set the markeredge color of curves"
              "\n   Usage: markeredgecolor <curve-list> <color-name>"
              "\n          Color names can be 'blue', 'red', etc, or '#eb70aa', a 6 digit set"
              "\n          of hexadecimal red-green-blue values (RRGGBB)."
              "\n          The entire set of HTML-standard color names is available."
              "\n          Try 'showcolormap' to see the available named colors!")

    def do_showstyles(self, line):
        """
        Show available matplotlib styles
        """

        try:
            if stylesLoaded:
                ss = pydvif.get_styles()
                print('\n')
                self.print_topics('Style Names (type style <style-name>):', ss, 15, 80)
            else:
                print("\nNo styles available.\n")
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_showstyles(self):
        print("\n   Procedure: show the available pre-defined styles provided by matplotlib."
              "\n   Usage: showstyles\n")

    def do_showcolormap(self, line):
        """
        Show the available named colors
        """

        try:
            ax = plt.gca()
            plt.cla()  # wipe current axes

            ratio = 1.0 / 3.0
            count = numpy.ceil(numpy.sqrt(len(mclr.cnames)))
            x_count = count * ratio
            y_count = count / ratio
            x = 0
            y = 0
            w = 1 / x_count
            h = 1 / y_count
            plt.xlim((0.0, 1.0))
            plt.ylim((0.0, 1.0))

            from matplotlib.collections import PatchCollection

            patches = []
            for c in mclr.cnames:
                pos = (x / x_count, y / y_count)
                rectangle = plt.Rectangle(pos, w, h, color=c)
                patches.append(rectangle)
                ax.add_artist(rectangle)  # needed for colors to show up, sigh :-(
                ax.annotate(c, xy=pos, fontsize='xx-small', verticalalignment='bottom', horizontalalignment='left')
                if y >= y_count - 1:
                    x += 1
                    y = 0
                else:
                    y += 1

            p = PatchCollection(patches)
            ax.add_collection(p)
            plt.draw()
            self.plotter.canvas.draw()

            x = input('hit return to go back to your plots: ')
            self.plotedit = True
        except:
            print('error - usage: showcolormap')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_showcolormap(self):
        print('\n   Procedure: show the available named colors'
              '\n   Usage: showcolormap'
              '\n   Hit <return> after viewing to go back to regular plotting\n')

    def do_mx(self, line):
        """
        Scale y values of curves by a constant
        """

        try:
            self.__mod_curve(line, 'mx')
            self.plotedit = True
        except:
            print('error - usage: mx <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_mx(self):
        print('\n   Procedure: Scale x values of curves by a constant'
              '\n   Usage: mx <curve-list> <value>\n')

    def do_divx(self, line):
        """
        Divide x values of curves by a constant
        """

        try:
            self.__mod_curve(line, 'divx')
            self.plotedit = True
        except:
            print('error - usage: divx <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_divx(self):
        print('\n   Procedure: Divide x values of curves by a constant\n   Usage: divx <curve-list> <value>\n')

    def do_my(self, line):
        """
        Scale y values of curves by a constant
        """

        try:
            self.__mod_curve(line, 'my')
            self.plotedit = True
        except:
            print('error - usage: my <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_my(self):
        print('\n   Procedure: Scale y values of curves by a constant'
              '\n   Usage: my <curve-list> <value>\n')

    def do_divy(self, line):
        """
        Divide y values of curves by a constant
        """

        try:
            self.__mod_curve(line, 'divy')
            self.plotedit = True
        except:
            print('error - usage: divy <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_divy(self):
        print('\n   Procedure: Divide y values of curves by a constant'
              '\n   Usage: divy <curve-list> <value>\n')

    def do_dx(self, line):
        """
        Shift curve x values by given constant
        """

        try:
            self.__mod_curve(line, 'dx')
            self.plotedit = True
        except:
            print('error - usage: dx <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_dx(self):
        print('\n   Procedure: Shift x values of curves by a constant\n   Usage: dx <curve-list> <value>\n')

    def do_dy(self, line):
        """
        Shift curve y values by given constant
        """

        try:
            self.__mod_curve(line, 'dy')
            self.plotedit = True
        except:
            print('error - usage: dy <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_dy(self):
        print('\n   Procedure: Shift y values of curves by a constant\n   Usage: dy <curve-list> <value>\n')

    def do_L2(self, line):
        """
        Take L2 norm of two curves
        """

        try:
            """take L2 norm of two curves given as args"""
            args = line.strip().split()
            if len(args) != 2 and len(args) != 4:
                raise RuntimeError("wrong number of args to L2")
            # put a '2' in between curves and xmin, xmax,
            # to indicate the order of norm to take
            args.insert(2, '2')
            # put args back into a line
            line = " ".join(args)
            # then pass to usual "norm" command
            self.do_norm(line)
        except:
            print("error - usage: L2 <curve> <curve> [<xmin> <xmax>]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_L2(self):
        print('\n   Procedure: makes new curve that is the L2 norm of two args; the L2-norm is '
              '\n (integral(  (curve1 - curve2)**2 ) )**(1/2) over the interval [xmin, xmax] .'
              '\n   Usage: L2 <curve> <curve>  [<xmin> <xmax>]\n  Also prints value of integral to command line.\n')

    def do_L1(self, line):
        """
        Take L1 norm of two curves
        """

        try:
            """take L1 norm of two curves given as args"""
            args = line.strip().split()
            if len(args) != 2 and len(args) != 4:
                raise RuntimeError("wrong number of args to L1")
            # put a '1' in between curves and xmin, xmax,
            # to indicate the order of norm to take
            args.insert(2, '1')
            # put args back into a line
            line = " ".join(args)
            # then pass to usual "norm" command
            self.do_norm(line)
        except:
            print("error - usage: L1 <curve> <curve> [<xmin> <xmax>]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_L1(self):
        print('\n   Procedure: makes new curve that is the L1 norm of two args; the L1-norm is '
              '\n integral(  |curve1 - curve2| ) over the interval [xmin, xmax] .'
              '\n   Usage: L1 <curve> <curve>  [<xmin> <xmax>]\n  Also prints value of integral to command line.\n')

    def do_norm(self, line):
        """
        Take arbitrary order norm of two curves
        """

        try:
            """take norm of order N of two curves given as args"""
            args = line.strip().split()
            if len(args) != 3 and len(args) != 5:
                raise RuntimeError("wrong number of args to norm")
            # curves a and b will be our operands
            a = self.curvefromlabel(args[0])
            b = self.curvefromlabel(args[1])
            c = a - b   # new numpy.array object
            c.y = abs(c.y)  # absolute value
            if args[2].lower() != "inf":
                N = int(args[2])  # order of the norm
                c = c**N
            if len(args) == 5:
                xmin = float(args[3])
                xmax = float(args[4])
                if xmax <= xmin:
                    raise RuntimeError("xmin > xmax or xmin == xmax in do_norm()")
            else:
                xmin = min(c.x)
                xmax = max(c.x)
            if args[2].lower() == "inf":
                Linf = 0.0
                for xi, yi in zip(c.x, c.y):
                    if xmin <= xi <= xmax:
                        Linf = max(Linf, yi)
                print("Linf norm = {:.4f}".format(Linf))
                d = c
                d.y = numpy.array([Linf] * c.y.shape[0])
                d.name = "Linf of " + a.plotname + " and " + b.plotname
            else:
                d = pydvif.integrate(c, xmin, xmax)[0]  # d = integral( c**N )
                d = d**(1.0 / N)
                print("L{:d} norm = {:.4f}".format(N, max(d.y)))
                d.name = "L%d of " % N + a.plotname + " and " + b.plotname
            self.addtoplot(d)
        except:
            print('error - usage: norm <curve> <curve> <p> [<xmin> <xmax>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_norm(self):
        print('\n   Procedure: makes new curve that is the norm of two args; the p-norm is '
              '\n              (integral(  (curve1 - curve2)**p ) )**(1/p) over the interval [xmin, xmax] .'
              '\n   Usage: norm <curve> <curve> <p> [<xmin> <xmax>]'
              '\n          where p=order which can be "inf" or an integer. '
              'Also prints value of integral to command line.\n')

    def do_max(self, line):
        """
        Make a new curve - the max of the specified curves
        """

        try:
            if not line:
                return 0
            if len(line.split(':')) > 1:
                self.do_max(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()

                if len(line) < 2:
                    return

                curves = list()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curves.append(self.plotlist[curvidx])
                    except pdvutil.CurveIndexError:
                        pass

                nc = pydvif.max_curve(curves)

                if nc is not None:
                    self.addtoplot(nc)
                    self.plotedit = True

        except:
            self.help_max()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_max(self):
        print('\n   Procedure: makes new curve with max y values of curves.'
              '\n   Usage: max <curve-list>\n')

    def do_min(self, line):
        """
        Make a new curve - the min of the specified curves
        """

        if not line:
            return 0

        if len(line.split(':')) > 1:
            self.do_min(pdvutil.getletterargs(line))
            return 0
        else:
            try:
                line = line.split()

                if len(line) < 2:
                    return

                curves = list()
                for i in range(len(line)):
                    curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    curves.append(self.plotlist[curvidx])

                nc = pydvif.min_curve(curves)

                if nc is not None:
                    self.addtoplot(nc)
                    self.plotedit = True
            except RuntimeError as rte:
                print('error: %s' % rte)
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            except:
                self.help_min()
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_min(self):
        print('\n   Procedure: makes new curve with min y values of curves.'
              '\n   Usage: min <curve-list>\n')

    def do_average(self, line):
        """
        Make a new curve - the average of the specified curves
        """

        if not line:
            return 0

        if len(line.split(':')) > 1:
            self.do_average(pdvutil.getletterargs(line))
            return 0
        else:
            try:
                line = line.split()

                if len(line) < 2:
                    return

                curves = list()
                for i in range(len(self.plotlist)):
                    for j in range(len(line)):
                        if self.plotlist[i].plotname == line[j].upper():
                            curves.append(self.plotlist[i])
                            break

                nc = pydvif.average_curve(curves)

                if nc is not None:
                    self.addtoplot(nc)
                    self.plotedit = True
            except RuntimeError as rte:
                print('error: %s' % rte)
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            except:
                self.help_average()
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_average(self):
        print('\n   Procedure: Average the specified curvelist over the intersection of their domains.'
              '\n   Usage: average <curvelist>\n')

    def do_fit(self, line):
        """
        Fit a curve with a polynomial function
        """

        try:
            """fit curve to line: usage is 'fit curve [n] [logx] [logy]', where n=order of fit, default is linear"""
            print("fitting curve: {}".format(line))
            args = line.strip().split()
            if len(args) == 0 or len(args) > 4:
                raise RuntimeError("wrong number of args to fit")

            c = self.curvefromlabel(args[0])
            logx, logy = False, False

            if "logx" in args:
                logx = True
                args.remove("logx")

            if "logy" in args:
                logy = True
                args.remove("logy")

            assert len(args) in (1, 2)
            if len(args) == 2:
                n = int(args[1])
            else:
                n = 1

            nc = pydvif.fit(c, n, logx, logy)
            nc.plotname = self.getcurvename()
            self.addtoplot(nc)
        except:
            print('error - usage: fit <curve> [n] [logx] [logy]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_fit(self):
        print('\n   Procedure: make new curve that is polynomial fit to argument.'
              '\n   Usage: fit <curve> [n] [logx] [logy]'
              '\n   n=1 by default, logy means take log(y-values) before fitting,'
              '\n   logx means take log(x-values) before fitting\n')

    def do_getx(self, line):
        """
        Return x values for a given y
        """

        try:
            self.__mod_curve(line, 'getx')
            print('')
        except:
            print('error - usage: getx <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getx(self):
        print('\n   Procedure: Return x values for a given y\n   Usage: getx <curve-list> <y-value>\n')

    def do_gety(self, line):
        """
        Return y values for a given x
        """

        try:
            self.__mod_curve(line, 'gety')
            print('')
        except:
            print('error - usage: gety <curve-list> <value>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_gety(self):
        print('\n   Procedure: Return y values for a given x\n   Usage: gety <curve-list> <x-value>\n')

    def do_getrange(self, line):
        """
        Return range of curves
        """

        if not line:
            return
        try:
            if len(line.split(':')) > 1:
                self.do_getrange(pdvutil.getletterargs(line))
                return 0
            else:
                print('\n   Get Range')
                line = line.split()
                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[idx]
                        plotname, miny, maxy = pydvif.getrange(cur)[0]
                        print('\nCurve ' + plotname)
                        print('    ymin: %.6e    ymax: %.6e' % (miny, maxy))
                    except pdvutil.CurveIndexError:
                        pass
                print('')
        except:
            print('error - usage: getrange <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getrange(self):
        print('\n   Procedure: Return range of curves\n   Usage: getrange <curve-list>\n   Shortcuts: get-range\n')

    def do_getdomain(self, line):
        """
        Return domain of curves
        """

        try:
            if len(line.split(':')) > 1:
                self.do_getdomain(pdvutil.getletterargs(line))
                return 0
            else:
                print('\n   Get Domain')
                line = line.split()

                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[idx]
                        plotname, minx, maxx = pydvif.getdomain(cur)[0]
                        print('\nCurve ' + plotname)
                        print('    xmin: %.6e    xmax: %.6e' % (minx, maxx))
                    except pdvutil.CurveIndexError:
                        pass
                print('')
        except:
            print('error - usage: getdomain <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getdomain(self):
        print('\n   Procedure: Return domain of curves\n   Usage: getdomain <curve-list>\n   Shortcuts: get-domain\n')

    def do_sum(self, line):
        """
        Return sum of the x and y values of each curve
        """

        try:
            if len(line.split(':')) > 1:
                self.do_sum(pdvutil.getletterargs(line))
                return 0
            else:
                print('\nSum:')
                line = line.split()

                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[idx]
                        plotname, sumx, sumy = pydvif.sum(cur)[0]
                        print(f'\nCurve {cur.plotname}: {plotname}')
                        print(f'\tsumx: {sumx:.6e}, sumy: {sumy:.6e}')
                    except pdvutil.CurveIndexError:
                        pass
                print('')
        except:
            print('error - usage: sum <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_sum(self):
        print('\n   Procedure: Return sum of the x and y values of each curve\n   Usage: sum <curve-list>\n')

    def do_area(self, line):
        """
        Return area of each curve
        """

        try:
            if len(line.split(':')) > 1:
                self.do_area(pdvutil.getletterargs(line))
                return 0
            else:
                print('\nArea:')
                line = line.split()

                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[idx]
                        plotname, area = pydvif.area(cur)[0]
                        print(f'\nCurve {cur.plotname}: {plotname}')
                        print(f'\tarea: {area:.6e}')
                    except pdvutil.CurveIndexError:
                        pass
                print('')
        except:
            print('error - usage: area <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_area(self):
        print('\n   Procedure: Return area of each curve\n   Usage: area <curve-list>\n')

    def do_getymax(self, line):
        """
        Return the maximum y-value for the curve within the specified domain
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:
                self.do_getymax(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                xlow = None
                xhi = None

                try:
                    xhi = float(line[-1])
                    line.pop(-1)
                except:
                    xhi = None

                try:
                    xlow = float(line[-1])
                    line.pop(-1)
                except:
                    xlow = None

                if (xlow is None and xhi is not None) or (xlow is not None and xhi is None):
                    raise RuntimeError("<xmin> and <xmax> must BOTH be specified")

                for i in line:
                    idx = pdvutil.getCurveIndex(i, self.plotlist)
                    cur = self.plotlist[idx]
                    plotname, xy_values = pydvif.getymax(cur, xlow, xhi)
                    print(f' \n{i.upper()} Curve {plotname}')
                    for x, y in xy_values:
                        print('    x: %.6e    y: %.6e\n' % (x, y))
        except:
            print('error - usage: getymax <curve> [<xmin> <xmax>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getymax(self):
        print('\n   Procedure: Return the maximum y-value for the curve within the specified domain.'
              '\n   Usage: getymax <curve> [<xmin> <xmax>]\n')

    def do_getymin(self, line):
        """
        Return the minimum y-value for the curve within the specified domain
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:
                self.do_getymin(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                xlow = None
                xhi = None

                try:
                    xhi = float(line[-1])
                    line.pop(-1)
                except:
                    xhi = None

                try:
                    xlow = float(line[-1])
                    line.pop(-1)
                except:
                    xlow = None

                if (xlow is None and xhi is not None) or (xlow is not None and xhi is None):
                    raise RuntimeError("<xmin> and <xmax> must BOTH be specified")

                for i in line:
                    idx = pdvutil.getCurveIndex(i, self.plotlist)
                    cur = self.plotlist[idx]
                    plotname, xy_values = pydvif.getymin(cur, xlow, xhi)
                    print(f' \n{i.upper()} Curve {plotname}')
                    for x, y in xy_values:
                        print('    x: %.6e    y: %.6e\n' % (x, y))
        except:
            print('error - usage: getymin <curve> [<xmin> <xmax>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getymin(self):
        print('\n   Procedure: Return the minimum y-value for the curve within the specified domain.'
              '\n   Usage: getymin <curve> [<xmin> <xmax>]\n')

    def do_cumsum(self, line):
        """
        Return the cumulative sum of the curve(s)
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:
                self.do_cumsum(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()

                for i in line:
                    idx = pdvutil.getCurveIndex(i, self.plotlist)
                    cur = self.plotlist[idx]
                    nc = pydvif.cumsum(cur)
                    self.addtoplot(nc)

                    self.plotedit = True
        except:
            print('error - usage: cumsum <curve>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_cumsum(self):
        print('\n   Procedure: Return the cumulative sum of the curve(s).'
              '\n   Usage: cumsum <curve>\n')

    def do_getlabel(self, line):
        """
        Return the given curve's label
        """

        try:
            if len(line.split(':')) > 1:
                self.do_getlabel(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()

                for i in range(len(self.plotlist)):
                    cur = self.plotlist[i]
                    for j in range(len(line)):
                        if cur.plotname == line[j].upper():
                            print(f"\n {line[j].upper()} Label = {cur.name}")
        except:
            print('error - usage: getlabel <curve>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getlabel(self):
        print("\n   Procedure: Return the given curve's label\n   Usage: getlabel <curve>\n")

    def do_sort(self, line):
        """
        Sort the specified curves so that their points are plotted in order of ascending x values
        """

        try:
            if len(line.split(':')) > 1:
                self.do_sort(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        j = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[j]
                        pydvif.sort(cur)
                    except pdvutil.CurveIndexError:
                        pass

            self.plotedit = True

        except:
            print('error - usage: sort <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sort(self):
        print('\n   Procedure: Sort the specified curves so that their points are plotted in order of ascending '
              'x values.'
              '\n   Usage: sort <curve-list>\n')

    def do_rev(self, line):
        """
        Swap x and y values for the specified curves.
        """

        try:
            if len(line.split(':')) > 1:
                self.do_rev(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        j = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[j]
                        pydvif.rev(cur)
                    except pdvutil.CurveIndexError:
                        pass
            self.plotedit = True

        except:
            print('error - usage: rev <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_rev(self):
        print('\n    Procedure: Swap x and y values for the specified curves. You may want to sort after this one. '
              '\n    Usage: rev <curve-list>\n')

    def do_random(self, line):
        """
        Generate random y values between -1 and 1 for the specified curves
        """

        try:
            if len(line.split(':')) > 1:
                self.do_random(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        j = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[j]
                        pydvif.random(cur)
                    except pdvutil.CurveIndexError:
                        pass
            self.plotedit = True

        except:
            print('error - usage: random <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_random(self):
        print('\n   Procedure: Generate random y values between -1 and 1 for the specified curves. '
              '\n   Usage: random <curve-list>\n')

    def do_disp(self, line):
        """
        Display the y-values in the specified curves
        """

        try:
            if len(line.split(':')) > 1:
                self.do_disp(pdvutil.getletterargs(line))
                return 0
            else:
                print('\n')
                line = line.split()
                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[idx]
                        ss = pydvif.disp(cur, False)
                        self.print_topics('Curve %s: %s' % (cur.plotname, cur.name), ss, 15, 100)
                    except pdvutil.CurveIndexError:
                        pass
        except:
            print('error - usage: disp <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_disp(self):
        print('\n   Procedure: Display the y-values in the specified curve(s). \n   Usage: disp <curve-list>\n')

    def do_dispx(self, line):
        """
        Display the x-values in the specified curves
        """

        try:
            if len(line.split(':')) > 1:
                self.do_dispx(pdvutil.getletterargs(line))
                return 0
            else:
                print('\n')
                line = line.split()
                for i in range(len(line)):
                    try:
                        idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[idx]
                        ss = pydvif.disp(cur)
                        self.print_topics('Curve %s: %s' % (cur.plotname, cur.name), ss, 15, 100)
                    except pdvutil.CurveIndexError:
                        pass
        except:
            print('error - usage: dispx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_dispx(self):
        print('\n   Procedure: Display the x-values in the specified curve(s). \n   Usage: dispx <curve-list>\n')

    def do_getnumpoints(self, line):
        """
        Display the number of points for the given curve
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:
                self.do_getnumpoints(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    cur = self.plotlist[idx]
                    print(f'\n    {line[i].upper()} Number of points = {pydvif.getnumpoints(cur)}')
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_getnumpoints(self):
        print('\n   Display the given curve\'s number of points.\n   usage: getnumpoints <curve>')

    def do_abs(self, line):
        """
        Take absolute value of y values of curves
        """

        try:
            self.__func_curve(line, 'abs', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: abs <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_abs(self):
        print('\n   Procedure: Take absolute value of y values of curves'
              '\n   Usage: abs <curve-list>\n')

    def do_absx(self, line):
        """
        Take absolute value of x values of curves
        """

        try:
            self.__func_curve(line, 'abs', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: absx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_absx(self):
        print('\n   Procedure: Take absolute value of x values of curves'
              '\n   Usage: absx <curve-list>\n')

    def do_log(self, line):
        """
        Take the natural logarithm of the curve y-values
        """

        try:
            self.__log(line, LogEnum.LOG)
            self.plotedit = True
        except:
            print('error - usage: log <curve-list> [keep-neg-vals: True | False]')
            if self.debug:
                print(traceback.print_exc(file=sys.stdout))

    def help_log(self):
        print('\n   Procedure: take natural logarithm of y-values of curves.'
              '\n              If the optional argument keep-neg-vals is set to True, then zero and negative'
              '\n              y-values will not be discarded. keep-neg-vals is False by default.'
              '\n   Usage: log <curve-list> [keep-neg-vals: True | False]\n   Shortcut: ln\n')

    def do_logx(self, line):
        """
        Take the natural logarithm of the curve x-values
        """

        try:
            self.__log(line, LogEnum.LOGX)
            self.plotedit = True
        except:
            print('error - usage: logx <curve-list> [keep-neg-vals: True | False]')
            if self.debug:
                print(traceback.print_exc(file=sys.stdout))

    def help_logx(self):
        print('\n   Procedure: take natural logarithm of x-values of curves.'
              '\n              If the optional argument keep-neg-vals is set to True, then zero and negative x-values'
              '\n              will not be discarded. keep-neg-vals is False by default.\n'
              '\n   Usage: logx <curve-list> [keep-neg-vals: True | False]\n   Shortcut: lnx\n')

    def do_log10(self, line):
        """
        Take the base 10 logarithm of the curve y-values
        """

        try:
            self.__log(line, LogEnum.LOG10)
            self.plotedit = True
        except:
            print('error - usage: log10 <curve-list> [keep-neg-vals: True | False]')
            if self.debug:
                print(traceback.print_exc(file=sys.stdout))

    def help_log10(self):
        print('\n   Procedure: take base 10 logarithm of y values of curves.'
              '\n              If the optional argument keep-neg-vals is set to True, then zero and negative x-values'
              '\n              will not be discarded. keep-neg-vals is False by default.'
              '\n   Usage: log10 <curve-list> [keep-neg-vals: True | False]')

    def do_log10x(self, line):
        """
        Take the base 10 logarithm of the curve x-values
        """

        try:
            self.__log(line, LogEnum.LOG10X)
            self.plotedit = True
        except:
            print('error - usage: log10x <curve-list> [keep-neg-vals: True | False]')
            if self.debug:
                print(traceback.print_exc(file=sys.stdout))

    def help_log10x(self):
        print('\n   Procedure: take base 10 logarithm of x values of curves.\n'
              '\n              If the optional argument keep-neg-vals is set to True, then zero and negative x-values'
              '\n              will not be discarded. keep-neg-vals is False by default.'
              '\n   Usage: log10x <curve-list> [keep-neg-vals: True | False]')

    def do_exp(self, line):
        """
        Exponentiate y values of curves, e**y
        """

        try:
            self.__func_curve(line, 'exp', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: exp <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_exp(self):
        print('\n   Procedure: e**y, exponentiate y values of curves'
              '\n   Usage: exp <curve-list>\n')

    def do_expx(self, line):
        """
        Exponentiate x values of curves, e**x
        """

        try:
            self.__func_curve(line, 'exp', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: expx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_expx(self):
        print('\n   Procedure: e**y, exponentiate x values of curves'
              '\n   Usage: expx <curve-list>\n')

    def do_cos(self, line):
        """
        Take cosine of y values of curves
        """

        try:
            self.__func_curve(line, 'cos', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: cos <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_cos(self):
        print('\n   Procedure: Take cosine of y values of curves'
              '\n   Usage: cos <curve-list>\n')

    def do_cosx(self, line):
        """
        Take cosine of x values of curves
        """

        try:
            self.__func_curve(line, 'cos', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: cosx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_cosx(self):
        print('\n   Procedure: Take cosine of x values of curves'
              '\n   Usage: cosx <curve-list>\n')

    def do_sin(self, line):
        """
        Take sine of y values of curves
        """

        try:
            self.__func_curve(line, 'sin', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: sin <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sin(self):
        print('\n   Procedure: Take sine of y values of curves'
              '\n   Usage: sin <curve-list>\n')

    def do_sinx(self, line):
        """
        Take sine of x values of curves
        """

        try:
            self.__func_curve(line, 'sin', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: sinx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sinx(self):
        print('\n   Procedure: Take sine of x values of curves'
              '\n   Usage: sinx <curve-list>\n')

    def do_tan(self, line):
        """
        Take tangent of y values of curves
        """

        try:
            self.__func_curve(line, 'tan', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: tan <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_tan(self):
        print('\n   Procedure: Take tangent of y values of curves'
              '\n   Usage: tan <curve-list>\n')

    def do_tanx(self, line):
        """
        Take tangent of x values of curves
        """

        try:
            self.__func_curve(line, 'tan', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: tanx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_tanx(self):
        print('\n   Procedure: Take tangent of x values of curves'
              '\n   Usage: tanx <curve-list>\n')

    def do_acos(self, line):
        """
        Take arccosine of y values of curves
        """

        try:
            self.__func_curve(line, 'acos', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: acos <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_acos(self):
        print('\n   Procedure: Take arccosine of y values of curves'
              '\n   Usage: acos <curve-list>\n')

    def do_acosx(self, line):
        """
        Take arccosine of x values of curves
        """

        try:
            self.__func_curve(line, 'acos', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: acosx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_acosx(self):
        print('\n   Procedure: Take arccosine of x values of curves'
              '\n   Usage: acosx <curve-list>\n')

    def do_asin(self, line):
        """
        Take arcsine of y values of curves.
        """

        try:
            self.__func_curve(line, 'asin', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: asin <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_asin(self):
        print('\n   Procedure: Take arcsine of y values of curves'
              '\n   Usage: asin <curve-list>\n')

    def do_asinx(self, line):
        """
        Take arcsine of x values of curves.

        :param line: User Command-Line Input (arsinx <curve-list>))
        :type line: string
        """

        try:
            self.__func_curve(line, 'asin', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: asinx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_asinx(self):
        print('\n   Procedure: Take arcsine of x values of curves'
              '\n   Usage: asinx <curve-list>\n')

    def do_atan(self, line):
        """
        Take arctangent of y values of curves
        """

        try:
            self.__func_curve(line, 'atan', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: atan <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_atan(self):
        print('\n   Procedure: Take arctangent of y values of curves'
              '\n   Usage: atan <curve-list>\n')

    def do_atanx(self, line):
        """
        Take arctangent of x values of curves
        """

        try:
            self.__func_curve(line, 'atan', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: atanx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_atanx(self):
        print('\n   Procedure: Take arctangent of x values of curves'
              '\n   Usage: atanx <curve-list>\n')

    def do_atan2(self, line):
        """
        Take atan2 of two curves
        """

        try:
            letterargs = [x.upper() for x in line.split()]
            assert len(letterargs) == 2
            a, b = None, None
            for p in self.plotlist:
                if p.plotname == letterargs[0]:
                    a = p
                elif p.plotname == letterargs[1]:
                    b = p
            assert a and b
            c = pydvif.atan2(a, b, tuple(letterargs))
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: atan curve1 curve2')
            if (self.debug):
                traceback.print_exc(file=sys.stdout)

    def help_atan2(self):
        print('\n   Procedure: Take atan2 of two curves'
              '\n   Usage: atan2 curve1 curve2\n')

    def do_cosh(self, line):
        """
        Take hyperbolic cosine of y values of curves
        """

        try:
            self.__func_curve(line, 'cosh', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: cosh <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_cosh(self):
        print('\n   Procedure: Take hyperbolic cosine of y values of curves'
              '\n   Usage: cosh <curve-list>\n')

    def do_coshx(self, line):
        """
        Take hyperbolic cosine of x values of curves
        """

        try:
            self.__func_curve(line, 'cosh', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: coshx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_coshx(self):
        print('\n   Procedure: Take hyperbolic cosine of x values of curves'
              '\n   Usage: coshx <curve-list>\n')

    def do_sinh(self, line):
        """
        Take hyperbolic sine of y values of curves
        """

        try:
            self.__func_curve(line, 'sinh', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: sinh <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sinh(self):
        print('\n   Procedure: Take hyperbolic sine of y values of curves'
              '\n   Usage: sinh <curve-list>\n')

    def do_sinhx(self, line):
        """
        Take hyperbolic sine of x values of curves
        """

        try:
            self.__func_curve(line, 'sinh', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: sinhx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sinhx(self):
        print('\n   Procedure: Take hyperbolic sine of x values of curves'
              '\n   Usage: sinhx <curve-list>\n')

    def do_tanh(self, line):
        """
        Take hyperbolic tangent of y values of curves
        """

        try:
            self.__func_curve(line, 'tanh', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: tanh <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_tanh(self):
        print('\n   Procedure: Take hyperbolic tangent of y values of curves'
              '\n   Usage: tanh <curve-list>\n')

    def do_tanhx(self, line):
        """
        Take hyperbolic tangent of x values of curves
        """

        try:
            self.__func_curve(line, 'tanh', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: tanhx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_tanhx(self):
        print('\n   Procedure: Take hyperbolic tangent of x values of curves'
              '\n   Usage: tanhx <curve-list>\n')

    def do_acosh(self, line):
        """
        Take hyperbolic arccosine of y values of curves
        """

        try:
            self.__func_curve(line, 'acosh', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: acosh <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_acosh(self):
        print('\n   Procedure: Take hyperbolic arccosine of y values of curves'
              '\n   Usage: acosh <curve-list>\n')

    def do_acoshx(self, line):
        """
        Take hyperbolic arccosine of x values of curves
        """

        try:
            self.__func_curve(line, 'acosh', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: acoshx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_acoshx(self):
        print('\n   Procedure: Take hyperbolic arccosine of x values of curves'
              '\n   Usage: acoshx <curve-list>\n')

    def do_asinh(self, line):
        """
        Take hyperbolic arcsine of y values of curves
        """

        try:
            self.__func_curve(line, 'asinh', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: asinh <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_asinh(self):
        print('\n   Procedure: Take hyperbolic arcsine of y values of curves'
              '\n   Usage: asinh <curve-list>\n')

    def do_asinhx(self, line):
        """
        Take hyperbolic arcsine of x values of curves
        """

        try:
            self.__func_curve(line, 'asinh', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: asinhx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_asinhx(self):
        print('\n   Procedure: Take hyperbolic arcsine of x values of curves'
              '\n   Usage: asinhx <curve-list>\n')

    def do_atanh(self, line):
        """
        Take hyperbolic arctangent of y values of curves
        """

        try:
            self.__func_curve(line, 'atanh', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: atanh <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_atanh(self):
        print('\n   Procedure: Take hyperbolic arctangent of y values of curves'
              '\n   Usage: atanh <curve-list>\n')

    def do_atanhx(self, line):
        """
        Take hyperbolic arctangent of x values of curves
        """

        try:
            self.__func_curve(line, 'atanh', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: atanhx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_atanhx(self):
        print('\n   Procedure: Take hyperbolic arctangent of x values of curves'
              '\n   Usage: atanhx <curve-list>\n')

    def do_j0(self, line):
        """
        Take the zeroth order Bessel function of y values of curves
        """

        try:
            self.__func_curve(line, 'j0', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: j0 <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_j0(self):
        print('\n   Procedure: Take the zeroth order Bessel function of y values of curves'
              '\n   Usage: j0 <curve-list>\n')

    def do_j0x(self, line):
        """
        Take the zeroth order Bessel function of x values of curves
        """

        try:
            self.__func_curve(line, 'j0', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: j0x <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_j0x(self):
        print('\n   Procedure: Take the zeroth order Bessel function of x values of curves'
              '\n   Usage: j0x <curve-list>\n')

    def do_j1(self, line):
        """
        Take the first order Bessel function of y values of curves
        """

        try:
            self.__func_curve(line, 'j1', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: j1 <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_j1(self):
        print('\n   Procedure: Take the first order Bessel function of y values of curves'
              '\n   Usage: j1 <curve-list>\n')

    def do_j1x(self, line):
        """
        Take the first order Bessel function of x values of curves
        """

        try:
            self.__func_curve(line, 'j1', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: j1x <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_j1x(self):
        print('\n   Procedure: Take the first order Bessel function of x values of curves'
              '\n   Usage: j1x <curve-list>\n')

    def do_jn(self, line):
        """
        Take the nth order Bessel function of y values of curves
        """

        try:
            self.__func_curve(line, 'jn', do_x=0, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: jn <curve-list> <n>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_jn(self):
        print('\n   Procedure: Take the nth order Bessel function of y values of curves'
              '\n   Usage: jn <curve-list> <n>\n')

    def do_jnx(self, line):
        """
        Take the nth order Bessel function of x values of curves
        """

        try:
            self.__func_curve(line, 'jn', do_x=1, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: jnx <curve-list> <n>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_jnx(self):
        print('\n   Procedure: Take the nth order Bessel function of x values of curves'
              '\n   Usage: jnx <curve-list> <n>\n')

    def do_y0(self, line):
        """
        Take the zeroth order Bessel function of the second kind of y values of curves
        """

        try:
            self.__func_curve(line, 'y0', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: y0 <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_y0(self):
        print('\n   Procedure: Take the zeroth order Bessel function of the second kind of y values of curves'
              '\n   Usage: y0 <curve-list>\n')

    def do_y0x(self, line):
        """
        Take the zeroth order Bessel function of the second kind of x values of curves
        """

        try:
            self.__func_curve(line, 'y0', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: y0x <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_y0x(self):
        print('\n   Procedure: Take the zeroth order Bessel function of the second kind of x values of curves'
              '\n   Usage: y0x <curve-list>\n')

    def do_y1(self, line):
        """
        Take the first order Bessel function of the second kind of y values of curves
        """

        try:
            self.__func_curve(line, 'y1', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: y1 <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_y1(self):
        print('\n   Procedure: Take the first order Bessel function of the second kind of y values of curves'
              '\n   Usage: y1 <curve-list>\n')

    def do_y1x(self, line):
        """
        Take the first order Bessel function of the second kind of x values of curves
        """

        try:
            self.__func_curve(line, 'y1', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: y1x <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_y1x(self):
        print('\n   Procedure: Take the first order Bessel function of the second kind of x values of curves'
              '\n   Usage: y1x <curve-list>\n')

    def do_yn(self, line):
        """
        Take the nth order Bessel function of the second kind of y values of curves
        """

        try:
            self.__func_curve(line, 'yn', do_x=0, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: yn <curve-list> n')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_yn(self):
        print('\n   Procedure: Take the nth order Bessel function of the second kind of y values of curves'
              '\n   Usage: yn <curve-list> <n>\n')

    def do_ynx(self, line):
        """
        Take the nth order Bessel function of the second kind of x values of curves
        """

        try:
            self.__func_curve(line, 'yn', do_x=1, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: ynx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ynx(self):
        print('\n   Procedure: Take the nth order Bessel function of the second kind of x values of curves'
              '\n   Usage: ynx <curve-list> <n>\n')

    def do_powa(self, line):
        """
        Raise a fixed value, a, to the power of the y values of the curves
        """

        try:
            self.__func_curve(line, 'powa', do_x=0, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: powa <curve-list> a')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_powa(self):
        print('\n   Procedure: Raise a fixed value, a, to the power of the y values of the curves'
              '\n   Usage: powa <curve-list> a\n')

    def do_powax(self, line):
        """
        Raise a fixed value, a, to the power of the x values of the curves
        """

        try:
            self.__func_curve(line, 'powa', do_x=1, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: powax <curve-list> a')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_powax(self):
        print('\n   Procedure: Raise a fixed value, a, to the power of the x values of the curves'
              '\n   Usage: powax <curve-list> a\n')

    def do_powr(self, line):
        """
        Raise the y values of the curves to a fixed power, y=y^p
        """

        try:
            self.__func_curve(line, 'powr', do_x=0, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: powr <curve-list> a')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_powr(self):
        print('\n   Procedure: Raise the y values of the curves to a fixed power, y=y^p'
              '\n   Usage: power <curve-list> p\n   Shortcuts: pow , powr\n')

    def do_powrx(self, line):
        """
        Raise the x values of the curves to a fixed power, x=x^p
        """

        try:
            self.__func_curve(line, 'powr', do_x=1, idx=-1)
            self.plotedit = True
        except:
            print('error - usage: powrx <curve-list> a')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_powrx(self):
        print('\n   Procedure: Raise the x values of the curves to a fixed power, x=x^p'
              '\n   Usage: powerx <curve-list> p\n   Shortcuts: powx , powrx\n')

    def do_recip(self, line):
        """
        Take the reciprocal of the y values of the curves
        """

        try:
            self.__func_curve(line, 'recip', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: recip <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_recip(self):
        print('\n   Procedure: Take the reciprocal of the y values of the curves'
              '\n   Usage: recip <curve-list>\n')

    def do_recipx(self, line):
        """
        Take the reciprocal of the x values of the curves
        """

        try:
            self.__func_curve(line, 'recip', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: recipx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_recipx(self):
        print('\n   Procedure: Take the reciprocal of the x values of the curves'
              '\n   Usage: recipx <curve-list>\n')

    def do_sqr(self, line):
        """
        Take the square of the y values of the curves
        """

        try:
            self.__func_curve(line, 'sqr', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: sqr <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sqr(self):
        print('\n   Procedure: Take the square of the y values of the curves'
              '\n   Usage: square <curve-list>\n   Shortcut: sqr\n')

    def do_sqrx(self, line):
        """
        Take the square of the x values of the curves
        """

        try:
            self.__func_curve(line, 'sqr', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: sqrx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sqrx(self):
        print('\n   Procedure: Take the square of the x values of the curves'
              '\n   Usage: squarex <curve-list>\n   Shortcut: sqrx\n')

    def do_sqrt(self, line):
        """
        Take the square root of the y values of the curves
        """

        try:
            self.__func_curve(line, 'sqrt', do_x=0)
            self.plotedit = True
        except:
            print('error - usage: sqrt <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sqrt(self):
        print('\n   Procedure: Take the square root of the y values of the curves'
              '\n   Usage: sqrt <curve-list>\n')

    def do_sqrtx(self, line):
        """
        Take the square root of the x values of the curves
        """

        try:
            self.__func_curve(line, 'sqrt', do_x=1)
            self.plotedit = True
        except:
            print('error - usage: sqrtx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_sqrtx(self):
        print('\n   Procedure: Take the square root of the x values of the curves'
              '\n   Usage: sqrtx <curve-list>\n')

    def do_xlabel(self, line):
        """
        Set a label for the x-axis
        """

        try:
            self.set_xlabel(line)
        except:
            print('error - usage: xlabel <label-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xlabel(self):
        print('\n   Procedure: Set a label for the x-axis'
              '\n   Usage: xlabel <label-name>\n')

    def do_ylabel(self, line):
        """
        Set a label for the y-axis
        """

        try:
            self.set_ylabel(line)
        except:
            print('error - usage: ylabel <label-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ylabel(self):
        print('\n   Procedure: Set a label for the y axis'
              '\n   Usage: ylabel <label-name>\n')

    def do_title(self, line):
        """
        Set a title for the plot
        """

        try:
            self.set_title(line)
        except:
            print('error - usage: title <title-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_title(self):
        print('\n   Procedure: Set a title for the plot'
              '\n   Usage: title <title-name>\n')

    def do_legend(self, line):
        """
        Show or hide the key/legend
        """

        try:
            locs = {'best': 0, 'ur': 1, 'ul': 2, 'll': 3, 'lr': 4, 'cl': 6, 'cr': 7, 'lc': 8, 'uc': 9, 'c': 10}
            line = line.strip().split()

            for i in range(len(line)):
                key = line[i].lower()

                if key in locs:
                    self.key_loc = locs[key]
                elif key == 'on':
                    self.showkey = True
                elif key == 'off':
                    self.showkey = False
                elif key in ['hide', 'show']:
                    if line[i + 1] == 'all':  # show/hide all curves
                        for cur in self.plotlist:
                            cur.legend_show = False if key == 'hide' else True
                    else:
                        if ':' in line[i + 1]:
                            ids = list(pdvutil.getletterargs(line[i + 1]).lower().split())
                        else:
                            ids = [line[j] for j in range(i + 1, len(line))]
                        for curve_id in ids:
                            curve = self.plotlist[pdvutil.getCurveIndex(curve_id, self.plotlist)]
                            curve.legend_show = False if key == 'hide' else True
                        break
                elif key in ['hideid', 'showid']:
                    if line[i + 1] == 'all':  # show/hide all curves
                        for cur in self.plotlist:
                            cur.name = cur.name.replace(f'`{cur.plotname}` ', '')
                            if key == 'showid':
                                cur.name = f'`{cur.plotname}` {cur.name}'
                            else:
                                cur.name.replace(f'`{cur.plotname}` ', '')
                    else:
                        if ':' in line[i + 1]:
                            ids = list(pdvutil.getletterargs(line[i + 1]).lower().split())
                        else:
                            ids = [line[j] for j in range(i + 1, len(line))]
                        for curve_id in ids:
                            curve = self.plotlist[pdvutil.getCurveIndex(curve_id, self.plotlist)]
                            curve.name = curve.name.replace(f'`{curve.plotname}` ', '')
                            if key == 'showid':
                                curve.name = f'`{curve.plotname}` {curve.name}'
                            else:
                                curve.name.replace(f'`{curve.plotname}` ', '')
                        break
                else:
                    try:
                        self.key_ncol = int(key)
                    except:
                        raise Exception('Invalid argument: %s' % key)
        except:
            print('error - usage: legend [on | off] [<position>] [<number of columns>] [<show/hide curve>] [<showid/hideid curve ids>]')  # noqae501
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_legend(self):
        print('\n   Variable: Show the legend if True. Set legend position as '
              'best, ur, ul, ll, lr, cl, cr, uc, lc, c. Select curves to add to or remove from the legend.'
              '\n   Usage: legend [on | off] [<position>] [<number of columns>] [<show/hide curve>] [<showid/hideid curve ids>]'  # noqae501
              '\n   Shortcuts: leg, key\n')

    def do_menulength(self, line):
        """
        Adjust the number of items shown in the 'menu' command
        """

        try:
            if len(line) == 0:
                print('menu length is currently', self.menulength)
            else:
                line = line.split()
                length = int(line[0])
                if length <= 0:
                    length = 1
                self.menulength = length
                print('changing menu length to ', self.menulength)
        except:
            print('error - usage: menulength [length]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_menulength(self):
        print('\n   Command: Adjust the number of items shown in the menu command '
              'If no length is given, the current menu length will be displayed.'
              '\n   Usage:  menulength [length]')

    def do_namewidth(self, line):
        """
        Adjust the width of the label column in 'menu' and 'lst' commands
        """

        try:
            if len(line) == 0:
                print('label column width is currently', self.namewidth)
            else:
                line = line.split()
                width = int(line[0])
                if width < 0:
                    width = 0
                self.namewidth = width
                print('changing label column width to ', self.namewidth)
        except:
            print('error - usage: namewidth [width]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_namewidth(self):
        print('\n   Command: change the width of the curve_name column of the menu and lst output. '
              'If no width is given, the current column width will be displayed.'
              '\n   Usage:  namewidth [width]')

    def do_xlabelwidth(self, line):
        """
        Adjust the width of the xlabel column in 'menu' and 'lst' commands
        """

        try:
            if len(line) == 0:
                print('xlabel column width is currently', self.xlabelwidth)
            else:
                line = line.split()
                width = int(line[0])
                if width < 0:
                    width = 0
                self.xlabelwidth = width
                print('changing xlabel column width to', self.xlabelwidth)
        except:
            print('error - usage: xlabelwidth [width]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xlabelwidth(self):
        print('\n   Command: change the width of the xlabel column of the menu and lst output. '
              'If no width is given, the current column width will be displayed.'
              '\n   Usage:  xlabelwidth [width]')

    def do_ylabelwidth(self, line):
        """
        Adjust the width of the ylabel column in 'menu' and 'lst' commands
        """

        try:
            if len(line) == 0:
                print('label column width is currently', self.ylabelwidth)
            else:
                line = line.split()
                width = int(line[0])
                if width < 0:
                    width = 0
                self.ylabelwidth = width
                print('changing ylabel column width to', self.ylabelwidth)
        except:
            print('error - usage: ylabelwidth [width]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ylabelwidth(self):
        print('\n   Command: change the width of the ylabel column of the menu and lst output. '
              'If no width is given, the current column width will be displayed.'
              '\n   Usage:  ylabelwidth [width]')

    def do_filenamewidth(self, line):
        """
        Adjust the width of the file column in 'menu' and 'lst' commands
        """

        try:
            if len(line) == 0:
                print('file column width is currently', self.filenamewidth)
            else:
                line = line.split()
                width = int(line[0])
                if width < 0:
                    width = 0
                self.filenamewidth = width
                print('changing file column width to', self.filenamewidth)
        except:
            print('error - usage: filenamewidth [width]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_filenamewidth(self):
        print('\n   Command: change the width of the file column of the menu and lst output. If no width is given, the'
              '\n            current column width will be displayed.'
              '\n   Usage:  filenamewidth [width]')

    def do_recordidwidth(self, line):
        """
        Adjust the width of the rec id column in 'menu' and 'lst' commands
        """

        try:
            if len(line) == 0:
                print('record_id column width is currently', self.recordidwidth)
            else:
                line = line.split()
                width = int(line[0])
                if width < 0:
                    width = 0
                self.recordidwidth = width
                print('changing rec id column width to', self.recordidwidth)
        except:
            print('error - usage: recordidwidth [width]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_recordidwidth(self):
        print('\n   Command: change the width of the record_id column of the menu and lst output. '
              'If no width is given, the current column width will be displayed.'
              '\n   Usage:  recordidwidth [width]')

    def do_handlelength(self, line):
        """
        Adjust the length of the lines in the legend
        """

        try:
            key = line.strip().split()[0]
            if key.upper() == "NONE":
                self.handlelength = None
            else:
                self.handlelength = max(0, int(key))
            self.plotedit = True
        except:
            print('error -- usage:')
            self.help_handlelength()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_handlelength(self):
        print('\n   Command: change the length of the lines in the legend')
        print('     Usage: handlelength <integer>')

    def do_minorticks(self, line):
        """
        Show or hide minor ticks
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showminorticks = False
            elif line == '1' or line.upper() == 'ON':
                self.showminorticks = True
            else:
                print('invalid input: requires on, off, 1, or 0 as argument')
        except:
            print('error - usage: minorticks <on | off | 1 | 0>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_minorticks(self):
        print('\n   Variable: Minor ticks are not visible by default.'
              '\n   On or 1 will make the minor ticks visible and off or 0 will hide the minor ticks.'
              '\n   Usage: minorticks <on | off | 1 | 0>')

    def do_border(self, line):
        """
        Show or hide the border
        """

        try:
            color = None
            line = line.split()
            arg_count = len(line)

            if arg_count == 1:
                show = line[0]
            elif arg_count == 2:
                show = line[0]
                color = line[1]
            else:
                raise RuntimeError('Too many arguments: Expected 1 or 2 but received {}'.format(arg_count))

            if show == '0' or show.upper() == 'OFF':
                self.bordercolor = None
            elif show == '1' or show.upper() == 'ON':
                if arg_count > 1:
                    if mclr.is_color_like(color):
                        self.bordercolor = color
                        self.plotedit = True
                    else:
                        raise RuntimeError('Invalid color {}'.format(color))
                else:
                    self.bordercolor = 'black'
            else:
                raise RuntimeError('invalid input: requires on, 1, off, or 0 as argument')

        except:
            print('error - usage: border <on | 1 | off | 0> [color-name]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_border(self):
        print('\n   Procedure: Show the border if on or 1, otherwise hide the border. The color-name'
              '\n              determines the color of the border. By default, the border color is black.'
              '\n   Usage: border <on | 1 | off | 0> [color-name]'
              '\n   Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set'
              '\n   of hexadecimal red-green-blue values (RRGGBB).'
              '\n   The entire set of HTML-standard color names is available.'
              '\n   Try "showcolormap" to see the available named colors!')

    def do_grid(self, line):
        """
        Show or hide the grid
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showgrid = False
            elif line == '1' or line.upper() == 'ON':
                self.showgrid = True
            else:
                print('invalid input: requires on or off as argument')
        except:
            print('error - usage: grid on | off')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_grid(self):
        print('\n   Variable: Show the grid if True\n   Usage: grid on | off\n')

    def do_axis(self, line):
        """
        Show or hide the axis
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showaxis = 'off'
            elif line == '1' or line.upper() == 'ON':
                self.showaxis = 'on'
            else:
                print('invalid input: requires on or off as argument')
        except:
            print('error - usage: axis on | off')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_axis(self):
        print('\n   Variable: Show the axis if True\n   Usage: axis on | off\n')

    def do_plot(self, line):
        """
        Show or hide the line plots
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showplot = 'off'
                self.showkey = False  # legend
            elif line == '1' or line.upper() == 'ON':
                self.showplot = 'on'
                self.showkey = True  # legend
            else:
                print('invalid input: requires on or off as argument')
        except:
            print('error - usage: plot on | off')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_plot(self):
        print('\n   Variable: Show the line plots if True\n   Usage: plot on | off\n')

    def do_recolor(self, line):
        """
        Reset the color of the line plots
        """

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        j = 0
        for i in range(len(self.plotlist)):
            self.do_color(f'{self.plotlist[i].plotname} {colors[j]}')
            j += 1
            if j == 7:
                j = 0

    def help_recolor(self):
        print('\n   Variable: Reset the color of the line plots\n')

    def do_merge(self, line):
        """
        Merge ultra files together
        """

        try:
            line = line.split()
            new_file = line[0]

            if os.path.exists(new_file):
                ans = input(f'{new_file} already exists. Overwrite? [y/n]: ')

                if ans.upper() in ['YES', 'Y']:
                    print(f'Overwriting {new_file}')
                elif ans.upper() in ['NO', 'N']:
                    print(f'Not overwriting {new_file}')
                    return
                else:
                    print('Please try again and type [y/n]')
                    return

            other_files = line[1:]
            with open(new_file, 'w') as f1:
                lines = []
                for other_file in other_files:
                    with open(other_file, 'r') as f2:
                        lines += f2.readlines()
                        lines += '\n'
                f1.writelines(lines)
        except:
            print('error - usage: merge <newfile> <myfile1> <myfile2> etc..')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_merge(self):
        print('\n   Variable: Merge ultra files together\n   Usage: merge <newfile> <myfile1> <myfile2> etc..\n')

    def do_gridcolor(self, line):
        """
        Set the grid color
        """

        if not line:
            return 0
        try:
            color = line.strip()
            if mclr.is_color_like(color):
                self.gridcolor = color
                self.plotedit = True
            else:
                print('error: invalid color ' + color)
                return 0
        except:
            print('error - usage: gridcolor <color-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_gridcolor(self):
        print('\n   Procedure: Set the color of the grid'
              '\n   Usage: gridcolor <color-name>'
              '\n   Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set'
              '\n   of hexadecimal red-green-blue values (RRGGBB).'
              '\n   The entire set of HTML-standard color names is available.'
              '\n   Try "showcolormap" to see the available named colors!')

    def do_gridstyle(self, line):
        """
        Change the grid style
        """

        if not line:
            return 0

        style = line.strip()

        if style == 'solid':
            self.gridstyle = '-'
        elif style == 'dot':
            self.gridstyle = ':'
        elif style == 'dash':
            self.gridstyle = '--'
        elif style == 'dashdot':
            self.gridstyle = '-.'
        else:
            print('error: invalid style ' + style)
            return 0

    def help_gridstyle(self):
        print('\n   Procedure: Set the line style for the grid.'
              '\n   Usage: gridstyle <style: solid | dash | dot | dashdot>\n')

    def do_gridwidth(self, line):
        """
        Set the grid line width
        """

        if not line:
            return 0

        try:
            self.gridwidth = float(line.strip())
        except:
            print('error - usage: gridwidth <width>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_gridwidth(self):
        print('\n   Procedure: Set the grid line width in points.\n   Usage: gridwidth <width>\n')

    def do_dataid(self, line):
        """
        Show or hide letter markers on plotted curves
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showletters = False
            elif line == '1' or line.upper() == 'ON':
                self.showletters = True
            else:
                print('invalid input: requires on or off as argument')
        except:
            print('error - usage: dataid <on | off>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_dataid(self):
        print('\n   Variable: Show curve identifiers if True'
              '\n   Usage: dataid <on | off>'
              '\n   Shortcuts: data-id\n')

    def do_xlogscale(self, line):
        """
        Show the x axis on a log scale
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.xlogscale = False
            elif line == '1' or line.upper() == 'ON':
                self.xlogscale = True
                plt.xscale('log')
                if self.xlim is not None:
                    xmin = max(1e-2, self.xlim[0])
                    self.xlim = (xmin, max(self.xlim[1], 1000.0 * xmin))
            else:
                print('invalid input: requires on or off as argument')
        except:
            print('error - usage: xlogscale <on | 1 | off | 0>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xlogscale(self):
        print('\n   Variable: Show x axis in log scale if True'
              '\n   Usage: xlogscale <on | 1 | off | 0>'
              '\n   Shortcuts: x-log-scale , xls\n')

    def do_ylogscale(self, line):
        """
        Show the y axis on a log scale
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.ylogscale = False
            elif line == '1' or line.upper() == 'ON':
                self.ylogscale = True
                plt.yscale('log')
                if self.ylim is not None:
                    ymin = max(1e-2, self.ylim[0])
                    self.ylim = (ymin, max(self.ylim[1], 1000.0 * ymin))
            else:
                print('invalid input: requires on or off as argument')
        except:
            print('error - usage: ylogscale <on | 1 | off | 0>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ylogscale(self):
        print('\n   Variable: Show y axis in log scale if True'
              '\n   Usage: ylogscale <on | 1 | off | 0>'
              '\n   Shortcuts: y-log-scale , yls\n')

    def do_guilims(self, line):
        """
        Set whether or not to use the GUI min/max values for the X and Y limits
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.guilims = False
                self.xlim = None
                self.ylim = None
            elif line == '1' or line.upper() == 'ON':
                self.guilims = True
                self.xlim = plt.gca().get_xlim()
                self.ylim = plt.gca().get_ylim()
            else:
                raise RuntimeError("{} is not a valid input.".format(line))
        except:
            print('error - usage: guilims on | off | 1 | 0')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_guilims(self):
        print('\n   Variable: Set whether or not to use the GUI min/max values for the X and Y limits. Default is off.'
              '\n   Usage: guilims on | off | 1 | 0\n')

    def do_update(self, line):
        """
        Set whether to update after each command
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.update = False
            elif line == '1' or line.upper() == 'ON':
                self.update = True
            else:
                print('invalid input: requires on/1 or off/0 as argument')
        except:
            print('error - usage: update <on | 1 | off | 0>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_update(self):
        print('\n   Variable: Update the plot after each command if ON or 1, otherwise don\'t update the plot.'
              '\n             Update the plot is ON by default.'
              '\n   Usage: update <on | 1 | off | 0>\n')

    def do_latex(self, line):
        """
        Set whether or not to use LaTeX font rendering
        """

        try:
            line = line.strip()

            if line == '0' or line.upper() == 'OFF':
                matplotlib.rc('text', usetex=False)
            elif line == '1' or line.upper() == 'ON':
                matplotlib.rc('text', usetex=True)
            else:
                print('invalid input: requires on, off, 1, or 0 as argument')
        except:
            print('latex on | off | 1 | 0')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_latex(self):
        print('\n   Variable: Use LaTeX font rendering if True. By default, LaTeX font rendering is off.'
              '\n   Usage: latex on | off | 1 | 0\n')

    def do_scatter(self, line):
        """
        Show given curves as points rather than continuous line
        """

        try:
            self.__mod_curve(line, 'scatter')
            self.plotedit = True
        except:
            print('error - usage: scatter <curve-list> <on | 1 | off | 0>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_scatter(self):
        print('\n   Procedure: Plot curves as scatter plots'
              '\n   Usage: scatter <curve-list> <on | 1 | off | 0>\n')

    def do_linespoints(self, line):
        """
        Show given curves as points and a line rather than continuous line
        """

        try:
            self.__mod_curve(line, 'linespoints')
            self.plotedit = True
        except:
            print('error - usage: linespoints <curve-list> on | off')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_linespoints(self):
        print('\n   Procedure: Plot curves as linespoints plots\n   Usage: linespoints <curve-list> on | off\n')

    def do_lnwidth(self, line):
        """
        Set line width of given curves
        """

        try:
            self.__mod_curve(line, 'lnwidth')
            self.plotedit = True
        except:
            print('error - usage: lnwidth <curve-list> <width>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_lnwidth(self):
        print('\n   Procedure: Set the line widths of curves\n   Usage: lnwidth <curve-list> <width>\n')

    def do_lnstyle(self, line):
        """
        Set line style of given curves
        """

        try:
            self.__mod_curve(line, 'lnstyle')
            self.plotedit = True
        except:
            print('error - usage: lnstyle <curve-list> <style: solid | dash | dot | dashdot '
                  '| loosely_dotted | long_dash_with_offset | loosely_dashed | dashed '
                  '| loosely_dashdotted | dashdotted | densely_dashdotted '
                  '| dashdotdotted | loosely_dashdotdotted | densely_dashdotdotted>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_lnstyle(self):
        print('\n   Procedure: Set the line style of curves'
              '\n   Usage: lnstyle <curve-list> <style: solid | dash | dot | dashdot '
              '| loosely_dotted | long_dash_with_offset | loosely_dashed | dashed '
              '| loosely_dashdotted | dashdotted | densely_dashdotted '
              '| dashdotdotted | loosely_dashdotdotted | densely_dashdotdotted>\n')

    def do_drawstyle(self, line):
        """
        Set draw style of given curves
        """

        try:
            self.__mod_curve(line, 'drawstyle')
            self.plotedit = True
        except:
            print('error - usage: drawstyle <curve-list> <style: default | steps | steps-pre | steps-post | steps-mid>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_drawstyle(self):
        print('\n   Procedure: Set the draw style of the curves'
              '\n   Usage: drawstyle <curve-list> <style: default | steps | steps-pre | steps-post | steps-mid>\n')

    def do_dashstyle(self, line):
        """
        Set dash style of given curves
        """

        try:
            options = line[line.index("["):]
            line = line[0:line.index("[")]
            self.modcurve(line, 'dashstyle', options)
            self.plotedit = True
        except:
            print("ERROR : dashstyle usage")
            self.help_dashstyle()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_dashstyle(self):
        print('''
                 Procedure: Set the style of dash or dot dash lines
                 Usage: dashstyle <curve-list> <[...]>
                     The python list is a list of integers, alternating how many pixels to turn on and off, for example:
                         [2, 2] : Two pixels on, two off (will result in a dot pattern).
                         [4, 2, 2, 2] : 4 on, 2 off, 2 on, 2 off (results in a dash-dot pattern).
                         [4, 2, 2, 2, 4, 2] : Gives a dash-dot-dash pattern.
                         [4, 2, 2, 2, 2, 2] : Gives a dash-dot-dot pattern.
                 See matplotlib 'set_dashes' command for more information.
             ''')

    def do_group(self, line):
        """
        Group curves based on name and file if curve names are the same
        """

        pn, cn, fn = self.do_listr('1')

        # Setting Linestyles at the file level
        files = []

        for f in fn:  # ordered set
            if f not in files:
                files.append(f)

        groups = {}

        for f in files:
            temp = []
            for i, plotname in enumerate(pn):
                if fn[i] == f:
                    temp.append(plotname)

            groups[f] = temp

        styles = [('solid', 'solid'),      # Same as (0, ()) or '-'
                  ('dot', 'dot'),    # Same as (0, (1, 1)) or ':'
                  ('dash', 'dash'),    # Same as '--'
                  ('dashdot', 'dashdot'),  # Same as '-.'
                  ('loosely_dotted', '(0, (1, 10))'),
                  ('long_dash_with_offset', '(5, (10, 3))'),
                  ('loosely_dashed', '(0, (5, 10))'),
                  ('dashed', '(0, (5, 5))'),
                  ('loosely_dashdotted', '(0, (3, 10, 1, 10))'),
                  ('dashdotted', '(0, (3, 5, 1, 5))'),
                  ('densely_dashdotted', '(0, (3, 1, 1, 1))'),
                  ('dashdotdotted', '(0, (3, 5, 1, 5, 1, 5))'),
                  ('loosely_dashdotdotted', '(0, (3, 10, 1, 10, 1, 10))'),
                  ('densely_dashdotdotted', '(0, (3, 1, 1, 1, 1, 1))')]

        for i, filename in enumerate(groups):
            if i < 14:
                curves_ = " ".join(groups[filename])
                self.do_lnstyle(curves_ + ' ' + styles[i][0].replace("'", ""))
            else:
                print('There are only fourteen linestyles available. Please reduce the number of files.')

        # Setting Colors at the curve level
        curve_names = []

        for curve_name in cn:  # ordered set
            temp_cn = curve_name.split(' - ')[0]
            if temp_cn not in curve_names:
                curve_names.append(temp_cn)

        groups = {}

        for curve_name in curve_names:
            temp = []
            for i, plotname in enumerate(pn):
                if cn[i].split(' - ')[0] == curve_name:
                    temp.append(plotname)

            groups[curve_name] = temp

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        for i, curve_name in enumerate(groups):
            if i < 10:
                curves_ = " ".join(groups[curve_name])
                self.do_color(curves_ + ' ' + colors[i].replace("'", ""))
            else:
                print('There are only ten colors available. Please reduce the number of same name curves.')

        self.updateplot

    def help_group(self):
        print('\n   Group curves based on name and file if curve names are the same.\n')

    def do_hide(self, line):
        """
        Turn hiding on for given curves
        """

        try:
            line = line + ' ' + 'ON'
            self.__mod_curve(line, 'hide')
            self.reset_xticks_labels()
        except:
            print('error - usage: hide <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_hide(self):
        print('\n   Procedure: Hide curves from view\n   Usage: hide <curve-list>\n')

    def do_show(self, line):
        """
        Turn hiding off for given curves
        """

        try:
            line = line + ' ' + 'OFF'
            self.__mod_curve(line, 'hide')
            self.reset_xticks_labels()
        except:
            print('error - usage: show <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_show(self):
        print('\n   Procedure: Reveal curves hidden by hide command'
              '\n   Usage: show <curve-list>\n')

    def do_style(self, line):
        """
        Use matplotlib style settings
        """

        try:
            line = line.split()
            self.plotter.style = line[0]
            self.updatestyle = True
            self.redraw = True
        except:
            print('error - usage: style <style-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_style(self):
        print('''
        Procedure: Use matplotlib style settings from a style specification.
        The style name of 'default' is reserved for reverting back to the
        default style settings.

        Usage: style <style-name>
        ''')

    def do_range(self, line):
        """
        Change the y range on the graph
        """

        try:
            line = line.split()
            if line and line[0] == 'de':
                self.ylim = None
            elif len(line) == 2:
                self.ylim = (float(line[0]), float(line[1]))
            else:
                print('error: exactly two arguments required or de for default')
        except:
            print('error - usage: range <low-lim> <high-lim> or range de')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_range(self):
        print("\n   Procedure: Set the range for plotting. Use 'de' for using the default limits (none)."
              "\n   Usage: range <low-lim> <high-lim> or range de"
              "\n   Shortcuts: ran\n")

    def do_domain(self, line):
        """
        Change the x domain on the graph
        """

        try:
            line = line.split()
            if (line and line[0] == 'de'):
                self.xlim = None
            elif (len(line) == 2):
                self.xlim = (float(line[0]), float(line[1]))
            else:
                print('error: exactly two arguments required or de for default')
        except:
            print('error - usage: domain <low-lim> <high-lim> or domain de')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_domain(self):
        print('\n   Procedure: Set the domain for plotting'
              '\n   Usage: domain <low-lim> <high-lim> or'
              '\n   Usage: domain de'
              '\n   Shortcuts: dom\n')

    def do_list(self, line):
        """
        List currently graphed curves
        """

        try:
            reg = re.compile(r"")
            if line:
                try:
                    reg = re.compile(r"%s" % line)
                except:
                    print("error - invalid label-pattern")
                    return 0

            print("{:<5} {:<{namewidth}.{namewidth}} {:<{xlabelwidth}.{xlabelwidth}} {:<{ylabelwidth}.{ylabelwidth}} "
                  .format('curve', 'curve_name', 'xlabel', 'ylabel',
                          namewidth=self.namewidth, xlabelwidth=self.xlabelwidth, ylabelwidth=self.ylabelwidth,
                          ) + # noqa w504
                  "{:<9} {:<9} {:<9} {:<9} {:<{filenamewidth}.{filenamewidth}} {:<{recordidwidth}.{recordidwidth}}"
                  .format('xmin', 'xmax', 'ymin', 'ymax', 'fname', 'record_id',
                          filenamewidth=self.filenamewidth, recordidwidth=self.recordidwidth))
            print("".join(['-'] * (5 + self.namewidth + self.xlabelwidth + self.ylabelwidth + 9 + 9 + 9 + 9 +  # noqaw504
                                   self.filenamewidth + self.recordidwidth + 9)))  # last digit is number of columns - 1
            for cur in self.plotlist:
                searchline = cur.name + ' ' + cur.filename
                if not line or reg.search(searchline):
                    plotname = ""
                    if cur.edited:
                        plotname = "*"
                    plotname = plotname + cur.plotname
                    name = cur.name
                    name = pdvutil.truncate(cur.name.ljust(self.namewidth), self.namewidth)
                    xlabel = cur.xlabel
                    xlabel = xlabel.ljust(self.xlabelwidth)
                    xlabel = pdvutil.truncate(xlabel, self.xlabelwidth)
                    ylabel = cur.ylabel
                    ylabel = ylabel.ljust(self.ylabelwidth)
                    ylabel = pdvutil.truncate(ylabel, self.ylabelwidth)
                    fname = cur.filename
                    fname = fname.ljust(self.filenamewidth)
                    fname = pdvutil.truncate(fname, self.filenamewidth, 'right')
                    record_id = cur.record_id
                    record_id = record_id.ljust(self.recordidwidth)
                    record_id = pdvutil.truncate(record_id, self.recordidwidth)
                    xmin = "%.2e" % min(cur.x)
                    xmax = "%.2e" % max(cur.x)
                    ymin = "%.2e" % min(cur.y)
                    ymax = "%.2e" % max(cur.y)
                    print("{:>5} {} {} {} {:9} {:9} {:9} {:9} {} {}".format(plotname, name, xlabel, ylabel, xmin,
                                                                            xmax, ymin, ymax, fname, record_id))
        except:
            print("error - usage: list [<label-pattern>]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_list(self):
        print("\n    {}\n    {}\n    {}\n".format("Macro: Display curves in list",
                                                  "Usage: list [<label-pattern>]",
                                                  "Shortcuts: lst"))

    def do_listr(self, line):
        """
        List currently graphed curves
        """

        group_plotnames = []
        group_curvenames = []
        group_filenames = []

        try:
            if not line:
                self.help_listr()
                return

            line = line.split()
            argcnt = len(line)
            pllen = len(self.plotlist)
            start = 0
            stop = pllen

            if argcnt == 1:
                start = int(line[0]) - 1
            elif argcnt == 2:
                start = int(line[0]) - 1
                stop = int(line[1])
            else:
                raise RuntimeError("Invalid number of arguments. Received {} expecting 1 or 2.".format(argcnt))

            # Clamp start/stop values in range(0, len(plotlist))
            if start < 0:
                start = 0

            if stop > pllen:
                stop = pllen

            print("{:<5} {:<{namewidth}.{namewidth}} {:<{xlabelwidth}.{xlabelwidth}} {:<{ylabelwidth}.{ylabelwidth}} "
                  .format('curve', 'curve_name', 'xlabel', 'ylabel',
                          namewidth=self.namewidth, xlabelwidth=self.xlabelwidth, ylabelwidth=self.ylabelwidth,
                          ) + # noqa w504
                  "{:<9} {:<9} {:<9} {:<9} {:<{filenamewidth}.{filenamewidth}} {:<{recordidwidth}.{recordidwidth}}"
                  .format('xmin', 'xmax', 'ymin', 'ymax', 'fname', 'record_id',
                          filenamewidth=self.filenamewidth, recordidwidth=self.recordidwidth))
            print("".join(['-'] * (5 + self.namewidth + self.xlabelwidth + self.ylabelwidth + 9 + 9 + 9 + 9 +  # noqaw504
                                   self.filenamewidth + self.recordidwidth + 9)))  # last digit is number of columns - 1
            for i in range(start, stop):
                curve = self.plotlist[i]
                plotname = ""
                if curve.edited:
                    plotname = "*"
                plotname = plotname + curve.plotname
                name = curve.name
                name = pdvutil.truncate(curve.name.ljust(self.namewidth), self.namewidth)
                xlabel = curve.xlabel
                xlabel = xlabel.ljust(self.xlabelwidth)
                xlabel = pdvutil.truncate(xlabel, self.xlabelwidth)
                ylabel = curve.ylabel
                ylabel = ylabel.ljust(self.ylabelwidth)
                ylabel = pdvutil.truncate(ylabel, self.ylabelwidth)
                fname = curve.filename
                fname = fname.ljust(self.filenamewidth)
                fname = pdvutil.truncate(fname, self.filenamewidth, 'right')
                record_id = curve.record_id
                record_id = record_id.ljust(self.recordidwidth)
                record_id = pdvutil.truncate(record_id, self.recordidwidth)
                xmin = "%.2e" % min(curve.x)
                xmax = "%.2e" % max(curve.x)
                ymin = "%.2e" % min(curve.y)
                ymax = "%.2e" % max(curve.y)
                print("{:>5} {} {} {} {:9} {:9} {:9} {:9} {} {}".format(plotname, name, xlabel, ylabel, xmin,
                                                                        xmax, ymin, ymax, fname, record_id))

                group_plotnames.append(plotname)
                group_curvenames.append(name)
                group_filenames.append(fname)

        except:
            print("error - usage: listr <start> [stop]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False
            return group_plotnames, group_curvenames, group_filenames

    def help_listr(self):
        print("\n   Macro: Display curves in range from start to stop in the list. If stop is not specified, it will"
              "\n          be set to the end of the plot list."
              "\n   Usage: listr <start> [stop]"
              "\n   Shortcuts: lstr")

    def do_kill(self, line):
        """
        Delete the specified entries from the menu
        """

        try:
            if not line:
                raise RuntimeError("Argument(s) missing.")

            if 'all' in line:
                self.curvelist = list()
            else:
                tmpcurvelist = list()

                for i in range(len(self.curvelist)):
                    if not str(i + 1) in line:
                        tmpcurvelist.append(self.curvelist[i])

                self.curvelist = tmpcurvelist
        except RuntimeError as rte:
            print('   error - %s' % rte)
            print('   usage: kill [all | number-list]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            print('error - usage: kill [all | number-list]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False
            self.plotter.updateDialogs()

    def help_kill(self):
        print('\n   Procedure: Delete the specified entries from the menu. \
              number-list is a space separated list of menu indexes'
              '\n   Usage: kill [all | number-list]')

    def do_menur(self, line):
        """
        Print out curves loaded from files
        """

        try:
            if not line:
                self.help_menur()
                return

            line = line.split()
            argcnt = len(line)
            start = 0
            stop = len(self.curvelist)

            if argcnt == 1:
                start = int(line[0]) - 1
            elif argcnt == 2:
                start = int(line[0]) - 1
                stop = int(line[1])
            else:
                raise RuntimeError("Invalid number of arguments. Received {} expecting 1 or 2.".format(argcnt))

            # Clamp start/stop values in range(0, len(curvelist))
            if start < 0:
                start = 0

            if stop > len(self.curvelist):
                stop = len(self.curvelist)

            print("{:>5} {:<{namewidth}.{namewidth}} {:<{xlabelwidth}.{xlabelwidth}} {:<{ylabelwidth}.{ylabelwidth}} "
                  .format('index', 'curve_name', 'xlabel', 'ylabel',
                          namewidth=self.namewidth, xlabelwidth=self.xlabelwidth, ylabelwidth=self.ylabelwidth,
                          ) + # noqa w504
                  "{:<9} {:<9} {:<9} {:<9} {:<{filenamewidth}.{filenamewidth}} {:<{recordidwidth}.{recordidwidth}}"
                  .format('xmin', 'xmax', 'ymin', 'ymax', 'fname', 'record_id',
                          filenamewidth=self.filenamewidth, recordidwidth=self.recordidwidth))
            print("".join(['-'] * (5 + self.namewidth + self.xlabelwidth + self.ylabelwidth + 9 + 9 + 9 + 9 +  # noqaw504
                                   self.filenamewidth + self.recordidwidth + 9)))  # last digit is number of columns - 1

            for i in range(start, stop):
                index = str(i + 1)
                name = self.curvelist[i].name
                name = name.ljust(self.namewidth)
                name = pdvutil.truncate(name, self.namewidth)
                xlabel = self.curvelist[i].xlabel
                xlabel = xlabel.ljust(self.xlabelwidth)
                xlabel = pdvutil.truncate(xlabel, self.xlabelwidth)
                ylabel = self.curvelist[i].ylabel
                ylabel = ylabel.ljust(self.ylabelwidth)
                ylabel = pdvutil.truncate(ylabel, self.ylabelwidth)
                fname = self.curvelist[i].filename
                fname = fname.ljust(self.filenamewidth)
                fname = pdvutil.truncate(fname, self.filenamewidth, 'right')
                record_id = self.curvelist[i].record_id
                record_id = record_id.ljust(self.recordidwidth)
                record_id = pdvutil.truncate(record_id, self.recordidwidth)
                xmin = "%.2e" % min(self.curvelist[i].x)
                xmax = "%.2e" % max(self.curvelist[i].x)
                ymin = "%.2e" % min(self.curvelist[i].y)
                ymax = "%.2e" % max(self.curvelist[i].y)
                print("{:>5} {} {} {} {:9} {:9} {:9} {:9} {} {}".format(index, name, xlabel, ylabel, xmin,
                                                                        xmax, ymin, ymax, fname, record_id))
        except:
            print("error - usage: menur <start> [stop]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_menur(self):
        print('\n   Macro: List the available curves from start to stop. If stop is not specified, it will be set to'
              '\n          the end of the curve list.'
              '\n   Usage: menur <start> [stop]')

    def do_menu(self, line):
        """
        Print out curves loaded from files
        """

        menu_j = 1
        j = 0
        try:
            reg = re.compile(r"")
            if line:
                try:
                    reg = re.compile(r"%s" % line)
                except:
                    print("error: invalid expression")
                    return 0

            print("{:>5} {:<{namewidth}.{namewidth}} {:<{xlabelwidth}.{xlabelwidth}} {:<{ylabelwidth}.{ylabelwidth}} "
                  .format('index', 'curve_name', 'xlabel', 'ylabel',
                          namewidth=self.namewidth, xlabelwidth=self.xlabelwidth, ylabelwidth=self.ylabelwidth,
                          ) + # noqa w504
                  "{:<9} {:<9} {:<9} {:<9} {:<{filenamewidth}.{filenamewidth}} {:<{recordidwidth}.{recordidwidth}}"
                  .format('xmin', 'xmax', 'ymin', 'ymax', 'fname', 'record_id',
                          filenamewidth=self.filenamewidth, recordidwidth=self.recordidwidth))
            print("".join(['-'] * (5 + self.namewidth + self.xlabelwidth + self.ylabelwidth + 9 + 9 + 9 + 9 +  # noqaw504
                                   self.filenamewidth + self.recordidwidth + 9)))  # last digit is number of columns - 1
            for i in range(len(self.curvelist)):
                searchline = self.curvelist[i].name + ' ' + self.curvelist[i].filename
                if not line or reg.search(searchline):
                    index = str(i + 1)
                    name = self.curvelist[i].name
                    name = name.ljust(self.namewidth)
                    name = pdvutil.truncate(name, self.namewidth)
                    xlabel = self.curvelist[i].xlabel
                    xlabel = xlabel.ljust(self.xlabelwidth)
                    xlabel = pdvutil.truncate(xlabel, self.xlabelwidth)
                    ylabel = self.curvelist[i].ylabel
                    ylabel = ylabel.ljust(self.ylabelwidth)
                    ylabel = pdvutil.truncate(ylabel, self.ylabelwidth)
                    fname = self.curvelist[i].filename
                    fname = fname.ljust(self.filenamewidth)
                    fname = pdvutil.truncate(fname, self.filenamewidth, 'right')
                    record_id = self.curvelist[i].record_id
                    record_id = record_id.ljust(self.recordidwidth)
                    record_id = pdvutil.truncate(record_id, self.recordidwidth)
                    xmin = "%.2e" % min(self.curvelist[i].x)
                    xmax = "%.2e" % max(self.curvelist[i].x)
                    ymin = "%.2e" % min(self.curvelist[i].y)
                    ymax = "%.2e" % max(self.curvelist[i].y)
                    print("{:>5} {} {} {} {:9} {:9} {:9} {:9} {} {}".format(index, name, xlabel, ylabel, xmin,
                                                                            xmax, ymin, ymax, fname, record_id))
                    j += 1
                if j == self.menulength * menu_j:
                    menu_j += 1
                    stop = input(f"Press Enter to see the next {self.menulength} curves OR n and then enter for no. "
                                 "Change menu length with `menulength #` after exiting the menu display screen.\n")
                    if stop in ['n', 'no', 'N', 'NO']:
                        break
        except:
            print("error - usage: menu [<regex>]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_menu(self):
        print("""\n   Macro: List the available curves\n   Usage: menu [<regex>]\n
                      Regular expressions are based on the Python regex syntax, not the UNIX syntax.
                      In particular, '*' is not the wildcard you might be expecting.

                      Some rules are:

                      'abc'   Matches anything that has 'abc' in it anywhere

                      '.'
                      (Dot)   Matches any character except a newline.

                      '^'
                      (Caret) Matches the start of the string.

                      '$'     Matches the end of the string.

                      []      Used to indicate a set of characters.

                      '*'
                      Causes the resulting RE to match 0 or more repetitions of the
                      preceding RE, as many repetitions as are possible.  ab* will match
                      'a', 'ab', or 'a' followed by any number of 'b's.

                      It is useful to know that '.*' matches any number of anythings, which
                      is often what people expect '*' to do.

                      EXAMPLES:

                      energy     matches   'fluid energy', 'energy from gas', and 'blow energy blow'

                      dt.*cycle  matches  'dt [sh] vs. cycle', and 'find dt on a bicycle please'.

                      ^foo.*rat$ matches 'foobarat', 'foo rat', and 'foolish boy, now you will be eaten by a rat'

                      VR[de]     matches 'bigVRdump', 'smallVRexit', but not 'mediumVRfront'

                      AX[deh-z]  matches 'myAXjob', 'yourAXexit', 'AXnow', but not 'AXfoo'

                      For a painfully complete explanation of the regex syntax, type 'help regex'.
                      """)

    def help_regex(self):
        print("\n    This is the Python help for the 're' module."
              "\n    'help menu' will give you a shorter version.")
        help(re)

    def do_drop(self, line):
        """
        Drop to python prompt
        """
        self.redraw = False
        return True

    def help_drop(self):
        print('\n   Macro: Enter the python prompt for custom input\n   Usage: drop\n')

    def do_quit(self, line):
        """
        Exit the program
        """

        try:
            readline.write_history_file(os.getenv('HOME') + '/.pdvhistory')
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.app.quit()
            sys.exit()
            return True

    def help_quit(self):
        print('\n   Macro: Exit PyDV\n   Usage: quit\n   Shortcuts: q\n')

    def do_image(self, line):
        """
        Save figure to file
        """

        try:
            line = line.split()
            optcnt = len(line)
            filename = 'plot'
            filetype = 'pdf'
            transparent = False
            dpi = 'figure'

            if optcnt >= 1:
                filename = line[0]

            if optcnt >= 2:
                filetype = line[1]

            if optcnt >= 3:
                if line[2].lower() == "true":
                    transparent = True

            if optcnt == 4:
                dpi = float(line[3])

            plt.gcf().set_size_inches(6, 4.41)
            plt.savefig(fname=filename + '.' + filetype, dpi=dpi, format=filetype, transparent=transparent)
        except:
            print("error - usage: image [filename=plot] [filetype=pdf: png | ps | pdf | svg] "
                  "\n                   [transparent=False: True | False] [dpi]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_image(self):
        print("\n   Macro: Save the current figure to an image file. All parameters are optional. The default value"
              "\n          for filename is 'plot', the default value for filetype is 'pdf' and the default value for "
              "\n          transparent is 'False'. dpi is the resolution in dots per inch and the default value is "
              "\n          the figure's dpi value."
              "\n   Usage: image [filename=plot] [filetype=pdf: png | ps | pdf | svg]"
              "\n                [transparent=False: True | False] [dpi]")

    def do_save(self, line):
        """
        Save given curves to a new ultra file
        """

        if not line:
            return 0
        try:
            line = line.split()
            filename = line.pop(0)
            line = ' '.join(line)
            if len(line.split(':')) > 1:
                self.do_save(filename + ' ' + pdvutil.getletterargs(line))
                return 0
            else:
                f = open(filename, 'w')
                save_labels = False
                if 'savelabels' in line:
                    save_labels = True
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        if save_labels:
                            f.write('# ' + cur.name + ' # xlabel ' + cur.xlabel + ' # ylabel ' + cur.ylabel + '\n')
                        else:
                            f.write('# ' + cur.name + '\n')
                        for dex in range(len(cur.x)):
                            f.write(' ' + str(cur.x[dex]) + ' ' + str(cur.y[dex]) + '\n')
                    except RuntimeError as rte:
                        print("I/O error: {}".format(rte))
        except:
            print('error - usage: save <file-name> <curve-list> <savelabels>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_save(self):
        print('\n   Macro: Save curves to file'
              '\n   Usage: save <file-name> <curve-list> <savelabels>\n')

    def do_savecsv(self, line):
        """
        Save given curves to a CSV file
        """

        if (not line):
            return 0
        try:
            line = line.split()
            filename = line.pop(0)
            line = ' '.join(line)
            if (len(line.split(':')) > 1):
                self.do_savecsv(filename + ' ' + pdvutil.getletterargs(line))
                return 0
            else:

                line = line.split()
                cols = []
                names = []
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        cols.append(cur.x.tolist())
                        cols.append(cur.y.tolist())
                        names.append(cur.name + ' [x]')
                        names.append(cur.name + ' [y]')
                    except RuntimeError as rte:
                        print("I/O error: {}".format(rte))

                with open(filename, "w+") as f:
                    writer = csv.writer(f)
                    writer.writerow(names)
                    for values in zip_longest(*cols):
                        writer.writerow(values)

        except:
            print('error - usage: savecsv <file-name> <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_savecsv(self):
        print('\n   Macro: Save curves to file in comma separated values (csv) format. Assumes all curves have the '
              '\n   same x basis. CSV file generated with number rows equal to number of points in first curve passed.'
              '\n   Usage: savecsv <file-name> <curve-list>\n')

    def do_annot(self, line):
        """
        Display text on the plot at the given plot location
        """

        if (not line):
            return 0
        try:
            argline = line.split()
            xloc = argline[-2]
            yloc = argline[-1]
            argdex = line.find(xloc)
            line = line[:argdex]
            self.usertexts.append([float(xloc), float(yloc), line])
        except:
            print('error - usage: annot <text> <xloc> <yloc>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_annot(self):
        print('\n   Macro: Display text on the plot by axis x and y location\n   Usage: annot <text> <xloc> <yloc>\n')

    def do_listannot(self, line):
        """
        List current annotations
        """

        try:
            for i in range(len(self.usertexts)):
                dex = str(i + 1).rjust(5)
                xloc = '%.4f' % self.usertexts[i][0]
                xloc.ljust(5)
                yloc = '%.4f' % self.usertexts[i][1]
                yloc.ljust(5)
                annot = self.usertexts[i][2]
                annot = pdvutil.truncate(annot.ljust(50), 50)
                print('%s   %s  %s   %s' % (dex, xloc, yloc, annot))
        except:
            print('error - usage: listannot')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_listannot(self):
        print('\n   Macro: List current annotations\n   Usage: listannot\n')

    def do_delannot(self, line):
        """
        Remove the specified annotations
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:  # check for list notation
                self.do_delannot(pdvutil.getnumberargs(line, self.filelist))
                return 0
            else:
                print(line)
                line = line.split()
                rmlist = []
                for i in range(len(line)):
                    rmlist.append(self.usertexts[int(line[i]) - 1])
                for text in rmlist:
                    self.usertexts.remove(text)
        except:
            print('error - usage: delannot <number-list-of-annotations>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_delannot(self):
        print('\n   Procedure: Delete annotations from list\n   Usage: delannot <number-list-of-annotations>\n')

    def do_span(self, line):
        """
        Generates a straight line of slope 1 and y intercept 0 in the specified
            domain with an optional number of points.

        :param line: User Command-Line Input (span <xmin> <xmax> [<# pts>])
        :type line: string
        """
        if not line:
            return 0
        try:
            line = line.split()
            numpts = 100
            if len(line) == 3:
                numpts = int(line.pop(-1))
            xmin = float(line[0])
            xmax = float(line[1])
            c = pydvif.span(xmin, xmax, numpts)
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: span <xmin> <xmax> [<# pts>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_span(self):
        print('\n   Procedure: Generates a straight line of slope 1 and y intercept 0 '
              'in the specified domain with an optional number of points'
              '\n   Usage: span <xmin> <xmax> [<# pts>]\n')

    def do_line(self, line):
        """
        Generate y = mx + b line
        """

        if not line:
            return 0
        try:
            line = line.split()
            numpts = 100
            if len(line) == 5:
                numpts = int(line.pop(-1))
            slope = float(line[0])
            yint = float(line[1])
            xmin = float(line[2])
            xmax = float(line[3])

            c = pydvif.line(slope, yint, xmin, xmax, numpts)
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: line <m> <b> <xmin> <xmax> [<# pts>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_line(self):
        print('\n   Procedure: Generate a line with y = mx + b and an optional number of points'
              '\n   Usage: line <m> <b> <xmin> <xmax> [<# pts>]\n')

    def do_makecurve(self, line):
        """
        Generate curve from given x and y points
        """

        if not line:
            return 0
        try:
            line = line.strip().split(')')
            x = numpy.fromstring(line[0].strip().strip('('), dtype=float, sep=' ')
            y = numpy.fromstring(line[1].strip().strip('('), dtype=float, sep=' ')

            if len(x) != len(y):
                raise RuntimeError('Must have same number of x and y values')

            c = curve.Curve('', 'Curve')
            c.x = x
            c.y = y
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: makecurve (<list of x-values>) (<list of y values>)')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_makecurve(self):
        print('\n   Macro: Generate a curve from two lists of numbers'
              '\n   Usage: makecurve (<list of x-values>) (<list of y values>)\n   Shortcuts: make-curve\n')

    def do_ymin(self, line):
        """
        Filter out points
        """

        try:
            self.__mod_curve(line, 'ymin')
            self.plotedit = True
        except:
            print('error - usage: ymin <curve-list> <limit>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ymin(self):
        print('\n   Procedure: Filter out points in curves whose y-values < limit'
              '\n   Usage: ymin <curve-list> <limit>\n')

    def do_ymax(self, line):
        """
        Filter out points
        """

        try:
            self.__mod_curve(line, 'ymax')
            self.plotedit = True
        except:
            print('error - usage: ymax <curve-list> <limit>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ymax(self):
        print('\n   Procedure: Filter out points in curves whose y-values > limit'
              '\n   Usage: ymax <curve-list> <limit>\n')

    def do_xmin(self, line):
        """
        Filter out points
        """

        try:
            self.__mod_curve(line, 'xmin')
            self.plotedit = True
        except:
            print('error - usage: xmin <curve-list> <limit>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xmin(self):
        print('\n   Procedure: Filter out points in curves whose x-values < limit'
              '\n   Usage: xmin <curve-list> <limit>\n')

    def do_xmax(self, line):
        """
        Filter out points
        """

        try:
            self.__mod_curve(line, 'xmax')
            self.plotedit = True
        except:
            print('error - usage: xmax <curve-list> <limit>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xmax(self):
        print('\n   Procedure: Filter out points in curves whose x-values > limit'
              '\n   Usage: xmax <curve-list> <limit>\n')

    def do_xminmax(self, line):
        """
        Filter out points; this is the only filter points function that returns a new curve
        due to how ULTRA behaved
        """

        if len(line.split(':')) > 1:
            self.do_xminmax(pdvutil.getletterargs(line))
            return
        else:
            try:
                line = line.split()
                xmax = line.pop(-1)
                xmin = line.pop(-1)
                curves = []
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curves.append(self.plotlist[curvidx])
                    except pdvutil.CurveIndexError:
                        pass

                for cur in curves:
                    curve_new = cur.copy()  # new curve
                    curve_new.name = 'Extract ' + cur.name.upper()  # ULTRA naming
                    curve_new.plotname = self.getcurvename()
                    curve_new.color = ''  # PyDV will pick a color on its own
                    self.addtoplot(curve_new)
                    minline = ' '.join(curve_new.plotname) + ' ' + xmin
                    maxline = ' '.join(curve_new.plotname) + ' ' + xmax
                    self.do_xmin(minline)
                    self.do_xmax(maxline)
                    # don't mark the new curve as having been edited by min and max; user doesn't care how we did it.
                    curve_new.edited = False

                self.plotedit = True

            except:
                print('error - usage: xminmax <curve-list> <low-lim> <high-lim>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_xminmax(self):
        print('\n   Procedure: Trim the selcted curves'
              '\n   Usage: xminmax <curve-list> <low-lim> <high-lim>\n   Shortcuts: xmm')

    def do_yminmax(self, line):
        """
        Filter out points
        """

        if len(line.split(':')) > 1:
            self.do_yminmax(pdvutil.getletterargs(line))
            return
        else:
            try:
                line = line.split()
                ymax = line.pop(-1)
                ymin = line.pop(-1)
                good_lines = []
                for i in range(len(line)):
                    try:
                        pdvutil.getCurveIndex(line[i], self.plotlist)
                        good_lines.append(line[i])
                    except pdvutil.CurveIndexError:
                        pass

                for curve_letter in good_lines:
                    minline = ' '.join(curve_letter) + ' ' + ymin
                    maxline = ' '.join(curve_letter) + ' ' + ymax
                    self.do_ymin(minline)
                    self.do_ymax(maxline)

                self.plotedit = True

            except:
                print('error - usage: yminmax <curve-list> <low-lim> <high-lim>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_yminmax(self):
        print('\n   Procedure: Trim the selcted curves'
              '\n   Usage: yminmax <curve-list> <low-lim> <high-lim>'
              '\n   Shortcuts: ymm')

    def do_filter(self, line):
        "Filter out points in the x and y axis"

        if len(line.split(':')) > 1:
            self.do_filter(pdvutil.getletterargs(line))
            return
        else:
            try:
                line = line.split()
                ymax = line.pop(-1)
                ymin = line.pop(-1)
                xmax = line.pop(-1)
                xmin = line.pop(-1)
                good_lines = []
                for i in range(len(line)):
                    try:
                        pdvutil.getCurveIndex(line[i], self.plotlist)
                        good_lines.append(line[i])
                    except pdvutil.CurveIndexError:
                        pass

                for curve_letter in good_lines:
                    x_minline = ' '.join(curve_letter) + ' ' + xmin
                    x_maxline = ' '.join(curve_letter) + ' ' + xmax
                    y_minline = ' '.join(curve_letter) + ' ' + ymin
                    y_maxline = ' '.join(curve_letter) + ' ' + ymax

                    self.do_xmin(x_minline)
                    self.do_xmax(x_maxline)
                    self.do_ymin(y_minline)
                    self.do_ymax(y_maxline)

                self.plotedit = True
            except:
                print('error - usage: filter <curve-list> <x-low-lim> <x-high-lim> <y-low-lim> <y-high-lim>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_filter(self):
        print('\n   Filter out points in the x and y axis'
              '\n   Usage: filter <curve-list> <x-low-lim> <x-high-lim> <y-low-lim> <y-high-lim>')

    def do_derivative(self, line):
        """
        Take derivative of the curve
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:
                self.do_derivative(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    cur = self.plotlist[idx]
                    nc = self.derivative(cur)
                    self.addtoplot(nc)

                self.plotedit = True
        except:
            print('error - usage: der <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_derivative(self):
        print('\n   Procedure: Take derivative of curves\n   Usage: derivative <curve-list>\n   Shortcuts: der\n')

    def do_integrate(self, line):
        """
        Take the integral of the curve
        """

        if not line:
            return 0
        try:
            if len(line.split(':')) > 1:
                self.do_integrate(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                xlow = None
                xhi = None
                subtrahend = 0

                try:
                    xhi = float(line[-1])
                    subtrahend = -1
                except:
                    xhi = None

                try:
                    xlow = float(line[-2])
                    subtrahend = -2
                except:
                    xlow = None

                if (xlow is None and xhi is not None) or (xlow is not None and xhi is None):
                    raise RuntimeError("<low-limit> and <high-limit> must BOTH be specified")

                stop = len(line) + subtrahend
                for i in range(stop):
                    for j in range(len(self.plotlist)):
                        cur = self.plotlist[j]
                        if cur.plotname == line[i].upper():
                            nc = pydvif.integrate(cur, xlow, xhi)[0]
                            self.addtoplot(nc)
                            break

                self.plotedit = True
        except:
            print('error - usage: integrate <curve-list> [<low-limit> <high-limit>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_integrate(self):
        print('\n   Procedure: Integrate curves\n   Usage: integrate <curve-list> [<low-limit> <high-limit>]'
              '\n   Shortcuts: int\n')

    def do_vs(self, line):
        """
        Plot y of one curve against y of another curve
        """

        if not line:
            return 0
        try:
            line = line.split()
            if len(line) != 2:
                return 0

            stuff = '0123456789'
            fidx1 = stuff.find(line[0])
            fidx2 = stuff.find(line[1])

            if fidx1 >= 0 and fidx2 >= 0:
                self.__vs_variant(line[0], line[1])
                return

            idx = pdvutil.getCurveIndex(line[0], self.plotlist)
            c1 = self.plotlist[idx]

            idx = pdvutil.getCurveIndex(line[1], self.plotlist)
            c2 = self.plotlist[idx]

            nc = pydvif.vs(c1, c2)

            self.addtoplot(nc)
            self.plotedit = True
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_vs(self):
        print('\n   Procedure: Plot the range of the first curve against the range of the second curve.'
              '\n   Usage: vs <curve1> <curve2>\n')

    def __vs_variant(self, arg0, arg1):
        """
        This variant support directly plotting curve numbers against each other
        """

        def _extract_curvelist_number(arg):
            if ord(arg[0].upper()) >= ord('A') and ord(arg[0].upper()) <= ord('Z'):  # Look for a.% type stuff
                ifile_target = ord(arg[0].upper()) - ord('A')
                icurve = 0
                ifile = 0
                lastfile = self.curvelist[0].filename
                while icurve < len(self.curvelist) and ifile < ifile_target:
                    icurve += 1
                    if self.curvelist[icurve].filename != lastfile:
                        ifile += 1
                        lastfile = self.curvelist[icurve].filename
                if icurve == len(self.curvelist):
                    print("error: curve index out of bounds: ", arg)
                    return 0
                icurve += int(arg.split('.')[-1]) - 1
                return icurve
            elif int(arg) > 0 and int(arg) <= len(self.curvelist):
                return int(arg) - 1
            else:
                print("error: curve index out of bounds: ", arg)
        icur1, icur2 = _extract_curvelist_number(arg0), _extract_curvelist_number(arg1)
        xc1, yc1 = numpy.array(self.curvelist[icur1].x), numpy.array(self.curvelist[icur1].y)
        xc2, yc2 = numpy.array(self.curvelist[icur2].x), numpy.array(self.curvelist[icur2].y)
        newfilename = ''
        newrecord_id = ''
        if self.curvelist[icur2].filename == self.curvelist[icur1].filename:
            newfilename = self.curvelist[icur2].filename
            if self.curvelist[icur2].record_id == self.curvelist[icur1].record_id:
                newrecord_id = self.curvelist[icur2].record_id
        nc = curve.Curve(newfilename, '%s vs %s' % (arg0, arg1), newrecord_id, self.curvelist[icur2].ylabel,
                         self.curvelist[icur1].ylabel)
        nc.x = yc2
        nc.y = numpy.interp(xc2, xc1, yc1)
        self.addtoplot(nc)
        self.plotedit = True
        return

    def do_errorbar(self, line):
        """
        Define error bars for a curve
        """

        if not line:
            return 0
        line = line.split()

        try:
            idx = pdvutil.getCurveIndex(line[0], self.plotlist)
            scur = self.plotlist[idx]

            # y-error-curve, y+error-curve
            idx = pdvutil.getCurveIndex(line[1], self.plotlist)
            cury1 = self.plotlist[idx]

            idx = pdvutil.getCurveIndex(line[2], self.plotlist)
            cury2 = self.plotlist[idx]

            # x-error-curve, x+error-curve
            curx1 = None
            curx2 = None
            if len(line) >= 5:
                idx = pdvutil.getCurveIndex(line[3], self.plotlist)
                curx1 = self.plotlist[idx]

                idx = pdvutil.getCurveIndex(line[4], self.plotlist)
                curx2 = self.plotlist[idx]

            # point-skip
            mod = 1
            if len(line) == 6:
                mod = line[5]
            elif len(line) == 4:
                mod = line[3]

            pydvif.errorbar(scur, cury1, cury2, curx1, curx2, mod)
            self.plotedit = True
        except:
            # scur.ebar = None
            print('error - usage: errorbar <curve> <y-error-curve> <y+error-curve> [<x-error-curve> <x+error-curve>]'
                  ' [<point-skip>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_errorbar(self):
        print('\n   Procedure: Plot error bars on the given curve. Note: y-error-curve and y+error-curve are curves'
              ' and not scalars.\n   Usage: errorbar <curve> <y-error-curve> <y+error-curve> '
              '[<x-error-curve> <x+error-curve>] [<point-skip>]\n   Shortcuts: error-bar\n')

    def do_errorrange(self, line):
        """
        Define a shaded error range for a curve
        """

        if not line:
            return 0
        try:
            idx = pdvutil.getCurveIndex(line.split()[0], self.plotlist)
            scur = self.plotlist[idx]

            self.do_errorbar(line)
            scur.erange = [scur.ebar[0], scur.ebar[1]]
            scur.ebar = None
            self.plotedit = True
        except:
            # scur.erange = None
            print('error - usage: errorrange <curve> <y-error-curve> <y+error-curve>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_errorrange(self):
        print('\n   Procedure: Plot shaded error region on given curve. Note: y-error-curve and y+error-curve are '
              'curves and not scalars\n   Usage: errorrange <curve> <y-error-curve> <y+error-curve>'
              '\n   Shortcuts: error-range\n')

    def help_marker(self):
        print('\n   Procedure: Set the marker symbol for the curves'
              '\n   Usage: marker <curve-list> <marker-style: + | . | circle | square | diamond> [<marker-size>]'
              '\n   Note: When setting this value through the interface or the curve object directly, '
              'use ONLY matplotlib supported marker types.'
              '\n       Matplotlib marker types are also supported here as well. '
              'See matplotlib documentation on markers for further information.'
              )

    def do_marker(self, line):
        """
        Set the marker for curves
        """
        self.do_linemarker(line)

    def do_linemarker(self, line):
        """
        Set the marker symbol for the curves
        """

        if not line:
            return 0
        try:
            markersize = None

            if len(line.split(':')) > 1:
                self.do_linemarker(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                ultra_markers = {'circle': 'o', 'square': 's', 'diamond': 'd'}
                try:
                    try:
                        markersize = float(line[-1])
                        marker = line[-2]
                    except:
                        markersize = None
                        marker = line[-1]
                    if marker in ultra_markers:
                        marker = ultra_markers[marker]
                except:
                    self.help_linemarker()
                    if self.debug:
                        traceback.print_exc(file=sys.stdout)

                for i in range(len(line)):
                    for j in range(len(self.plotlist)):
                        cur = self.plotlist[j]
                        if cur.plotname == line[i].upper():
                            cur.markerstyle = marker
                            if (markersize):
                                cur.markersize = markersize
                            break
            self.plotedit = True
        except:
            self.help_linemarker()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_linemarker(self):
        print('\n   Procedure: Set the marker symbol for the curves'
              '\n   Usage: linemarker <curve-list> <marker-style: + | . | circle | square | diamond> [<marker-size>]'
              '\n   Note: When setting this value through the interface or the curve object directly, '
              'use ONLY matplotlib supported marker types.'
              '\n       Matplotlib marker types are also supported here as well. '
              'See matplotlib documentation on markers for further information.'
              )

    def do_smooth(self, line):
        """
        Smooth the curve to given degree
        """

        if not line:
            return 0
        try:
            line = line.split()

            try:
                factor = int(line[-1])
                line.pop(-1)
            except:
                factor = 1

            line = ' '.join(line)

            if len(line.split(':')) > 1:
                self.do_smooth(pdvutil.getletterargs(line) + str(factor))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        pydvif.smooth(cur, factor)
                        cur.edited = True
                    except pdvutil.CurveIndexError:
                        pass

            self.plotedit = True

        except:
            print('error - usage: smooth <curve-list> [<smooth-factor>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_smooth(self):
        print('\n   Procedure: Smooth the curve to the given degree.'
              '\n   Usage: smooth <curve-list> [<smooth-factor>]\n')

    def do_fft(self, line):
        """
        Make a new curve - the Fourier Transform of y-values the given curves
        """

        if not line:
            return 0

        if len(line.split(':')) > 1:
            self.do_fft(pdvutil.getletterargs(line))
            return 0
        else:
            try:
                line = line.split()
                for item in line:
                    idx = pdvutil.getCurveIndex(item, self.plotlist)
                    c1 = self.plotlist[idx]
                    nc1, nc2 = pydvif.fft(c1, norm="ortho")
                    self.addtoplot(nc1)
                    self.addtoplot(nc2)

                self.plotedit = True
            except:
                print('error - usage: fft <curve-list>')
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_fft(self):
        print('\n   Procedure: Compute the one-dimensional discrete Fourier Transform of the y values of the curves.'
              '\n              Return real and imaginary parts.'
              '\n   Usage: fft <curve-list>\n')

    def do_appendcurves(self, line):
        """
        Merge list of curves
        """

        if not line:
            return 0

        if len(line.split(':')) > 1:
            self.do_appendcurves(pdvutil.getletterargs(line))
            return 0
        else:
            try:
                line = line.split()

                if len(line) < 2:
                    return

                curves = list()
                for i in range(len(self.plotlist)):
                    for j in range(len(line)):
                        if self.plotlist[i].plotname == line[j].upper():
                            curves.append(self.plotlist[i])
                            break

                nc = pydvif.appendcurves(curves)

                if nc is not None:
                    self.addtoplot(nc)
                    self.plotedit = True
            except RuntimeError as rte:
                print('error: %s' % rte)
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
            except:
                self.help_appendcurves()
                if self.debug:
                    traceback.print_exc(file=sys.stdout)

    def help_appendcurves(self):
        print('\n   Procedure: Merge a list of curves over the union of their domains. Where domains overlap, take'
              '\n              the average of the curve\'s y-values.'
              '\n   Usage: appendcurves <curve-list>\n')

    def do_alpha(self, line):
        if not line:
            return 0

        try:
            line = line.split()
            linelen = len(line)
            if linelen == 3 or linelen == 4:
                for i in range(len(self.plotlist)):
                    if self.plotlist[i].plotname == line[0].upper():
                        c1 = self.plotlist[i]
                        break
                for i in range(len(self.plotlist)):
                    if self.plotlist[i].plotname == line[1].upper():
                        c2 = self.plotlist[i]
                        break
                for i in range(len(self.plotlist)):
                    if self.plotlist[i].plotname == line[2].upper():
                        c3 = self.plotlist[i]
                        break

                if linelen == 4:
                    npts = int(line[3])
                    nc = pydvif.alpha(c1, c2, c3, npts)
                else:
                    nc = pydvif.alpha(c1, c2, c3)

                self.addtoplot(nc)
                self.plotedit = True
            else:
                raise RuntimeError("Wrong number of arguments, expecting 3 or 4 but received %d." % len(line))
        except RuntimeError as rte:
            print('error: %s' % rte)
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            self.help_alpha()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_alpha(self):
        print('\n   Procedure: Find the alpha'
              '\n   Usage: alpha <calculated-a> <calculated-i> <response> [# points]')

    def do_convolve(self, line):
        print(f"convol {line}")
        print("Use convolc for (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t))")
        print("Use convolb for (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) / Int(-inf, inf, dt*h(t))")

    def help_convolve(self):
        print("Use convolc for (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t))")
        print("Use convolb for (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) / Int(-inf, inf, dt*h(t))")

    def do_convolveb(self, line):
        """
        Make a new curve - slower convolution which doesn't use FFT
        """

        if not line:
            return 0
        try:
            line = line.split()
            for i in range(len(self.plotlist)):
                if self.plotlist[i].plotname == line[0].upper():
                    c1 = self.plotlist[i]
                    break
            for i in range(len(self.plotlist)):
                if self.plotlist[i].plotname == line[1].upper():
                    c2 = self.plotlist[i]
                    break

            if len(line) == 2:
                nc = pydvif.convolveb(c1, c2, debug=self.debug)
            elif len(line) == 3:
                npts = int(line[2])
                nc = pydvif.convolveb(c1, c2, npts, debug=self.debug)
            elif len(line) == 4:
                npts = int(line[2])
                npts_interp = int(line[3])
                nc = pydvif.convolveb(c1, c2, npts, npts_interp, debug=self.debug)
            else:
                raise RuntimeError("Wrong number of arguments, expecting 2 or 3 but received %d." % len(line))

            self.addtoplot(nc)
            self.plotedit = True
        except RuntimeError as rte:
            print('error: %s' % rte)
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            self.help_convolveb()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_convolveb(self):
        print('\n   Procedure: Computes the convolution of the two given curves'
              '\n              (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) /'
              '\n                         Int(-inf, inf, dt*h(t))'
              '\n   This slower method uses direct integration and minimal interpolations.'
              '\n   Usage: convolveb <curve1> <curve2> [# points] [# points interpolation]\n   Shortcuts: convolb')

    def do_convolvec(self, line):
        """
        Make a new curve - slower convolution which doesn't use FFT
        """

        if not line:
            return 0
        try:
            line = line.split()
            for i in range(len(self.plotlist)):
                if self.plotlist[i].plotname == line[0].upper():
                    c1 = self.plotlist[i]
                    break
            for i in range(len(self.plotlist)):
                if self.plotlist[i].plotname == line[1].upper():
                    c2 = self.plotlist[i]
                    break

            if len(line) == 2:
                nc = pydvif.convolvec(c1, c2, debug=self.debug)
            elif len(line) == 3:
                npts = int(line[2])
                nc = pydvif.convolvec(c1, c2, npts, debug=self.debug)
            elif len(line) == 4:
                npts = int(line[2])
                npts_interp = int(line[3])
                nc = pydvif.convolvec(c1, c2, npts, npts_interp, debug=self.debug)
            else:
                raise RuntimeError("Wrong number of arguments, expecting 2 or 3 but received %d." % len(line))

            self.addtoplot(nc)
            self.plotedit = True
        except RuntimeError as rte:
            print('error: %s' % rte)
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            self.help_convolvec()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_convolvec(self):
        print('\n   Procedure: Computes the convolution of the two given curves'
              '\n              (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t))'
              '\n   This slower method uses direct integration and minimal interpolations.'
              '\n   Usage: convolvec <curve1> <curve2> [# points] [# points interpolation]\n   Shortcuts: convolc')

    def do_diffMeasure(self, line):
        """
        Make two new curves - the diff-measure of two given curves
        """

        if not line:
            return 0
        try:
            try:
                tolerance = float(line.split()[-1])
                line = line.split()
                line.pop(-1)
                line = ' '.join(line)
            except:
                tolerance = 1e-8

            line = line.split()
            idx = pdvutil.getCurveIndex(line[0], self.plotlist)
            c1 = self.plotlist[idx]

            idx = pdvutil.getCurveIndex(line[1], self.plotlist)
            c2 = self.plotlist[idx]

            cdiff, cint = pydvif.diffMeasure(c1, c2, tolerance)
            self.addtoplot(cdiff)
            self.addtoplot(cint)
            self.plotedit = True
            print('Difference measure for curves ' + c1.plotname + ' and ' + c2.plotname + ': ' + str(cint.y[-1]))
        except:
            print('error: requires exactly two curves as arguments')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_diffMeasure(self):
        print('\n   Procedure: Compare two curves. For the given curves a fractional difference measure and its '
              'average is computed\n   Usage: diffMeasure <curve1> <curve2> [tolerance]\n')

    def do_correl(self, line):
        """
        Compute the correlation function of the two curves
        """

        if not line:
            return 0

        try:
            line = line.split()

            if len(line) != 2:
                raise RuntimeError("Wrong number of arguments, expecting 2 but received %d." % len(line))

            idx = pdvutil.getCurveIndex(line[0], self.plotlist)
            c1 = self.plotlist[idx]

            idx = pdvutil.getCurveIndex(line[1], self.plotlist)
            c2 = self.plotlist[idx]

            nc = pydvif.correlate(c1, c2, 'same')
            self.addtoplot(nc)
            self.plotedit = True
        except RuntimeError as rte:
            print('error: %s' % rte)
            self.help_correl()
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            self.help_correl()
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_correl(self):
        print('\n   Procedure: Compute the correlation function of the two curves.'
              '\n   Usage: correl <curve1> <curve2>\n')

    def do_theta(self, line):
        """
        Generate a unit step distribution
        """

        try:
            line = line.split()
            xmin = float(line[0])
            x0 = float(line[1])
            xmax = float(line[2])
            if len(line) == 4:
                numpts = float(line[3])
            else:
                numpts = 100

            c = pydvif.theta(xmin, x0, xmax, numpts)
            self.addtoplot(c)
            self.plotedit = True

        except:
            print('Usage: xmin x0 xmax [# points]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_theta(self):
        print('\n   Procedure: Generate a unit step distribution.'
              '\n   Usage: xmin x0 xmax [# points]\n')

    def do_normalize(self, line):
        """
        Normalize a curve
        """

        try:

            idx = pdvutil.getCurveIndex(line, self.plotlist)
            c1 = self.plotlist[idx]
            c = pydvif.normalize(c1)
            self.addtoplot(c)
            self.plotedit = True

        except:
            print('Usage: normalize <curve>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_normalize(self):
        print('\n   Procedure: Normalize a curve.'
              '\n   Usage: normalize <curve>\n')

    def do_hypot(self, line):
        """
        Calculate harmonic average of two curves, sqrt(a^2+b^2)
        """

        try:
            line = line.split()
            idx = pdvutil.getCurveIndex(line[0], self.plotlist)
            c1 = self.plotlist[idx]
            idx = pdvutil.getCurveIndex(line[1], self.plotlist)
            c2 = self.plotlist[idx]
            c = pydvif.hypot(c1, c2)
            self.addtoplot(c)
            self.plotedit = True

        except:
            print('Usage: hypot <curve1> <curve2>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_hypot(self):
        print('\n   Procedure: Calculate harmonic average of two curves, sqrt(a^2+b^2).'
              '\n   Usage: hypot <curve1> <curve2>\n')

    def do_delta(self, line):
        """
        Procedure: Generate a Dirac delta distribution such that
                   Int(xmin, xmax, dt*delta(t - x0)) = 1
        """

        try:
            line = line.split()
            xmn = float(line[0])
            x0 = float(line[1])
            xmx = float(line[2])
            if len(line) > 3:
                npts = float(line[3])
            else:
                npts = 100
            c = pydvif.delta(xmn, x0, xmx, npts)
            self.addtoplot(c)
            self.plotedit = True

        except:
            print('Usage: delta <xmin> <x0> <xmax> [<# points>]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_delta(self):
        print('\n   Procedure: Generate a Dirac delta distribution such that.'
              '\n   Int(xmin, xmax, dt*delta(t - x0)) = 1'
              '\n   Usage: delta <xmin> <x0> <xmax> [<# points>]\n')

    def do_bkgcolor(self, line):
        """
        Changes background color of the plot, window, or both
        """

        try:
            line = line.split()
            color = line[-1]

            if color.lower() == 'reset':
                color = None
                component = 'reset'
            else:
                if not mclr.is_color_like(color):
                    print('error: invalid color ' + color)
                    self.redraw = False
                    return 0

                if len(line) > 1:
                    component = line[0].lower()
                    if component != 'plot' and component != 'window' and component != 'reset':
                        raise ValueError('\'%s\' is an invalid component name' % component)
                else:
                    component = 'all'

            if component == 'reset':
                self.figcolor = self.plotter.figcolor
                self.plotcolor = '#dddddd'
            else:
                if component == 'all' or component == 'window':
                    self.figcolor = color

                if component == 'all' or component == 'plot':
                    self.plotcolor = color

            self.plotedit = True
        except ValueError as ve:
            print('\nerror - %s' % ve.message)
            print('usage: bkgcolor <[plot | window] color-name | reset>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            print('usage: bkgcolor <[plot | window] color-name | reset>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_bkgcolor(self):
        print("\n    Procedure: Change the background color of the given component. If no component name is specified,"
              " then both components will be given the same color. See (https://matplotlib.org/users/colors.html) for "
              "all the different ways to specify color-name. \'reset\' will return the plot and window colors to their"
              " original values.\n\n    Usage: bkgcolor <[plot | window] color-name | reset>")

    def do_fontcolor(self, line):
        """
        Edits the font color for various text components
        """

        try:
            line = line.split()
            color = line[-1]
            if not mclr.is_color_like(color):
                print('error: invalid color ' + color)
                self.redraw = False
                return 0

            if len(line) > 1:
                com = line[0]
                if (com != 'xlabel' and com != 'ylabel' and com != 'xaxis' and com != 'yaxis'
                        and com != 'title' and com != 'legend'):  # noqaw503
                    raise ValueError('\'%s\' is an invalid component name' % com)
            else:
                com = 'all'

            if com == 'all' or com == 'xlabel':
                self.xlabelcolor = color

            if com == 'all' or com == 'ylabel':
                self.ylabelcolor = color

            if com == 'all' or com == 'xaxis':
                self.xtickcolor = color

            if com == 'all' or com == 'yaxis':
                self.ytickcolor = color

            if com == 'all' or com == 'title':
                self.titlecolor = color

            if com == 'all' or com == 'legend':
                self.keycolor = color

            self.plotedit = True
        except ValueError as ve:
            print('\nerror - %s' % ve.message)
            print('usage: fontcolor [<component: xlabel | ylabel | xaxis | yaxis '
                  '| legend | title>] <color-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        except:
            print('error - usage: fontcolor [<component: xlabel | ylabel | xaxis | yaxis '
                  '| legend | title>] <color-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_fontcolor(self):
        print('\n   Procedure: Change the font color of given component. '
              'If no component is given the font color is changed for all components.'
              '\n   Usage: fontcolor [<component: xlabel | ylabel | xaxis | yaxis | legend | title>] <color-name>\n')

    def do_fontsize(self, line):
        """
        Edits the font size for various text components
        """

        try:
            line = line.split()
            size = line[-1]
            if (size != 'default' and size != 'de' and size != 'x-small' and size != 'small'
                    and size != 'medium' and size != 'large' and size != 'x-large'):  # noqaw503
                size = float(size)
                if (size > 40):
                    size = 40
            if (len(line) > 1):
                com = line[0]
            else:
                com = 'all'
            if (com == 'all' or com == 'title'):
                if (size == 'default' or size == 'de'):
                    self.titlefont = 'large'
                else:
                    self.titlefont = size
            if (com == 'all' or com == 'xlabel'):
                if (size == 'default' or size == 'de'):
                    self.xlabelfont = 'medium'
                else:
                    self.xlabelfont = size
            if (com == 'all' or com == 'ylabel'):
                if (size == 'default' or size == 'de'):
                    self.ylabelfont = 'medium'
                else:
                    self.ylabelfont = size
            if (com == 'all' or com == 'legend'):
                if (size == 'default' or size == 'de'):
                    self.keyfont = 'small'
                else:
                    self.keyfont = size
            if (com == 'all' or com == 'tick'):
                if (size == 'default' or size == 'de'):
                    self.axistickfont = 'medium'
                else:
                    self.axistickfont = size
            if (com == 'all' or com == 'curve'):
                if (size == 'default' or size == 'de'):
                    self.curvelabelfont = 'medium'
                else:
                    self.curvelabelfont = size
            if (com == 'all' or com == 'annotation'):
                if (size == 'default' or size == 'de'):
                    self.annotationfont = 'medium'
                else:
                    self.annotationfont = size
        except:
            print('error - usage: fontsize [<component: title | xlabel | ylabel | legend | tick | curve | annotation>] '
                  '<numerical-size | small | medium | large | default>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_fontsize(self):
        print('\n   Procedure: Change the font size of given component, or overall scaling factor'
              '\n   Usage: fontsize [<component: title | xlabel | ylabel | legend '
              '| tick | curve | annotation>] <numerical-size | small | medium | large | default>\n')

    def do_gaussian(self, line):
        """
        Generate a gaussian function
        """

        if not line:
            return 0
        try:
            num = 100   # num of points
            nsd = 3     # num of half-widths

            line = line.split()

            if len(line) < 3:
                raise RuntimeError("Wrong number of arguments")

            if len(line) == 4:
                num = int(line[-1])
            elif len(line) == 5:
                nsd = float(line[-1])
                num = int(line[-2])

            amp = float(line[0])
            wid = float(line[1])
            center = float(line[2])

            c = pydvif.gaussian(amp, wid, center, num, nsd)
            self.addtoplot(c)
            self.plotedit = True
        except:
            print('error - usage: gaussian <amplitude> <width> <center> [<# points> [<# half-widths>]]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_gaussian(self):
        print('\n   Procedure: Generate a gaussian function.'
              '\n   Usage: gaussian <amplitude> <width> <center> [<# points> [<# half-widths>]] \n')

    def do_geometry(self, line):
        """
        Change the window size and location
        """

        try:
            line = line.split()
            if len(line) != 4:
                raise RuntimeError("Wrong number of arguments, expecting 4 but received %d." % len(line))

            self.geometry = int(line[0]), int(line[1]), int(line[2]), int(line[3])
            self.plotter.updatePlotGeometry(self.geometry)
        except:
            self.redraw = False
            print('error - usage: geometry <xsize> <ysize> <xlocation> <ylocation>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_geometry(self):
        print('\n   Procedure: Change the window size and location in pixels'
              '\n   Usage: geometry <xsize> <ysize> <xlocation> <ylocation>'
              '\n   Shortcuts: geom\n')

    def do_plotlayout(self, line):
        """
        Adjust the plot layout parameters
        """

        try:
            line = line.split()
            paramcnt = len(line)

            if paramcnt == 4:
                plt.subplots_adjust(left=float(line[0]),
                                    bottom=float(line[3]),
                                    right=float(line[1]),
                                    top=float(line[2]))
            elif paramcnt == 1 and line[0].lower() == "de":
                defaultPlotLayout = self.plotter.defaultPlotLayout

                if defaultPlotLayout is not None:
                    plt.subplots_adjust(left=defaultPlotLayout["left"],
                                        bottom=defaultPlotLayout["bottom"],
                                        right=defaultPlotLayout["right"],
                                        top=defaultPlotLayout["top"],
                                        wspace=defaultPlotLayout["wspace"],
                                        hspace=defaultPlotLayout["hspace"])
            elif paramcnt == 0:
                paramlist = list()
                paramlist.append("left: {}".format(self.plotter.fig.subplotpars.left))
                paramlist.append("right: {}".format(self.plotter.fig.subplotpars.right))
                paramlist.append("top: {}".format(self.plotter.fig.subplotpars.top))
                paramlist.append("bottom: {}".format(self.plotter.fig.subplotpars.bottom))
                print('\n')
                self.print_topics('Plot Layout (Borders):', paramlist, 15, 40)
            else:
                raise ValueError("Unknown argument(s)")
        except:
            self.redraw = False
            print("error - usage: plotlayout [<left> <right> <top> <bottom> || de]")
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_plotlayout(self):
        print("\n   Procedure: Adjust the plot layout parameters. Where 'left' is the position of the left edge of the"
              "\n              plot as a fraction of the figure width, 'right' is the position of the right edge of the"
              "\n              plot, as a fraction of the figure width, 'top' is the position of the top edge of the "
              "\n              plot, as a fraction of the figure height and 'bottom' is the position of the bottom edge"
              "\n              of the plot, as a fraction of the figure height. Alternatively, 'de' will revert to the"
              "\n              default plot layout values. "
              "\n              If no arguments are given, the plot's current layout settings will be displayed."
              "\n   Usage: plotlayout [<left> <right> <top> <bottom> || de]"
              "\n   Shortcut: pl\n")

    def do_reid(self, line):
        """
        Re-id command re-identifies all the curves into continuous alphabetical order
        """

        try:
            for i in range(len(self.plotlist)):
                c = self.plotlist[i]  # get i'th curve object
                if (i < 26):
                    c.plotname = chr(ord('A') + i)  # label by alphabet
                else:
                    c.plotname = '@' + str(i + 1)  # after first 26 curves, go to @N labels
        except:
            print('error - usage: re-id or reid')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_reid(self):
        print('\n   Procedure: relabel all the curves in order.'
              '\n   Usage: re-id\n')

    def do_label(self, line):
        """
        Change label for a curve
        """

        try:
            if len(line.split(':')) > 1:
                self.do_label(pdvutil.getletterargs(line))
                return 0
            else:
                line_labels = line.split('#')[1:]  # First entry will be curves

                if line_labels:  # Multiple curves and labels
                    curves = line.split('#')[0].split()
                else:  # single curve and label
                    curves = line.split()[0]
                    line_labels = [' '.join(line.split()[1:])]

                for i in range(len(curves)):
                    idx = pdvutil.getCurveIndex(curves[i], self.plotlist)
                    cur = self.plotlist[idx]
                    cur.name = line_labels[i]

                self.plotedit = True
        except:
            print('error - usage: label <curve> <new-label>\n')
            print('For multiple curves, each label must start with #')
            print('label a:c #mynewlabel #my other label #my thirdlabel')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_label(self):
        print('\n   Procedure: Change the key and list label for a curve\n   Usage: label <curve> <new-label>\n')
        print('   For multiple curves, each label must start with #')
        print('   label a:c #mynewlabel #my other label #my thirdlabel')

    def do_labelrecordids(self, line):
        """
        Change label for a curve to the recordid
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showrecordidinlegend = False
            elif line == '1' or line.upper() == 'ON':
                self.showrecordidinlegend = True
            else:
                raise RuntimeError('invalid input: requires on or off as argument')
        except:
            print('error - usage: labelrecordids <on | off>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_labelrecordids(self):
        print('\n   Variable: Add curve recordid to the legend label if "on", otherwise hide curve recordid if "off".'
              '\n   Usage: labelrecordids <on | off>')

    def do_labelfilenames(self, line):
        """
        Change label for a curve to the filename
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showfilenameinlegend = False
            elif line == '1' or line.upper() == 'ON':
                self.showfilenameinlegend = True
            else:
                raise RuntimeError('invalid input: requires on or off as argument')
        except:
            print('error - usage: labelfilenames <on | off>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_labelfilenames(self):
        print('\n   Variable: Add curve filename to the legend label if "on", otherwise hide curve filename if "off".'
              '\n   Usage: labelfilenames <on | off>\n')

    def do_labelcurve(self, line):
        """
        Change label for a curve to the curve letter
        """

        try:
            line = line.strip()
            if line == '0' or line.upper() == 'OFF':
                self.showcurveinlegend = False
            elif line == '1' or line.upper() == 'ON':
                self.showcurveinlegend = True
            else:
                raise RuntimeError('invalid input: requires on or off as argument')
        except:
            print('error - usage: labelcurve <on | off>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_labelcurve(self):
        print('\n   Variable: Add curve letter to the legend label if "on", otherwise hide curve letter if "off".'
              '\n   Usage: labelcurve <on | off>')

    def do_run(self, line):
        """
        Run a list of commands from a file
        """

        try:
            fname = line.strip()
            if fname[0] == '~':
                fname = os.getenv('HOME') + fname[1:]
            f = open(fname, 'r')
            for fline in f:
                try:
                    if len(fline.strip()) == 0:
                        continue  # skip blank lines
                    if fline.strip()[0] == '#':
                        continue  # skip comment lines
                    fline = self.precmd(fline.strip())
                    args = fline.split()
                    cmd = args.pop(0)
                    if cmd == 'image':
                        self.updateplot
                    args = ' '.join(args)
                    send = 'self.do_' + cmd + '(\'' + args + '\')'
                    result = eval(send)  # noqa f841
                except SystemExit:
                    self.do_quit(line)
                except:
                    print('invalid command: ' + fline.strip())
                    if self.debug:
                        traceback.print_exc(file=sys.stdout)
            self.plotedit = True
            self.updateplot
        except SystemExit:
            self.do_quit(line)
        except:
            print('error - usage: run <filename>')
            if (self.debug):
                traceback.print_exc(file=sys.stdout)

    def help_run(self):
        print('\n   Procedure: Execute a list of commands from a file\n   Usage: run <filename>\n')

    def do_movefront(self, line):
        """
        Move given curves to the front of the plot
        """

        try:
            if len(line.split(':')) > 1:
                self.do_movefront(pdvutil.getletterargs(line))
                return 0
            else:
                highest = 0
                for c in self.plotlist:
                    if c.plotprecedence > highest:
                        highest = c.plotprecedence

                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        cur = self.plotlist[curvidx]
                        cur.plotprecedence = highest + 1
                    except pdvutil.CurveIndexError:
                        pass

                self.plotedit = True
        except:
            print('error - usage: movefront <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_movefront(self):
        print('\n   Procedure: Move the given curves so they are plotted on top'
              '\n   Usage: movefront <curve-list>\n')

    def do_custom(self, line):
        """
        Read in a file of custom functions
        """

        try:
            fname = line.strip()
            try:
                if fname[0] == '~':
                    fname = os.getenv('HOME') + fname[1:]
                f = open(fname, 'r')
                funcfile = f.read()
                funcs = re.findall(r'def do_\w+', funcfile)
                funcs = [func.replace('def ', '') for func in funcs]
                exec(funcfile)
                # print locals()

                for func in funcs:
                    exec('self.' + func + ' = types.MethodType(' + func + ', self)')
            except:
                print("error - invalid file: {}".format(fname))
                if self.debug:
                    traceback.print_exc(file=sys.stdout)
        except:
            print('error - usage: custom <file-name>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_custom(self):
        print("\n   Procedure: Load a file of custom functions to extend PDV. "
              "\n              Functions must be of the form 'def do_commandname(self, line): ...'"
              "\n   Usage: custom <file-name>\n")

    def do_alias(self, line):
        """
        Allow user defined command synonyms
        """

        try:
            cmd = line.split()[0]
            alias = line.split()[1]

            function = 'def do_' + alias + '(self, line): self.do_' + cmd + '(line)'
            exec(function)
            exec('self.do_' + alias + ' = types.MethodType(do_' + alias + ', self)')
        except:
            print('error - usage: alias <command> <alias>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.redraw = False

    def help_alias(self):
        print('\n   Procedure: Define a synonym for an existing command\n   Usage: alias <command> <alias>\n')

    def do_copy(self, line):
        """
        Plot copies of the given curves
        """

        try:
            if len(line.split(':')) > 1:
                self.do_copy(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()
                for i in range(len(line)):
                    plotidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    cur = self.plotlist[plotidx]
                    curout = cur.copy()
                    curout.plotname = ''
                    curout.color = ''
                    self.addtoplot(curout)

                self.plotedit = True
        except:
            print('error - usage: copy <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_copy(self):
        print('\n   Procedure: Copy and plot the given curves\n   Usage: copy <curve-list>\n')

    def do_makeextensive(self, line):
        """
        Set the y-values such that y[i] *= (x[i+1] - x[i])
        """

        try:
            if len(line.split(':')) > 1:
                self.do_makeextensive(pdvutil.getletterargs(line))
                return 0
            else:
                curves = list()
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curves.append(self.plotlist[curvidx])
                    except pdvutil.CurveIndexError:
                        pass

                if len(curves) > 0:
                    pydvif.makeextensive(curves)
                else:
                    raise RuntimeError('Need to specify a valid curve or curves')

        except:
            print('error - usage: makeextensive <curve-list>\n  Shortcut: mkext')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_makeextensive(self):
        print('\n   Procedure: Set the y-values such that y[i] *= (x[i+1] - x[i]) '
              '\n   Usage: makeextensive <curve-list>\n   Shortcut: mkext')

    def do_makeintensive(self, line):
        """
        Set the y-values such that y[i] /= (x[i+1] - x[i])
        """

        try:
            if len(line.split(':')) > 1:
                self.do_makeintensive(pdvutil.getletterargs(line))
                return 0
            else:
                curves = list()
                line = line.split()
                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curves.append(self.plotlist[curvidx])
                    except pdvutil.CurveIndexError:
                        pass

                if len(curves) > 0:
                    pydvif.makeintensive(curves)
                else:
                    raise RuntimeError('Need to specify a valid curve or curves')

        except:
            print('error - usage: makeintensive <curve-list>\n  Shortcut: mkint')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_makeintensive(self):
        print('\n   Procedure: Set the y-values such that y[i] /= (x[i+1] - x[i]) '
              '\n   Usage: makeintensive <curve-list>\n   Shortcut: mkint')

    def do_dupx(self, line):
        """
        Duplicate the x-values such that y = x for each of the given curves
        """

        try:
            if len(line.split(':')) > 1:
                self.do_dupx(pdvutil.getletterargs(line))
                return 0
            else:
                curves = list()
                line = line.split()

                for i in range(len(line)):
                    try:
                        plotidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curves.append(self.plotlist[plotidx])
                    except pdvutil.CurveIndexError:
                        pass

                if len(curves) > 0:
                    pydvif.dupx(curves)

        except:
            print('error - usage: dupx <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_dupx(self):
        print('\n   Procedure: Duplicate the x-values such that y = x for each of the given curves'
              '\n   Usage: dupx <curve-list>\n')

    def do_xindex(self, line):
        """
        Create curves with y-values vs. integer index values
        """

        try:
            if len(line.split(':')) > 1:
                self.do_xindex(pdvutil.getletterargs(line))
                return 0
            else:
                curves = list()
                line = line.split()

                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curves.append(self.plotlist[curvidx])
                    except pdvutil.CurveIndexError:
                        pass

                if len(curves) > 0:
                    pydvif.xindex(curves)
                else:
                    raise RuntimeError('Need to specify a valid curve or curves')

        except:
            print('error - usage: xindex <curve-list>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xindex(self):
        print('\n   Procedure: Create curves with y-values vs. integer index values'
              '\n   Usage: xindex <curve-list>\n')

    def do_ticks(self, line):
        """
        Set the number of ticks on the axes
        """

        try:
            if line.strip() == 'de':
                self.xticks = 'de'
                self.yticks = 'de'
            else:
                numticks = int(line)

                if numticks > 50:
                    numticks = 50
                elif numticks < 2:
                    numticks = 2

                self.xticks = numticks
                self.yticks = numticks
        except:
            print('error - usage: ticks <quantity> or ticks de')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ticks(self):
        print('\n   Variable: Set the maximum number of major ticks on the x- and y-axes'
              '\n   Usage: ticks <quantity> or'
              '\n   Usage: ticks de\n')

    def do_yticks(self, line):
        """
        Set the yticks explicitly
        """

        try:
            if line.strip() == 'de':
                self.yticks = 'de'
            elif isinstance(eval(line.strip()), Number):
                self.yticks = eval(line.strip())
            elif isinstance(eval(line.strip()), tuple):
                if isinstance(eval(line.strip())[0], Number):
                    self.yticks = eval(line.strip())
                else:
                    locs, labels = eval(line)
                    self.yticks = (locs, labels)
        except:
            print('error - usage: yticks <de | integer | (list of locations) | (list of locations), (list of labels)>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_yticks(self):
        print('\n   Variable: Set the locations of major ticks on the y axis'
              '\n   Usage: yticks < de | integer | (list of locations) | (list of locations), (list of labels)>')

    def do_xticks(self, line):
        """
        Set the xticks explicitly
        """

        try:
            if line.strip() == 'de':
                self.xticks = 'de'
            elif isinstance(eval(line.strip()), Number):
                self.xticks = eval(line.strip())
            elif isinstance(eval(line.strip()), tuple):
                if isinstance(eval(line.strip())[0], Number):
                    self.xticks = eval(line.strip())
                else:
                    locs, labels = eval(line)
                    self.xticks = (locs, labels)
        except:
            print('error - usage: xticks < de | integer | (list of locations) | (list of locations), (list of labels)>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xticks(self):
        print('\n   Variable: Set the locations or the maximum number of major ticks on the x axis (de = default).'
              '\n   Usage: xticks <de | integer | (list of locations) | (list of locations), (list of labels)>')

    def do_xtickcolor(self, line):
        """
        Set the color for the x ticks
        """

        try:
            line = line.split()

            if len(line) == 1:  # which = 'major'
                if line[0] == 'de':
                    self.xmajortickcolor = 'black'
                else:
                    self.xmajortickcolor = line[0]
            elif len(line) == 2:  # which = 'major|minor|both'
                if line[1].upper() == 'MAJOR':
                    if line[0] == 'de':
                        self.xmajortickcolor = 'black'
                    else:
                        self.xmajortickcolor = line[0]
                elif line[1].upper() == 'MINOR':
                    if line[0] == 'de':
                        self.xminortickcolor = 'black'
                    else:
                        self.xminortickcolor = line[0]
                elif line[1].upper() == 'BOTH':
                    if line[0] == 'de':
                        self.xmajortickcolor = 'black'
                        self.xminortickcolor = 'black'
                    else:
                        self.xmajortickcolor = line[0]
                        self.xminortickcolor = line[0]
                else:
                    raise ValueError("Unknown type of axis: %s" % line[1])
            else:
                raise RuntimeError('Too many arguments, expecting 1 or 2 but received %d' % len(line))
        except:
            print('error - usage: xtickcolor color [which: major | minor | both]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xtickcolor(self):
        print('\n   Variable: Set the color of the ticks on the x axis. Default is apply to major ticks only.'
              '\n   Usage: xtickcolor color [which: major | minor | both]\n'
              '\n   Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set'
              '\n   of hexadecimal red-green-blue values (RRGGBB).'
              '\n   The entire set of HTML-standard color names is available.'
              '\n   Try "showcolormap" to see the available named colors!\n')

    def do_ytickcolor(self, line):
        """
        Set the color for the ticks on the y axis
        """

        try:
            line = line.split()

            if len(line) == 1:  # which = 'major'
                if line[0] == 'de':
                    self.ymajortickcolor = 'black'
                else:
                    self.ymajortickcolor = line[0]
            elif len(line) == 2:  # which = 'major|minor|both'
                if line[1].upper() == 'MAJOR':
                    if line[0] == 'de':
                        self.ymajortickcolor = 'black'
                    else:
                        self.ymajortickcolor = line[0]
                elif line[1].upper() == 'MINOR':
                    if line[0] == 'de':
                        self.yminortickcolor = 'black'
                    else:
                        self.yminortickcolor = line[0]
                elif line[1].upper() == 'BOTH':
                    if line[0] == 'de':
                        self.ymajortickcolor = 'black'
                        self.yminortickcolor = 'black'
                    else:
                        self.ymajortickcolor = line[0]
                        self.yminortickcolor = line[0]
                else:
                    raise ValueError("Unknown type of axis: %s" % line[1])
            else:
                raise RuntimeError('Too many arguments, expecting 1 or 2 but received %d' % len(line))
        except:
            print('error - usage: ytickcolor color [which: major | minor | both]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ytickcolor(self):
        print('\n   Variable: Set the color of the ticks on the y axis. Default is apply to major ticks only.'
              '\n   Usage: ytickcolor color [which: major | minor | both]\n'
              '\n   Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set'
              '\n   of hexadecimal red-green-blue values (RRGGBB).'
              '\n   The entire set of HTML-standard color names is available.'
              '\n   Try "showcolormap" to see the available named colors!\n')

    def do_xticklength(self, line):
        """
        Set the xticks length explicitly
        """

        try:
            line = line.split()

            if len(line) == 1:  # which = 'major'
                if line[0] == 'de':
                    self.xticklength = 4
                else:
                    self.xticklength = float(line[0])
            elif len(line) == 2:    # which = 'major|minor|both'
                if line[1].upper() == 'MAJOR':
                    if line[0] == 'de':
                        self.xticklength = 4
                    else:
                        self.xticklength = float(line[0])
                elif line[1].upper() == 'MINOR':
                    if line[0] == 'de':
                        self.xminorticklength = 2
                    else:
                        self.xminorticklength = float(line[0])
                elif line[1].upper() == 'BOTH':
                    if line[0] == 'de':
                        self.xticklength = 4
                        self.xminorticklength = 2
                    else:
                        self.xticklength = float(line[0])
                        self.xminorticklength = float(line[0])
                else:
                    raise ValueError("Unknown type of axis: %s" % line[1])
            else:
                raise RuntimeError('Too many arguments, expecting 1 or 2 but received %d' % len(line))
        except:
            print('error - usage: xticklength number [which: major | minor | both]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xticklength(self):
        print('\n   Variable: Set the length (in points) of x ticks on the x axis. '
              'Default is apply to major ticks only.'
              '\n   Usage: xticklength number [which: major | minor | both]')

    def do_yticklength(self, line):
        """
        Set the yticks length explicitly
        """

        try:
            line = line.split()

            if len(line) == 1:
                if line[0] == 'de':
                    self.yticklength = 4
                else:
                    self.yticklength = float(line[0])
            elif len(line) == 2:
                if line[1].upper() == 'MAJOR':
                    if line[0] == 'de':
                        self.yticklength = 4
                    else:
                        self.yticklength = float(line[0])
                elif line[1].upper() == 'MINOR':
                    if line[0] == 'de':
                        self.yminorticklength = 2
                    else:
                        self.yminorticklength = float(line[0])
                elif line[1].upper() == 'BOTH':
                    if line[0] == 'de':
                        self.yticklength = 4
                        self.yminorticklength = 2
                    else:
                        self.yticklength = float(line[0])
                        self.yminorticklength = float(line[0])
                else:
                    raise ValueError("Unknown type of axis: %s" % line[1])
            else:
                raise RuntimeError('Too many arguments, expecting 1 or 2 but received %d' % len(line))
        except:
            print('error - usage: yticklength number [which: major | minor | both]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_yticklength(self):
        print('\n   Variable: Set the length (in points) of y ticks on the y axis. '
              'Default is apply to major ticks only.'
              '\n   Usage: yticklength number [which: major | minor | both]')

    def do_xtickwidth(self, line):
        """
        Set the xticks width explicitly
        """

        try:
            line = line.split()

            if len(line) == 1:
                if line[0] == 'de':
                    self.xtickwidth = 1
                else:
                    self.xtickwidth = float(line[0])
            elif len(line) == 2:
                if line[1].upper() == 'MAJOR':
                    if line[0] == 'de':
                        self.xtickwidth = 1
                    else:
                        self.xtickwidth = float(line[0])
                elif line[1].upper() == 'MINOR':
                    if line[0] == 'de':
                        self.xminortickwidth = 0.5
                    else:
                        self.xminortickwidth = float(line[0])
                elif line[1].upper() == 'BOTH':
                    if line[0] == 'de':
                        self.xtickwidth = 1
                        self.xminortickwidth = 0.5
                    else:
                        self.xtickwidth = float(line[0])
                        self.xminortickwidth = float(line[0])
                else:
                    raise ValueError("Unknown type of axis: %s" % line[1])
            else:
                raise RuntimeError('Too many arguments, expecting 1 or 2 but received %d' % len(line))
        except:
            print('error - usage: xtickwidth number [which: major | minor | both]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xtickwidth(self):
        print('\n   Variable: Set the width (in points) of x ticks on the x axis. Default is apply to major ticks only.'
              '\n   Usage: xtickwidth number [which: major | minor | both]')

    def do_ytickwidth(self, line):
        """
        Set the yticks width explicitly
        """

        try:
            line = line.split()

            if len(line) == 1:
                if line[0] == 'de':
                    self.ytickwidth = 1
                else:
                    self.ytickwidth = float(line[0])
            elif len(line) == 2:
                if line[1].upper() == 'MAJOR':
                    if line[0] == 'de':
                        self.ytickwidth = 1
                    else:
                        self.ytickwidth = float(line[0])
                elif line[1].upper() == 'MINOR':
                    if line[0] == 'de':
                        self.yminortickwidth = 0.5
                    else:
                        self.yminortickwidth = float(line[0])
                elif line[1].upper() == 'BOTH':
                    if line[0] == 'de':
                        self.ytickwidth = 1
                        self.yminortickwidth = 0.5
                    else:
                        self.ytickwidth = float(line[0])
                        self.yminortickwidth = float(line[0])
                else:
                    raise ValueError("Unknown type of axis: %s" % line[1])
            else:
                raise RuntimeError('Too many arguments, expecting 1 or 2 but received %d' % len(line))
        except:
            print('error - usage: ytickwidth number [which: major | minor | both]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ytickwidth(self):
        print('\n   Variable: Set the width (in points) of y ticks on the y axis. Default is apply to major ticks only.'
              '\n   Usage: ytickwidth number [which: major | minor | both]')

    def do_ytickformat(self, line):
        """
        Set the ytickformat explicitly
        """

        try:
            if line.strip() == 'plain':
                self.ytickformat = 'de'
            else:
                self.ytickformat = line.strip()
        except:
            print('error - usage: ytickformat <plain | sci | exp | 10** | %[width][.precision][type]>.')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ytickformat(self):
        print('\n   Variable: Set the format of major ticks on the y axis'
              '\n   Usage: ytickformat <plain | sci | exp | 10** | %[width][.precision][type]>.  '
              '\n          Default is plain. %[width][.precision][type] is the C-style (old Python style) '
              'format string (e.g., %5.1e).'
              '\n          Note: exp and 10** only apply when ylogscale is set to on. C-style '
              'formating only applies when ylogscale is set to off.')

    def do_xtickformat(self, line):
        """
        Set the xtickformat explicitly
        """

        try:
            if line.strip() == 'plain':
                self.xtickformat = 'de'
            else:
                self.xtickformat = line.strip()
        except:
            print('error - usage: xtickformat <plain | sci | exp | 10** | %[width][.precision][type]>.')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xtickformat(self):
        print('\n   Variable: Set the format of major ticks on the x axis'
              '\n   Usage: xtickformat <plain | sci | exp | 10** | %[width][.precision][type]>.  '
              '\n          Default is plain. %[width][.precision][type] is the C-style (old Python style) '
              'format string (e.g., %5.1e).'
              '\n          Note: exp and 10** only apply when xlogscale is set to on. C-style '
              'formating only applies when xlogscale is set to off.')

    def do_xtickrotation(self, line):
        """
        Set the xtickrotation explicitly
        """

        try:
            self.xtickrotation = float(line.strip())
        except:
            print('error - usage: xtickrotation <degree>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_xtickrotation(self):
        print('\n   Variable: Set the rotation of tick labels on the x axis'
              '\n   Usage: xtickrotation <degree>')

    def do_ytickrotation(self, line):
        """
        Set the ytickrotation explicitly
        """

        try:
            self.ytickrotation = float(line.strip())
        except:
            print('error - usage: ytickrotation <degree>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_ytickrotation(self):
        print('\n   Variable: Set the rotation of tick labels on the y axis'
              '\n   Usage: ytickrotation <degree>')

    def do_fontstyle(self, line):
        """
        Set the font family
        """

        try:
            matplotlib.rc('font', family=line.strip())
        except:
            print('error - usage: fontstyle <serif | sans-serif | monospace>')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_fontstyle(self):
        print('\n   Variable: Set the fontstyle family\n   Usage: fontstyle <serif | sans-serif | monospace>\n')

    def do_subsample(self, line):
        """
        Subsample the curves, i.e., reduce to every nth value
        """

        try:
            if not line:
                return 0
            if len(line.split(':')) > 1:
                self.do_subsample(pdvutil.getletterargs(line))
                return 0
            else:
                line = line.split()

                try:
                    stride = int(line[-1])
                    line.pop(-1)
                except:
                    stride = 2
                curvelist = list()

                for i in range(len(line)):
                    try:
                        curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                        curvelist.append(self.plotlist[curvidx])
                    except pdvutil.CurveIndexError:
                        pass

                if len(curvelist) > 0:
                    print("\nSubsampling the data by stride %i...\n" % stride)
                    pydvif.subsample(curvelist, stride, True)

                self.plotedit = True

        except:
            print('error - usage: subsample <curve-list> [stride]')
            if self.debug:
                traceback.print_exc(file=sys.stdout)

    def help_subsample(self):
        print('\n    Procedure: Subsample the curves by the optional stride. The default value for stride is 2.'
              '\n    Usage: subsample <curve-list> [stride]')

    ########################################################################################################
    # helper functions #
    ########################################################################################################

    def find_xrange(self):
        """
        Find the proper x-range
        """

        orderlist = sorted(self.plotlist, key=lambda x: x.plotprecedence)
        xmin, xmax = 1e300, -1e300
        for cur in orderlist:
            if not cur.hidden:
                xmin = min(xmin, min(cur.x))
                xmax = max(xmax, max(cur.x))
        if self.xlogscale:
            xmin = 1e-2
            for cur in orderlist:
                if not cur.hidden:
                    xdat = numpy.array(cur.x)
                    for i in range(len(xdat)):
                        if xdat[i] < 1e-300:
                            xdat[i] = 1e301
                    localmin = min(xdat)
                    if localmin and localmin < xmin:
                        xmin = localmin
            if xmax < xmin:
                xmax = xmin * 10000
        return xmin, xmax

    def find_yrange(self):
        """
        Find the proper y-range
        """

        orderlist = sorted(self.plotlist, key=lambda x: x.plotprecedence)
        ymin, ymax = 1e300, -1e300
        for cur in orderlist:
            if not cur.hidden:
                ymin = min(ymin, min(cur.y))
                ymax = max(ymax, max(cur.y))
        if self.ylogscale:
            ymin = 1e-2
            for cur in orderlist:
                if not cur.hidden:
                    localmin = min(numpy.ma.masked_where(numpy.ma.array(cur.y) < 1e-300, numpy.ma.array(cur.y)))
                    if localmin and localmin < ymin:
                        ymin = localmin
            if ymax < ymin:
                ymax = ymin * 10000
            ymin *= 0.95
            ymax *= 1.05
        else:
            bump = 0.05 * (ymax - ymin)
            ymin -= bump
            ymax += bump
        return ymin, ymax

    def curvefromlabel(self, label):
        """
        Get curve from its label/plot name
        """

        label = label.upper()
        for c in self.plotlist:
            if c.plotname == label:
                return c

        raise ValueError('label "%s" not found in the plot list' % label)

    def addtoplot(self, cur):
        """
        Ensure curve is valid and add it to the plotlist
        """

        if (cur.plotname == '' or (len(cur.plotname) > 1 and cur.plotname[0] != '@')):
            cur.plotname = self.getcurvename()

        cur.x = numpy.array(cur.x)
        cur.y = numpy.array(cur.y)
        if (len(cur.x) < 1 or len(cur.y) < 1):
            raise ValueError('curve must have one or more points')
            return
        if (len(cur.x) != len(cur.y)):
            raise ValueError('curve must have same number of x and y values')
            return
        if (cur.plotname[:1] != '@' and ord(cur.plotname) >= ord('A') and ord(cur.plotname) <= ord('Z')):
            self.plotlist.insert((ord(cur.plotname) - ord('A')), cur)
        else:
            self.plotlist.insert(int(cur.plotname[1:]) - 1, cur)

        self.reset_xticks_labels()
        self.set_xlabel(cur.xlabel, from_curve=True)
        self.set_ylabel(cur.ylabel, from_curve=True)
        self.set_title(cur.title, from_curve=True)
        self.set_filename(cur.filename, from_curve=True)
        self.set_record_id(cur.record_id, from_curve=True)

    def reset_xticks_labels(self):
        """
        Reset xtick labels whenever there is a new curve added/hidden/deleted
        """

        # Create an overall dictionary for all the xtick labels
        reset = True
        for i, labeled_curve in enumerate(self.plotlist):
            if labeled_curve.xticks_labels and not labeled_curve.hidden:
                # Clear if previous dict exists
                if self.xtick_labels and reset:
                    self.xtick_labels = {}
                    reset = False
                for key, val in labeled_curve.xticks_labels.items():
                    self.xtick_labels[key] = val

        # Update overall dictionary with increasing integers
        if self.xtick_labels:
            for i, (key, val) in enumerate(self.xtick_labels.items()):
                self.xtick_labels[key] = i

        # Update each individual curve x tick label dictionary with overall dictionary values
        x_labels = []
        for i, labeled_curve in enumerate(self.plotlist):

            if labeled_curve.xticks_labels and not labeled_curve.hidden:
                x_labels = []

                for xval in labeled_curve.x:
                    for key, val in labeled_curve.xticks_labels.items():
                        if xval == val:
                            x_labels.append(key)
                            break

                # Convert x values to new values from overall dictionary
                x_new = [self.xtick_labels[label] for label in x_labels]
                y_new = labeled_curve.y
                x_labels, x_new, y_new, = zip(*sorted(zip(x_labels, x_new, y_new)))

                labeled_curve.x = numpy.array(x_new)
                labeled_curve.y = numpy.array(y_new)
                labeled_curve.xticks_labels = {label: self.xtick_labels[label] for label in list(x_labels)}
                labeled_curve.scatter = True

        # X tick label string for labeled data
        if x_labels:
            str1 = "("
            str2 = "("
            for key, val in self.xtick_labels.items():
                str1 += f"{val}, "
                str2 += f"'{key}', "
            str1 = str1[:-2]
            str1 += ")"
            str2 = str2[:-2]
            str2 += ")"
            xticks_str = str1 + ", " + str2

            self.do_xticks(xticks_str)

            if self.xtickrotation == 0:
                self.xtickrotation = 90

        # Leave custom xticks if there is no labeled data
        elif not self.xtick_labels:
            self.do_xticks(str(self.xticks))

        # Reset x tick labels if there is no labeled data
        else:
            self.xticks = 'de'
            self.xtick_labels = {}

    def derivative(self, cur):
        """
        Return derivative of curve
        """

        nc = pydvif.derivative(cur)
        nc.plotname = self.getcurvename()
        return nc

    def getcurvename(self):
        """
        Find the next available curve name for the plot
        """

        name = ''
        for i in range(len(self.plotlist)):
            if (i < 26):
                if (self.plotlist[i].plotname != chr(ord('A') + i)):
                    return '' + chr(ord('A') + i)
            else:
                if (self.plotlist[i].plotname != ('@' + str(i + 1))):
                    name = '@' + str(i + 1)
                    return name
        if (len(self.plotlist) < 26):
            return '' + chr(ord('A') + len(self.plotlist))
        else:
            name = '@' + str(len(self.plotlist) + 1)
            return name

    def getclosest(self, array, value):
        """
        Find closest value in numpy array
        """

        i = (numpy.abs(array - value)).argmin()
        return i

    def modcurve(self, line, flag, arg):
        """
        Operate on given curves by constant value depending on given operation flag
        """

        if not line:
            return 0
        modvalue = arg
        if len(line.split(':')) > 1:
            self.modcurve(pdvutil.getletterargs(line), flag, arg)
            return 0
        else:
            line = line.split()
            for i in range(len(line)):
                try:
                    curidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    cur = self.plotlist[curidx]

                    if (flag == 'my'):
                        cur.y *= float(modvalue)
                        cur.edited = True
                    elif (flag == 'mx'):
                        cur.x *= float(modvalue)
                        cur.edited = True
                    elif (flag == 'divy'):
                        if (float(modvalue) == 0):
                            modvalue = '1e-10'
                        cur.y /= float(modvalue)
                        cur.edited = True
                    elif (flag == 'divx'):
                        if (float(modvalue) == 0):
                            modvalue = '1e-10'
                        cur.x /= float(modvalue)
                        cur.edited = True
                    elif (flag == 'dy'):
                        cur.y += float(modvalue)
                        cur.edited = True
                    elif (flag == 'dx'):
                        cur.x += float(modvalue)
                        cur.edited = True
                    elif (flag == 'scatter'):
                        if (modvalue == '0' or modvalue.upper() == 'OFF'):
                            cur.scatter = False
                        elif (modvalue == '1' or modvalue.upper() == 'ON'):
                            cur.scatter = True
                    elif (flag == 'linespoints'):
                        if (modvalue == '0' or modvalue.upper() == 'OFF'):
                            cur.linespoints = False
                        elif (modvalue == '1' or modvalue.upper() == 'ON'):
                            cur.linespoints = True
                    elif (flag == 'lnwidth'):
                        cur.linewidth = float(modvalue)
                    elif flag == 'lnstyle':
                        if modvalue == 'solid':
                            cur.linestyle = '-'
                        elif modvalue == 'dot':
                            cur.linestyle = ':'
                        elif modvalue == 'dash':
                            cur.linestyle = '--'
                        elif modvalue == 'dashdot':
                            cur.linestyle = '-.'
                        elif modvalue == 'loosely_dotted':
                            cur.linestyle = (0, (1, 10))
                        elif modvalue == 'long_dash_with_offset':
                            cur.linestyle = (5, (10, 3))
                        elif modvalue == 'loosely_dashed':
                            cur.linestyle = (0, (5, 10))
                        elif modvalue == 'dashed':
                            cur.linestyle = (0, (5, 5))
                        elif modvalue == 'loosely_dashdotted':
                            cur.linestyle = (0, (3, 10, 1, 10))
                        elif modvalue == 'dashdotted':
                            cur.linestyle = (0, (3, 5, 1, 5))
                        elif modvalue == 'densely_dashdotted':
                            cur.linestyle = (0, (3, 1, 1, 1))
                        elif modvalue == 'dashdotdotted':
                            cur.linestyle = (0, (3, 5, 1, 5, 1, 5))
                        elif modvalue == 'loosely_dashdotdotted':
                            cur.linestyle = (0, (3, 10, 1, 10, 1, 10))
                        elif modvalue == 'densely_dashdotdotted':
                            cur.linestyle = (0, (3, 1, 1, 1, 1, 1))
                        cur.dashes = None  # Restore default dash behaviour
                    elif (flag == 'drawstyle'):
                        # default, steps, steps-pre, steps-post
                        cur.drawstyle = modvalue
                    elif (flag == 'dashstyle'):
                        if modvalue[:2].upper() == 'DE':
                            cur.dashes = None
                        else:
                            val = eval(modvalue)
                            assert isinstance(val, list)
                            assert len(val) % 2 == 0
                            assert min(val) > 0
                            cur.dashes = val
                    elif (flag == 'hide'):
                        if (modvalue == 'OFF'):
                            cur.hidden = False
                        elif (modvalue == 'ON'):
                            cur.hidden = True
                    elif (flag == 'getx'):
                        try:
                            getxvalues = pydvif.getx(cur, float(modvalue))

                            if getxvalues:
                                print('\nCurve ' + cur.plotname)

                                for i in range(len(getxvalues)):
                                    x, y = getxvalues[i]
                                    print('    x: %.6e    y: %.6e\n' % (x, y))
                        except ValueError as detail:
                            print('Error: %s' % detail)

                    elif (flag == 'gety'):
                        try:
                            getyvalues = pydvif.gety(cur, float(modvalue))

                            if getyvalues:
                                print('\nCurve ' + cur.plotname)

                                for i in range(len(getyvalues)):
                                    x, y = getyvalues[i]
                                    print('    x: %.6e    y: %.6e' % (x, y))
                        except ValueError as detail:
                            print('Error: %s' % detail)
                    elif (flag == 'xmin'):
                        nx = []
                        ny = []
                        for dex in range(len(cur.x)):
                            if (cur.x[dex] >= float(modvalue)):
                                nx.append(cur.x[dex])
                                ny.append(cur.y[dex])
                        if (len(nx) > 0):
                            cur.x = numpy.array(nx)
                            cur.y = numpy.array(ny)
                            cur.edited = True
                            if len(nx) == 1:
                                cur.marker = 'o'
                                cur.markersize = 3
                        else:
                            j = pdvutil.getCurveIndex(cur.plotname, self.plotlist)
                            cur.plotname = ''
                            self.plotlist.pop(j)
                    elif (flag == 'xmax'):
                        nx = []
                        ny = []
                        for dex in range(len(cur.x)):
                            if (cur.x[dex] <= float(modvalue)):
                                nx.append(cur.x[dex])
                                ny.append(cur.y[dex])
                        if (len(nx) > 0):
                            cur.x = numpy.array(nx)
                            cur.y = numpy.array(ny)
                            cur.edited = True
                            if len(nx) == 1:
                                cur.marker = 'o'
                                cur.markersize = 3
                        else:
                            j = pdvutil.getCurveIndex(cur.plotname, self.plotlist)
                            cur.plotname = ''
                            self.plotlist.pop(j)
                    elif (flag == 'ymin'):
                        nx = []
                        ny = []
                        for dex in range(len(cur.y)):
                            if (cur.y[dex] >= float(modvalue)):
                                nx.append(cur.x[dex])
                                ny.append(cur.y[dex])
                        if (len(nx) > 0):
                            cur.x = numpy.array(nx)
                            cur.y = numpy.array(ny)
                            cur.edited = True
                            if len(nx) == 1:
                                cur.marker = 'o'
                                cur.markersize = 3
                        else:
                            j = pdvutil.getCurveIndex(cur.plotname, self.plotlist)
                            cur.plotname = ''
                            self.plotlist.pop(j)
                    elif (flag == 'ymax'):
                        nx = []
                        ny = []
                        for dex in range(len(cur.y)):
                            if (cur.y[dex] <= float(modvalue)):
                                nx.append(cur.x[dex])
                                ny.append(cur.y[dex])
                        if (len(nx) > 0):
                            cur.x = numpy.array(nx)
                            cur.y = numpy.array(ny)
                            cur.edited = True
                            if len(nx) == 1:
                                cur.marker = 'o'
                                cur.markersize = 3
                        else:
                            j = pdvutil.getCurveIndex(cur.plotname, self.plotlist)
                            cur.plotname = ''
                            self.plotlist.pop(j)
                except:
                    if self.debug:
                        traceback.print_exc(file=sys.stdout)

    def func_curve(self, line, flag, do_x=0, arg=0):
        """
        Operate on given curves by a function
        """

        if not line:
            return 0
        if len(line.split(':')) > 1:
            self.func_curve(pdvutil.getletterargs(line), flag, do_x, arg)
            return 0
        else:
            line = line.split()
            for i in range(len(line)):
                try:
                    idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    cur = self.plotlist[idx]

                    if (flag == 'abs'):
                        if (do_x == 0):
                            cur.y = numpy.abs(cur.y)
                            cur.name = 'abs(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.abs(cur.x)
                            cur.name = 'absx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'exp'):
                        if (do_x == 0):
                            cur.y = numpy.exp(cur.y)
                            if cur.name[:3] == 'log':
                                # Pop off the log( from the front and the ) from the back
                                cur.name = cur.name[4:-1]
                            else:
                                cur.name = 'exp(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.exp(cur.x)
                            if cur.name[:4] == 'logx':
                                # Pop off the logx( from the front and the ) from the back
                                cur.name = cur.name[5:-1]
                            else:
                                cur.name = 'expx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'sin'):
                        if (do_x == 0):
                            cur.y = numpy.sin(cur.y)
                            cur.name = 'sin(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.sin(cur.x)
                            cur.name = 'sinx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'cos'):
                        if (do_x == 0):
                            cur.y = numpy.cos(cur.y)
                            cur.name = 'cos(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.cos(cur.x)
                            cur.name = 'cosx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'tan'):
                        if (do_x == 0):
                            cur.y = numpy.tan(cur.y)
                            cur.name = 'tan(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.tan(cur.x)
                            cur.name = 'tanx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'asin'):
                        if (do_x == 0):
                            cur.y = numpy.arcsin(cur.y)
                            cur.name = 'asin(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.arcsin(cur.x)
                            cur.name = 'asinx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'acos'):
                        if (do_x == 0):
                            cur.y = numpy.arccos(cur.y)
                            cur.name = 'acos(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.arccos(cur.x)
                            cur.name = 'acosx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'atan'):
                        if (do_x == 0):
                            cur.y = numpy.arctan(cur.y)
                            cur.name = 'atan(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.arctan(cur.x)
                            cur.name = 'atanx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'sinh'):
                        if (do_x == 0):
                            cur.y = numpy.sinh(cur.y)
                            cur.name = 'sinh(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.sinh(cur.x)
                            cur.name = 'sinhx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'cosh'):
                        if (do_x == 0):
                            cur.y = numpy.cosh(cur.y)
                            cur.name = 'cosh(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.cosh(cur.x)
                            cur.name = 'coshx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'tanh'):
                        if (do_x == 0):
                            cur.y = numpy.tanh(cur.y)
                            cur.name = 'tanh(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.tanh(cur.x)
                            cur.name = 'tanhx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'asinh'):
                        if (do_x == 0):
                            cur.y = numpy.arcsinh(cur.y)
                            cur.name = 'asinh(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.arcsinh(cur.x)
                            cur.name = 'asinhx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'acosh'):
                        if (do_x == 0):
                            cur.y = numpy.arccosh(cur.y)
                            cur.name = 'acosh(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.arccosh(cur.x)
                            cur.name = 'acoshx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'atanh'):
                        if (do_x == 0):
                            cur.y = numpy.arctanh(cur.y)
                            cur.name = 'atanh(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.arctanh(cur.x)
                            cur.name = 'atanhx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'j0'):
                        if do_x == 0:
                            cur.y = scipy.special.j0(cur.y)
                            cur.name = 'j0(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = scipy.special.j0(cur.x)
                            cur.name = 'j0x(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'j1'):
                        if (do_x == 0):
                            cur.y = scipy.special.j1(cur.y)
                            cur.name = 'j1(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = scipy.special.j1(cur.x)
                            cur.name = 'j1x(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'jn'):
                        if (do_x == 0):
                            cur.y = scipy.special.jn(float(arg), cur.y)
                            cur.name = 'jn(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = scipy.special.jn(float(arg), cur.x)
                            cur.name = 'jnx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'y0'):
                        if (do_x == 0):
                            cur.y = scipy.special.y0(cur.y)
                            cur.name = 'y0(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = scipy.special.y0(cur.x)
                            cur.name = 'y0x(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'y1'):
                        if (do_x == 0):
                            cur.y = scipy.special.y1(cur.y)
                            cur.name = 'y1(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = scipy.special.y1(cur.x)
                            cur.name = 'y1x(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'yn'):
                        if (do_x == 0):
                            cur.y = scipy.special.yn(int(arg), cur.y)
                            cur.name = 'yn(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = scipy.special.yn(int(arg), cur.x)
                            cur.name = 'ynx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'powa'):
                        if (do_x == 0):
                            cur.y = numpy.power(float(arg), cur.y)
                            cur.name = 'powa(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.power(float(arg), cur.x)
                            cur.name = 'powax(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'powr'):
                        if (do_x == 0):
                            cur.y = numpy.power(cur.y, float(arg))
                            cur.name = 'powr(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.power(cur.x, float(arg))
                            cur.name = 'powrx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'recip'):
                        if (do_x == 0):
                            cur.y = numpy.reciprocal(cur.y)
                            cur.name = 'recip(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.reciprocal(cur.x)
                            cur.name = 'recipx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'sqr'):
                        if (do_x == 0):
                            cur.y = numpy.square(cur.y)
                            cur.name = 'sqr(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.square(cur.x)
                            cur.name = 'sqrx(' + cur.name + ')'
                            cur.edited = True
                    elif (flag == 'sqrt'):
                        if (do_x == 0):
                            cur.y = numpy.sqrt(cur.y)
                            cur.name = 'sqrt(' + cur.name + ')'
                            cur.edited = True
                        else:
                            cur.x = numpy.sqrt(cur.x)
                            cur.name = 'sqrtx(' + cur.name + ')'
                            cur.edited = True
                except:
                    if self.debug:
                        traceback.print_exc(file=sys.stdout)

    def apply_uichanges(self):
        """
        Applies the changes made by the user from the GUI.
        """

        # this attribute value never gets updated... apply_uichanges() never gets called
        self.plotter.plotChanged = False
        cur_axes = plt.gca()  # Get current axes

        # Save Logscale
        if cur_axes.get_xscale() == "linear":
            self.xlogscale = False
        else:
            self.xlogscale = True

        if cur_axes.get_yscale() == "linear":
            self.ylogscale = False
        else:
            self.ylogscale = True

        # Save plot title
        self.title = cur_axes.get_title()

        # Save x and y limits
        if self.guilims:
            self.xlim = cur_axes.get_xlim()
            self.ylim = cur_axes.get_ylim()

        # Save x and y labels
        self.xlabel = cur_axes.get_xlabel()
        self.ylabel = cur_axes.get_ylabel()

        # Update Curves
        orderlist = sorted(self.plotlist, key=lambda x: x.plotprecedence)
        plotcurvelist = cur_axes.get_lines()

        for i in range(len(plotcurvelist)):
            if not orderlist[i].hidden:
                c = orderlist[i]
                c.name = plotcurvelist[i].get_label()
                c.linestyle = plotcurvelist[i].get_linestyle()
                c.drawstyle = plotcurvelist[i].get_drawstyle()
                c.linewidth = plotcurvelist[i].get_linewidth()
                c.color = plotcurvelist[i].get_color()
                # Marker properties
                c.markerstyle = plotcurvelist[i].get_marker()
                c.markersize = plotcurvelist[i].get_markersize()
                c.markerfacecolor = plotcurvelist[i].get_markerfacecolor()
                c.markeredgecolor = plotcurvelist[i].get_markeredgecolor()

    @property
    def updateplot(self):
        """
        Iterates through plotlist and displays curves on graph
        """

        try:
            if stylesLoaded:
                if self.updatestyle:
                    styles = pydvif.get_styles()

                    try:
                        idx = styles.index(self.plotter.style)
                        style.use(styles[idx])
                    except:
                        if len(styles) > 0:
                            print("\nStyle Error: %s doesn't exist, defaulting to %s\n" % (self.plotter.style,
                                                                                           styles[0]))
                            self.plotter.style = styles[0]
                            style.use(styles[0])
                        else:
                            print("\nStyle Error: no styles available\n")

                    self.updatestyle = False

            plt.clf()
            # cur_axes = self.plotter.current_axes
            cur_axes = plt.gca()
            cur_axes.cla()

            # Border
            cur_axes.spines['bottom'].set_color(self.bordercolor)
            cur_axes.spines['top'].set_color(self.bordercolor)
            # cur_axes.spines['bottom'].set_smart_bounds(True)
            # cur_axes.spines['top'].set_smart_bounds(True)
            cur_axes.spines['right'].set_color(self.bordercolor)
            cur_axes.spines['left'].set_color(self.bordercolor)

            if self.plotcolor is not None:
                cur_axes.patch.set_facecolor(self.plotcolor)

            if self.figcolor is not None:
                self.plotter.fig.set_facecolor(self.figcolor)

            # Setup Plot Attributes
            xlabeltext = plt.xlabel(self.xlabel, fontsize=self.xlabelfont,
                                    weight=self.xlabelweight, style=self.xlabelstyle)
            if self.xlabelcolor is not None:
                xlabeltext.set_color(self.xlabelcolor)

            ylabeltext = plt.ylabel(self.ylabel, fontsize=self.ylabelfont,
                                    weight=self.ylabelweight, style=self.ylabelstyle)
            if self.ylabelcolor is not None:
                ylabeltext.set_color(self.ylabelcolor)

            title = plt.title(self.title, fontsize=self.titlefont)
            if self.titlecolor is not None:
                title.set_color(self.titlecolor)

            if self.xtickcolor is not None:
                for label in cur_axes.get_xticklabels():
                    label.set_color(self.xtickcolor)

            if self.ytickcolor is not None:
                for label in cur_axes.get_yticklabels():
                    label.set_color(self.ytickcolor)

            plt.xticks(size=self.axistickfont)
            plt.yticks(size=self.axistickfont)

            for tlabel in cur_axes.get_xticklabels(minor=True):
                plt.setp(tlabel, size=self.axistickfont)
            for tlabel in cur_axes.get_yticklabels(minor=True):
                plt.setp(tlabel, size=self.axistickfont)

            if len(self.plotlist) < 1:
                plt.draw()
                self.plotter.canvas.update()
                self.plotter.canvas.draw()
                return 0

            # Show in legend if enabled
            for cur in self.plotlist:
                # Show curve letter in legend if enabled
                addstr = str('[' + cur.plotname + ']')
                if cur.name.find(addstr) != -1:
                    strarr = cur.name.split(addstr)
                    cur.name = ''.join(strarr).strip()
                if self.showcurveinlegend:
                    cur.name = addstr + ' ' + cur.name

                # only for sina files
                if cur.filename.endswith('.json'):
                    # Show curve recordid in legend if enabled
                    addrstr = str('- ' + cur.record_id)
                    if cur.name.find(addrstr) != -1:
                        rstrarr = cur.name.split(addrstr)
                        cur.name = ''.join(rstrarr).strip()
                    if self.showrecordidinlegend:
                        cur.name = cur.name + ' ' + addrstr

                # Show curve filename in legend if enabled
                addfstr = str('- ' + cur.filename)
                if cur.name.find(addfstr) != -1:
                    fstrarr = cur.name.split(addfstr)
                    cur.name = ''.join(fstrarr).strip()
                if self.showfilenameinlegend:
                    cur.name = cur.name + ' ' + addfstr

            # set scaling and tick locations
            #
            # Notes on matplotlib that I found very helpful:
            #
            # plt.gca() is "get current axes instance"
            # ScalarFormatter works with linear scales, MaxNLocator
            # LogFormatter is needed to work with LogLocator, produces 1,10,100,...
            # LogFormatterExponent produces 0,1,2,...
            # LogFormatterMathtext produces 10**0,10**1,10**2,...
            xls = self.xlogscale
            yls = self.ylogscale

            if (xls):
                cur_axes.set_xscale('log')
                # cur_axes.set_xscale('log', nonposx='clip')
            if (yls):
                cur_axes.set_yscale('log')
                # cur_axes.set_yscale('log', nonposy='clip')

# thinking about what we want here
#              xticks de
#                     or a number
#                     or a list of locations
#                     or a tuple of (locations, labels)
#              xls on or off
#              xtickformat = 'sci', 'plain', 'exp', '10**'
            if self.showminorticks:
                plt.minorticks_on()
                cur_axes.tick_params(axis='x', which='minor', length=self.xminorticklength,
                                     width=self.xminortickwidth, color=self.xminortickcolor)
                cur_axes.tick_params(axis='y', which='minor', length=self.yminorticklength,
                                     width=self.yminortickwidth, color=self.yminortickcolor)

            # set x,y tick sizes and tick label format
            cur_axes.tick_params(axis='x', length=self.xticklength, width=self.xtickwidth, color=self.xmajortickcolor,
                                 labelrotation=self.xtickrotation)
            cur_axes.tick_params(axis='y', length=self.yticklength, width=self.ytickwidth, color=self.ymajortickcolor,
                                 labelrotation=self.ytickrotation)
            yaxis = cur_axes.yaxis
            xaxis = cur_axes.xaxis
            self.tickFormat(yaxis, self.ylogscale, self.yticks, self.ytickformat)
            self.tickFormat(xaxis, self.xlogscale, self.xticks, self.xtickformat)

            # plot the grid, if grid turned on
            if self.showgrid:
                if plt.xlim is not None and plt.ylim is not None:
                    if ((plt.xlim()[0] * 100 > plt.xlim()[1] and xls) or (plt.ylim()[0] * 100 > plt.ylim()[1] and yls)):
                        plt.grid(True, which='both', color=self.gridcolor,
                                 linestyle=self.gridstyle, linewidth=self.gridwidth)
                    else:
                        plt.grid(True, color=self.gridcolor, linestyle=self.gridstyle, linewidth=self.gridwidth)
                else:
                    plt.grid(True, color=self.gridcolor, linestyle=self.gridstyle, linewidth=self.gridwidth)
            else:
                plt.grid(False)

            # order list in which curves should be plotted
            orderlist = sorted(self.plotlist, key=lambda x: x.plotprecedence)

            # plot the curves
            for cur in orderlist:
                if not cur.hidden:
                    xdat = numpy.array(cur.x)
                    ydat = numpy.array(cur.y)
                    if yls:
                        for i in range(len(ydat)):
                            if (ydat[i] < 0):
                                ydat[i] = 1e-301  # custom ydata clipping
                    if xls:
                        for i in range(len(xdat)):
                            if xdat[i] < 0:
                                xdat[i] = 1e-301  # custom ydata clipping

                    if cur.ebar is not None:
                        plt.errorbar(xdat,
                                     ydat,
                                     yerr=[cur.ebar[0], cur.ebar[1]],
                                     xerr=[cur.ebar[2], cur.ebar[3]],
                                     fmt='-')
                        c = plt.plot(xdat, ydat)
                    elif cur.erange is not None:
                        c = plt.plot(xdat, ydat)
                        plt.fill_between(xdat,
                                         ydat - cur.erange[0],
                                         ydat + cur.erange[1],
                                         alpha=0.4,
                                         color=c[0].get_color())
                        c = plt.plot(xdat, ydat)
                    else:
                        c = plt.plot(xdat, ydat)

                    if cur.color != '':
                        plt.setp(c, color=cur.color)
                    else:
                        cur.color = c[0].get_color()

                    if cur.linespoints:
                        plt.setp(c, marker=cur.marker, markersize=cur.markersize, linestyle=cur.linestyle)
                    elif cur.scatter:
                        plt.setp(c, marker=cur.marker, markersize=cur.markersize, linestyle=' ')
                    else:
                        if cur.markeredgecolor is None:
                            cur.markeredgecolor = cur.color
                        if cur.markerfacecolor is None:
                            cur.markerfacecolor = cur.color
                        if cur.markerstyle is None:
                            cur.markerstyle = 'None'

                        # plt.setp(c, marker=cur.markerstyle, markeredgecolor=cur.markeredgecolor,
                        # markerfacecolor=cur.markerfacecolor, linestyle=cur.linestyle)
                        if self.showplot == 'off':
                            linestyle = 'None'
                            markerstyle = 'None'
                        else:
                            linestyle = cur.linestyle
                            markerstyle = cur.markerstyle
                        plt.setp(c, marker=markerstyle, markersize=cur.markersize,
                                 markeredgecolor=cur.markeredgecolor,
                                 markerfacecolor=cur.markerfacecolor, linestyle=linestyle)

                        c[0].set_drawstyle(cur.drawstyle)
                        # Work-around for set_drawstyle bug (https://github.com/matplotlib/matplotlib/issues/10338)
                        c[0]._invalidx = True

                    if cur.linewidth:
                        plt.setp(c, lw=cur.linewidth)
                        plt.setp(c, mew=cur.linewidth)
                    elif self.linewidth:
                        plt.setp(c, lw=self.linewidth)
                        plt.setp(c, mew=self.linewidth)

                    if cur.legend_show:
                        plt.setp(c, label=cur.name)

                    if cur.dashes is not None:
                        c[0].set_dashes(cur.dashes)

            # ensure proper view limits
            # plt.axis('tight')

            if self.xlim is not None:
                plt.xlim(self.xlim[0], self.xlim[1])

            if self.ylim is not None:
                plt.ylim(self.ylim[0], self.ylim[1])

            # plot the curve labels
            if self.showletters and self.showplot == 'on':
                # get range and domain of plot
                xmin = plt.axis()[0]
                xmax = plt.axis()[1]
                ymin = plt.axis()[2]
                ymax = plt.axis()[3]
                spacing = (xmax - xmin) / 6
                offset = 0
                for cur in orderlist:
                    if not cur.hidden:
                        plt.text(cur.x[0], cur.y[0], cur.plotname, color=cur.color, fontsize=self.curvelabelfont)
                        curxmax = max(cur.x)
                        curxmin = min(cur.x)
                        if self.xlim is not None:
                            if self.xlim[1] < curxmax:
                                curxmax = self.xlim[1]
                            if self.xlim[0] > curxmin:
                                curxmin = self.xlim[0]
                        spacing = (curxmax - curxmin) / 6
                        labelx = curxmin + offset * spacing / len(self.plotlist)
                        while labelx < curxmax:  # print letter labels along curves
                            close = self.getclosest(cur.x, labelx)
                            if (cur.y[close] <= ymax and cur.y[close] >= ymin):
                                plt.text(cur.x[close], cur.y[close], cur.plotname,
                                         color=cur.color, fontsize=self.curvelabelfont)
                            labelx += spacing
                        plt.text(cur.x[-1], cur.y[-1], cur.plotname, color=cur.color, fontsize=self.curvelabelfont)
                        offset += 1

            # fonts/labels/legend
            if self.showkey:
                leg = plt.legend(fancybox=True, numpoints=1, loc=self.key_loc,
                                 ncol=self.key_ncol, handlelength=self.handlelength)
                if leg is not None:
                    leg.get_frame().set_alpha(0.9)
                    leg.set_draggable(state=True)
                    ltext = leg.get_texts()
                    plt.setp(ltext, fontsize=self.keyfont)
                    plt.setp(ltext, color=self.keycolor)

            for text in self.usertexts:
                plt.text(text[0], text[1], text[2], fontsize=self.annotationfont)

            if self.showaxis == 'off':
                plt.axis('off')
            else:
                plt.axis('on')

            plt.draw()
            self.plotter.canvas.update()
            self.plotter.canvas.draw()

        except RuntimeError as detail:
            if (detail[-1].split()[0] == 'LaTeX'):
                print('error: invalid LaTeX syntax')
            else:
                print('error: draw may not have completed properly: %s' % detail)
            if (self.debug):
                traceback.print_exc(file=sys.stdout)
        except OverflowError:
            print('Caught overflow error attempting to plot.  Try using "subsample" to reduce the data.')
        except:
            print('error: draw may not have completed properly')
            if (self.debug):
                traceback.print_exc(file=sys.stdout)
        finally:
            self.plotter.updateDialogs()

    def load(self, fname, gnu=False, pattern=None, matches=None):
        """
        Load an ultra file and add parsed curves to the curvelist
        """

        curves = pydvif.read(fname, gnu, self.xCol, self.debug, pattern, matches)
        if len(curves) > 0:
            self.curvelist += curves
            self.filelist.append((fname, len(curves)))

    def load_csv(self, fname, col):
        """
        Load a csv (commas separated values) text data file, add parsed curves to the curvelist
        """
        curves = pydvif.readcsv(fname, col, self.debug)
        if len(curves) > 0:
            self.curvelist += curves
            self.filelist.append((fname, len(curves)))

    def load_sina(self, fname):
        """
        Load a Sina JSON data file, add parsed curves to the curvelist
        """

        curves = pydvif.readsina(fname, self.debug)
        if len(curves) > 0:
            self.curvelist += curves
            self.filelist.append((fname, len(curves)))

    def loadrc(self):
        """
        Read in a resource definition file
        """

        try:
            f = open(os.getenv('HOME') + '/.pdvrc', 'r')

            for line in f:
                try:
                    line = line.split('=')
                    var = line[0].strip().lower()
                    val = line[1].strip()
                    if (var == 'xlabel'):
                        self.xlabel = val
                    elif (var == 'ylabel'):
                        self.ylabel = val
                    elif (var == 'title'):
                        self.title = val
                    elif (var == 'menulength'):
                        self.menulength = int(val)
                    elif (var == 'namewidth'):
                        self.namewidth = int(val)
                    elif (var == 'xlabelwidth'):
                        self.xlabelwidth = int(val)
                    elif (var == 'ylabelwidth'):
                        self.ylabelwidth = int(val)
                    elif (var == 'filenamewidth'):
                        self.filenamewidth = int(val)
                    elif (var == 'recordidwidth'):
                        self.recordidwidth = int(val)
                    elif (var == 'key'):
                        if (val.upper() == 'ON' or val == str(1)):
                            self.showkey = True
                        else:
                            self.showkey = False
                    elif var == 'grid':
                        if val.upper() == 'ON' or val == str(1):
                            self.showgrid = True
                        else:
                            self.showgrid = False
                    elif (var == 'letters'):
                        if (val.upper() == 'ON' or val == str(1)):
                            self.showletters = True
                        else:
                            self.showletters = False
                    elif (var == 'geometry'):
                        vals = val.split()
                        self.geometry = vals[0], vals[1], vals[2], vals[3]
                    elif (var == 'initcommands'):
                        self.initrun = ''.join(val)
                    elif var == 'fontsize':
                        self.titlefont = val
                        self.xlabelfont = val
                        self.ylabelfont = val
                        self.keyfont = val
                        self.axistickfont = val
                        self.curvelabelfont = val
                        self.annotationfont = val
                    elif var == 'lnwidth':
                        self.linewidth = val
                except:
                    continue
            f.close()
        except:
            return 0

    # set tick format and locations
    def tickFormat(self, axis, logscale, ticks, tickformat):
        if logscale:
            if tickformat == 'de' or tickformat == 'sci':
                axis.set_major_formatter(matplotlib.ticker.LogFormatter())
            elif tickformat == 'exp':
                axis.set_major_formatter(matplotlib.ticker.LogFormatterExponent())
            elif tickformat == '10**':
                axis.set_major_formatter(matplotlib.ticker.LogFormatterMathtext())
            else:
                if tickformat[0] == '%':
                    print('\nWarning: C-style formating can not be applied when logscale is on')
                else:
                    print('\nError: Unknown xtick format (%s)' % tickformat)

                axis.set_major_formatter(matplotlib.ticker.LogFormatter())
        else:
            if tickformat == 'de' or tickformat == 'exp' or tickformat == '10**':
                if tickformat == 'exp' or tickformat == '10**':
                    print('\nWarning: logscale is off. exp and 10** only apply when logscale is on')

                axis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
            elif tickformat == 'sci':
                axis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%5.2e'))
            else:
                if tickformat[0] == '%':
                    if tickformat[-1] in ('d', 'e', 'E', 'f', 'F'):
                        axis.set_major_formatter(matplotlib.ticker.FormatStrFormatter(tickformat))
                    else:
                        print('\nError: %s is an unsupported xtickformat type' % tickformat[-1])
                        axis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))
                else:
                    print("\nError: Unknown xtick format. Try adding '%' to the beginning of your format string")
                    axis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))

        # if ticks is set, figure out what user wants for ticks
        if ticks != 'de':
            if isinstance(ticks, int):
                # print 'setting ticks to number ', ticks
                axis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=ticks))
            elif isinstance(ticks, tuple):  # could be locations, could be (locations, labels)
                if isinstance(ticks[0], Number):  # it's a tuple of locations
                    # print 'setting ticks to tuple ', ticks
                    axis.set_major_locator(matplotlib.ticker.FixedLocator(ticks))
                    axis.set_major_formatter(matplotlib.ticker.FixedFormatter(ticks))
                if isinstance(ticks[0], tuple) and len(ticks) == 2:  # it's (locations, labels)
                    # print 'setting ticks to loc,label ', ticks
                    axis.set_major_locator(matplotlib.ticker.FixedLocator(ticks[0]))
                    axis.set_major_formatter(matplotlib.ticker.FixedFormatter(ticks[1]))
            else:  # I can't figure this out, throw an exception
                print("CAN'T SET TICKS!!!")
                raise RuntimeError('ticks set to bad value')

    def console_run(self):
        while True:
            self.cmdloop(f'\n\tPython Data Visualizer {pydv_version}  -  {pydv_date}\n'
                         f'\tType "help" for more information.\n'
                         f'\tDocumentation can be found here:\n'
                         f'\t\tLLNL (more current):   https://lc.llnl.gov/weave/pydv/html/index.html\n'
                         f'\t\tGitHub:                https://pydv.readthedocs.io/en/latest/\n'
                         f'\tRunning from {os.path.abspath(__file__)}\n\n')
            print('\n   Starting Python Console...\n   Ctrl-D to return to PyDV\n')
            console = code.InteractiveConsole(locals())
            console.interact()

    ################################################################################################
    # private functions #
    ################################################################################################

    def __log(self, line, log_type=LogEnum.LOG):
        if not line:
            return 0

        if len(line.split(':')) > 1:
            self.__log(pdvutil.getletterargs(line))
            return 0
        else:
            line = line.split()
            keepnegs = False

            if line[-1].upper() == 'TRUE':
                keepnegs = True
                line.pop(-1)
            elif line[-1].upper() == 'FALSE':
                keepnegs = False
                line.pop(-1)

            curves = list()
            for i in range(len(line)):
                try:
                    curvidx = pdvutil.getCurveIndex(line[i], self.plotlist)
                    curves.append(self.plotlist[curvidx])
                except pdvutil.CurveIndexError:
                    pass
                except:
                    print('error - usage: log <curve-list> [keep-neg-vals: True | False]')
                    if self.debug:
                        traceback.print_exc(file=sys.stdout)

            if log_type == LogEnum.LOG:
                pydvif.log(curves, keepnegs)
            elif log_type == LogEnum.LOGX:
                pydvif.logx(curves, keepnegs)
            elif log_type == LogEnum.LOG10:
                pydvif.log10(curves, keepnegs)
            elif log_type == LogEnum.LOG10X:
                pydvif.log10x(curves, keepnegs)
            else:
                raise RuntimeError("Unknown log type: {}".format(log_type))

    def __mod_curve(self, line, func, idx=-1):
        if not line:
            return

        line = line.split()
        value = line.pop(idx)

        if len(line) > 0:
            line = ' '.join(line)
        else:
            raise RuntimeError("Unexpected empty line")

        self.modcurve(line, func, value)

    def __func_curve(self, line, func, do_x=0, idx=None):
        if not line:
            return

        value = 0
        line = line.split()

        if idx is not None:
            value = line.pop(idx)

        if len(line) > 0:
            line = ' '.join(line)
        else:
            raise RuntimeError("Unexpected empty line")

        self.func_curve(line, func, do_x, value)

    def __qtMsgHandler(self, msgtype, context, msg):
        if self.debug:
            if msgtype == QtDebugMsg:
                print("\nQt Debug: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))
            elif msgtype == QtWarningMsg:
                print("\nQt Warning: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))
            elif msgtype == QtCriticalMsg:
                print("\nQt Critical: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))
            elif msgtype == QtFatalMsg:
                print("\nQt Fatal: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))
            elif msgtype == QtSystemMsg:
                print("\nQt System: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))
            elif msgtype == QtInfoMsg:
                print("\nQt Info: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))
            else:
                print("\nUnknown Message Type: %s (%s:%u, %s)\n" % (msg, context.file, context.line, context.function))

    ################################################################################################
    # main function #
    ################################################################################################

    def main(self):

        matplotlib.rc('text', usetex=False)
        matplotlib.rc('font', family='sans-serif')
        self.loadrc()

        qInstallMessageHandler(self.__qtMsgHandler)

        self.app = QApplication(sys.argv)
        self.plotter = pdvplot.Plotter(self)
        self.plotter.updatePlotGeometry(self.geometry)

        try:
            readline.read_history_file(os.getenv('HOME') + '/.pdvhistory')
        except:
            f = open(os.getenv('HOME') + '/.pdvhistory', 'w')
            f.close()

        # throw into column format mode if there is a -gnu or -csv arg
        gnu = False
        csv = False
        json = False  # throw into JSON mode if there's a -sina
        for i in range(len(sys.argv[1:])):
            if sys.argv[i] == '-gnu':
                gnu = True
                try:
                    self.xCol = int(sys.argv[i + 1])
                    sys.argv.pop(i + 1)
                except ValueError:
                    self.xCol = 0
                sys.argv.remove('-gnu')
                break
            if sys.argv[i] == '-csv':
                csv = True
                try:
                    self.xCol = int(sys.argv[i + 1])
                    sys.argv.pop(i + 1)
                except ValueError:
                    self.xCol = 0
                sys.argv.remove('-csv')
                break
            if sys.argv[i] == '-sina':
                json = True
                sys.argv.remove('-sina')
                break
        if gnu or csv:
            print('Going to column format, using ', self.xCol, ' for x-axis data')
        elif json:
            print('Going to JSON format, loading all curves from curve_sets.')

        initarg = False
        other_args = ['-s',]
        for i in range(len(sys.argv)):  # look for command line args:
            not_in_other_args = sys.argv[i] not in other_args
            if (i != 0):  # '-i commandfile', and/or 'datafile1 datafile2 ...'
                if (sys.argv[i] == '-i' or sys.argv[i] == '--init'):
                    initarg = True
                if not_in_other_args:
                    if (initarg):
                        initarg = sys.argv[i]
                    elif json:
                        self.load_sina(sys.argv[i])
                    else:
                        if not csv:
                            self.load(sys.argv[i], gnu)
                        else:
                            self.load_csv(sys.argv[i])

                if sys.argv[i] == '-s':
                    self.showplot = 'off'
                    self.showkey = False

        if (self.initrun is not None):  # does the .pdvrc specify a file to run of initial commands?
            self.do_run(self.initrun)  # yes? then run the file.

        if (isinstance(initarg, str)):  # If there was a '-i file' specified, run that file
            self.do_run(initarg)

        self.postcmd(0, 'run')

        try:
            # Start interactive console in separate thread
            thread = Thread(target=self.console_run)
            thread.start()

            # Start PyDV Application
            self.plotter.show()
            self.app.exec_()
        except SystemExit:
            self.app.quit()
            sys.exit()
        except KeyboardInterrupt:
            self.app.quit()
            sys.exit()
        except:
            if self.debug:
                traceback.print_exc(file=sys.stdout)
            else:
                pass


def main():
    Command().main()


if __name__ == '__main__':
    main()
