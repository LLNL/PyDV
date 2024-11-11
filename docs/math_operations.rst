.. _math_operations:

Math Operations
===============

These functions provide a mechanism for performing mathematical operations on specified **plotted** curves
which can be seen with the command `list`.

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input.

   **[PyDV]:** = Python Data Visualizer command-line prompt.

abs
---

Take the absolute value of the y values of the curves. Modifies the existing curve.

.. code::

   [PyDV]: abs <curve-list>

   Ex:
      [PyDV]: abs a
      [PyDV]: abs a:b
      [PyDV]: abs c d

absx
----

Take the absolute value of the x values of the curves. Modifies the existing curve.

.. code::

   [PyDV]: absx <curve-list>

   Ex:
      [PyDV]: absx a
      [PyDV]: absx a:b
      [PyDV]: absx c d

acos
----

Take arccosine of y values of curves

.. code::

   [PyDV]: acos <curve-list>

   Ex:
      [PyDV]: acos a
      [PyDV]: acos a:b
      [PyDV]: acos c d

acosh
-----

Take hyperbolic arccosine of y values of curves.

.. code::

   [PyDV]: acosh <curve-list>

   Ex:
      [PyDV]: acosh a
      [PyDV]: acosh a:b
      [PyDV]: acosh c d

acoshx
------

Take hyperbolic arccosine of x values of curves.

.. code::

   [PyDV]: acoshx <curve-list>

   Ex:
      [PyDV]: acoshx a
      [PyDV]: acoshx a:b
      [PyDV]: acoshx c d

acosx
-----

Take arccosine of x values of curves
.. code::

   [PyDV]: acosx <curve-list>

   Ex:
      [PyDV]: acosx a
      [PyDV]: acosx a:b
      [PyDV]: acosx c d

add
---

Take the sum of curves. If the optional *value* is specified it will add the y-values of
the curves by *value* (equivalent to using the **dy** command). **Shortcut:** +

.. note::
   Be sure that the x points are in increasing order as PyDV uses numpy.interp().

.. note::
   Adding curves by a number modifies the curve. If you want to create a new
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: add <curve-list> [value]

   Ex:
      [PyDV]: add a
      [PyDV]: add a:b
      [PyDV]: add c d
      [PyDV]: add c d 7

add_h
-----
Adds curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: add_h <list-of-menu-numbers>

   Ex:
      [PyDV]: add_h 1
      [PyDV]: add_h 1:2
      [PyDV]: add_h 3 4

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

   Ex:
      [PyDV]: asin a
      [PyDV]: asin a:b
      [PyDV]: asin c d

asinx
-----

Take arcsine of x values of curves
.. code::

   [PyDV]: asinx <curve-list>

   Ex:
      [PyDV]: asinx a
      [PyDV]: asinx a:b
      [PyDV]: asinx c d

asinh
-----

Take hyperbolic arcsine of y values of curves.

.. code::

   [PyDV]: asinh <curve-list>

   Ex:
      [PyDV]: asinh a
      [PyDV]: asinh a:b
      [PyDV]: asinh c d

asinhx
------

Take hyperbolic arcsine of x values of curves.

.. code::

   [PyDV]: asinhx <curve-list>

   Ex:
      [PyDV]: asinhx a
      [PyDV]: asinhx a:b
      [PyDV]: asinhx c d

atan
----

Take arctangent of y values of curves.

.. code::

   [PyDV]: atan <curve-list>

   Ex:
      [PyDV]: atan a
      [PyDV]: atan a:b
      [PyDV]: atan c d

atanx
-----

Take arctangent of x values of curves.

.. code::

   [PyDV]: atanx <curve-list>

   Ex:
      [PyDV]: atanx a
      [PyDV]: atanx a:b
      [PyDV]: atanx c d

atan2
-----

Take atan2 of two curves.

.. code::

   [PyDV]: atan2 <curve1> <curve2>

   Ex:
      [PyDV]: atan2 a
      [PyDV]: atan2 a:b
      [PyDV]: atan2 c d

atanh
-----

Take hyperbolic arctangent of y values of curves.

.. code::

   [PyDV]: atanh <curve-list>

   Ex:
      [PyDV]: atanh a
      [PyDV]: atanh a:b
      [PyDV]: atanh c d

atanhx
------

Take hyperbolic arctangent of x values of curves.

.. code::

   [PyDV]: atanhx <curve-list>

   Ex:
      [PyDV]: atanhx a
      [PyDV]: atanhx a:b
      [PyDV]: atanhx c d

average
-------

Average the specified curvelist over the intersection of their domains.

.. code::

   [PyDV]: average <curve-list>

   Ex:
      [PyDV]: average a
      [PyDV]: average a:b
      [PyDV]: average c d

convolve
--------

Computes the convolution of the two given curves. This is similar to the slower **convolc** method in ULTRA that uses direct integration and minimal interpolations. **Shortcut:** convol

**THIS IS DEPRECIATED**

.. code::

   [PyDV]: convolve <curve1> <curve2> [points]

convolveb
---------

Computes the convolution of the two given curves and normalizes by the area under the second curve. This computes the integrals directly which avoid padding and aliasing problems associated with FFT methods (it is however slower). **Shortcut:** convolb

(g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) / Int(-inf, inf, dt*h(t))

.. code::

   [PyDV]: convolveb <curve1> <curve2> [points] [points_interp]

   Ex:
      [PyDV]: convolveb g h
      [PyDV]: convolveb g h 200
      [PyDV]: convolveb g h 200 200

convolvec
---------

Computes the convolution of the two given curves with no normalization. This computes the integrals directly which avoid padding and aliasing problems associated with FFT methods (it is however slower). **Shortcut:** convolc

(g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t))

.. code::

   [PyDV]: convolvec <curve1> <curve2> [points] [points_interp]

   Ex:
      [PyDV]: convolvec g h
      [PyDV]: convolvec g h 200
      [PyDV]: convolvec g h 200 200

correl
------

Computes the cross-correlation of two curves.

.. code::

   [PyDV]: correl <curve1> <curve2>

   Ex:
      [PyDV]: correl a b

cos
---

Take the cosine of the y values of the curves.

.. code::

   [PyDV]: cos <curve-list>

   Ex:
      [PyDV]: cos a
      [PyDV]: cos a:b
      [PyDV]: cos c d

cosx
----

Take the cosine of the x values of the curves.

.. code::

   [PyDV]: cosx <curve-list>

   Ex:
      [PyDV]: cosx a
      [PyDV]: cosx a:b
      [PyDV]: cosx c d

cosh
----

Take hyperbolic cosine of y values of curves.

.. code::

   [PyDV]: cosh <curve-list>

   Ex:
      [PyDV]: cosh a
      [PyDV]: cosh a:b
      [PyDV]: cosh c d

coshx
-----

Take hyperbolic cosine of x values of curves.

.. code::

   [PyDV]: coshx <curve-list>

   Ex:
      [PyDV]: coshx a
      [PyDV]: coshx a:b
      [PyDV]: coshx c d

cumsum
-----

Create new curve which is the cumulative sum of the original curve.

.. code::

   [PyDV]: cumsum <curve-list>

   Ex:
      [PyDV]: cumsum a
      [PyDV]: cumsum a:b
      [PyDV]: cumsum c d

dx
--

Shift x values of curves by a constant.

.. code::

   [PyDV]: dx <curve-list> <value>

   Ex:
      [PyDV]: dx a 3
      [PyDV]: dx a:b 3
      [PyDV]: dx c d 3

dy
--

Shift y values of curves by a constant.

.. code::

   [PyDV]: dy <curve-list> <value>

   Ex:
      [PyDV]: dy a 3
      [PyDV]: dy a:b 3
      [PyDV]: dy c d 3

divide
------

Take quotient of curves. If the optional *value* is specified it will divide the
y-values of the curves by *value* (equivalent to using the **divy** command).
**Shortcuts:** /, div

.. note::
   Be sure that the x points are in increasing order as PyDV uses numpy.interp().

.. note::
   Dividing curves by a number modifies the curve. If you want to create a new
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: divide <curve-list> [value]

   Ex:
      [PyDV]: divide a
      [PyDV]: divide a:b
      [PyDV]: divide c d
      [PyDV]: divide c d 7

divide_h
--------

Divides curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: divide_h <list-of-menu-numbers>

   Ex:
      [PyDV]: divide_h 1
      [PyDV]: divide_h 1:2
      [PyDV]: divide_h 3 4

divx
----

Procedure: Divide x values of curves by a constant.

.. code::

   [PyDV]: divx <curve-list> <value>

   Ex:
      [PyDV]: divx a 7
      [PyDV]: divx a:b 7
      [PyDV]: divx c d 7
      [PyDV]: divx c d 7

divy
----

Procedure: Divide y values of curves by a constant.

.. code::

   [PyDV]: divy <curve-list> <value>

   Ex:
      [PyDV]: divy a 7
      [PyDV]: divy a:b 7
      [PyDV]: divy c d 7
      [PyDV]: divy c d 7

error-bar
---------

Plot error bars on the given curve.

.. code::

   [PyDV]: errorbar <curve> <y-error-curve> <y+error-curve> [x-error-curve x+error-curve] [point-skip]

   Ex:
      [PyDV]: errorbar a 2 3
      [PyDV]: errorbar a 2 3 4 5
      [PyDV]: errorbar a 2 3 4 5 2

errorrange
----------

Plot shaded error region on given curve, **Shortcut: error-range**

.. code::

   [PyDV]: errorrange <curve> <y-error-curve> <y+error-curve>

   Ex:
      [PyDV]: errorrannge a 2 3
exp
---

e**y, exponentiate y values of the curves.

.. code::

   [PyDV]: exp <curve-list>

   Ex:
      [PyDV]: exp a
      [PyDV]: exp a:b
      [PyDV]: exp c d

expx
----

e**y, exponentiate x values of the curves.

.. code::

   [PyDV]: expx <curve-list>

   Ex:
      [PyDV]: expx a
      [PyDV]: expx a:b
      [PyDV]: expx c d

fft
---

Compute the one-dimensional discrete Fourier Transform for the y-values of the curves.

.. code::

   [PyDV]: fft <curve-list>

   Ex:
      [PyDV]: fft a
      [PyDV]: fft a:b
      [PyDV]: fft c d

fftx
----

Compute the one-dimensional discrete Fourier Transform for the x-values of the curves.

.. code::

   [PyDV]: fftx <curve-list>

   Ex:
      [PyDV]: fftx a
      [PyDV]: fftx a:b
      [PyDV]: fftx c d

gaussian
--------

Generate a gaussian function.

.. code::

   [PyDV]: gaussian <amplitude> <width> <center> [<# points> [<# half-widths>]]

   Ex:
      [PyDV]: gaussian 5 2 0
      [PyDV]: gaussian 5 2 0 100
      [PyDV]: gaussian 5 2 0 100 2

j0
--

Take the zeroth order Bessel function of y values of curves

.. code::

   [PyDV]: j0 <curve-list>

   Ex:
      [PyDV]: j0 a
      [PyDV]: j0 a:b
      [PyDV]: j0 c d

j0x
---

Take the zeroth order Bessel function of x values of curves

.. code::

   [PyDV]: j0x <curve-list>

   Ex:
      [PyDV]: j0x a
      [PyDV]: j0x a:b
      [PyDV]: j0x c d

j1
--

Take the first order Bessel function of y values of curves

.. code::

   [PyDV]: j1 <curve-list>

   Ex:
      [PyDV]: j1 a
      [PyDV]: j1 a:b
      [PyDV]: j1 c d

j1x
---

Take the first order Bessel function of x values of curves

.. code::

   [PyDV]: j1x <curve-list>

   Ex:
      [PyDV]: j1x a
      [PyDV]: j1x a:b
      [PyDV]: j1x c d

jn
--

Take the nth order Bessel function of y values of curves

.. code::

   [PyDV]: jn <curve-list> <n>

   Ex:
      [PyDV]: jn a 4
      [PyDV]: jn a:b 4
      [PyDV]: jn c d 4

jnx
---

Take the nth order Bessel function of x values of curves

.. code::

   [PyDV]: jnx <curve-list> <n>

   Ex:
      [PyDV]: jnx a 4
      [PyDV]: jnx a:b 4
      [PyDV]: jnx c d 4

L1
--

Makes new curve that is the L1 norm of two args; the L1 norm is integral( \|curve1 - curve2\| ) over the interval [xmin,xmax]. Also prints value of integral to command-line.

.. code::

   [PyDV]: L1 <curve1> <curve2> [<xmin> <xmax>]

   Ex:
      [PyDV]: L1 a b
      [PyDV]: L1 a b 4 10

L2
--

Makes new curve that is the L2 norm of two args; the L2 norm is integral( (curve1 - curve2)**2 )**(1/2) over the interval [xmin,xmax]. Also prints value of integral to command-line.

.. code::

   [PyDV]: L2 <curve1> <curve2> [<xmin> <xmax>]

   Ex:
      [PyDV]: L2 a b
      [PyDV]: L2 a b 4 10

log
---

Take the natural logarithm of the y values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative y-values will be discarded. *keep-neg-vals* is true by default. **Shortcut: ln**

.. code::

   [PyDV]: log <curve-list> [keep-neg-vals: True | False]

   Ex:
      [PyDV]: log a
      [PyDV]: log a:b
      [PyDV]: log c d
      [PyDV]: log c d True

logx
----

Take the natural logarithm of the x values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative x-values will be discarded. *keep-neg-vals* is true by default. **Shortcut: lnx** 

.. code::

   [PyDV]: logx <curve-list> [keep-neg-vals: True | False]

   Ex:
      [PyDV]: logx a
      [PyDV]: logx a:b
      [PyDV]: logx c d
      [PyDV]: logx c d True

log10
-----

Take the base 10 logarithm of the y values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative y-values will be discarded. *keep-neg-vals* is true by default.

.. code::

   [PyDV]: log10 <curve-list> [keep-neg-vals: True | False]

   Ex:
      [PyDV]: log10 a
      [PyDV]: log10 a:b
      [PyDV]: log10 c d
      [PyDV]: log10 c d True

log10x
------

Take the base 10 logarithm of the x values of the curves. If the optional argument *keep-neg-vals* is set to false, then zero and negative y-values will be discarded. *keep-neg-vals* is true by default.

.. code::

   [PyDV]: log10x <curve-list> [keep-neg-vals: True | False]

   Ex:
      [PyDV]: log10x a
      [PyDV]: log10x a:b
      [PyDV]: log10x c d
      [PyDV]: log10x c d True

makeintensive
-------------

Set the y-values such that y[i] = y[i] / (x[i+1] - x[i]). **Shortcut: mkint**

.. code::

   [PyDV]: makeintensive <curve-list>

   Ex:
      [PyDV]: makeintensive a
      [PyDV]: makeintensive a:b
      [PyDV]: makeintensive c d

makeextensive
-------------

Set the y-values such that y[i] = y[i] * (x[i+1] - x[i]). **Shortcut: mkext**

.. code::

   [PyDV]: makeextensive <curve-list>

   Ex:
      [PyDV]: makeextensive a
      [PyDV]: makeextensive a:b
      [PyDV]: makeextensive c d

max
---

Makes a new curve with max y values of curves passed in curvelist.

.. code::

   [PyDV]: max <curve-list>

   Ex:
      [PyDV]: max a
      [PyDV]: max a:b
      [PyDV]: max c d

min
---

Makes a new curve with min y values of curves passed in curvelist.

.. code::

   [PyDV]: min <curve-list>

   Ex:
      [PyDV]: min a
      [PyDV]: min a:b
      [PyDV]: min c d

mx
--

Scale the x values of the curves by a fixed value.

.. code::

   [PyDV]: mx <curve-list> <value>

   Ex:
      [PyDV]: mx a 2
      [PyDV]: mx a:b 2
      [PyDV]: mx c d 2

multiply
--------

Take the product of curves. If the optional *value* is specified it will multiply the 
y-values of the curves by *value* (equivalent to using the **my** command). 
**Shortcuts:** \*, mult

.. note::
   Be sure that the x points are in increasing order as PyDV uses numpy.interp().

.. note::
   Multiplying curves by a number modifies the curve. If you want to create a new 
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: multiply <curve-list> [value]

   Ex:
      [PyDV]: multiply a
      [PyDV]: multiply a:b
      [PyDV]: multiply c d
      [PyDV]: multiply c d 7

multiply_h
----------

Multiplies curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: multiply_h <list-of-menu-numbers>

   Ex:
      [PyDV]: multiply_h 1
      [PyDV]: multiply_h 1:2
      [PyDV]: multiply_h 3 4

my
--

Scale the y values of the curves by a fixed value.

.. code::

   [PyDV]: my <curve-list> <value>

   Ex:
      [PyDV]: my a 2
      [PyDV]: my a:b 2
      [PyDV]: my c d 2

norm
----

Makes a new curve that is the norm of two args. Also prints the value of the integral to command line.

.. code::

   [PyDV]: norm <curve> <curve> <p> <xmin> <xmax>

   Ex:
      [PyDV]: norm a b 2 10 15

.. note::
   The p-norm is (integral( (curve1 - curve2)**p )**(1/p) over the interval [xmin, xmax],
   where p = order.

powa
----

Raise a fixed value, a, to the power of the y values of the curves.

.. code::

   [PyDV]: powa <curve-list> <a>

   Ex:
      [PyDV]: powa a 2
      [PyDV]: powa a:b 2
      [PyDV]: powa c d 2

powax
-----

Raise a fixed value, a, to the power of the x values of the curves.

.. code::

   [PyDV]: powax <curve-list> <a>

   Ex:
      [PyDV]: powax a 2
      [PyDV]: powax a:b 2
      [PyDV]: powax c d 2

powr
----

Raise the y values of the curves to a fixed power p.

.. code::

   [PyDV]: powr <curve-list> <p>

   Ex:
      [PyDV]: powr a 2
      [PyDV]: powr a:b 2
      [PyDV]: powr c d 2

powrx
-----

Raise the x values of the curves to a fixed power p.

.. code::

   [PyDV]: powrx <curve-list> <p>

   Ex:
      [PyDV]: powrx a 2
      [PyDV]: powrx a:b 2
      [PyDV]: powrx c d 2

recip
-----

Take the reciprocal of the y values of the curves.

.. code::

   [PyDV]: recip <curve-list>

   Ex:
      [PyDV]: recip a
      [PyDV]: recip a:b
      [PyDV]: recip c d

recipx
------

Take the reciprocal of the x values of the curves.

.. code::

   [PyDV]: recipx <curve-list>

   Ex:
      [PyDV]: recipx a
      [PyDV]: recipx a:b
      [PyDV]: recipx c d

sin
---

Take the sine of the y values of the curve

.. code::

   [PyDV]: sin <curve-list>

   Ex:
      [PyDV]: sin a
      [PyDV]: sin a:b
      [PyDV]: sin c d

sinx
----

Take the sine of the x values of the curve

.. code::

   [PyDV]: sinx <curve-list>

   Ex:
      [PyDV]: sinx a
      [PyDV]: sinx a:b
      [PyDV]: sinx c d

sinh
----

Take the hyperbolic sine of the y values of the curve

.. code::

   [PyDV]: sinh <curve-list>

   Ex:
      [PyDV]: sinh a
      [PyDV]: sinh a:b
      [PyDV]: sinh c d

smooth
------

Smooth the curve to the given degree.

.. code::

   [PyDV]: smooth <curve-list> [smooth-factor]

   Ex:
      [PyDV]: sin a
      [PyDV]: sin a:b
      [PyDV]: sin c d
      [PyDV]: sin c d 4

sqr
---

Take the square of the y values of the curves.

.. code::

   [PyDV]: sqr <curve-list>

   Ex:
      [PyDV]: sqr a
      [PyDV]: sqr a:b
      [PyDV]: sqr c d

sqrx
----

Take the square of the x values of the curves.

.. code::

   [PyDV]: sqrx <curve-list>

   Ex:
      [PyDV]: sqrx a
      [PyDV]: sqrx a:b
      [PyDV]: sqrx c d

sqrt
----

Take the squre root of the y values of the curves.

.. code::

   [PyDV]: sqrt <curve-list>

   Ex:
      [PyDV]: sqrt a
      [PyDV]: sqrt a:b
      [PyDV]: sqrt c d

sqrtx
-----

Take the squre root of the x values of the curves.

.. code::

   [PyDV]: sqrtx <curve-list>

   Ex:
      [PyDV]: sqrtx a
      [PyDV]: sqrtx a:b
      [PyDV]: sqrtx c d

subtract
--------

Take the difference of curves. A single curve can be specified, resulting in the
negating of its y-values. If the optional *value* is specified it will subtract the
y-values of the curves by *value* (similar to using the **dy** command).
**Shortcuts:** --, sub

.. note::
   Be sure that the x points are in increasing order as PyDV uses numpy.interp().

.. note::
   Subtracting curves by a number modifies the curve. If you want to create a new
   curve then copy the original curve first using the copy command.

.. code::

   [PyDV]: subtract <curve-list> [value]

   Ex:
      [PyDV]: subtract a
      [PyDV]: subtract a:b
      [PyDV]: subtract c d
      [PyDV]: subtract c d 7

subtract_h
----------

Subtracts curves that have been read from a file but not yet plotted. **list-of-menu-numbers**
are the index values displayed in the first column of the **menu** command.

.. code::

   [PyDV]: subtract_h <list-of-menu-numbers>

   Ex:
      [PyDV]: subtract_h 1
      [PyDV]: subtract_h 1:2
      [PyDV]: subtract_h 3 4

tan
---

Take the tangent of y values of curves

.. code::

   [PyDV]: tan <curve-list>

   Ex:
      [PyDV]: tan a
      [PyDV]: tan a:b
      [PyDV]: tan c d

tanx
----

Take the tangent of x values of curves

.. code::

   [PyDV]: tanx <curve-list>

   Ex:
      [PyDV]: tanx a
      [PyDV]: tanx a:b
      [PyDV]: tanx c d

tanh
----

Take the hyperbolic tangent of y values of curves

.. code::

   [PyDV]: tanh <curve-list>

   Ex:
      [PyDV]: tanh a
      [PyDV]: tanh a:b
      [PyDV]: tanh c d

tanhx
-----

Take the hyperbolic tangent of x values of curves

.. code::

   [PyDV]: tanhx <curve-list>

   Ex:
      [PyDV]: tanhx a
      [PyDV]: tanhx a:b
      [PyDV]: tanhx c d

xmax
----

Filter out points in curves whose x-values greater than limit

.. code::

   [PyDV]: xmax <curve-list> <limit>

   Ex:
      [PyDV]: xmax a 3
      [PyDV]: xmax a:b 3
      [PyDV]: xmax c d 3

xmin
----

Filter out points in curves whose x-values less than limit

.. code::

   [PyDV]: xmin <curve-list> <limit>

   Ex:
      [PyDV]: xmin a 3
      [PyDV]: xmin a:b 3
      [PyDV]: xmin c d 3

y0
--

Take the zeroth order Bessel function of the second kind of the y values of the curves.

.. code::

   [PyDV]: y0 <curve-list>

   Ex:
      [PyDV]: y0 a
      [PyDV]: y0 a:b
      [PyDV]: y0 c d

y0x
---

Take the zeroth order Bessel function of the second kind of the x values of the curves.

.. code::

   [PyDV]: y0x <curve-list>

   Ex:
      [PyDV]: y0x a
      [PyDV]: y0x a:b
      [PyDV]: y0x c d

y1
--

Take the first order Bessel function of the second kind of the y values of the curves.

.. code::

   [PyDV]: y1 <curve-list>

   Ex:
      [PyDV]: y1 a
      [PyDV]: y1 a:b
      [PyDV]: y1 c d

y1x
---

Take the first order Bessel function of the second kind of the x values of the curves.

.. code::

   [PyDV]: y1x <curve-list>

   Ex:
      [PyDV]: y1x a
      [PyDV]: y1x a:b
      [PyDV]: y1x c d

ymax
----

Filter out points in curves whose y-values greater than limit

.. code::

   [PyDV]: ymax <curve-list> <limit>

   Ex:
      [PyDV]: ymax a 3
      [PyDV]: ymax a:b 3
      [PyDV]: ymax c d 3

ymin
----

Filter out points in curves whose y-values less than limit

.. code::

   [PyDV]: ymin <curve-list> <limit>

   Ex:
      [PyDV]: ymin a 3
      [PyDV]: ymin a:b 3
      [PyDV]: ymin c d 3

yminmax
-------

Trim the selected curves. **Shortcut: ymm**

.. code::

   [PyDV]: yminmax <curve-list> <low-limit> <high-lim>

   Ex:
      [PyDV]: yminmax a 3 7
      [PyDV]: yminmax a:b 3 7
      [PyDV]: yminmax c d 3 7

yn
--

Take the nth order Bessel function of the second kind of y values of curves

.. code::

   [PyDV]: yn <curve-list> <n>

   Ex:
      [PyDV]: yn a 3
      [PyDV]: yn a:b 3
      [PyDV]: yn c d 3

ynx
---

Take the nth order Bessel function of the second kind of x values of curves

.. code::

   [PyDV]: ynx <curve-list> <n>

   Ex:
      [PyDV]: ynx a 3
      [PyDV]: ynx a:b 3
      [PyDV]: ynx c d 3

derivative
----------

Take the derivative of curves. **Shortcut:** der

.. code::

   [PyDV]: derivative <curve-list>

   Ex:
      [PyDV]: y1x a
      [PyDV]: y1x a:b
      [PyDV]: y1x c d

diffMeasure
-----------

Compare two curves. For the given curves a fractional difference measure and its average is computed

.. code::

   [PyDV]: diffMeasure <curve1> <curve2> [tolerance]

   Ex:
      [PyDV]: diffMeasure a b
      [PyDV]: diffMeasure a b 0.1

fit
---

Make new curve that is polynomial fit to argument. n=1 by default, logy means take log(y-values) before fitting, logx means take log(x-values) before fitting

.. code::

   [PyDV]: fit <curve> [n] [logx] [logy]

   Ex:
      [PyDV]: fit a
      [PyDV]: fit a 2
      [PyDV]: fit a 2 logx
      [PyDV]: fit a 2 logy

integrate
---------

Compute the definite integral of each curve in the list over the specified domain. **Shortcut:** int

.. code::

   [PyDV]: integrate <curve-list> [low-limit high-limit]

   Ex:
      [PyDV]: integrate a
      [PyDV]: integrate a:b
      [PyDV]: integrate c d
      [PyDV]: integrate c d 3 7

span
----

Generates a straight line of slope 1 and y intercept 0 in the specified domain with an optional number of points

.. code::

   [PyDV]: span <xmin> <xmax> [points]

   Ex:
      [PyDV]: span 1 10
      [PyDV]: span 1 10 200

vs
--

Plot the range of the first curve against the range of the second curve

.. code::

   [PyDV]: vs <curve1> <curve2>

   Ex:
      [PyDV]: vs a b
