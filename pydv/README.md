# README #

## PDV is a 1D graphics and data analysis tool, heavily based on the ULTRA plotting tool. ##

To use it, download the source, and run with Python.  You need pyside or pyqt4, matplotlib and numpy installed.

### PyDV Importable Interface Module ###
You can now call most of PyDV's functionality from within a Python script. Below is an example of how to do this.
        
        import sys
        sys.path.append("/usr/gapps/pydv/2.0")
        import pydvpy as pydvif

        curves = list()
        curves.append(pydvif.span(1,10,6))
        pydvif.save('myFile.txt', curves)

### Links ###
* PDV Home Page: https://lc.llnl.gov/confluence/display/PYDV/PDV%3A+Python+Data+Visualizer 
* PDV JIRA: https://lc.llnl.gov/jira/projects/PYDV
* PDV Build and Test Results: https://lc.llnl.gov/bamboo/browse/PYDV-BUIL
* Ultra User's Manual: https://wci.llnl.gov/codes/pact/ultra.html

### Who do I talk to? ###

* Sarah El-Jurf <eljurf1@llnl.gov>
* Jorge Moreno <moreno45@llnl.gov>
