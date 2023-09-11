.. _plot_control_commands:

Plot Control Commands
=====================

These functions control the plotting characteristics of PyDV which affect all displayed curves.

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input.

   **[PyDV]:** = Python Data Visualizer command-line prompt.

annot
-----

Display text on the plot at point (x, y).

.. code::

   [PyDV]: annot <text> <x> <y>

border
------

Show the border if **on** or **1**, otherwise hide the border. The **color-name** determines the color of the border. By default, the border color is black.

.. code::

   [PyDV]: border <on | 1 | off | 0> [color-name]

bkgcolor
--------

Change the background color of the plot, window, or both

.. code::

   [PyDV]: bkgcolor <[plot | window] color-name | reset>

dashstyle
---------

Set the style of dash or dot dash lines. The python list is a list of integers, alternating how many pixels to turn on and off, for example:

    [2, 2] : Two pixels on, two off (will result in a dot pattern).

    [4, 2, 2, 2] : 4 on, 2 off, 2 on, 2 off (results in a dash-dot pattern).

    [4, 2, 2, 2, 4, 2] : Gives a dash-dot-dash pattern.

    [4, 2, 2, 2, 2, 2] : Gives a dash-dot-dot pattern.

    See matplotlib 'set_dashes' command for more information.

.. code::

    [PyDV]: dashstyle <curve-list> <[...]>

dataid
------

Show curve identifiers if True. **Alternative Form: data-id**

.. code::

   [PyDV]: dataid <on | off>

delannot
--------

Delete annotations from list.

.. code::

   [PyDV]: delannot <number-list-of-annotations>

domain
------

Set the domain for plotting. Using de (for default) will let the curves determine the domain.

.. code::

   [PyDV]: domain <low-lim> <high-lim>

                 OR

   [PyDV]: domain de

fontcolor
---------

Change the font color of given plot component.

.. code::

   [PyDV]: fontcolor [<component: xlabel | ylabel | title | xaxis | yaxis>] <color-name>

fontsize
--------

Change the font size of given component, or overall scaling factor.

.. code::

   [PyDV]: fontsize [<component: title | xlabel | ylabel | key | tick | curve | annotation>] <numerical-size | small | medium | large | default>

fontstyle
---------

Set the fontstyle family.

.. code::

   [PyDV]: fontstyle <serif | sans-serfif | monospace>

geometry
--------

Change the PyDV window size and location in pixels.

.. code::

   [PyDV]: geometry <xsize> <ysize> <xlocation> <ylocation>

grid
----

Set whether or not to draw grid lines on the graph. Default is off.

.. code::

   [PyDV]: grid <on | off>

gridcolor
---------

Set the color of the grid.

.. code::

   [PyDV]: gridcolor <color-name>

gridstyle
---------

Set the line style for the grid.

.. code::

   [PyDV]: gridstyle <style: solid | dash | dot | dashdot>

gridwidth
---------

Set the grid line width in points.

.. code::

   [PyDV]: gridwidth <width>

group
-----

Group curves based on name and file if curve names are the same. Max number of same name curves is 14.

.. code::

   [PyDV]: group

guilims
-------

Set whether or not to use the GUI min/max values for the X and Y limits. Default is off.

.. code::

   [PyDV]: guilims <on | off>

handlelength
------------

Adjust the length of the line(s) in the legend.

.. code::

   [PyDV]: handlelength <length>

image
-----

Save the current figure to an image file. All parameters are optional. The default value
for **filename** is *plot*, the default value for **filetype** is *pdf* and the default value for
**transparent** is *False*. **dpi** is the resolution in dots per inch and the default value is 
the figure's dpi value.

.. code::

   [PyDV]: image [filename=plot] [filetype=pdf: png | ps | pdf | svg] [transparent=False: True | False] [dpi]

label
-----

Change the key and list label for a curve.

.. code::

   [PyDV]: label <curve> <new-label>

labelcurve
----------

Add curve letter to the legend label if **on**, otherwise hide curve letter if **off**.

.. code::

   [PyDV]: labelcurve <on | off>

labelfilenames
--------------

Add curve filename to the legend label if **on**, otherwise hide curve filename if **off**.
Note: Command will only work with curves from Sina files.

.. code::

   [PyDV]: labelfilenames <on | off>

labelrecordids
--------------

Add curve recordid to the legend label if **on**, otherwise hide curve recordid if **off**.
Note: Command will only work with curves from Sina files with valid record ids.

.. code::

   [PyDV]: labelrecordids <on | off>

latex
-----

Use LaTeX font rendering if True

.. code::

   [PyDV]: latex on | off

legend
------

Show/Hide the legend with on | off or set legend position with ur, ul, ll, lr, cl, cr, uc, lc.
Specify the number of columns to use in the legend.
Specify curves to add to or remove from the legend using the `hide` or `show` keywords followed by the ids of the curves.
Note: Commands after `hide`/`show` will not be processed, so make sure these are the last in the command list.
**Shortcuts: leg, key**

.. code::

   [PyDV]: legend <on | off> [position] [<number of columns>] [<show/hide curve ids]

lnstyle
-------

Set the line style of the specified curves.

.. code::

   [PyDV]: lnstyle <curve-list> <style: solid | dash | dot | dotdash>

lnwidth
-------

Set the line widths of the specified curves. A line width of 0 will give the thinnest line which the host graphics system supports.

.. code::

   [PyDV]: lnwidth <curve-list> <width>

marker
------

Set the marker symbol and scale (optionally) for scatter plots. You can also use any of the matplotlib supported marker types as well. See the matplotlib documentation on markers for further information.

.. code::

   [PyDV]: marker <curve-list> <marker-style: + | . | circle | square | diamond> [marker-size]

minorticks
----------

Minor ticks are not visible by default. On will make the minor ticks visible and off will hide the minor ticks.

.. code::

   [PyDV]: minorticks <on | off>

movefront
---------

Move the given curves so they are plotted on top.

.. code::

   [PyDV]: movefront <curve-list>

plotlayout
----------

Adjust the plot layout parameters. Where **left** is the position of the left edge of the 
plot as a fraction of the figure width, **right** is the position of the right edge of the 
plot, as a fraction of the figure width, **top** is the position of the top edge of the plot, 
as a fraction of the figure height and **bottom** is the position of the bottom edge of the plot, 
as a fraction of the figure height. Alternatively, *de* will revert to the default plot layout values.

If no arguments are given, the plot's current layout settings will be displayed.

.. code::

   [PyDV]: plotlayout [<left> <right> <top> <bottom> || de] 

range
------

Set the range for plotting. Using de (for default) will let the curves determine the range. **Shortcut: ran**

.. code::

   [PyDV]: range <low-lim> <high-lim> | de

style
-----

Use matplotlib style settings from a style specification. The style name of **default** (if
available) is reserved for reverting back to the default style settings.

.. code::

   [PyDV]: style <style-name>

ticks
-----

Set the maximum number of major ticks on the axes.

.. code::

   [PyDV]: ticks <quantity> | de

title
-----

Set a title for the plot

.. code::

   [PyDV]: title <title-name>

update
------

Update the plot after each command if True.

.. code::

   [PyDV]: update on | off

xlabel
------

Set a label for the x axis

.. code::

   [PyDV]: xlabel <label-name>

xlogscale
---------

Set log scale on or off for the x-axis. **Alternative Form: x-log-scale**, **Shortcut: xls**

.. code::

   [PyDV]: xlogscale <on | off>

xtickcolor
----------

Set the color of the ticks on the x-axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: xticks <de | color> [which: major | minor | both]

xticks
------

Set the locations of major ticks on the x-axis

.. code::

   [PyDV]: xticks de | <number> | <list of locations> | <list of locations, list of labels>

xtickformat
-----------

Set the format of major ticks on the x axis. Default is plain.

.. code::

   [PyDV]: xtickformat <plain | sci | exp | 10**>

xticklength
-----------

Set the length (in points) of x ticks on the axis. Default is apply to major ticks only.

.. code::

   [PyDV]: xticklength <number> [which: major | minor | both]

xtickwidth
----------

Set the width (in points) of x ticks on the x axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: xtickwidth <number> [which: major | minor | both]

ylabel
------

Set a label for the y axis

.. code::

   [PyDV]: ylabel <label-name>

ylogscale
---------

Set log scale on or off for the y-axis. **Alternative Form: y-log-scale**, **Shortcut: yls**

.. code::

   [PyDV]: ylogscale <on | off>

ytickcolor
----------

Set the color of the ticks on the y-axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: ytickcolor <de | color> [which: major | minor | both]

ytickformat
-----------

Set the format of major ticks on the y axis. Default is plain.

.. code::

   [PyDV]: ytickformat <plain | sci | exp | 10**>

yticklength
-----------

Set the length (in points) of y ticks on the y axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: yticklength <number> [which: major | minor | both]

ytickwidth
----------

Set the width (in points) of y ticks on the y axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: ytickwidth <number> [which: major | minor | both]

yticks
------

Set the locations of major ticks on the y axis.

.. code::

   [PyDV]: yticks de | <number> | <list of locations> | <list of locations, list of labels>
