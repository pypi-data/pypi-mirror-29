# dbasefilter.py
# Copyright (c) 2016 Roger Marsh
# Licence: See LICENSE.txt (BSD licence)

"""Filter selected fields in a dBase file replacing values by null.

The filtered records can be accessed individually, or all the filtered records
can be written to a file or a BytesIO instance in CSV or dBase format.

"""

import os
import os.path
import io
import csv
import ast

# www.digitalpreservation.gov/formats/fdd/fdd00325.shtml
# is a good place to start when looking for format detail.
START = 'start'
LENGTH = 'length'
TYPE = 'type'
DBASE_FIELDATTS = {
    START: int,
    LENGTH: int,
    TYPE: bytes,
    }
_VERSIONMAP = {b'\x03':'dBase III'}
C, N, L, D, M = b'C', b'N', b'L', b'D', b'M'
_FIELDTYPE = {
    C: 'Character',
    N: 'Numeric',
    L: 'Boolean',
    D: 'Date',
    M: 'Memo',
    }
_DELETED = 42 # compared with data[n] where type(data) is bytes
_EXISTS = 32 # compared with data[n] where type(data) is bytes
_PRESENT = {_DELETED:None, _EXISTS:None}


class dBaseFilterError(Exception):
    pass


class dBaseFilter(object):
    """Filter selected fields in a dBase file replacing values by null.

    If a string is given it is assumed to be a filename and is opened 'rb'.  If
    a bytestring is given a BytesIO instance is created containing bytestring.

    If a list of fields to keep is given the values of all other field are
    replaced by null.

    If a list of fields to discard is given the values of these fields are
    replaced by null.

    When both keep and discard lists are given, keep is applied first and
    discard is applied to the fields which were kept.
    
    The first, last, nearest, next, prior, and setat, methods return repr(value)
    for compatibility with the rmappsup.dbaseapi package.  This is despite the
    data already being available as a dictionary of values keyed by field name.
    
    """

    def __init__(self, filename_or_bytestring, keep=(), discard=()):
        """Note dBase file and filters, and initialize data structures."""
        if not isinstance(filename_or_bytestring, (str, bytes)):
            raise dBaseFilterError(
                'filename_or_bytestring argument must be str or bytes.')
        for a in (keep, discard):
            for i in a:
                if isinstance(i, str):
                    continue
                raise dBaseFilterError(
                    '"keep" and "discard" arguments must be iterable of str.')
        self.filename_or_bytestring = filename_or_bytestring
        self.keep = frozenset(keep)
        self.discard = frozenset(discard)
        self._set_closed_state()

    @property
    def is_dbf_format(self):
        """Return True if file is DBF format otherwise False."""
        return self.file_object is not None

    def __del__(self):
        """Close dBase file on instance destruction."""
        self.close()

    def close(self):
        """Close dBase file and initialize data structures."""
        try:
            try:
                self.file_object.close()
            except:
                pass
        finally:
            self._set_closed_state()

    def first(self):
        """Return first record not marked as deleted."""
        value = self.first_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, value)
            elif self.record_control not in _PRESENT:
                return None
            value = self.next_record()

    def last(self):
        """Return last record not marked as deleted."""
        value = self.last_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, value)
            elif self.record_control not in _PRESENT:
                return None
            value = self.prior_record()

    def nearest(self, record_number):
        """Return nearest record not marked as deleted."""
        self._set_record_number(record_number)
        value = self._get_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, value)
            elif self.record_control not in _PRESENT:
                return None
            value = self.next_record()

    def next(self):
        """Return next record not marked as deleted."""
        value = self.next_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, value)
            elif self.record_control not in _PRESENT:
                return None
            value = self.next_record()

    def open_and_test_dbf(self):
        """Open file or BytesIO and get structure if it is in DBF format.

        A DBF file meets the following conditions:

        Byte 0 == b'\x03'  (other values indicate compatible format)
        file size == header size + record size x number of records

        The file size test allows for an extra b'\x1a' byte at the end of the
        file.
        
        """
        if isinstance(self.filename_or_bytestring, str):
            try:
                self.file_object = open(self.filename_or_bytestring, 'rb')
            except:
                raise dBaseFilterError(
                    ''.join(('Unable to open file\n\n',
                             self.filename_or_bytestring)))
        elif isinstance(self.filename_or_bytestring, bytes):
            try:
                self.file_object = io.BytesIO(self.filename_or_bytestring)
            except:
                raise dBaseFilterError(
                    ''.join(('Unable to create "in-memory" file for ',
                             'dBase file data.')))
        else:
            raise dBaseFilterError('Filename or bytes data required.')

        # file header consists of 32 bytes
        # field definitions are 32 bytes
        # field definition trailer is 1 byte \r

        try:
            eof = self.file_object.seek(0, io.SEEK_END)
            self.file_object.seek(-1, io.SEEK_END)
            last_byte = self.file_object.read(1)
            self.file_object.seek(0, io.SEEK_SET)
            header = self.file_object.read(32)
            self.version = header[0:1]
            if self.version not in _VERSIONMAP:
                self.file_object.close()
                self._set_closed_state()
                return
            self.record_count = int.from_bytes(header[4:8], 'little')
            self.first_record_seek = int.from_bytes(header[8:10], 'little')
            self.record_length = int.from_bytes(header[10:12], 'little')
            size = self.first_record_seek+self.record_count*self.record_length
            if size == eof:
                self.eof_byte = False
            elif size+1 == eof and last_byte == b'\x1a':
                self.eof_byte = True
            else:
                self.file_object.close()
                self._set_closed_state()
                return
            self.file_header.append(header)
            fieldnames = []
            self.fields = {}
            fieldstart = 1
            fielddef = self.file_object.read(32)
            terminator = fielddef[0]
            while terminator != b'\r'[0]:
                if len(fielddef) != 32:
                    self.file_object = self.close()
                    break
                self.file_header.append(fielddef)
                nullbyte = fielddef.find(b'\x00', 0)
                if nullbyte == -1:
                    nullbyte = 11
                elif nullbyte > 10:
                    nullbyte = 11
                fieldname = fielddef[:nullbyte].decode('iso-8859-1')
                ftype = fielddef[11:12]
                fieldlength = fielddef[16]
                if ftype in _FIELDTYPE:
                    fieldnames.append(fieldname)
                    self.fields[fieldname] = {}
                    self.fields[fieldname][LENGTH] = fieldlength
                    self.fields[fieldname][START] = fieldstart
                    self.fields[fieldname][TYPE] = ftype
                fieldstart += fieldlength
                fielddef = self.file_object.read(32)
                terminator = fielddef[0]
            self.record_number = None
            self.record_select = None
            self.record_control = None
            self.fieldnames = tuple(fieldnames)
            fieldnames.sort()
            self.sortedfieldnames = tuple(fieldnames)
        except:
            self.file_object.close()
            self._set_closed_state()
            raise dBaseFilterError('Unable to process dBase file header.')

    def prior(self):
        """Return prior record not marked as deleted."""
        value = self.prior_record()
        while value:
            if self.record_control == _EXISTS:
                return (self.record_select, value)
            elif self.record_control not in _PRESENT:
                return None
            value = self.prior_record()

    def setat(self, record_number):
        """Return record at record_number.  Return None if deleted."""
        self._set_record_number(record_number)
        value = self._get_record()
        if value:
            if self.record_control == _EXISTS:
                return (self.record_select, value)

    def _set_closed_state(self):
        """Initialize data structures used in processing dBase file."""
        self.file_object = None
        self.version = None
        self.record_count = None
        self.first_record_seek = None
        self.record_length = None
        self.fields = dict()
        self.record_number = None
        self.record_select = None
        self.record_control = None
        self.record_data = None # most recent _get_record() return
        self.file_header = [] # 1 header + n field definitions each 32 bytes
        self.fieldnames = None
        self.sortedfieldnames = None
        self.eof_byte = None
        
    def first_record(self):
        """Position at and return first record."""
        self._select_first()
        return self._get_record()

    def _get_record(self):
        """Return selected record after applying keep and discard filters.
        
        Copy record deleted/exists marker to self.record_control.
        
        """
        if self.file_object == None:
            return None
        if self.record_select < 0:
            self.record_select = -1
            return None
        elif self.record_select >= self.record_count:
            self.record_select = self.record_count
            return None
        self.record_number = self.record_select
        seek = (
            self.first_record_seek +
            self.record_number *
            self.record_length)
        tell = self.file_object.tell()
        if seek != tell:
            self.file_object.seek(seek - tell, 1)
        record_data = bytearray(self.file_object.read(self.record_length))
        self.record_control = record_data[0]
        if self.record_control in _PRESENT:
            result = {}
            for fieldname in self.fieldnames:
                s = self.fields[fieldname][START]
                l = self.fields[fieldname][LENGTH]
                if self.keep:
                    if fieldname not in self.keep:
                        record_data[s:s+l] = b' ' * l
                if self.discard:
                    if fieldname in self.discard:
                        record_data[s:s+l] = b' ' * l

                # Do not decode bytes because caller knows codec to use
                result[fieldname] = record_data[s:s+l].strip()

            self.record_data = bytes(record_data)
            return repr({k:bytes(v) for k, v in result.items()})
        else:
            self.record_data = bytes(record_data)
            return None

    def last_record(self):
        """Position at and return last record."""
        self._select_last()
        return self._get_record()

    def next_record(self):
        """Position at and return next record."""
        self._select_next()
        return self._get_record()

    def prior_record(self):
        """Position at and return prior record."""
        self._select_prior()
        return self._get_record()

    def _select_first(self):
        """Set record selection cursor at first record."""
        self.record_select = 0
        return self.record_select

    def _select_last(self):
        """Set record selection cursor at last record."""
        self.record_select = self.record_count - 1
        return self.record_select

    def _select_next(self):
        """Set record selection cursor at next record."""
        try:
            self.record_select = self.record_number + 1
            return self.record_select
        except TypeError:
            if self.record_number is None:
                return self._select_first()

    def _select_prior(self):
        """Set record selection cursor at prior record."""
        try:
            self.record_select = self.record_number - 1
            return self.record_select
        except TypeError:
            if self.record_number is None:
                return self._select_last()

    def _set_record_number(self, number):
        """Set record selection cursor at the specified record."""
        if not isinstance(number, int):
            self.record_select = -1
        elif number > self.record_count:
            self.record_select = self.record_count
        elif number < 0:
            self.record_select = -1
        else:
            self.record_select = number

    def to_dbf(self, keep=None, discard=None):
        """Return copy of dBase file after applying keep and discard filters."""
        dbase_copy = io.BytesIO()
        dbase_copy.write(b''.join(self.file_header))
        dbase_copy.write(b'\r')
        r = self.first_record()
        while r:
            if keep or discard:
                record_data = bytearray(self.record_data)
                for fieldname in self.fieldnames:
                    s = self.fields[fieldname][START]
                    l = self.fields[fieldname][LENGTH]
                    if keep:
                        if fieldname not in keep:
                            record_data[s:s+l] = b' ' * l
                    if discard:
                        if fieldname in discard:
                            record_data[s:s+l] = b' ' * l
                dbase_copy.write(bytes(record_data))
            else:
                dbase_copy.write(self.record_data)
            r = self.next_record()
        if self.eof_byte:
            dbase_copy.write(b'\x1a')
        return dbase_copy.getvalue()

    def to_csv(self, encoding='utf-8', keep=None, discard=None):
        """Return data in csv format after applying keep and discard filters."""
        csv_copy = io.StringIO()
        csv_writer = csv.DictWriter(csv_copy, fieldnames=self.fieldnames)
        csv_writer.writeheader()
        r = self.first()
        while r:
            row = {k:bytes(v).decode(encoding)
                   for k, v in ast.literal_eval(r[-1]).items()}
            if keep:
                for k in row.keys():
                    if k not in keep:
                        row[k] = ''
            if discard:
                for k in row.keys():
                    if k in discard:
                        row[k] = ''
            csv_writer.writerow(row)
            r = self.next()
        return csv_copy.getvalue()
