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


Installation Instructions
=========================

Install the package by typing

   python setup.py install

at the command prompt with setup.py in the current directory.

You may need to give the path and version of Python depending on your system's configuration:

   <path to python>/python<version> setup.py install

   For example

      C:\\Python33\\python setup.py install

         on Microsoft Windows or

      python3.3 setup.py install

         on Unix-like systems.


Run
===

The command to run this package is:

   python -m filterzippeddbf.filter

You may need to give the path and version of Python depending on your system's configuration:

   <path to python>/python<version> -m filterzippeddbf.filter

   For example

      C:\\Python33\\python -m filterzippeddbf.filter

         on Microsoft Windows or

      python3.3 -m filterzippeddbf.filter

         on Unix-like systems.

Or use the facilities of your desktop (Microsoft Windows, GNOME, KDE, ...) to set up a convenient way of starting FilterZippedDBF. 

Right-click with the pointer over the FilterZippedDBF window to display a menu of actions.
