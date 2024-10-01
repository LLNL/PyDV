.. _curve_inquiry_commands:

Curve Inquiry Commands
======================

These functions provide a mechanism for obtaining information about specified **plotted** curves
which can be seen with the command `list`.

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input.

   **[PyDV]:** = Python Data Visualizer command-line prompt.

area
-----

Calculate the area of the curves.

.. code::

   [PyDV]: area <curve-list>

   Ex:
      [PyDV]: area a
      [PyDV]: area a:b
      [PyDV]: area c d

disp
----

Display the y-values in the specified curve(s).

.. code::

   [PyDV]: disp <curve-list> [format <format>]

   Ex:
      [PyDV]: disp a
      [PyDV]: disp a:b
      [PyDV]: disp c d
      [PyDV]: disp c d format e
      [PyDV]: disp c d format .4e

dispx
-----

Display the x-values in the specified curve(s).

.. code::

   [PyDV]: dispx <curve-list> [format <format>]

   Ex:
      [PyDV]: dispx a
      [PyDV]: dispx a:b
      [PyDV]: dispx c d
      [PyDV]: dispx c d format e
      [PyDV]: dispx c d format .4e

eval
----

Evaluate mathematical operations on curves.

.. code::

   [PyDV]: eval <curve-operations>

   Ex:
      [PyDV]: eval a+b

getattributes
-------------

Return (to the terminal) the attributes of a curve, such as: color, style, width, etc.

.. code::

   [PyDV]: getattributes <curve-list>

   Ex:
      [PyDV]: getattributes a
      [PyDV]: getattributes a:b
      [PyDV]: getattributes c d

getdomain
---------

Return (to the terminal) the domains for the list of curves.

.. code::

   [PyDV]: getdomain <curve-list>

   Ex:
      [PyDV]: getdomain a
      [PyDV]: getdomain a:b
      [PyDV]: getdomain c d

getlabel
--------

Return (to the terminal) the given curve's label.

.. code::

   [PyDV]: getlabel <curve-list>

   Ex:
      [PyDV]: getlabel a
      [PyDV]: getlabel a:b
      [PyDV]: getlabel c d

getnumpoints
------------

Display the number of points for the given curve.

.. code::

   [PyDV]: getnumpoints <curve-list>

   Ex:
      [PyDV]: getnumpoints a
      [PyDV]: getnumpoints a:b
      [PyDV]: getnumpoints c d

getrange
--------

Return (to the terminal) the ranges for the list of curves.

.. code::

   [PyDV]: getrange <curve-list>

   Ex:
      [PyDV]: getrange a
      [PyDV]: getrange a:b
      [PyDV]: getrange c d

getx
----

Return the x values for a given y

.. code::

   [PyDV]: getx <curve-list> <y-value>

   Ex:
      [PyDV]: getx a 1.2
      [PyDV]: getx a:b 1.2
      [PyDV]: getx c d 1.2

gety
----

Return the y values for a given x

.. code::

   [PyDV]: gety <curve-list> <x-value>

   Ex:
      [PyDV]: gety a 3.3
      [PyDV]: gety a:b 3.3
      [PyDV]: gety c d 3.3

stats
-----

Show various statistics about the curve.

.. code::

   [PyDV]: stats <curve-list>

   Ex:
      [PyDV]: stats a
      [PyDV]: stats a:b
      [PyDV]: stats c d

sum
-----

Calculate the sum of the x and y values of the curves.

.. code::

   [PyDV]: sum <curve-list>

   Ex:
      [PyDV]: sum a
      [PyDV]: sum a:b
      [PyDV]: sum c d

getymin
-------

Return xy-parings of the x values with the corresponding minimum y-value for the
curve within the specified domain. If no domain is given, then the full domain
range is used.

.. code::

   [PyDV]: getymin <curve> [<xmin> <xmax>]

   Ex:
      [PyDV]: getymin a
      [PyDV]: getymin a 2 7
      [PyDV]: getymin a:b
      [PyDV]: getymin a:b 2 7
      [PyDV]: getymin c d
      [PyDV]: getymin c d 2 7
getymax
-------

Return xy-parings of the x values with the corresponding maximum y-value for the
curve within the specified domain. If no domain is given, then the full domain
range is used.

.. code::

   [PyDV]: getymax <curve> [<xmin> <xmax>]

   Ex:
      [PyDV]: getymax a
      [PyDV]: getymax a 2 7
      [PyDV]: getymax a:b
      [PyDV]: getymax a:b 2 7
      [PyDV]: getymax c d
      [PyDV]: getymax c d 2 7