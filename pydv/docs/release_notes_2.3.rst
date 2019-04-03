.. _release_notes_2.3:

Release Notes For PyDV 2.3
==========================

Bug Fixes
---------

* Fixed the **getx** and **gety** commands to work with horizontal/vertical lines. 
* Fixed the sign issue with subtracting curves.

Enhancements
------------

* Added window to display the contents of the **list** command. You can also delete curves from this window.
* Allow figure size specification in **create_plot**.
* Enhanced the **list** command to use a regex for filtering the list. 
* Display the **menu** command contents in a popup window. Can also plot and delete curves from the popup window.
* Enhanced the read command to filter the curves as they are read in. Also, the user can specify the number of matched curves to read in.
* Added the **getlabel** command that prints the given curve's label.
* Added the **getnumpoints** command that prints the given curve's number of points.
* Added the **kill** command that deletes specified entries from the menu.

