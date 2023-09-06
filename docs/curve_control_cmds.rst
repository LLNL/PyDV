.. _curve_control_commands:

Curve Control Commands
======================

These functions control the individual curves that are currently being displayed. They range in type from controlling the appearance of the curve to deleting it. They also include the "non-mathematical" mechanisms which may generate curves. 

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input. 

   **[PyDV]:** = Python Data Visualizer command-line prompt.

**appendcurves - 2.4**
----------------------

Merge a list of curves over the union of their domains. Where the domains overlap, take the average of the curve's y-values.

.. code::
 
   [PyDV]: appendcurves <curve-list>

color
-----

Set the color of curves. Color names can be "blue", "red", etc., or "#eb70aa", a 6 digit set of hexadecimal red-green-blue values (RRGGBB). The entire set of HTML-standard color names is available. Type *showcolormap* to see the available named colors.

.. code::
 
   [PyDV]: color <curve-list> <color>

curve
-----

Select curves from the menu for plotting. **Shortcut: cur**

.. code::
 
   [PyDV]: curve [menu <regex>] <list-of-menu-numbers> 

**dupx - 2.4**
--------------

Duplicate x-values so that y=x for each of the specified curves.

.. code::
    
   [PyDV]: dupx <curve-list> 

linemarker
----------

Set the marker symbol for the curves.

.. code::
 
   [PyDV]: linemarker <curve-list> <marker-style: + | . | circle | square | diamond> [<marker-size>]   

.. note::
   When setting this value through the interface or the curve object directly, 
   use ONLY matplotlib supported marker types. Matplotlib marker types are also 
   supported here as well. See matplotlib documentation on markers for further 
   information.

markerfacecolor
---------------

Set the markerface color of curves. Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set of hexadecimal red-green-blue values (RRGGBB). The entire set of HTML-standard color names is available. Try "showcolormap" to see the available named colors.

.. code::
 
   [PyDV]: markerfacecolor <curve-list> <color-name>   

markeredgecolor
---------------

Set the markeredge color of curves. Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set of hexadecimal red-green-blue values (RRGGBB). The entire set of HTML-standard color names is available. Try "showcolormap" to see the available named colors.

.. code::
 
   [PyDV]: markeredgecolor <curve-list> <color-name>   

showcolormap
------------

Show the available named colors.

.. code::
    
   [PyDV]: showcolormap 

showstyles
----------

Show the available plot styles.

.. code::
    
   [PyDV]: showstyles

copy
----

Copy and plot the given curves

.. code::
    
   [PyDV]: copy <curve-list> 

del
---

Delete the specified curves. **Shortcut: del**

.. code::
    
   [PyDV]: delete <curve-list>

**dupx - 2.4**
--------------

Duplicate the x-values such that y=x for each of the given curves

.. code::
    
   [PyDV]: dupx <curve-list>

hide
----

Hide the specified curves from view.

.. code::
    
   [PyDV]: hide <curve-list>

line
----

Generate a line with y = mx + b and an optional number of points.

.. code::
    
   [PyDV]: line <m> <b> <xmin> <xmax> [# pts]

linespoints
-----------

Plot curves as linespoints plots.

.. code::
    
   [PyDV]: linespoints <curve-list> on | off 

makecurve
----------

Generate a curve from two lists of numbers. Each list must be delimited by parentheses. **Alternative Form: make-curve**

.. code::
    
   [PyDV]: makecurve (<list of x-values) (<list of y-values>)

newcurve
--------

Creates a new curve from an expression.

.. code::
    
   [PyDV]: newcurve <numpy expression> 

.. note::

   For convenience, both math and numpy modules have been imported into the namespace.
   Just FYI, this feature is way outside the ULTRA syntax that PyDV is mostly based on.
   EXAMPLE:
   
   [PyDV]: newcurve sin(a.x*2*pi)/(h.y**2)

   This creates a new curve according to the above expression. **Shortcut: nc**

.. warning::

   * Currently, newcurve is hard-wired to only handle single-letter labels.
     Curve names used in the expression cannot be the @N type we use after
     we run out of letters. Sorry (April 2015).
   * A common error is to forget the .x or .y on the curve label name.
   * All the arrays in your expression have to span the same domain! Currently (4/2015), newcurve
     will generate a curve from different domains (with no error message), and that curve
     will almost certainly not be what you intended.

random
------

Generate random y values between -1 and 1 for the specified curves.

.. code::
    
   [PyDV]: random <curve-list>

redo
----

Redo the last undo curve operation.

.. code::
    
   [PyDV]: redo

reid
----

Relabel all the curves in order. **Alternative Form: re-id**

.. code::
    
   [PyDV]: reid

rev
---

Swap x and y values for the specified curves. You may want to sort after this one.

.. code::
    
   [PyDV]: rev <curve-list>

scatter
-------

Plot curves as scatter diagrams or connected lines.

.. code::
    
   [PyDV]: scatter <curve-list> <on | off>

show
----

Reveal the specified curves hidden by the hide command

.. code::
    
   [PyDV]: show <curve-list>

sort
----

Sort the specified curves so that their points are plotted in order of ascending x values.

.. code::
    
   [PyDV]: sort <curve-list>

subsample
---------

Subsample the curves by the optional stride. Default value for stride is 2.

.. code::
    
   [PyDV]: subsample <curve-list> [stride]

undo
----

Undo the last operation on plotted curves.

.. code::
    
   [PyDV]: undo 

**xindex - 2.4**
----------------

Create curves with y-values vs. integer index values.

.. code::
    
   [PyDV]: xindex <curve-list> 

xminmax
-------

Trim the specified curves. **Shortcut: xmm**

.. code::
    
   [PyDV]: xminmax <curve-list> <low-lim> <high-lim>


