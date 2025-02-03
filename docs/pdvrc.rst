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

menulength=length
---------

Change the length of the menu before it prompts the user to press enter.

namewidth=width
---------------

Change the width of the `curve_name` column of the menu and lst output.

xlabelwidth=width
---------------

Change the width of the `xlabel` column of the menu and lst output.

ylabelwidth=width
---------------

Change the width of the `ylabel` column of the menu and lst output.

filenamewidth=width
---------------

Change the width of the `fname` column of the menu and lst output.

recordidwidth=width
---------------

Change the width of the `record_id` column of the menu and lst output.

key=ON | OFF
------------

Show the legend if key=ON, otherwise hide it if key=OFF.

grid=ON | OFF
------------

Show the plot grid if key=ON, otherwise hide it if key=OFF.

letters=ON | OFF
----------------

Show or hide letter markers on plotted curves.

geometry=val1 val2 val3 val4
----------------------------

Change the PyDV window size and location in pixels where val1 is the x-size, val2 is the y-size, val3 is the x-location, and val4 is the y-location.

initcommands=filename
---------------------

Specify a file to run the initial commands.

fontsize=size
-------------

Change the font size

lnwidth=width
-------------

Change the default line width of the curves.

group=ON | OFF
----------------

Group plotted curves.
