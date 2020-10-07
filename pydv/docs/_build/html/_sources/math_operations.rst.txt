.. _math_operations:

Math Operations
===============

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input.

   **[PyDV]:** = Python Data Visualizer command-line prompt.

abs
---

Take the absolute value of the y values of the curves. Modifies the existing curve.

.. code::

   [PyDV]: abs <curve-list>


absx
----

Take the absolute value of the x values of the curves. Modifies the existing curve.

.. code::

   [PyDV]: absx <curve-list>

acos
----

Take arccosine of y values of curves

.. code::

   [PyDV]: acos <curve-list>

acosh
-----

Take hyperbolic arccosine of y values of curves.

.. code::

   [PyDV]: acosh <curve-list>

acoshx
------

Take hyperbolic arccosine of x values of curves.

.. code::

   [PyDV]: acoshx <curve-list>

acosx
-----

Take arccosine of x values of curves
.. code::

   [PyDV]: acosx <curve-list>

add
---

Take the sum of curves. If the optional *value* is specified it will add the y-values of 
the curves by *value* (equivalent to using the **dy** command). **Shortcut:** +

.. note::
   Adding curves by a number modifies the curve. If you want to create a new 
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: add <curve-list> [value]

add_h
-----
Adds curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: add_h <list-of-menu-numbers>

alpha
-----

Find the alpha.

.. code::

   [PyDV]: alpha <calculated-a> <calculated-i> <response> [# points]

asin
----

Take arcsine of y values of curves

.. code::

   [PyDV]: asin <curve-list>

asinx
-----

Take arcsine of x values of curves
.. code::

   [PyDV]: asinx <curve-list>

asinh
-----

Take hyperbolic arcsine of y values of curves.

.. code::

   [PyDV]: asinh <curve-list>

asinhx
------

Take hyperbolic arcsine of x values of curves.

.. code::

   [PyDV]: asinhx <curve-list>

atan
----

Take arctangent of y values of curves.

.. code::

   [PyDV]: atan <curve-list>

atanx
-----

Take arctangent of x values of curves.

.. code::

   [PyDV]: atanx <curve-list>

atan2
-----

Take atan2 of two curves.

.. code::

   [PyDV]: atan2 <curve1> <curve2>

atanh
-----

Take hyperbolic arctangent of y values of curves.

.. code::

   [PyDV]: atanh <curve-list>

atanhx
------

Take hyperbolic arctangent of x values of curves.

.. code::

   [PyDV]: atanhx <curve-list>

average
-------

Average the specified curvelist over the intersection of their domains.

.. code::

   [PyDV]: average <curve-list>

convolve
--------

Computes the convolution of the two given curves. This is similar to the slower **convolc** method in ULTRA that uses direct integration and minimal interpolations. **Shortcut:** convol

.. code::

   [PyDV]: convolve <curve1> <curve2> [points]

convolveb
---------

Computes the convolution of the two given curves and normalizing the second curve by the area under the curve. This computes the integrals directly which avoid padding and aliasing problems associated with FFT methods (it is however slower). **Shortcut:** convolb

.. code::

   [PyDV]: convolveb <curve1> <curve2> [points]

convolvec
---------

Computes the convolution of the two given curves with no normalization. This computes the integrals directly which avoid padding and aliasing problems associated with FFT methods (it is however slower). **Shortcut:** convolb

.. code::

   [PyDV]: convolveb <curve1> <curve2> [points]

**correl - 2.4.2**
------------------

Computes the cross-correlation of two curves.

.. code::

   [PyDV]: correl <curve1> <curve2>

cos
---

Take the cosine of the y values of the curves.

.. code::

   [PyDV]: cos <curve-list>

cosx
----

Take the cosine of the x values of the curves.

.. code::

   [PyDV]: cosx <curve-list>

cosh
----

Take hyperbolic cosine of y values of curves.

.. code::

   [PyDV]: cosh <curve-list>

coshx
-----

Take hyperbolic cosine of x values of curves.

.. code::

   [PyDV]: coshx <curve-list>

dx
--

Shift x values of curves by a constant.

.. code::

   [PyDV]: dx <curve-list> <value>

dy
--

Shift y values of curves by a constant.

.. code::

   [PyDV]: dy <curve-list> <value>

divide
------

Take quotient of curves. If the optional *value* is specified it will divide the 
y-values of the curves by *value* (equivalent to using the **divy** command). 
**Shortcuts:** /, div

.. note::
   Dividing curves by a number modifies the curve. If you want to create a new 
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: divide <curve-list> [value]

divide_h
--------

Divides curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: divide_h <list-of-menu-numbers>

divx
----

Procedure: Divide x values of curves by a constant.

.. code::

   [PyDV]: divx <curve-list> <value>

divy
----

Procedure: Divide y values of curves by a constant.

.. code::

   [PyDV]: divy <curve-list> <value>

error-bar
---------

Plot error bars on the given curve.

.. code::

   [PyDV]: errorbar <curve> <y-error-curve> <y+error-curve> [x-error-curve x+error-curve] [point-skip]

errorrange
----------

Plot shaded error region on given curve, **Shortcut: error-range**

.. code::

   [PyDV]: errorrange <curve> <y-error-curve> <y+error-curve>

exp
---

e**y, exponentiate y values of the curves.

.. code::

   [PyDV]: exp <curve-list>

expx
----

e**y, exponentiate x values of the curves.

.. code::

   [PyDV]: expx <curve-list>

fft
---

Compute the one-dimensional discrete Fourier Transform for the y-values of the curves.

.. code::

   [PyDV]: fft <curve-list>

fftx
----

Compute the one-dimensional discrete Fourier Transform for the x-values of the curves.

.. code::

   [PyDV]: fftx <curve-list>

gaussian
--------

Generate a gaussian function.

.. code::

   [PyDV]: gaussian <amplitude> <width> <center> [<# points> [<# half-widths>]]

j0
--

Take the zeroth order Bessel function of y values of curves

.. code::

   [PyDV]: j0 <curve-list>

j0x
---

Take the zeroth order Bessel function of x values of curves

.. code::

   [PyDV]: j0x <curve-list>

j1
--

Take the first order Bessel function of y values of curves

.. code::

   [PyDV]: j1 <curve-list>

j1x
---

Take the first order Bessel function of x values of curves

.. code::

   [PyDV]: j1x <curve-list>

jn
--

Take the nth order Bessel function of y values of curves

.. code::

   [PyDV]: jn <curve-list> n

jnx
---

Take the nth order Bessel function of x values of curves

.. code::

   [PyDV]: jnx <curve-list> n

L1
--

Makes new curve that is the L1 norm of two args; the L1 norm is integral( \|curve1 - curve2\| ) over the interval [xmin,xmax]. Also prints value of integral to command-line.

.. code::

   [PyDV]: L1 <curve1> <curve2> [<xmin> <xmax>]

L2
--

Makes new curve that is the L2 norm of two args; the L2 norm is integral( (curve1 - curve2)**2 )**(1/2) over the interval [xmin,xmax]. Also prints value of integral to command-line.

.. code::

   [PyDV]: L2 <curve1> <curve2> [<xmin> <xmax>]

log
---

Take the natural logarithm of the y values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative y-values will be discarded. *keep-neg-vals* is true by default. **Shortcut: ln**

.. code::

   [PyDV]: log <curve-list> [keep-neg-vals: True | False]

logx
----

Take the natural logarithm of the x values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative x-values will be discarded. *keep-neg-vals* is true by default. **Shortcut: lnx** 

.. code::

   [PyDV]: logx <curve-list> [keep-neg-vals: True | False]

log10
-----

Take the base 10 logarithm of the y values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative y-values will be discarded. *keep-neg-vals* is true by default.

.. code::

   [PyDV]: log10 <curve-list> [keep-neg-vals: True | False]

log10x
------

Take the base 10 logarithm of the x values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative y-values will be discarded. *keep-neg-vals* is true by default.

.. code::

   [PyDV]: log10x <curve-list> [keep-neg-vals: True | False]

**makeintensive - 2.4.2**
-------------------------

Set the y-values such that y[i] = y[i] / (x[i+1] - x[i]). **Shortcut: mkint**

.. code::

  [PyDV]: makeintensive <curve-list>

**makeextensive - 2.4.2**
-------------------------

Set the y-values such that y[i] = y[i] * (x[i+1] - x[i]). **Shortcut: mkext**

.. code::

  [PyDV]: makeextensive <curve-list>

max
---

Makes a new curve with max y values of curves passed in curvelist.

.. code::

  [PyDV]: max <curve-list>

min
---

Makes a new curve with min y values of curves passed in curvelist.

.. code::

  [PyDV]: min <curve-list>

mx
--

Scale the x values of the curves by a fixed value.

.. code::

   [PyDV]: mx <curve-list> <value>

multiply
--------

Take the product of curves. If the optional *value* is specified it will multiply the 
y-values of the curves by *value* (equivalent to using the **my** command). 
**Shortcuts:** \*, mult

.. note::
   Multiplying curves by a number modifies the curve. If you want to create a new 
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: multiply <curve-list> [value]

multiply_h
----------

Multiplies curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: multiply_h <list-of-menu-numbers>

my
--

Scale the y values of the curves by a fixed value.

.. code::

   [PyDV]: my <curve-list> <value>

norm
----

Makes a new curve that is the norm of two args. Also prints the value of the integral to command line.

.. code::

   [PyDV]: norm <curve> <curve> <p> <xmin> <xmax>

.. note::
   The p-norm is (integral( (curve1 - curve2)**p )**(1/p) over the interval [xmin, xmax],
   where p = order.

powa
----

Raise a fixed value, a, to the power of the y values of the curves.

.. code::

   [PyDV]: powa <curve-list> <a>

powax
-----

Raise a fixed value, a, to the power of the x values of the curves.

.. code::

   [PyDV]: powax <curve-list> <a>

powr
----

Raise the y values of the curves to a fixed power p.

.. code::

   [PyDV]: powr <curve-list> <p>

powrx
-----

Raise the x values of the curves to a fixed power p.

.. code::

   [PyDV]: powrx <curve-list> <p>

recip
-----

Take the reciprocal of the y values of the curves.

.. code::

   [PyDV]: recip <curve-list>

recipx
------

Take the reciprocal of the x values of the curves.

.. code::

   [PyDV]: recipx <curve-list>

sin
---

Take the sine of the y values of the curve

.. code::

   [PyDV]: sin <curve-list>

sinx
----

Take the sine of the x values of the curve

.. code::

   [PyDV]: sinx <curve-list>

sinh
----

Take the hyperbolic sine of the y values of the curve

.. code::

   [PyDV]: sinh <curve-list>

smooth
------

Smooth the curve to the given degree.

.. code::

   [PyDV]: smooth <curve-list> [smooth-factor]

sqr
---

Take the square of the y values of the curves.

.. code::

   [PyDV]: sqr <curve-list>

sqrx
----

Take the square of the x values of the curves.

.. code::

   [PyDV]: sqrx <curve-list>

sqrt
----

Take the squre root of the y values of the curves.

.. code::

   [PyDV]: sqrt <curve-list>

sqrtx
-----

Take the squre root of the x values of the curves.

.. code::

   [PyDV]: sqrtx <curve-list>

subtract
--------

Take the difference of curves. A single curve can be specified, resulting in the 
negating of its y-values. If the optional *value* is specified it will subtract the 
y-values of the curves by *value* (similar to using the **dy** command).
**Shortcuts:** --, sub

.. note::
   Subtracting curves by a number modifies the curve. If you want to create a new 
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: subtract <curve-list> [value]

subtract_h
----------

Subtracts curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: subtract_h <list-of-menu-numbers>

tan
---

Take the tangent of y values of curves

.. code::

   [PyDV]: tan <curve-list>

tanx
----

Take the tangent of x values of curves

.. code::

   [PyDV]: tanx <curve-list>

tanh
----

Take the hyperbolic tangent of y values of curves

.. code::

   [PyDV]: tanh <curve-list>

tanhx
-----

Take the hyperbolic tangent of x values of curves

.. code::

   [PyDV]: tanhx <curve-list>

xmax
----

Filter out points in curves whose x-values greater than limit

.. code::

   [PyDV]: xmax <curve-list> <limit>

xmin
----

Filter out points in curves whose x-values less than limit

.. code::

   [PyDV]: xmin <curve-list> <limit>

y0
--

Take the zeroth order Bessel function of the second kind of the y values of the curves.

.. code::

   [PyDV]: y0 <curve-list>

y0x
---

Take the zeroth order Bessel function of the second kind of the x values of the curves.

.. code::

   [PyDV]: y0x <curve-list>

y1
--

Take the first order Bessel function of the second kind of the y values of the curves.

.. code::

   [PyDV]: y1 <curve-list>

y1x
---

Take the first order Bessel function of the second kind of the x values of the curves.

.. code::

   [PyDV]: y1x <curve-list>

ymax
----

Filter out points in curves whose y-values greater than limit

.. code::

   [PyDV]: ymax <curve-list> <limit>

ymin
----

Filter out points in curves whose y-values less than limit

.. code::

   [PyDV]: ymin <curve-list> <limit>

yminmax
-------

Trim the selected curves. **Shortcut: ymm**

.. code::

   [PyDV]: yminmax <curve-list> <low-limit> <high-lim>

yn
--

Take the nth order Bessel function of the second kind of y values of curves

.. code::

   [PyDV]: yn <curve-list> <n>

ynx
---

Take the nth order Bessel function of the second kind of x values of curves

.. code::

   [PyDV]: ynx <curve-list> <n>

derivative
----------

Take the derivative of curves. **Shortcut:** der

.. code::

   [PyDV]: derivative <curve-list>

diffMeasure
-----------

Compare two curves. For the given curves a fractional difference measure and its average is computed

.. code::

   [PyDV]: diffMeasure <curve1> <curve2> [tolerance]

fit
---

Make new curve that is polynomial fit to argument. n=1 by default, logy means take log(y-values) before fitting, logx means take log(x-values) before fitting

.. code::

   [PyDV]: fit <curve> [n] [logx] [logy]

integrate
---------

Compute the definite integral of each curve in the list over the specified domain. **Shortcut:** int

.. code::

   [PyDV]: integrate <curve-list> [low-limit high-limit]

span
----

Generates a straight line of slope 1 and y intercept 0 in the specified domain with an optional number of points

.. code::

   [PyDV]: span <xmin> <xmax> [points]

vs
--

Plot the range of the first curve against the range of the second curve

.. code::

   [PyDV]: vs <curve1> <curve2>
