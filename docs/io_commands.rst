.. _io_commands:

I/O Commands
===============

These commands access disk files either for reading or writing.

.. note::
   **< >** = Required user input.

   **[< >]** = Optional user input. 

   **[PyDV]** = Python Data Visualizer command-line prompt.

read
----

Read curves from the specified ASCII file and optionally filter by regex. The next available prefix (see the prefix command) is automatically assigned the menu index of the first curve in each data file read. For column oriented (.gnu) files optionally specify the x-column number before the file name. **Shortcut: rd**

.. code::
 
   [PyDV]: read [(regex) matches] [x-col] <filename>

readcsv
-------

Read CSV data file. The next available prefix (see the prefix command) is automatically assigned the menu index of the first curve in each data file read. For column oriented (.gnu) files optionally specify the x-column number before the file name. **Shortcut: rdcsv**

.. code::
 
   [PyDV]: readcsv [x-col] <filename.csv>

readsina
--------

Read all curves from Sina data file.
PyDV assumes there is only one record in the Sina file, and if there are more than one then PyDV only reads the first.
PyDV also assumes there is only one independent variable per curve_set; if there are more than one then PyDV may exhibit undefined behavior.
The next available prefix (see the prefix command) is automatically assigned the menu index of the first curve in each data file read.
**Shortcut: rdsina**

.. code::
 
   [PyDV]: readsina <filename.json>

run
---

Execute a list of commands from a file.

.. code::
 
   [PyDV]: run <filename>

save
----

Saves curves to a file in text format.

.. code::

   [PyDV]: save <filename> <curve-list>

savecsv
-------

Save curves to file in comma separated values (CSV) format. Assumes all curves have the same x basis.

.. code::

   [PyDV]: savecsv <filename> <curve-list>

