.. _env_inquiry_commands:

Environmental Inquiry Commands
==============================

These functions are provided to gain access to information about the state of the PyDV session. Information such as the state of global variables and system help packages is made available through these functions.

.. note::
   **< >** = Required user input.

   **[ ]** = Optional user input. 

   **[PyDV]:** = Python Data Visualizer command-line prompt.

help
----

Return infroamtion about the specified command, variable, or command category. If no argument is supplied, return a list of available commands.

.. code::
 
   [PyDV]: help [command]

list
----

Return a list of the curves currently displayed. A regular expression may be supplied for matching against the curve label to be listed. **Shortcut: lst**

.. code::
    
   [PyDV]: list <label-pattern>

listr
-----

Return a list of the curves currently displayed in range from **start** to **stop**. If **stop** is not
specified, it will be set to the end of the plot list. **Shortcut: lstr**

.. code::
    
   [PyDV]: listr <start> [stop]

listannot
---------

List current annotations.

.. code::
    
   [PyDV]: listannot

menu
----

Return a selection of the curves available for plotting. A regular expression may be supplied for matching against the curve label to be listed.

.. code::
    
   [PyDV]: menu <label-pattern>

menur
-----

Return a selection of the curves available for plotting in the range from **start** to **stop**. If 
**stop** is not specified, it will be set to the end of the curve list.

.. code::
    
   [PyDV]: menur <start> [stop]

system
------

Allows passing commands to the operating system. **Shortcut: ! or shell**

.. code::
    
   [PyDV]: system <command>

