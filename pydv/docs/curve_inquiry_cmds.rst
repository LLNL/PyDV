.. _curve_inquiry_commands:

Curve Inquiry Commands
======================

These functions provide a mechanism for obtaining information about specified curves.

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input.

   **[PyDV]:** = Python Data Visualizer command-line prompt.

disp
----

Display the y-values in the specified curve(s).

.. code::

   [PyDV]: disp <curve-list>

dispx
-----

Display the x-values in the specified curve(s).

.. code::

   [PyDV]: dispx <curve-list>

eval
----

Evaluate mathematical operations on curves.

.. code::

   [PyDV]: eval <curve-operations>

**getattributes - 2.4**
-----------------------

Return (to the terminal) the attributes of a curve, such as: color, style, width, etc.

.. code::

  [PyDV]: getattributes <curve>

getdomain
---------

Return (to the terminal) the domains for the list of curves.

.. code::

   [PyDV]: getdomain <curve-list>

**getlabel - 2.3**
------------------

Return (to the terminal) the given curve's label.

.. code::

   [PyDV]: getlabel <curve>

**getnumpoints - 2.3**
----------------------

Display the number of points for the given curve.

.. code::

   [PyDV]: getnumpoints <curve>

getrange
--------

Return (to the terminal) the ranges for the list of curves.

.. code::

   [PyDV]: getrange <curve-list>

getx
----

Return the x values for a given y

.. code::

   [PyDV]: getx <curve-list> <y-value>

gety
----

Return the y values for a given x

.. code::

   [PyDV]: gety <curve-list> <x-value>

**stats - 2.4**
---------------

Calculate the mean and standard deviation for the curves and display the results on the terminal.

.. code::

   [PyDV]: stats <curve-list>
