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

Display text on the plot at point (x, y). List of annotations can be seen with `listannot`.

.. code::

   [PyDV]: annot <text> <x> <y>

   Ex:
      [PyDV]: annot mytext 1 2

border
------

Show the border if **on** or **1**, otherwise hide the border. The **color-name** determines the color of the border. By default, the border color is black.

.. code::

   [PyDV]: border <on | 1 | off | 0> [color-name]

   Ex:
      [PyDV]: border on
      [PyDV]: border on blue
      [PyDV]: border off

bkgcolor
--------

Change the background color of the plot, window, or both

.. code::

   [PyDV]: bkgcolor <[plot | window] color-name | reset>

   Ex:
      [PyDV]: bkgcolor plot blue
      [PyDV]: bkgcolor window blue
      [PyDV]: bkgcolor reset

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

   Ex:
      [PyDV]: dashstyle a [2, 2]
      [PyDV]: dashstyle a:b [2, 2]
      [PyDV]: dashstyle c d [2, 2]

dataid
------

Show curve identifiers on plot if True. **Alternative Form: data-id**

.. code::

   [PyDV]: dataid <on | off>

   Ex:
      [PyDV]: dataid on
      [PyDV]: dataid off

delannot
--------

Delete annotations from list. List of annotations can be seen with `listannot`.

.. code::

   [PyDV]: delannot <number-list-of-annotations>

   Ex:
      [PyDV]: listannot
      [PyDV]: delannot 1
      [PyDV]: delannot 1:2
      [PyDV]: delannot 3 4

domain
------

Set the domain for plotting. Using de (for default) will let the curves determine the domain.

.. code::

   [PyDV]: domain <low-lim> <high-lim>

   Ex:
      [PyDV]: domain 3 7
      [PyDV]: domain de

fontcolor
---------

Change the font color of given plot component.

.. code::

   [PyDV]: fontcolor [<component: xlabel | ylabel | title | xaxis | yaxis>] <color-name>

   Ex:
      [PyDV]: fontcolor xlabel blue
      [PyDV]: fontcolor ylabel blue
      [PyDV]: fontcolor title blue
      [PyDV]: fontcolor xaxis blue
      [PyDV]: fontcolor yaxis blue

fontsize
--------

Change the font size of given component, or overall scaling factor.

.. code::

   [PyDV]: fontsize [<component: title | xlabel | ylabel | key | tick | curve | annotation>] <numerical-size | small | medium | large | default>

   Ex:
      [PyDV]: fontsize title 12
      [PyDV]: fontsize xlabel small
      [PyDV]: fontsize ylabel medium
      [PyDV]: fontsize key large
      [PyDV]: fontsize tick default
      [PyDV]: fontsize curve 12
      [PyDV]: fontsize annotation small

fontstyle
---------

Set the fontstyle family.

.. code::

   [PyDV]: fontstyle <serif | sans-serif | monospace>

   Ex:
      [PyDV]: fontstyle serif
      [PyDV]: fontstyle sans-serif
      [PyDV]: fontstyle monospace

geometry
--------

Change the PyDV window size and location in pixels.

.. code::

   [PyDV]: geometry <xsize> <ysize> <xlocation> <ylocation>

   Ex:
      [PyDV]: geometry 500 500 250 250

grid
----

Set whether or not to draw grid lines on the graph. Default is off.

.. code::

   [PyDV]: grid <on | off>

   Ex:
      [PyDV]: grid on
      [PyDV]: grid off

gridcolor
---------

Set the color of the grid.

.. code::

   [PyDV]: gridcolor <color-name>

   Ex:
      [PyDV]: gridcolor blue  # white is default

gridstyle
---------

Set the line style for the grid.

.. code::

   [PyDV]: gridstyle <style: solid | dash | dot | dashdot>

   Ex:
      [PyDV]: gridstyle solid
      [PyDV]: gridstyle dash
      [PyDV]: gridstyle dot
      [PyDV]: gridstyle dashdot

gridwidth
---------

Set the grid line width in points.

.. code::

   [PyDV]: gridwidth <width>

   Ex:
      [PyDV]: gridwidth 5

group
-----

Group curves based on name and file if curve names are the same. Max number of same name curves is 14.
Can also update title to curve name and change labels to filenames if all curves share the same name.
If `title` is passed, one can adjust the filename label with number of `slashes` as well.
If `off` is passed, will reset curves back to normal and stop automatic grouping.
Note: `title` also looks at hidden curves thus need to delete curves (e.g. `del a`).

.. code::

   [PyDV]: group <title <slashes #> > <off>
   Ex:
      [PyDV]: group
      [PyDV]: group title
      [PyDV]: group title slashes 2
      [PyDV]: group off

guilims
-------

Set whether or not to use the GUI min/max values for the X and Y limits. Default is off.

.. code::

   [PyDV]: guilims <on | off>

   Ex:
      [PyDV]: guilims on
      [PyDV]: guilims off

handlelength
------------

Adjust the length of the line(s) in the legend.

.. code::

   [PyDV]: handlelength <length>

   Ex:
      [PyDV]: handlelength 10

image
-----

Save the current figure to an image file. All parameters are optional. The default value
for **filename** is *plot*, the default value for **filetype** is *pdf* and the default value for
**transparent** is *False*. **dpi** is the resolution in dots per inch and the default value is
the figure's dpi value. Width and height are in pixels.

.. code::

   [PyDV]: image [filename=plot] [filetype=pdf: png | ps | pdf | svg] [transparent=False: True | False] [dpi] [width] [height]

   Ex:
      [PyDV]: image my_plot png
      [PyDV]: image my_plot png True
      [PyDV]: image my_plot png True 100
      [PyDV]: image my_plot png True 100 1920 1080

label
-----

Change the key and list label for a curve.

.. code::

   [PyDV]: label <curve> <new-label>

   Ex:
      [PyDV]: label a my_new_label

labelcurve
----------

Add curve letter to the legend label if **on**, otherwise hide curve letter if **off**.

.. code::

   [PyDV]: labelcurve <on | off>

   Ex:
      [PyDV]: labelcurve on
      [PyDV]: labelcurve off

labelfilenames
--------------

Add curve filename to the legend label if **on**, otherwise hide curve filename if **off**.
Note: Command will only work with curves from Sina files.

.. code::

   [PyDV]: labelfilenames <on | off>

   Ex:
      [PyDV]: labelfilenames on
      [PyDV]: labelfilenames off

labelrecordids
--------------

Add curve recordid to the legend label if **on**, otherwise hide curve recordid if **off**.
Note: Command will only work with curves from Sina files with valid record ids.

.. code::

   [PyDV]: labelrecordids <on | off>

   Ex:
      [PyDV]: labelrecordids on
      [PyDV]: labelrecordids off

latex
-----

Use LaTeX font rendering if True

.. code::

   [PyDV]: latex on | off

   Ex:
      [PyDV]: latex on
      [PyDV]: latex off

legend
------

Show/Hide the legend with on | off or set legend position with ur, ul, ll, lr, cl, cr, uc, lc.
Specify the number of columns to use in the legend.
Specify curves to add to or remove from the legend using the `hide` or `show` keywords followed by the ids of the curves.
Note: Commands after `hide`/`show` will not be processed, so make sure these are the last in the command list.
**Shortcuts: leg, key**

.. code::

   [PyDV]: legend <on | off> [position] [<number of columns>] [<show/hide curve ids>]

   Ex:
      [PyDV]: legend on
      [PyDV]: legend on ul
      [PyDV]: legend on ul 2
      [PyDV]: legend on ul 2
      [PyDV]: legend on ul 2 showid a
      [PyDV]: legend on ul 2 showid a:b
      [PyDV]: legend on ul 2 showid c d
      [PyDV]: legend on ul 2 showid all
      [PyDV]: legend on ul 2 hideid a
      [PyDV]: legend on ul 2 hideid a:b
      [PyDV]: legend on ul 2 hideid c d
      [PyDV]: legend on ul 2 hideid all

lnstyle
-------

Set the line style of the specified curves.

.. code::

   [PyDV]: lnstyle <curve-list> <style: solid | dash | dot | dotdash>

   Ex:
      [PyDV]: lnstyle a solid
      [PyDV]: lnstyle a:b dash
      [PyDV]: lnstyle c d dot

lnwidth
-------

Set the line widths of the specified curves. A line width of 0 will give the thinnest line which the host graphics system supports.

.. code::

   [PyDV]: lnwidth <curve-list> <width>

   Ex:
      [PyDV]: lnwidth a 2
      [PyDV]: lnwidth a:b 2
      [PyDV]: lnwidth c d 2

marker
------

Set the marker symbol and scale (optionally) for scatter plots. You can also use any of the matplotlib supported marker types as well. See the matplotlib documentation on markers for further information.

.. code::

   [PyDV]: marker <curve-list> <marker-style: + | . | circle | square | diamond> [marker-size]

   Ex:
      [PyDV]: marker a +
      [PyDV]: marker a:b .
      [PyDV]: marker c d circle

minorticks
----------

Minor ticks are not visible by default. On will make the minor ticks visible and off will hide the minor ticks.

.. code::

   [PyDV]: minorticks <on | off>

   Ex:
      [PyDV]: minorticks on
      [PyDV]: minorticks off

movefront
---------

Move the given curves so they are plotted on top.

.. code::

   [PyDV]: movefront <curve-list>

   Ex:
      [PyDV]: movefront a
      [PyDV]: movefront a:b
      [PyDV]: movefront c d

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

   Ex:
      [PyDV]: plotlayout left
      [PyDV]: plotlayout right
      [PyDV]: plotlayout top
      [PyDV]: plotlayout bottom
      [PyDV]: plotlayout de

range
------

Set the range for plotting. Using de (for default) will let the curves determine the range. **Shortcut: ran**

.. code::

   [PyDV]: range <low-lim> <high-lim> | de

   Ex:
      [PyDV]: range 3 7
      [PyDV]: range de

style
-----

Use matplotlib style settings from a style specification. The style name of **default** (if
available) is reserved for reverting back to the default style settings. You can type the command `showstyles` and
see `Matplotlib's' Style sheets reference <https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html>`_.

.. code::

   [PyDV]: style <style-name>

   Ex:
      [PyDV]: style classic

ticks
-----

Set the maximum number of major ticks on the axes.

.. code::

   [PyDV]: ticks <quantity> | de

   Ex:
      [PyDV]: ticks 3
      [PyDV]: ticks de

title
-----

Set a title for the plot

.. code::

   [PyDV]: title <title-name>

   Ex:
      [PyDV]: title my_title

update
------

Update the plot after each command if True.

.. code::

   [PyDV]: update on | off

   Ex:
      [PyDV]: update on
      [PyDV]: update off

xlabel
------

Set a label for the x axis

.. code::

   [PyDV]: xlabel <label-name>

   Ex:
      [PyDV]: xlabel my_x_label

xlogscale
---------

Set log scale on or off for the x-axis. **Alternative Form: x-log-scale**, **Shortcut: xls**

.. code::

   [PyDV]: xlogscale <on | off>

   Ex:
      [PyDV]: xlogscale on
      [PyDV]: xlogscale off

xtickcolor
----------

Set the color of the ticks on the x-axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: xtickcolor <de | color> [which: major | minor | both]

   Ex:
      [PyDV]: xtickcolor blue major
      [PyDV]: xtickcolor blue minor
      [PyDV]: xtickcolor blue both
      [PyDV]: xtickcolor de both

xticks
------

Set the locations of major ticks on the x-axis

.. code::

   [PyDV]: xticks de | <number> | <list of locations> | <list of locations, list of labels>

   Ex:
      [PyDV]: xticks 3
      [PyDV]: xticks (1, 2, 3)
      [PyDV]: xticks (1, 2, 3), ('first label', 'second label', 'third label')
      [PyDV]: xticks de

xtickformat
-----------

Set the format of major ticks on the x axis. Default is plain.

.. code::

   [PyDV]: xtickformat <plain | sci | exp | 10**>

   Ex:
      [PyDV]: xtickformat plain
      [PyDV]: xtickformat sci
      [PyDV]: xtickformat exp
      [PyDV]: xtickformat 10**

xticklength
-----------

Set the length (in points) of x ticks on the axis. Default is apply to major ticks only.

.. code::

   [PyDV]: xticklength <number> [which: major | minor | both]

   Ex:
      [PyDV]: xticklength 2 major
      [PyDV]: xticklength 2 minor
      [PyDV]: xticklength 2 both

xtickwidth
----------

Set the width (in points) of x ticks on the x axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: xtickwidth <number> [which: major | minor | both]

   Ex:
      [PyDV]: xtickwidth 2 major
      [PyDV]: xtickwidth 2 minor
      [PyDV]: xtickwidth 2 both

xtickrotation
----------

Set the rotation (in degrees) of the tick labels on the x axis.

.. code::

   [PyDV]: xtickrotation <degree>

   Ex:
      [PyDV]: xtickrotation 45

xtickha
----------

Set the horizontal alignment of tick labels on the x axis. Default is center.

.. code::

   [PyDV]: xtickha <center | right | left>

   Ex:
      [PyDV]: xtickha right

xtickva
----------

Set the vertical alignment of tick labels on the x axis. Default is top.

.. code::

   [PyDV]: xtickva <center | top | bottom>

   Ex:
      [PyDV]: xtickva center

ylabel
------

Set a label for the y axis

.. code::

   [PyDV]: ylabel <label-name>

   Ex:
      [PyDV]: ylabel my_y_label

ylogscale
---------

Set log scale on or off for the y-axis. **Alternative Form: y-log-scale**, **Shortcut: yls**

.. code::

   [PyDV]: ylogscale <on | off>

   Ex:
      [PyDV]: ylogscale on
      [PyDV]: ylogscale off

ytickcolor
----------

Set the color of the ticks on the y-axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: ytickcolor <de | color> [which: major | minor | both]

   Ex:
      [PyDV]: ytickcolor blue major
      [PyDV]: ytickcolor blue minor
      [PyDV]: ytickcolor blue both
      [PyDV]: ytickcolor de both

ytickformat
-----------

Set the format of major ticks on the y axis. Default is plain.

.. code::

   [PyDV]: ytickformat <plain | sci | exp | 10**>

   Ex:
      [PyDV]: ytickformat plain
      [PyDV]: ytickformat sci
      [PyDV]: ytickformat exp
      [PyDV]: ytickformat 10**

yticklength
-----------

Set the length (in points) of y ticks on the y axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: yticklength <number> [which: major | minor | both]

   Ex:
      [PyDV]: yticklength 2 major
      [PyDV]: yticklength 2 minor
      [PyDV]: yticklength 2 both

ytickwidth
----------

Set the width (in points) of y ticks on the y axis. Default is to apply to major ticks only.

.. code::

   [PyDV]: ytickwidth <number> [which: major | minor | both]

   Ex:
      [PyDV]: ytickwidth 2 major
      [PyDV]: ytickwidth 2 minor
      [PyDV]: ytickwidth 2 both

yticks
------

Set the locations of major ticks on the y axis.

.. code::

   [PyDV]: yticks de | <number> | <list of locations> | <list of locations, list of labels>

   Ex:
      [PyDV]: yticks 3
      [PyDV]: yticks (1, 2, 3)
      [PyDV]: yticks (1, 2, 3), ('first label', 'second label', 'third label')
      [PyDV]: yticks de

ytickrotation
----------

Set the rotation (in degrees) of the tick labels on the y axis.

.. code::

   [PyDV]: ytickrotation <degree>

   Ex:
      [PyDV]: ytickrotation 45

ytickha
----------

Set the horizontal alignment of tick labels on the y axis. Default is right.

.. code::

   [PyDV]: ytickha <center | right | left>

   Ex:
      [PyDV]: ytickha center

ytickva
----------

Set the vertical alignment of tick labels on the y axis. Default is center.

.. code::

   [PyDV]: ytickva <center | top | bottom>

   Ex:
      [PyDV]: ytickva top

tightlayout
----------

Turn on plot tight layout. Useful if tick labels are long.

.. code::

   [PyDV]: tightlayout <on | off>

   Ex:
      [PyDV]: tightlayout on
