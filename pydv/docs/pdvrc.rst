.. _pdvrc:

.pdvrc File Format
==================

.. note::
   The **.pdvrc** file allows the user to initialize PyDV settings at startup time. PyDV expects the **.pdvrc** file to be located in the User's Home Directory. The format of the **.pdvrc** file is 'key=value'. Below are all of the currently recognized settings.

xlabel=label
------------

Set the label for the x-axis to label.

ylabel=label
------------

Set the label for the y-axis to label.

title=str
---------

Set the title for the plot to str.


key=ON | OFF
------------

Show the legend if key=ON, otherwise hide it if key=OFF.

letters=ON | OFF
----------------

Show or hide letter markers on plotted curves.

geometry=val1 val2 val3 val4
----------------------------

Change the PyDV window size and location in pixels where val1 is the x-size, val2 is the y-size, val3 is the x-location, and val4 is the y-location.

initcommands=filename
---------------------

Specify a file to run the initial commands.

namewidth=width
---------------

Change the width of teh first column of the menu and lst output.

fontsize=size
-------------

Change the font size 

lnwidth=width
-------------

Change the default line width of the curves.

