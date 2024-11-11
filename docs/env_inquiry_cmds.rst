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

   Ex:
      [PyDV]: help list

list
----

Return a list of the plotted curves currently displayed. A regular expression may be supplied for matching against the curve label to be listed. **Shortcut: lst**

.. code::

   [PyDV]: list <label-pattern>

   Ex:
      [PyDV]: list
      [PyDV]: list my.*curves

listr
-----

Return a list of the plotted curves currently displayed in range from **start** to **stop**. If **stop** is not
specified, it will be set to the end of the plot list. **Shortcut: lstr**

.. code::

   [PyDV]: listr <start> [stop]

   Ex:
      [PyDV]: listr 1
      [PyDV]: listr 1 10

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

   Ex:
      [PyDV]: menu
      [PyDV]: menu my.*curves

menur
-----

Return a selection of the curves available for plotting in the range from **start** to **stop**. If
**stop** is not specified, it will be set to the end of the curve list.

.. code::

   [PyDV]: menur <start> [stop]

   Ex:
      [PyDV]: menur 1
      [PyDV]: menur 1 10

system
------

Allows passing commands to the operating system. **Shortcut: ! or shell**

.. code::

   [PyDV]: system <command>

   Ex:
      [PyDV]: system echo $PATH

