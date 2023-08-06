=======================
Filter zipped DBF files
=======================

.. contents::


Description
===========

FilterZippedDBF allows values in unwanted fields in zipped DBF files to be removed.

The zip archive is extracted into memory, so a permanent copy containing the values in unwanted fields is not made.  In particular when the zip archive is
downloaded.

A list of files in a zip archive is displayed.

A list of fields in each DBF file is displayed.

Select the fields whose values are to be removed.

Save the files individually or write a new zip archive, with the values in the selected fields removed.


Layout
======

FilterZippedDBF contains three panes arranged vertically.

The top pane contains the Uniform Resource Locator (URL) of the zip archive to be filtered.  The URL may be typed, or a local URL may selected using the open file dialogue.

The middle pane contains the list of files extracted from a zip archive.  The fields in each DBF file are listed just below the file name.

The bottom pane is where the content of a filtered DBF file may be displayed in CSV format.

Actions
=======

Right-click with the pointer over the FilterZippedDBF window to display a menu of actions.

The actions displayed depend on whether a zip archive is open, and where the pointer is hovering.  The pointer can be hovering over an extracted file name, a field name, or somewhere else.

The Next and Prior actions move a field cursor (lighter green) or a file cursor (darker green) round the lists of fields and files.  Some of the keyboard equivalents of pointer actions work on the field or file highlighted by cursor.

Browse
------

 Select a zip archive on the local computer using a dialogue.  The URL for the selected file replaces the current content of the top pane.

Close URL
---------

 The middle pane, which contains the list of files extracted from a zip archive, and the bottom pane, which may contain the content of a DBF file in CSV format, are cleared.

(De)select Current Field
------------------------

 Select, or deselect, the field highlighted by cursor for inclusion in the list of fields whose values are to be removed when filtering the file or creating a new zip archive.

(De)select Current File
-----------------------

 Select, or deselect, the file highlighted by cursor for inclusion in the list of files to be removed when creating a new zip archive.

(De)select Field
----------------

 Select, or deselect, the field under the pointer for inclusion in the list of fields whose values are to be removed when filtering the file or creating a new zip archive.

(De)select File
---------------

 Select, or deselect, the file under the pointer for inclusion in the list of files to be removed when creating a new zip archive.

Extract File
------------

 Extract the file under the pointer, or highlighted by cursor, to a file selected using a save file dialogue.

Filter to Zip Archive
---------------------

 Filter and copy the files to a new zip archive selected using a save file dialogue.  The values of the selected fields, highlighted blue, are removed and the selected files are not included in the new archive.

 The new zip archive does not have a password.

Filter to CSV
-------------

 Extract and filter the file under the pointer, or highlighted by cursor, to a CSV file selected using a save file dialogue.  The values of the selected fields, highlighted blue, are removed.

Filter to DBF
-------------

 Extract and filter the file under the pointer, or highlighted by cursor, to a DBF file selected using a save file dialogue.  The values of the selected fields, highlighted blue, are removed.

Help
----

 Display this file.

 An HTML version is included in FilterZippedDBF.  It is created using Python's rst2html tool.

Next Field
----------

 Move the field cursor (lighter green) to the next field.

Next File
---------

 Move the file cursor (darker green) to the next field.

Open or Download
----------------

 Extract the files in the zip archive named in the top pane to memory files.

 The zip archive name is put in the upper row of the top pane, and the password for the zipped archive is put in the lower row of the top pane.

Prior Field
-----------

 Move the field cursor (lighter green) to the prior field.

Prior File
----------

 Move the file cursor (darker green) to the prior field.

Show as CSV
-----------

 Extract and filter the file under the pointer, or highlighted by cursor, and display it in the bottom pane in CSV format.  The values of the selected fields, highlighted blue, are removed.
