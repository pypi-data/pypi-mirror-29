# urlzippedfile.py
# Copyright 2016 Roger Marsh
# License: See LICENSE.txt (BSD licence)

"""Open files extracted from a zipped file as 'in-memory' files.

The dBaseFilter class is used to decide which are DBF files and note their
structure.

"""

import zipfile

from . import dbasefilter


class URLZippedFileError(Exception):
    pass


class URLZippedFile:
    """Extract in-memory copies of files in a zip archive."""

    def __init__(self, zippedfile, password):
        """Extract contents of zippedfile into byte-strings."""
        zipped = zipfile.ZipFile(zippedfile)
        self.contents = {}
        self.filenames = []
        self.filters = {}
        for i in zipped.infolist():
            self.filenames.append(i.filename)
            self.contents[i.filename] = zipped.open(i, pwd=password).read()
        self.edited_zipped = {}

    def open_zipped_file(self, filename):
        """Open content of filename as a BytesIO and test for being DBF."""
        if filename in self.filters:
            return
        dbf = dbasefilter.dBaseFilter(self.contents[filename])
        dbf.open_and_test_dbf()
        self.filters[filename] = dbf

    def close(self):
        """Close all the data objects derived from zipped file."""
        for dbf in self.filters.values():
            dbf.close()
        self.contents = {}
        self.filenames = []
        self.filters = {}
        self.edited_zipped = {}

    def __del__(self):
        """Close all the data objects derived from zipped file."""
        self.close()
