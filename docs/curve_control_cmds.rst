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

   Ex:
      [PyDV]: appendcurves a:b
      [PyDV]: appendcurves c d

color
-----

Set the color of curves. Color names can be "blue", "red", etc., or "#eb70aa", a 6 digit set of hexadecimal red-green-blue values #RRGGBB. The entire set of HTML-standard color names is available. Type *showcolormap* to see the available named colors which will show up in the PyDV plotting area (hit return to go back to your plots).

.. code::
 
   [PyDV]: color <curve-list> <color>

   Ex:
      [PyDV]: color a blue
      [PyDV]: color a:b blue
      [PyDV]: color c d blue
      [PyDV]: color a #aabb33
      [PyDV]: showcolormap
      hit return to go back to your plots
      [PyDV]: color a lime

curve
-----

Select curves from the menu for plotting. **Shortcut: cur**

.. code::
 
   [PyDV]: curve [menu (<regex>)] <list-of-menu-numbers> 

   Ex:
      [PyDV]: cur 1
      [PyDV]: cur 2:3
      [PyDV]: cur 4 5
      [PyDV]: cur (.*my_curves.*)

**dupx - 2.4**
--------------

Duplicate x-values so that y=x for each of the specified curves.

.. code::
    
   [PyDV]: dupx <curve-list> 

   Ex:
      [PyDV]: dupx a
      [PyDV]: dupx a:b
      [PyDV]: dupx c d

linemarker
----------

Set the marker symbol for the curves.

.. code::
 
   [PyDV]: linemarker <curve-list> <marker-style: + | . | circle | square | diamond> [<marker-size>]   

   Ex:
      [PyDV]: linemarker a +
      [PyDV]: linemarker a:b .
      [PyDV]: linemarker c d circle
      [PyDV]: linemarker c d square 5

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

   Ex:
      [PyDV]: markerfacecolor a blue
      [PyDV]: markerfacecolor a:b blue
      [PyDV]: markerfacecolor c d blue

markeredgecolor
---------------

Set the markeredge color of curves. Color names can be "blue", "red", etc, or "#eb70aa", a 6 digit set of hexadecimal red-green-blue values (RRGGBB). The entire set of HTML-standard color names is available. Try "showcolormap" to see the available named colors.

.. code::
 
   [PyDV]: markeredgecolor <curve-list> <color-name>   

   Ex:
      [PyDV]: markeredgecolor a blue
      [PyDV]: markeredgecolor a:b blue
      [PyDV]: markeredgecolor c d blue

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

   Ex:
      [PyDV]: copy a
      [PyDV]: copy a:b
      [PyDV]: copy c d

del
---

Delete the specified curves. **Shortcut: del**

.. code::
    
   [PyDV]: delete <curve-list>

   Ex:
      [PyDV]: delete a
      [PyDV]: delete a:b
      [PyDV]: delete c d

hide
----

Hide the specified curves from view.

.. code::
    
   [PyDV]: hide <curve-list>

   Ex:
      [PyDV]: hide a
      [PyDV]: hide a:b
      [PyDV]: hide c d

line
----

Generate a line with y = mx + b and an optional number of points.

.. code::
    
   [PyDV]: line <m> <b> <xmin> <xmax> [# pts]

   Ex:
      [PyDV]: line 3 7 -1 20
      [PyDV]: line 3 7 -1 20 200

linespoints
-----------

Plot curves as linespoints plots.

.. code::
    
   [PyDV]: linespoints <curve-list> on | off 

   Ex:
      [PyDV]: linespoints a on
      [PyDV]: linespoints a:b on
      [PyDV]: linespoints c d off

makecurve
----------

Generate a curve from two lists of numbers. Each list must be delimited by parentheses. **Alternative Form: make-curve**

.. code::
    
   [PyDV]: makecurve (<list of x-values>) (<list of y-values>)

   Ex:
      [PyDV]: makecurve (1 2 3) (20 30 40)

newcurve
--------

Creates a new curve from an expression.

.. code::
    
   [PyDV]: newcurve <numpy expression> 

.. note::

   For convenience, the numpy module has been imported into the namespace.
   Just FYI, this feature is way outside the ULTRA syntax that PyDV is mostly based on.
   EXAMPLE:
   
   [PyDV]: newcurve numpy.sin(a.x*2*numpy.pi)/(b.y**2)

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

   Ex:
      [PyDV]: random a
      [PyDV]: random a:b
      [PyDV]: random c d

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

   Ex:
      [PyDV]: rev a
      [PyDV]: rev a:b
      [PyDV]: rev c d

scatter
-------

Plot curves as scatter diagrams or connected lines.

.. code::
    
   [PyDV]: scatter <curve-list> <on | off>

   Ex:
      [PyDV]: scatter a on
      [PyDV]: scatter a:b on
      [PyDV]: scatter c d off

show
----

Reveal the specified curves hidden by the hide command

.. code::
    
   [PyDV]: show <curve-list>

   Ex:
      [PyDV]: show a
      [PyDV]: show a:b
      [PyDV]: show c d

sort
----

Sort the specified curves so that their points are plotted in order of ascending x values.

.. code::
    
   [PyDV]: sort <curve-list>

   Ex:
      [PyDV]: sort a
      [PyDV]: sort a:b
      [PyDV]: sort c d

subsample
---------

Subsample the curves by the optional stride. Default value for stride is 2.

.. code::
    
   [PyDV]: subsample <curve-list> [stride]

   Ex:
      [PyDV]: subsample a 3
      [PyDV]: subsample a:b 3
      [PyDV]: subsample c d 3

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

   Ex:
      [PyDV]: xindex a
      [PyDV]: xindex a:b
      [PyDV]: xindex c d

xminmax
-------

Trim the specified curves. **Shortcut: xmm**

.. code::
    
   [PyDV]: xminmax <curve-list> <low-lim> <high-lim>

   Ex:
      [PyDV]: xminmax a 1 3
      [PyDV]: xminmax a:b 1 3
      [PyDV]: xminmax c d 1 3
