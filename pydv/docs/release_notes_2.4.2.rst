.. _release_notes_2.4.2:

Release Notes For PyDV 2.4.2
============================

Bug Fixes
---------

* Fixed the FFT command to produce two curves for the complex and imaginary part like Ultra 
* Corrected the 'off by one' index error for curves named with the '@' symbol
* The xtick commands now display the correct help information
* errorbar command works now

Enhancements
------------

* Implemented the convol, convolb, and convolc commands like their Ultra equivalent 
* Added the intensize and extensive commands
* Added the correl command
* Added the system command to allow passing commands to the operating system
* Allow the user to optionally throw away zero and negative values when using the log commands
* Updated the integrate command to use a new color for the new curve it produces
* Added the getymax/getymin commands
* Enhanced the convol commands to add the number of points to the label

