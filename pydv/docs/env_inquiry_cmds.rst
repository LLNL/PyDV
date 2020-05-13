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

lst
---

Return a list of the curves currently displayed. A regular expression may be supplied for matching against the curve label to be listed. 

.. code::
    
   [PyDV]: lst <label-pattern>

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

**system - 2.4.2**
------------------

Allows passing commands to the operating system. **Shortcut: ! or shell**

.. code::
    
   [PyDV]: system <command>

