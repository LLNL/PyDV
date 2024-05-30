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

   Ex:
      [PyDV]: read my_file.ult
      [PyDV]: read my.*curves my_file.ult
      [PyDV]: read my.*curves 1 my_file.ult

readcsv
-------

Read CSV data file. The next available prefix (see the prefix command) is automatically assigned the menu index of the first curve in each data file read. 
For column oriented (.gnu) files optionally specify the x-column number before the file name. If the columns are in x and y pairs with `savecsv` below, the 
[x-col] must be specified as `paired`. **Shortcut: rdcsv**

.. code::
 
   [PyDV]: readcsv <filename.csv> [x-col]

   Ex:
      [PyDV]: readcsv my_file.csv
      [PyDV]: readcsv my_file.csv 2
      [PyDV]: readcsv my_file.csv paired

readsina
--------

Read all curves from Sina data file.
PyDV assumes there is only one record in the Sina file, and if there are more than one then PyDV only reads the first.
PyDV also assumes there is only one independent variable per curve_set; if there are more than one then PyDV may exhibit undefined behavior.
The next available prefix (see the prefix command) is automatically assigned the menu index of the first curve in each data file read.
**Shortcut: rdsina**

.. code::
 
   [PyDV]: readsina <filename.json>

   Ex:
      [PyDV]: readsina my_file.json

run
---

Execute a list of commands from a file.

.. code::
 
   [PyDV]: run <filename>

   Ex:
      [PyDV]: run my_file

save
----

Saves plotted curves to a file in text format. Can also save labels in the file which can be read back in.

.. code::

   [PyDV]: save <filename> <curve-list> [savelabels]

   Ex:
      [PyDV]: save my_saved_file.ult a
      [PyDV]: save my_saved_file.ult b d
      [PyDV]: save my_saved_file.ult b:d
      [PyDV]: save my_saved_file.ult b:d savelabels

savecsv
-------

Saves plotted curves to file in comma separated values (CSV) format. Assumes all curves have the same x basis.

.. code::

   [PyDV]: savecsv <filename> <curve-list>

   Ex:
      [PyDV]: savecsv my_saved_file.csv b
      [PyDV]: savecsv my_saved_file.csv b d
      [PyDV]: savecsv my_saved_file.csv b:d

