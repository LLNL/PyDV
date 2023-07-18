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

import numpy as np

class CurveIndexError(ValueError): pass

## getCurveIndex returns integer index to curve in plotlist from plotname
def getCurveIndex(plotname, plotlist):
    for j in range(len(plotlist)):
        if plotname.upper() == plotlist[j].plotname:
            return j
    raise CurveIndexError("pdvutil.py getCurveIndex - failed to find curve index")
        
##parses and calculates mathematical input for curves, then updates plot##
def parsemath(line, plotlist, commander, xdomain):
    line = line.replace('+', ' + ')
    line = line.replace('-', ' - ')
    line = line.replace('*', ' * ')
    line = line.replace('/', ' / ')
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    line = line.split()
    # build the line of operations
    sendline = ''
    step = True
    shared_x = []
    for val in line:
        dex = None
        if(val[0] == '@'): # are we a curve labeled @N, i.e., beyond a-z?
            dex = int(val[1:]) - 1
            sendline += ' plotlist['+str(dex)+'] '
            
            try:
                step_i = eval('plotlist['+str(dex)+'].step')
                if step_i and step:
                    shared_x.extend(eval('plotlist['+ str(dex) +'].x'))
            except:
                step_i = False

        elif(len(val) == 1 and ord(val.upper()) <= ord('Z') and ord(val.upper()) >= ord('A')): # or a curve a-z?
            dex = ord(val.upper()) - ord('A')
            sendline += ' plotlist['+ str(dex) +'] '
            
            try:
                step_i = eval('plotlist['+str(dex)+'].step')
                if step_i and step:
                    shared_x.extend(eval('plotlist['+ str(dex) +'].x'))
            except:
                step_i = False

        else:                                         # no?, then just insert the operation (+,-,*,/, etc)
            sendline += val

        if not step_i:
            step = False

    sendline = sendline.lstrip()
    c = eval(sendline)  # evaluate it --- this works because math ops are defined for, and return, curve objects
    c.name = ' '.join(line).replace('commander.', '').title()  # set name
    c.plotname = commander.getcurvename()                      # set label
    c.step = False

    if step:
        shared_x = set(shared_x)
        sendliney = ''
        maths = [0] * len(line)

        for i, val in enumerate(line):
            dex = None
            if(val[0] == '@'): # are we a curve labeled @N, i.e., beyond a-z?
                dex = int(val[1:]) - 1
                x = list(eval('plotlist['+str(dex)+'].x'))
                y = list(eval('plotlist['+str(dex)+'].y'))
                
                for xs in shared_x:
                    if xs not in x:
                        
                        idxs = [i for i,v in enumerate(x) if v < xs]
                        
                        if not idxs: # missing data at the beginning of the list
                            y.insert(0, 0.0)
                            y.insert(1, 0.0)
                            x.insert(0, xs)
                            x.insert(1, x[1])
                        elif idxs[-1]+2>len(x): # missing data at the end of the list
                            y[-1] = 0.0
                            y.insert(idxs[-1]+1, 0.0)
                            y.insert(idxs[-1]+2, 0.0)
                            x.insert(idxs[-1]+1, xs)
                            x.insert(idxs[-1]+2, xs)
                        else: # missing data in between
                            y.insert(idxs[-1]+1, y[idxs[-1]])
                            y.insert(idxs[-1]+2, y[idxs[-1]])
                            x.insert(idxs[-1]+1, xs)
                            x.insert(idxs[-1]+2, xs)
                
                maths[i] = np.array(y)
                sendliney += ' maths['+str(i)+'] '
                
            elif(len(val) == 1 and ord(val.upper()) <= ord('Z') and ord(val.upper()) >= ord('A')): # or a curve a-z?
                dex = ord(val.upper()) - ord('A')
                x = list(eval('plotlist['+str(dex)+'].x'))
                y = list(eval('plotlist['+str(dex)+'].y'))
                
                for xs in shared_x:
                    if xs not in x:
                        
                        idxs = [i for i,v in enumerate(x) if v < xs]
                        
                        if not idxs: # missing data at the beginning of the list
                            y.insert(0, 0.0)
                            y.insert(1, 0.0)
                            x.insert(0, xs)
                            x.insert(1, x[1])
                        elif idxs[-1]+2>len(x): # missing data at the end of the list
                            y[-1] = 0.0
                            y.insert(idxs[-1]+1, 0.0)
                            y.insert(idxs[-1]+2, 0.0)
                            x.insert(idxs[-1]+1, xs)
                            x.insert(idxs[-1]+2, xs)
                        else: # missing data in between
                            y.insert(idxs[-1]+1, y[idxs[-1]])
                            y.insert(idxs[-1]+2, y[idxs[-1]])
                            x.insert(idxs[-1]+1, xs)
                            x.insert(idxs[-1]+2, xs)
                
                maths[i] = np.array(y)
                sendliney += ' maths['+str(i)+'] '

            else:
                sendliney += val

        sendliney = sendliney.lstrip()

        c.x = x
        c.y = eval(sendliney)
        c.step = True
        
    if c.x is None or len(c.x) < 2:
        print('error: curve overlap is not sufficient')
        return 0
    # put new curve into plotlist
    if(c.plotname[:1] != '@' and ord(c.plotname) >= ord('A') and ord(c.plotname) <= ord('Z')):
        plotlist.insert((ord(c.plotname) - ord('A')), c)
    else:
        plotlist.insert((int(c.plotname[1:])-1), c)
    return c
    #pultry.updateplot()
    

##get a full list of arguments from compact list or mixed notation (ex 4:11)##
def getnumberargs(line, filelist):
    line = line.split(':')
    arglist = ''
    if(len(line) > 1):
        for i in range(len(line)):
            line[i] = line[i].strip()
        if(len(line[0].split()) > 1):   #check for non list args
            nolist = line[0].split()
            nolist.pop(-1)
            nolist = ' '.join(nolist)
            arglist += nolist + ' '
        for i in range(len(line)-1):
            if(i > 0):
                if(len(line[i].split()) > 2):   #check for non list args
                    nolist = line[i].split()
                    nolist.pop(-1)
                    nolist.pop(0)
                    nolist = ' '.join(nolist)
                    arglist += nolist + ' '
            start = line[i].split()[-1]
            end = line[i+1].split()[0]
            if(len(start.split('.')) > 1):
                filedex = ord(start[0].upper()) - ord('A')
                start = start.split('.')[-1]
                if(filedex != 0):
                    for f in range(filedex):
                        start = str(int(start) + filelist[f][1])
            if(len(end.split('.')) > 1):
                filedex = ord(end[0].upper()) - ord('A')
                end = end.split('.')[-1]
                if(filedex != 0):
                    for f in range(filedex):
                        end = str(int(end) + filelist[f][1])
            args = ''
            delta = int(end) - int(start)
            if delta >= 0:
                step = 1
            else:
                step = -1
            for j in range(int(start), int(start) + delta + step, step):
                args += str(j) + ' '
            arglist += args + ' '
        if(len(line[-1].split()) > 1):   #check for non list args
            nolist = line[-1].split()
            nolist.pop(0)
            nolist = ' '.join(nolist)
            arglist += nolist + ' '
    return arglist


##get a full list of arguments from compact list or mixed notation (ex a:d)##
def getletterargs(line):
    line = line.split(':')  #begin arduous list parsing
    arglist = ''
    if len(line) > 1:
        for i in range(len(line)):
            line[i] = line[i].strip()

        # check for non list args
        if len(line[0].split()) > 1:
            nolist = line[0].split()
            nolist.pop(-1)
            nolist = ' '.join(nolist)
            arglist += nolist + ' '

        for i in range(len(line)-1):
            if i > 0:
                # check for non list args
                if len(line[i].split()) > 2:
                    nolist = line[i].split()
                    nolist.pop(-1)
                    nolist.pop(0)
                    nolist = ' '.join(nolist)
                    arglist += nolist + ' '

            start = line[i].split()[-1].upper()

            if start[0] == '@':
                start = int(start[1:]) - 1
            else:
                start = ord(start[0]) - ord('A')

            end = line[i+1].split()[0].upper()

            if end[0] == '@':
                end = int(end[1:]) - 1
            else:
                end = ord(end[0]) - ord('A')

            args = ''
            for j in range((int(end)-int(start))+1):
                if j+int(start) > 25:
                    args += '@' + str(j+int(start)+1) + ' '
                else:
                    args += chr(j+int(start) + ord('A')) + ' '
            arglist += args + ''

        # check for non list args
        if len(line[-1].split()) > 1:
            nolist = line[-1].split()
            nolist.pop(0)
            nolist = ' '.join(nolist)
            arglist += nolist + ' '  #end arduous list parsing
            
    return arglist


##truncate a string to given length##
def truncate(string, size, justify='left'):

    if len(string) > size:
        if justify == 'left':
            string = string[:size]
        elif justify == 'right':
            extra = len(string) - size + 3
            string = '...'+string[extra:]

    return string


def get_actual_index(origref, val):
    for i in range(len(origref)):
        if origref[i] == val:
            return i

    return -1
