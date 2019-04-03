import numpy

## getCurveIndex returns integer index to curve in plotlist from plotname
def getCurveIndex(plotname, plotlist):
    for j in range(len(plotlist)):
        if plotname.upper() == plotlist[j].plotname:
            return j
    raise RuntimeError, "pdvutil.py getCurveIndex - failed to find curve index"
        
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
    for val in line:
        dex = None
        if(val[0] == '@'): # are we a curve labeled @N, i.e., beyond a-z?
            dex = int(val[1:]) + 1
            sendline += ' plotlist['+str(dex)+'] '
        elif(len(val) == 1 and ord(val.upper()) <= ord('Z') and ord(val.upper()) >= ord('A')): # or a curve a-z?
            dex = ord(val.upper()) - ord('A')
            sendline += ' plotlist['+ str(dex) +'] '
        else:                                         # no?, then just insert the operation (+,-,*,/, etc)
            sendline += val
    sendline = sendline.lstrip()
    #print sendline
    c = eval(sendline)  # evaluate it --- this works because math ops are defined for, and return, curve objects
    c.name = ' '.join(line).replace('commander.', '').title()  # set name
    c.plotname = commander.getcurvename()                      # set label
    if c.x is None or len(c.x) < 2:
        print 'error: curve overlap is not sufficient'
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
            for j in xrange(int(start), int(start) + delta + step, step):
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
            start = line[i].split()[-1].upper()
            if(start[0] == '@'):
                start = int(start[1:])
            else:
                start = ord(start[0]) - ord('A')
            end = line[i+1].split()[0].upper()
            if(end[0] == '@'):
                end = int(end[1:])
            else:
                end = ord(end[0]) - ord('A')
            args = ''
            for j in range(int(end)-int(start)+1):
                if(j+int(start) > 25):
                    args += '@' + str(j+int(start)) + ' '
                else:
                    args += chr(j+int(start) + ord('A')) + ' '
            arglist += args + ''
        if(len(line[-1].split()) > 1):   #check for non list args
            nolist = line[-1].split()
            nolist.pop(0)
            nolist = ' '.join(nolist)
            arglist += nolist + ' '  #end arduous list parsing
    return arglist
        

##truncate a string to given length##
def truncate(string, size):
    if(len(string) > size):
        string = string[:size]
    return string


def get_actual_index(origref, val):
    for i in range(len(origref)):
        if origref[i] == val:
            return i

    return -1
