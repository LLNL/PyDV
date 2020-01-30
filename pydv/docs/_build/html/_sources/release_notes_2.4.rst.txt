.. _release_notes_2.4:

Release Notes For PyDV 2.4
==========================

Bug Fixes
---------

* Display updates correctly after running a batch file
* Draw style command can now draw all of the step options (pre, post, mid)
* Fixed the lableFileNames command from adding the filename more than once
* For certain commands that create a new curve, ensured that all attributes were copied to the new curve
* Fixed a bug in the integrate command that ignored the upper and lower limits
* Fixed a bug in the subsample command. Also, enhanced it so the user needs to specify a curve(s)

Enhancements
------------

* Added the dupx command
* Added the xindex command
* Added the append-curves command
* Added the average command
* Added the max command
* Added the min command
* Added the get-attributes command
* Added the stats command
* Removed unused 'Plot Name' column in the Menu dialog
* Piecewise constant plots are now supported
* The font size and font color can be changed only for the legend
* The getx and gety command now returns all the x- and y-values for a given y- or x-value respectively
* The .pdvrc file supports more default values (fontsize, lnwidth)
* Improved the syntax of the legend command
* Added the bkgcolor command that allows the use to change the background color of the plot, window, or both
* The menu and curve regex option is now done over the curve name and filename
* Both the x- and y-column can be specified when reading in an ULTRA text file

