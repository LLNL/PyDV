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

custom
------

Load a file of custom functions to extend PyDV. Functions must be of the form 'def do_commandname(self, line): ...

.. code::
 
   [PyDV]: custom <file-name> 

debug
-----

Show debug tracebacks if True

.. code::
 
   [PyDV]: debug on | off 

drop
----

Start the Python Interactive Console

.. code::
 
   [PyDV]: drop 

erase
-----

Erase all curves on the screen but leave the limits untouched. **Shortcut: era**

.. code::
 
   [PyDV]: erase 

kill
----

Delete the specified entries from the menu. 

.. code::
 
   [PyDV]: kill [all | number-list] 

namewidth
---------

Change the width of the first column of the **menu** and **lst** output.

.. code::
 
   [PyDV]: namewidth <integer> 

quit
----

Exit PyDV. **Shortcut: q**

.. code::
 
   [PyDV]: quit 

