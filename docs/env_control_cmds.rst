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

Load a Python file of custom functions to extend PyDV. Functions must be of the form **'def do_commandname(self, line): ...'**.

This custom Python script is imported at the `pdv.py` level and thus you can use the methods within `class Command():` by calling `self.do_METHOD_NAME():`.
These are the methods used in the [PyDV] command line prompt that are detailed in this documentation.

The `pydvpy.py` module is imported as `pydvif` which means you can also use the PyDV Python API functions by calling `pydvif.FUNCTION_NAME():`.

Below are some template functions that are used throughout PyDV. The parameter `line` is the text that is passed into the function after the function name in the PyDV Command Line Interface.
These functions should have `try` statements so that PyDV doesn't crash if there is an error. Be sure to pass in the command `debug on` to PyDV to get more information about any errors.

.. code::

   [PyDV]: custom <file-name>

   Ex:
      Python file outside of PyDV containing custom functions:

         my_custom_functions.py:

            import os


            def do_mycustomfunction(self, line):
               """
               Create new curve and add it to the `self.curvelist()`.
               These are the curves shown with the `menu` command.
               """

               try:
                  num_curves = int(line)
                  for i in range(num_curves):
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
               except:
                     print('error - usage: mycustomfunction <int>')
                     if self.debug:
                        traceback.print_exc(file=sys.stdout)


            def do_myothercustomfunction(self, line):
               """
               Calling other functions within PyDV.
               """

               try:
                  files = line.split()

                  TEST_DIR = os.path.dirname(os.path.abspath(__file__))
                  self.do_read(os.path.join(TEST_DIR, '../tests', files[0]))
                  self.do_readsina(os.path.join(TEST_DIR, '../tests', files[1]))
               except:
                     print('error - usage: myothercustomfunction <filenames>')
                     if self.debug:
                        traceback.print_exc(file=sys.stdout)


            def do_createcustomcurve(self, line):
               """
               Create new curve and add it to the `self.plotlist()`.
               These are the curves shown with the `list` command.
               """

               if not line:
                     return 0
               try:
                     if len(line.split(':')) > 1:
                        self.do_createcustomcurve(pdvutil.getletterargs(line))
                        return 0
                     else:
                        line = line.split()

                        for i in line:
                           idx = pdvutil.getCurveIndex(i, self.plotlist)
                           cur = self.plotlist[idx]
                           x = cur.x + 10
                           y = cur.y - 10
                           nc = pydvif.makecurve(x, y, name=name, fname=fname, xlabel=xlabel, ylabel=ylabel, title=title,  # noqa F821
                                       record_id=record_id)
                           self.addtoplot(nc)

                           self.plotedit = True
               except:
                     print('error - usage: createcustomcurve <curve-list>')
                     if self.debug:
                        traceback.print_exc(file=sys.stdout)


            def do_customcurveinfo(self, line):
               """
               Acquire information from the the curves in `self.plotlist()`.
               """

               try:
                     if len(line.split(':')) > 1:
                        self.do_customcurveinfo(pdvutil.getletterargs(line))
                        return 0
                     else:
                        print('\nCustom Curve Info:')
                        line = line.split()

                        for i in range(len(line)):
                           try:
                                 idx = pdvutil.getCurveIndex(line[i], self.plotlist)
                                 cur = self.plotlist[idx]
                                 info = numpy.sum(cur.x) + 10
                                 print(f'\nCurve {cur.plotname}: {cur.name}')
                                 print(f'\tInfo: {info:.6e}')
                           except pdvutil.CurveIndexError:
                                 pass
                        print('')
               except:
                     print('error - usage: customcurveinfo <curve-list>')
                     if self.debug:
                        traceback.print_exc(file=sys.stdout)
               finally:
                     self.redraw = False


      Within PyDV CLI:

         [PyDV]: debug on
         [PyDV]: custom my_custom_functions.py
         [PyDV]: mycustomfunction
         [PyDV]: myothercustomfunction
         [PyDV]: createcustomcurve a:b
         [PyDV]: customcurveinfo a:b

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
