.. _release_notes_2.2:

Release Notes For PyDV 2.2
==========================

Bug Fixes
---------

* Fixed the interpolation function for two curves
* Got alias command working again by adding back the removed import new line

Enhancements
------------

* Added convolvef math command that performs a convolution of two curves using the Fast Fourier transform method
* Added Fast Fourier Transform math command
* Added disp and dispx commands for displaying the curves y- and x-values
* Enhanced the read command to optionally use a regular expression to filter the curves that are read in
* Created a method in the PyDV Python interface to filter curves using a regular expression
* Added handlelength command to control the length of lines in the legend
* Allow namewidth to be changed from the .pdvrc file
* Added documentation for the .pdrc file format

