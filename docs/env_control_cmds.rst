.. _env_control_commands:

Environmental Control Commands
==============================

These functions allow you to manipulate the environment of PyDV on a global level. They are useful to avoid repeated use of other commands or to change the state of PyDV in dramatic ways.

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input. 

   **[PyDV]:** = Python Data Visualizer command-line prompt.

alias
-----

Define a synonym for  an existing command.

.. code::
 
   [PyDV]: alias <command> <alias>

   Ex:
      [PyDV]: alias list l

custom
------

Load a file of custom functions to extend PyDV. Functions must be of the form **'def do_commandname(self, line): ...'**.

This custom Python script is imported at the `pdv.py` level and thus you can use the methods within `class Command():` by calling `self.do_METHOD_NAME():`.
These are the methods used in the [PyDV] command line prompt that are detailed in this documentation.

The `pydvpy.py` module is imported as `pydvif` which means you can also use the PyDV Python API functions by calling `pydvif.FUNCTION_NAME():`.

.. code::
 
   [PyDV]: custom <file-name> 

   Ex:
      my_custom_functions.py:
         import os


         def do_mycustomfunction(self, line):

            for i in range(4):
               x = [i, i + 1, i + 2]
               y = x
               name = f'TestCurve_{i}'
               fname = f'TestFilename_{i}'
               xlabel = f'TestXlabel_{i}'
               ylabel = f'TestYlabel_{i}'
               title = f'TestTitle_{i}'
               record_id = f'TestRecordID_{i}'
               c = pydvif.makecurve(x, y, name=name, fname=fname, xlabel=xlabel, ylabel=ylabel, title=title,  # noqa F821
                                    record_id=record_id)
               self.curvelist.append(c)


         def do_myothercustomfunction(self, line):

            TEST_DIR = os.path.dirname(os.path.abspath(__file__))
            self.do_read(os.path.join(TEST_DIR, '../tests', 'step.ult'))
            self.do_readsina(os.path.join(TEST_DIR, '../tests', 'testSinaData2.json'))

      [PyDV]: custom my_custom_functions.py

   Afterwards:
      [PyDV]: mycustomfunction
      [PyDV]: myothercustomfunction

debug
-----

Show debug tracebacks if True

.. code::
 
   [PyDV]: debug on | off 

   Ex:
      [PyDV]: debug on
      [PyDV]: debug off

drop
----

Start the Python Interactive Console

.. code::
 
   [PyDV]: drop 

   Ex:
      [PyDV]: drop 

   Afterwards:
      >>> import matplotlib.pyplot as plt
      >>> plt.ion()
      >>> my_fig = plt.gcf()  # get figure object
      >>> my_axis = plt.gca()  # get axis object
      >>> my_axis.plot([1, 2], [5, 6])
      >>> Ctrl+D  # to go back into pydv
      [PyDV]: quit  # only if you want to quit pydv

erase
-----

Erase all curves on the screen but leave the limits untouched. **Shortcut: era**

.. code::
 
   [PyDV]: erase 

filenamewidth
-------------

Change the width of the fname column of the menu and lst output. If no width is given, the 
current column width will be displayed.

.. code::
 
   [PyDV]: filenamewidth <integer> 

   Ex:
      [PyDV]: filenamewidth
      [PyDV]: filenamewidth 100

kill
----

Delete the specified entries from the menu. 

.. code::
 
   [PyDV]: kill [all | number-list] 

   Ex:
      [PyDV]: kill all
      [PyDV]: kill 5:7

namewidth
---------

Change the width of the first column of the **menu** and **lst** output.

.. code::
 
   [PyDV]: namewidth <integer> 

   Ex:
      [PyDV]: namewidth
      [PyDV]: namewidth 100

recordidwidth
-------------

Change the width of the record_id column of the menu and lst output. If no width is given, the 
current column width will be displayed.

.. code::
 
   [PyDV]: recordidwidth <integer> 

   Ex:
      [PyDV]: recordidwidth
      [PyDV]: recordidwidth 100

quit
----

Exit PyDV. **Shortcut: q**

.. code::
 
   [PyDV]: quit 

xlabelwidth
-----------

Change the width of the xlabel column of the menu and lst output. If no width is given, the 
current column width will be displayed.

.. code::
 
   [PyDV]: xlabelwidth <integer> 

   Ex:
      [PyDV]: xlabelwidth
      [PyDV]: xlabelwidth 100

ylabelwidth
-----------

Change the width of the ylabel column of the menu and lst output. If no width is given, the 
current column width will be displayed.

.. code::
 
   [PyDV]: ylabelwidth <integer> 

   Ex:
      [PyDV]: ylabelwidth
      [PyDV]: ylabelwidth 100

menulength
-----------

Change the number of curves displayed when executing the `menu` command before Enter needs to be pressed.
If no length is given, the current menu length will be displayed.

.. code::

   [PyDV]: menulength <integer>

   Ex:
      [PyDV]: menulength
      [PyDV]: menulength 100
